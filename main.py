import bpy
import importlib
import os
import sys

# ----------------------------------------------------------------------------
# Add the path of this script to sys.path so its modules can be imported.
# ----------------------------------------------------------------------------
script_dir = os.path.dirname(bpy.context.space_data.text.filepath)
sys.path.append(script_dir)

# ----------------------------------------------------------------------------
# Project imports
# ----------------------------------------------------------------------------
from conway3d import create_animation

# ----------------------------------------------------------------------------
# Reload the modules for this project
# ----------------------------------------------------------------------------
MOD_PREFIX = 'conway3d'
map(
    importlib.reload,
    [module for (name, module) in sys.modules.items()
     if name.startswith(MOD_PREFIX)]
)

# ----------------------------------------------------------------------------
# Start the actual project
# ----------------------------------------------------------------------------
create_animation()
