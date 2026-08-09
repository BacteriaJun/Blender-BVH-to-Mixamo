"""UE5 skeleton profile and FBX export helpers.

V3.4.0 focuses on a stable UE5 pipeline:
- keep the proven Constraint Bake retargeting algorithm;
- convert the baked Mixamo-style skeleton to UE-style names;
- add a real root bone and optional Manny-style helper bones;
- export FBX with repeatable Unreal-oriented settings.

This is a UE5-friendly humanoid profile. It is closer to UE5/Manny naming than
raw Mixamo, but it is still intentionally safer than trying to fully recreate
Epic Manny/Quinn deformation and control rigs inside Blender.
"""

import re

import bpy
from mathutils import Vector

from .armature_utils import ensure_object_mode
from .logger import log_info, log_warning

TARGET_MIXAMO = 'MIXAMO'
TARGET_UE5_BASIC = 'UE5_BASIC'

UE5_ROOT_NONE = 'NO_ROOT_MOTION'
UE5_ROOT_BONE = 'ROOT_BONE_MOTION'
UE5_ROOT_PELVIS = 'PELVIS_ONLY'

MIXAMO_TO_UE5_BASIC = {
    'mixamorig:Hips': 'pelvis',
    'mixamorig:Spine': 'spine_01',
    'mixamorig:Spine1': 'spine_02',
    'mixamorig:Spine2': 'spine_03',
    'mixamorig:Neck': 'neck_01',
    'mixamorig:Head': 'head',
    'mixamorig:LeftShoulder': 'clavicle_l',
    'mixamorig:LeftArm': 'upperarm_l',
    'mixamorig:LeftForeArm': 'lowerarm_l',
    'mixamorig:LeftHand': 'hand_l',
    'mixamorig:RightShoulder': 'clavicle_r',
    'mixamorig:RightArm': 'upperarm_r',
    'mixamorig:RightForeArm': 'lowerarm_r',
    'mixamorig:RightHand': 'hand_r',
    'mixamorig:LeftUpLeg': 'thigh_l',
    'mixamorig:LeftLeg': 'calf_l',
    'mixamorig:LeftFoot': 'foot_l',
    'mixamorig:LeftToeBase': 'ball_l',
    'mixamorig:RightUpLeg': 'thigh_r',
    'mixamorig:RightLeg': 'calf_r',
    'mixamorig:RightFoot': 'foot_r',
    'mixamorig:RightToeBase': 'ball_r',
    'mixamorig:LeftHandThumb1': 'thumb_01_l',
    'mixamorig:LeftHandThumb2': 'thumb_02_l',
    'mixamorig:LeftHandThumb3': 'thumb_03_l',
    'mixamorig:LeftHandIndex1': 'index_01_l',
    'mixamorig:LeftHandIndex2': 'index_02_l',
    'mixamorig:LeftHandIndex3': 'index_03_l',
    'mixamorig:LeftHandMiddle1': 'middle_01_l',
    'mixamorig:LeftHandMiddle2': 'middle_02_l',
    'mixamorig:LeftHandMiddle3': 'middle_03_l',
    'mixamorig:LeftHandRing1': 'ring_01_l',
    'mixamorig:LeftHandRing2': 'ring_02_l',
    'mixamorig:LeftHandRing3': 'ring_03_l',
    'mixamorig:LeftHandPinky1': 'pinky_01_l',
    'mixamorig:LeftHandPinky2': 'pinky_02_l',
    'mixamorig:LeftHandPinky3': 'pinky_03_l',
    'mixamorig:RightHandThumb1': 'thumb_01_r',
    'mixamorig:RightHandThumb2': 'thumb_02_r',
    'mixamorig:RightHandThumb3': 'thumb_03_r',
    'mixamorig:RightHandIndex1': 'index_01_r',
    'mixamorig:RightHandIndex2': 'index_02_r',
    'mixamorig:RightHandIndex3': 'index_03_r',
    'mixamorig:RightHandMiddle1': 'middle_01_r',
    'mixamorig:RightHandMiddle2': 'middle_02_r',
    'mixamorig:RightHandMiddle3': 'middle_03_r',
    'mixamorig:RightHandRing1': 'ring_01_r',
    'mixamorig:RightHandRing2': 'ring_02_r',
    'mixamorig:RightHandRing3': 'ring_03_r',
    'mixamorig:RightHandPinky1': 'pinky_01_r',
    'mixamorig:RightHandPinky2': 'pinky_02_r',
    'mixamorig:RightHandPinky3': 'pinky_03_r',
}

