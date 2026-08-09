"""Compatibility module for retarget operator separation.
The current conversion operator delegates to core.retarget_engine.
"""
from ..core.retarget_engine import transfer_animation

__all__ = ["transfer_animation"]
