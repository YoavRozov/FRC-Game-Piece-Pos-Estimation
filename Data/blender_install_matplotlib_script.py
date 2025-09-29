# Run this script in Blender's scripting environment to install matplotlib
import subprocess
import sys
import bpy

# Get Blender's user scripts/modules path
target_path = bpy.utils.user_resource("SCRIPTS", path="modules")
print("Installing to:", target_path)

# Install matplotlib into Blender's modules directory
subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib", f"--target={target_path}"])

# Add the modules path to sys.path
modules_path = bpy.utils.user_resource("SCRIPTS", path="modules")
if modules_path not in sys.path:
    sys.path.append(modules_path)

import matplotlib.pyplot as plt

plt.plot([1, 2, 3], [4, 5, 6])