UE5_BASIC_REQUIRED = [
    'root', 'pelvis', 'spine_01', 'spine_02', 'spine_03', 'neck_01', 'head',
    'clavicle_l', 'upperarm_l', 'lowerarm_l', 'hand_l',
    'clavicle_r', 'upperarm_r', 'lowerarm_r', 'hand_r',
    'thigh_l', 'calf_l', 'foot_l', 'ball_l',
    'thigh_r', 'calf_r', 'foot_r', 'ball_r',
]

UE5_AUXILIARY_BONES = [
    'ik_foot_root', 'ik_foot_l', 'ik_foot_r',
    'ik_hand_root', 'ik_hand_gun', 'ik_hand_l', 'ik_hand_r',
]


def _rename_action_paths(armature, rename_map):
    action = armature.animation_data.action if armature.animation_data else None
    if not action:
        return 0
    updated = 0
    for fcurve in action.fcurves:
        if 'pose.bones[' not in fcurve.data_path:
            continue
        match = re.search(r'pose\.bones\["([^"]+)"\]', fcurve.data_path)
        if not match:
            continue
        old_name = match.group(1)
        new_name = rename_map.get(old_name)
        if new_name:
            fcurve.data_path = fcurve.data_path.replace(f'pose.bones["{old_name}"]', f'pose.bones["{new_name}"]')
            updated += 1
    return updated


def _rename_mesh_vertex_groups(armature, rename_map):
    renamed = 0
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        has_modifier = any(mod.type == 'ARMATURE' and mod.object == armature for mod in obj.modifiers)
        if not has_modifier and obj.parent != armature:
            continue
        for old_name, new_name in rename_map.items():
            vg = obj.vertex_groups.get(old_name)
            if vg and not obj.vertex_groups.get(new_name):
                vg.name = new_name
                renamed += 1
    return renamed


def _bone_midpoint(edit_bone):
    return (edit_bone.head + edit_bone.tail) * 0.5


def _make_helper_bone(edit_bones, name, head, tail, parent=None):
    if name in edit_bones:
        bone = edit_bones[name]
    else:
        bone = edit_bones.new(name)
    bone.head = Vector(head)
    bone.tail = Vector(tail)
    if (bone.tail - bone.head).length < 0.001:
        bone.tail = bone.head + Vector((0, 0, 0.05))
    bone.parent = parent
    bone.use_connect = False
    bone.use_deform = False
    return bone


def _ensure_root_bone(armature):
    ensure_object_mode()
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    eb = armature.data.edit_bones
    pelvis = eb.get('pelvis') or eb.get('mixamorig:Hips')
    if 'root' not in eb:
        root = eb.new('root')
        if pelvis:
            root.head = pelvis.head.copy()
            root.tail = pelvis.head.copy()
            root.tail.z += max(pelvis.length * 0.25, 0.1)
        else:
            root.head = (0, 0, 0)
            root.tail = (0, 0, 0.1)
        root.use_deform = False
        log_info('已新增UE5 root骨骼')
    else:
        root = eb['root']
        root.use_deform = False
    pelvis = eb.get('pelvis')
    if pelvis:
        pelvis.parent = root
        pelvis.use_connect = False
    bpy.ops.object.mode_set(mode='OBJECT')


