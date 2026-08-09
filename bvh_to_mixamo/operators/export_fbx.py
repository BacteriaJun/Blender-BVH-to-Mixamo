"""FBX export operators for Mixamo and Unreal Engine 5 workflows."""

import traceback

import bpy
from bpy.types import Operator

from ..core.export_profiles import (
    EXPORT_PROFILE_MIXAMO,
    EXPORT_PROFILE_UE5,
    export_armature_by_profile,
    resolve_export_profile,
)
from ..core.logger import log_error, log_info


def _get_export_armature(context):
    scene = context.scene
    if scene.bvh_last_output_armature and scene.bvh_last_output_armature in bpy.data.objects:
        obj = bpy.data.objects[scene.bvh_last_output_armature]
        if obj.type == 'ARMATURE':
            return obj
    active = context.view_layer.objects.active
    if active and active.type == 'ARMATURE':
        return active
    selected = [obj for obj in context.selected_objects if obj.type == 'ARMATURE']
    return selected[0] if selected else None


def _run_export(context, report, profile=None):
    scene = context.scene
    armature = _get_export_armature(context)
    if not armature:
        report({'ERROR'}, 'Create or select an Armature first, or complete one conversion before exporting.')
        return {'CANCELLED'}
    if not scene.bvh_export_path:
        report({'ERROR'}, 'Set the FBX output path first.')
        return {'CANCELLED'}
    active_profile = profile or resolve_export_profile(scene)
    try:
        path = export_armature_by_profile(
            armature,
            scene.bvh_export_path,
            active_profile,
            include_mesh=scene.bvh_export_include_mesh,
        )
        scene.bvh_last_output_armature = armature.name
        label = 'UE5' if active_profile == EXPORT_PROFILE_UE5 else 'Mixamo'
        log_info(f'{label} FBXexport completed: {path}')
        report({'INFO'}, f'{label} FBXexport completed: {path}')
        return {'FINISHED'}
    except Exception as exc:
        log_error(f'FBX export failed: {exc}')
        log_error(traceback.format_exc())
        report({'ERROR'}, f'FBX export failed: {exc}')
        return {'CANCELLED'}


class MIXAMO_OT_export_fbx(Operator):
    bl_idname = "mixamo.export_fbx"
    bl_label = "Export with Selected Preset"
    bl_description = "Export the current or most recent output armature using the selected FBX export preset."
    bl_options = {'REGISTER'}

    def execute(self, context):
        return _run_export(context, self.report)


class MIXAMO_OT_export_mixamo_fbx(Operator):
    bl_idname = "mixamo.export_mixamo_fbx"
    bl_label = "Export Mixamo FBX"
    bl_description = "Export the current or most recent output armature with the Mixamo/general FBX preset."
    bl_options = {'REGISTER'}

    def execute(self, context):
        return _run_export(context, self.report, profile=EXPORT_PROFILE_MIXAMO)


class MIXAMO_OT_export_ue5_fbx(Operator):
    bl_idname = "mixamo.export_ue5_fbx"
    bl_label = "Export UE5 FBX"
    bl_description = "Export the current or most recent output armature with the built-in UE5 FBX preset."
    bl_options = {'REGISTER'}

    def execute(self, context):
        return _run_export(context, self.report, profile=EXPORT_PROFILE_UE5)


def export_selected_fbx(filepath):
    bpy.ops.export_scene.fbx(filepath=filepath, use_selection=True, add_leaf_bones=False)


def export_selected_fbx_for_unreal(filepath):
    from ..core.export_profiles import export_armature_to_ue5_fbx
    active = bpy.context.view_layer.objects.active
    return export_armature_to_ue5_fbx(active, filepath, include_mesh=True)
