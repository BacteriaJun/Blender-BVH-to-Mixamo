"""Compatibility module for future dedicated BVH import operators.
The current UI uses file_selectors.py and convert.py; this module keeps the v3.2 project layout extensible.
"""
from ..core.bvh_parser import import_bvh, read_bvh_framerate

__all__ = ["import_bvh", "read_bvh_framerate"]
