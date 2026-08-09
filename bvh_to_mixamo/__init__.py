import bpy

from .addon_info import ADDON_NAME, ADDON_VERSION, bl_info
from .core.logger import log_info
from .operators import classes as operator_classes
from .properties import register_properties, unregister_properties
from .ui import classes as ui_classes

classes = operator_classes + ui_classes
VERSION = '.'.join(str(part) for part in ADDON_VERSION)


def register():
    register_properties()
    for cls in classes:
        bpy.utils.register_class(cls)
    log_info(f'{ADDON_NAME} v{VERSION} registered | 3D View > N Sidebar > BVH Retarget')


def unregister():
    for cls in reversed(classes):
        try:
            bpy.utils.unregister_class(cls)
        except RuntimeError:
            pass
    unregister_properties()
    log_info(f'{ADDON_NAME} v{VERSION} unregistered')


if __name__ == '__main__':
    register()
