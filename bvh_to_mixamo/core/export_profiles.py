"""FBX export profiles for Mixamo and Unreal Engine workflows.

V3.4.1 adds a small export layer so users do not need to manually configure
Blender's FBX exporter every time. Mixamo and UE5 use different practical
settings, so both are exposed as first-class export presets.
"""

import bpy

from .armature_utils import ensure_object_mode
from .logger import log_info
from .ue5_profile import TARGET_UE5_BASIC, get_armature_meshes

EXPORT_PROFILE_AUTO = 'AUTO'
EXPORT_PROFILE_MIXAMO = 'MIXAMO_FBX'
EXPORT_PROFILE_UE5 = 'UE5_FBX'


def _normalize_fbx_path(filepath):
    if not filepath:
        raise ValueError('请先设置FBX输出路径')
    if not filepath.lower().endswith('.fbx'):
        filepath += '.fbx'
    return filepath


def resolve_export_profile(scene):
    profile = getattr(scene, 'bvh_export_profile', EXPORT_PROFILE_AUTO)
    if profile == EXPORT_PROFILE_AUTO:
        return EXPORT_PROFILE_UE5 if scene.bvh_target_skeleton == TARGET_UE5_BASIC else EXPORT_PROFILE_MIXAMO
    return profile


def select_export_set(armature, include_mesh=True):
    for obj in bpy.context.scene.objects:
        obj.select_set(False)
    if include_mesh:
        for mesh in get_armature_meshes(armature):
            mesh.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature


def export_armature_to_mixamo_fbx(armature, filepath, include_mesh=True):
    """Export the current Mixamo-style armature with a stable general FBX preset.

    This preset keeps Mixamo bone names intact and avoids UE-specific root/axis
    assumptions. It is intended for the existing Mixamo/template workflow and for
    general DCC reuse.
    """
    filepath = _normalize_fbx_path(filepath)
    if not armature or armature.type != 'ARMATURE':
        raise ValueError('Mixamo FBX导出需要选中或指定一个Armature')
    ensure_object_mode()
    select_export_set(armature, include_mesh=include_mesh)
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
    log_info(f'Mixamo FBX已导出: {filepath}')
    return filepath


def export_armature_to_ue5_fbx(armature, filepath, include_mesh=True):
    """Export an armature and linked meshes using Unreal-oriented FBX settings."""
    filepath = _normalize_fbx_path(filepath)
    if not armature or armature.type != 'ARMATURE':
        raise ValueError('UE5 FBX导出需要选中或指定一个Armature')
    ensure_object_mode()
    select_export_set(armature, include_mesh=include_mesh)
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


def export_armature_by_profile(armature, filepath, profile, include_mesh=True):
    if profile == EXPORT_PROFILE_UE5:
        return export_armature_to_ue5_fbx(armature, filepath, include_mesh=include_mesh)
    if profile == EXPORT_PROFILE_MIXAMO:
        return export_armature_to_mixamo_fbx(armature, filepath, include_mesh=include_mesh)
    raise ValueError(f'未知FBX导出预设: {profile}')