def _add_manny_style_auxiliary_bones(armature):
    """Add a conservative subset of UE5 Manny-style IK/helper bones.

    These bones are non-deforming helper bones. They improve UE-style skeleton layout
    and IK Retargeter friendliness without trying to fake full Manny deformation.
    """
    ensure_object_mode()
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    eb = armature.data.edit_bones
    root = eb.get('root')
    pelvis = eb.get('pelvis')
    if not root or not pelvis:
        bpy.ops.object.mode_set(mode='OBJECT')
        log_warning('缺少root或pelvis，跳过UE5辅助骨骼生成')
        return 0

    created = 0
    foot_l = eb.get('foot_l')
    foot_r = eb.get('foot_r')
    hand_l = eb.get('hand_l')
    hand_r = eb.get('hand_r')

    base = pelvis.head.copy()
    ik_foot_root = _make_helper_bone(eb, 'ik_foot_root', base, base + Vector((0, 0, 0.08)), parent=root)
    for side, foot in [('l', foot_l), ('r', foot_r)]:
        if foot:
            pos = foot.tail.copy()
            _make_helper_bone(eb, f'ik_foot_{side}', pos, pos + Vector((0, 0, 0.08)), parent=ik_foot_root)
            created += 1

    ik_hand_root = _make_helper_bone(eb, 'ik_hand_root', base + Vector((0, 0, 0.12)), base + Vector((0, 0, 0.20)), parent=root)
    gun_pos = hand_r.head.copy() if hand_r else base + Vector((0, -0.2, 1.0))
    ik_hand_gun = _make_helper_bone(eb, 'ik_hand_gun', gun_pos, gun_pos + Vector((0, 0, 0.08)), parent=ik_hand_root)
    if hand_l:
        pos = hand_l.tail.copy()
        _make_helper_bone(eb, 'ik_hand_l', pos, pos + Vector((0, 0, 0.08)), parent=ik_hand_gun)
        created += 1
    if hand_r:
        pos = hand_r.tail.copy()
        _make_helper_bone(eb, 'ik_hand_r', pos, pos + Vector((0, 0, 0.08)), parent=ik_hand_gun)
        created += 1

    # Lightweight twist helpers. Non-deforming and parented in-chain to improve naming compatibility.
    twist_specs = [
        ('upperarm_twist_01_l', 'upperarm_l'), ('lowerarm_twist_01_l', 'lowerarm_l'),
        ('upperarm_twist_01_r', 'upperarm_r'), ('lowerarm_twist_01_r', 'lowerarm_r'),
        ('thigh_twist_01_l', 'thigh_l'), ('calf_twist_01_l', 'calf_l'),
        ('thigh_twist_01_r', 'thigh_r'), ('calf_twist_01_r', 'calf_r'),
    ]
    for twist_name, parent_name in twist_specs:
        parent = eb.get(parent_name)
        if not parent:
            continue
        mid = _bone_midpoint(parent)
        direction = parent.vector.normalized() if parent.length > 0 else Vector((0, 0, 1))
        _make_helper_bone(eb, twist_name, mid, mid + direction * max(parent.length * 0.2, 0.05), parent=parent)
        created += 1

    bpy.ops.object.mode_set(mode='OBJECT')
    log_info(f'已生成UE5辅助骨骼/IK骨骼: {created} 个')
    return created


def _split_pelvis_motion_to_root(armature, mode):
    if mode != UE5_ROOT_BONE:
        return
    action = armature.animation_data.action if armature.animation_data else None
    if not action:
        return
    pelvis_curves = [fc for fc in action.fcurves if fc.data_path == 'pose.bones["pelvis"].location']
    if not pelvis_curves:
        log_warning('未找到pelvis位移曲线，跳过Root Motion拆分')
        return
    for fc in list(pelvis_curves):
        if fc.array_index not in (0, 1):
            continue
        new_fc = action.fcurves.new(data_path='pose.bones["root"].location', index=fc.array_index)
        for kp in fc.keyframe_points:
            new_kp = new_fc.keyframe_points.insert(kp.co.x, kp.co.y, options={'FAST'})
            new_kp.interpolation = kp.interpolation
        new_fc.update()
        for kp in fc.keyframe_points:
            kp.co.y = 0.0
            kp.handle_left.y = 0.0
            kp.handle_right.y = 0.0
        fc.update()
    log_info('已将pelvis水平位移拆分到root骨骼，pelvis保留垂直身体运动')


