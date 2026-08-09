import traceback

import bpy

from .armature_utils import calculate_motion_scale, ensure_object_mode
from .logger import log_error, log_info

ROOT_KEEP = 'KEEP'
ROOT_IN_PLACE = 'IN_PLACE'
ROOT_SCALE = 'SCALE'
RETARGET_CONSTRAINT = 'CONSTRAINT_BAKE'

LIMB_KEYWORDS = (
    'LeftArm', 'LeftForeArm', 'LeftHand', 'RightArm', 'RightForeArm', 'RightHand',
    'LeftUpLeg', 'LeftLeg', 'LeftFoot', 'RightUpLeg', 'RightLeg', 'RightFoot',
    'UpperArm', 'LowerArm', 'Hand', 'UpperLeg', 'LowerLeg', 'Foot',
)



def estimate_chain_length(armature, chain):
    total = 0.0
    for bone_name in chain:
        bone = armature.data.bones.get(bone_name) if armature else None
        if not bone:
            return 0.0
        total += bone.length
    return total


def calculate_motion_scale_for_mapping(source_armature, target_armature, target_to_source_mapping=None):
    """Calculate scale for same-name Mixamo or mapped target rigs.

    When target_to_source_mapping is provided, keys are target bone names and
    values are source Mixamo bone names. This is used by the VRM body-only
    profile where the target keeps J_Bip_* names.
    """
    if not target_to_source_mapping:
        return calculate_motion_scale(source_armature, target_armature)
    source_to_target = {src: tgt for tgt, src in target_to_source_mapping.items()}
    source_chains = [
        ('mixamorig:LeftUpLeg', 'mixamorig:LeftLeg', 'mixamorig:LeftFoot'),
        ('mixamorig:RightUpLeg', 'mixamorig:RightLeg', 'mixamorig:RightFoot'),
    ]
    ratios = []
    for source_chain in source_chains:
        target_chain = tuple(source_to_target.get(name, '') for name in source_chain)
        source_len = estimate_chain_length(source_armature, source_chain)
        target_len = estimate_chain_length(target_armature, target_chain)
        if source_len > 0 and target_len > 0:
            ratios.append(target_len / source_len)
    if ratios:
        ratio = sum(ratios) / len(ratios)
        log_info(f'Motion Scale按映射腿长计算: ratio={ratio:.4f}')
        return ratio
    log_info('映射腿长不可用，回退到同名Mixamo比例计算')
    return calculate_motion_scale(source_armature, target_armature)


def get_action_frame_range(armature):
    action = armature.animation_data.action if armature.animation_data else None
    if action:
        return int(action.frame_range[0]), int(action.frame_range[1])
    return bpy.context.scene.frame_start, bpy.context.scene.frame_end


def clear_pose_constraints(armature):
    if not armature or armature.type != 'ARMATURE':
        return
    for pose_bone in armature.pose.bones:
        for constraint in list(pose_bone.constraints):
            pose_bone.constraints.remove(constraint)


def transfer_animation_with_constraints(source_armature, target_armature, root_motion_mode=ROOT_SCALE, target_to_source_mapping=None):
    log_info('使用稳定Constraint Bake兼容模式转移动画')
    if not source_armature.animation_data or not source_armature.animation_data.action:
        log_error('源骨骼没有动画数据')
        return False

    original_frame = bpy.context.scene.frame_current
    original_active = bpy.context.view_layer.objects.active
    original_scale = source_armature.scale.copy()
    source_original_pos = source_armature.location.copy()
    frame_start, frame_end = get_action_frame_range(source_armature)

    try:
        scale_ratio = calculate_motion_scale_for_mapping(source_armature, target_armature, target_to_source_mapping) if root_motion_mode == ROOT_SCALE else 1.0
        source_armature.scale = (scale_ratio, scale_ratio, scale_ratio)
        source_armature.location = target_armature.location.copy()
        bpy.context.view_layer.update()

        if not target_armature.animation_data:
            target_armature.animation_data_create()
        if target_armature.animation_data.action:
            target_armature.animation_data.action = None

        bpy.context.view_layer.objects.active = target_armature
        ensure_object_mode()
        bpy.ops.object.mode_set(mode='POSE')
        clear_pose_constraints(target_armature)

        added = 0
        for pose_bone in target_armature.pose.bones:
            target_bone_name = pose_bone.name
            source_bone_name = target_to_source_mapping.get(target_bone_name, target_bone_name) if target_to_source_mapping else target_bone_name
            if source_bone_name not in source_armature.pose.bones:
                continue
            if source_bone_name == 'mixamorig:Hips' and root_motion_mode != ROOT_IN_PLACE:
                loc = pose_bone.constraints.new('COPY_LOCATION')
                loc.target = source_armature
                loc.subtarget = source_bone_name
                loc.target_space = 'LOCAL'
                loc.owner_space = 'LOCAL'
            rot = pose_bone.constraints.new('COPY_ROTATION')
            rot.target = source_armature
            rot.subtarget = source_bone_name
            is_limb = any((key in source_bone_name) or (key in target_bone_name) for key in LIMB_KEYWORDS)
            rot.target_space = 'POSE' if is_limb else 'LOCAL'
            rot.owner_space = 'POSE' if is_limb else 'LOCAL'
            added += 1
        log_info(f'添加了 {added} 个骨骼约束')

        ensure_object_mode()
        bpy.context.view_layer.objects.active = target_armature
        target_armature.select_set(True)
        source_armature.select_set(False)
        bpy.ops.object.mode_set(mode='POSE')
        for pose_bone in target_armature.pose.bones:
            pose_bone.bone.select = True
        log_info(f'开始烘焙动画: {frame_start} - {frame_end}')
        bpy.ops.nla.bake(
            frame_start=frame_start,
            frame_end=frame_end,
            only_selected=True,
            visual_keying=True,
            clear_constraints=True,
            clear_parents=False,
            use_current_action=False,
            bake_types={'POSE'},
        )
        clear_pose_constraints(target_armature)
        ensure_object_mode()
        return bool(target_armature.animation_data and target_armature.animation_data.action)
    except Exception as exc:
        log_error(f'Constraint Bake动画转移失败: {exc}')
        log_error(traceback.format_exc())
        return False
    finally:
        source_armature.scale = original_scale
        source_armature.location = source_original_pos
        bpy.context.scene.frame_current = original_frame
        if original_active:
            bpy.context.view_layer.objects.active = original_active
        ensure_object_mode()


def simplify_fcurves(armature, factor=0.01):
    if not armature.animation_data or not armature.animation_data.action:
        return
    action = armature.animation_data.action
    for fcurve in action.fcurves:
        try:
            fcurve.simplify(factor=factor)
        except Exception:
            continue
    log_info(f'已尝试简化F-Curves，factor={factor}')


def transfer_animation(source_armature, target_armature, root_motion_mode=ROOT_SCALE, simplify_after_bake=False, simplify_factor=0.01, target_to_source_mapping=None):
    ok = transfer_animation_with_constraints(source_armature, target_armature, root_motion_mode=root_motion_mode, target_to_source_mapping=target_to_source_mapping)
    if ok and simplify_after_bake:
        simplify_fcurves(target_armature, simplify_factor)
    if ok and target_armature.animation_data and target_armature.animation_data.action:
        action = target_armature.animation_data.action
        log_info(f'目标骨骼动画完成: {action.name}, F曲线={len(action.fcurves)}, 帧范围={action.frame_range}')
    return ok
