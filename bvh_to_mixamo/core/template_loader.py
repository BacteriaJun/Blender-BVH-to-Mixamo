import os
import shutil
import tempfile

import bpy

from .armature_utils import find_mixamo_armature_in_objects, is_mixamo_armature
from .logger import log_info, log_warning
from .paths import get_default_template_fbx_path, get_templates_dir
from .vrm_profile import is_vrm_body_armature

TEMPLATE_PRESET_BUILTIN_DEFAULT = 'BUILTIN_DEFAULT_CHARACTER'
TEMPLATE_PRESET_BUILTIN_WHITE = 'BUILTIN_WHITE_CHARACTER'
TEMPLATE_PRESET_BUILTIN_PINK = 'BUILTIN_PINK_CHARACTER'
TEMPLATE_PRESET_BUILTIN_PURPLE = 'BUILTIN_PURPLE_CHARACTER'
TEMPLATE_PRESET_BUILTIN_BLACK = 'BUILTIN_BLACK_CHARACTER'
TEMPLATE_PRESET_BUILTIN_GREEN = 'BUILTIN_GREEN_CHARACTER'
TEMPLATE_PRESET_CUSTOM_FBX = 'CUSTOM_FBX'

TEMPLATE_REGISTRY = {
    TEMPLATE_PRESET_BUILTIN_DEFAULT: {
        "name": "Default Character",
        "filename": "mixamo_default_character.fbx",
        "format": "FBX",
        "description": "Built-in Mixamo-compatible standard character template",
    },
    TEMPLATE_PRESET_BUILTIN_WHITE: {
        "name": "Default White",
        "filename": "mixamo_default_white.fbx",
        "format": "FBX",
        "description": "Built-in white material variant with the same template rig",
    },
    TEMPLATE_PRESET_BUILTIN_PINK: {
        "name": "Default Pink",
        "filename": "mixamo_default_pink.fbx",
        "format": "FBX",
        "description": "Built-in pink material variant with the same template rig",
    },
    TEMPLATE_PRESET_BUILTIN_PURPLE: {
        "name": "Default Purple",
        "filename": "mixamo_default_purple.fbx",
        "format": "FBX",
        "description": "Built-in purple material variant with the same template rig",
    },
    TEMPLATE_PRESET_BUILTIN_BLACK: {
        "name": "Default Black",
        "filename": "mixamo_default_black.fbx",
        "format": "FBX",
        "description": "Built-in black material variant with the same template rig",
    },
    TEMPLATE_PRESET_BUILTIN_GREEN: {
        "name": "Default Green",
        "filename": "mixamo_default_green.fbx",
        "format": "FBX",
        "description": "Built-in green material variant with the same template rig",
    },
}


def get_template_fbx_path(context):
    preset = getattr(context.scene, "bvh_template_preset", TEMPLATE_PRESET_BUILTIN_DEFAULT)
    if preset == TEMPLATE_PRESET_CUSTOM_FBX:
        path = getattr(context.scene, "bvh_custom_template_fbx_path", "")
        if not path:
            raise FileNotFoundError("Please select a custom FBX/VRM character file.")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Custom character file does not exist: {path}")
        if not path.lower().endswith((".fbx", ".vrm", ".glb", ".gltf")):
            raise ValueError("Custom character template must be a .fbx, .vrm, .glb, or .gltf file.")
        return path
    template_info = TEMPLATE_REGISTRY.get(preset) or TEMPLATE_REGISTRY[TEMPLATE_PRESET_BUILTIN_DEFAULT]
    filename = template_info.get("filename", "mixamo_default_character.fbx")
    if preset == TEMPLATE_PRESET_BUILTIN_DEFAULT:
        path = get_default_template_fbx_path()
    else:
        path = os.path.join(get_templates_dir(), filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Built-in character template is missing: {path}")
    return path


def _import_vrm_or_gltf(filepath):
    """Import VRM through Blender's glTF importer.

    Blender's native glTF importer can usually read VRM because VRM is based on
    binary glTF. If the .vrm extension is rejected by a local Blender build, this
    function retries with a temporary .glb copy.
    """
    try:
        bpy.ops.import_scene.gltf(filepath=filepath)
        return
    except Exception as first_exc:
        if not filepath.lower().endswith('.vrm'):
            raise
        tmp = None
        try:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.glb')
            tmp.close()
            shutil.copyfile(filepath, tmp.name)
            bpy.ops.import_scene.gltf(filepath=tmp.name)
            log_warning(f'直接导入VRM失败，已用临时GLB路径重试: {first_exc}')
        finally:
            if tmp and os.path.exists(tmp.name):
                try:
                    os.remove(tmp.name)
                except Exception:
                    pass


def import_character_template_fbx(template_path):
    if not template_path or not os.path.exists(template_path):
        raise FileNotFoundError(f"Character template does not exist: {template_path}")
    before = set(bpy.data.objects)
    log_info(f"Importing character template: {template_path}")
    lower = template_path.lower()
    if lower.endswith('.fbx'):
        bpy.ops.import_scene.fbx(filepath=template_path)
    elif lower.endswith(('.vrm', '.glb', '.gltf')):
        _import_vrm_or_gltf(template_path)
    else:
        raise ValueError('Unsupported character template format. Use FBX, VRM, GLB, or GLTF.')

    imported = [obj for obj in bpy.data.objects if obj not in before]
    if not imported:
        raise RuntimeError("No imported objects were detected after importing the character template.")

    armatures = [obj for obj in imported if obj and obj.type == 'ARMATURE']
    armature = None
    for candidate in armatures:
        if is_vrm_body_armature(candidate):
            armature = candidate
            break
    if not armature:
        armature = find_mixamo_armature_in_objects(imported) or find_mixamo_armature_in_objects(bpy.context.selected_objects)
    if not armature:
        raise RuntimeError("No armature object was found in the character template.")

    if not (is_mixamo_armature(armature) or is_vrm_body_armature(armature)):
        log_warning("The template armature is not a typical Mixamo or VRM J_Bip rig; the add-on will still attempt to use it as the target.")
    if armature.animation_data and armature.animation_data.action:
        armature.animation_data.action = None
    base_name = os.path.splitext(os.path.basename(template_path))[0]
    armature.name = f"{base_name}_AnimatedRig"
    armature.data.name = f"{base_name}_AnimatedRigData"
    for obj in imported:
        obj.select_set(False)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature
    log_info(f"Character template import completed. Target armature: {armature.name}，Imported object count: {len(imported)}")
    return armature, imported