def convert_mixamo_armature_to_ue5_basic(armature, root_motion_mode=UE5_ROOT_NONE, add_auxiliary_bones=True):
    """Convert a baked Mixamo-style armature to a UE5-friendly humanoid profile."""
    if not armature or armature.type != 'ARMATURE':
        raise ValueError('UE5转换需要一个有效Armature')
    log_info('开始转换为UE5 Humanoid骨架')
    updated_curves = _rename_action_paths(armature, MIXAMO_TO_UE5_BASIC)
    renamed_vgroups = _rename_mesh_vertex_groups(armature, MIXAMO_TO_UE5_BASIC)
    ensure_object_mode()
    bpy.context.view_layer.objects.active = armature
    armature.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    eb = armature.data.edit_bones
    renamed = 0
    for old_name, new_name in MIXAMO_TO_UE5_BASIC.items():
        if old_name in eb and new_name not in eb:
            eb[old_name].name = new_name
            renamed += 1
    bpy.ops.object.mode_set(mode='OBJECT')
    _ensure_root_bone(armature)
    if add_auxiliary_bones:
        _add_manny_style_auxiliary_bones(armature)
    _split_pelvis_motion_to_root(armature, root_motion_mode)
    missing = [name for name in UE5_BASIC_REQUIRED if name not in armature.data.bones]
    if missing:
        log_warning('UE5骨架仍缺失部分核心骨骼: ' + ', '.join(missing[:20]))
    log_info(f'UE5转换完成: bones_renamed={renamed}, fcurves={updated_curves}, vertex_groups={renamed_vgroups}, missing={len(missing)}')
    if not armature.name.endswith('_UE5') and not armature.name.endswith('_UE5Basic'):
        armature.name = armature.name.replace('Mixamo', 'UE5') if 'Mixamo' in armature.name else armature.name + '_UE5'
    return armature


def get_armature_meshes(armature):
    meshes = []
    for obj in bpy.context.scene.objects:
        if obj.type != 'MESH':
            continue
        has_modifier = any(mod.type == 'ARMATURE' and mod.object == armature for mod in obj.modifiers)
        if has_modifier or obj.parent == armature:
            meshes.append(obj)
    return meshes


def select_armature_export_set(armature, include_mesh=True):
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    if include_mesh:
        for mesh in get_armature_meshes(armature):
            mesh.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature


def export_armature_to_ue5_fbx(armature, filepath, include_mesh=True):
    """Export an armature and linked meshes using Unreal-oriented FBX settings."""
    if not filepath:
        raise ValueError('请先设置FBX输出路径')
    if not filepath.lower().endswith('.fbx'):
        filepath += '.fbx'
    if not armature or armature.type != 'ARMATURE':
        raise ValueError('UE5 FBX导出需要选中或指定一个Armature')
    ensure_object_mode()
    select_armature_export_set(armature, include_mesh=include_mesh)
    bpy.ops.export_scene.fbx(
        filepath=filepath,
        use_selection=True,
        object_types={'ARMATURE', 'MESH'} if include_mesh else {'ARMATURE'},
        add_leaf_bones=False,
        use_armature_deform_only=False,
        bake_anim=True,
        bake_anim_use_all_bones=True,
        bake_anim_use_nla_strips=False,
        bake_anim_use_all_actions=False,
        bake_anim_force_startend_keying=True,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_UNITS',
        use_space_transform=True,
        primary_bone_axis='Y',
        secondary_bone_axis='X',
        armature_nodetype='NULL',
    )
    log_info(f'UE5 FBX已导出: {filepath}')
    return filepath


def export_selected_fbx_for_unreal(filepath):
    active = bpy.context.view_layer.objects.active
    if not active or active.type != 'ARMATURE':
        selected_armatures = [obj for obj in bpy.context.selected_objects if obj.type == 'ARMATURE']
        active = selected_armatures[0] if selected_armatures else None
    return export_armature_to_ue5_fbx(active, filepath, include_mesh=True)
