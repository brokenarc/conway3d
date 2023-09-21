from abc import ABC, abstractmethod
import math
from typing import Any

import bpy
from mathutils import Vector

from .blendutil import get_child_by_name, set_active_layer_collection

C = bpy.context
D = bpy.data
