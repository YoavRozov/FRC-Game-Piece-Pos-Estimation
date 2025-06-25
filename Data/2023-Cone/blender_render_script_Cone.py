# Import necessary libraries
from matplotlib import path                 # For point-in-polygon detection
import bpy                                 # Blender's Python API
from bpy import context
import numpy as np                         # Numerical operations
import mathutils                           # Blender-specific vector math
import sys                                 # System interaction (e.g., output to console)
import time                                # Timing for progress estimation
import math                                # Standard math functions

# Set the object to be moved and rotated
target_obj = bpy.data.objects['CONE']

# Reference plane defining the field of view area
fov_plane = bpy.data.objects['Plane']

# Folder where images and data will be saved
output_folder = "your_output_folder"

def update_progress(progress, eta):
    """
    Print a simple text progress bar with estimated time remaining.
    
    Args:
        progress (int): Current progress as a percentage (0–100).
        eta (float): Estimated time remaining (in minutes).
    """
    sys.stdout.write('\r[{0}] {1}%  ETA: {2}m'.format('#' * progress, progress, round(eta, 2)))
    sys.stdout.flush()

def is_point_in_polygon(point, polygon):
    """
    Check if a 2D point lies within a given polygon.

    Args:
        point (tuple): (x, y) coordinates of the point.
        polygon (list): List of (x, y) vertices forming the polygon.

    Returns:
        bool: True if inside, False otherwise.
    """
    p = path.Path(polygon)
    return p.contains_points([point])

def find_vertices_positions():
    """
    Retrieve the world-space (x, y) positions of the plane's corners.

    Returns:
        list: Polygon defined by reordered vertex coordinates.
    """
    polygon = []
    v = fov_plane.data.vertices
    for vertax in v:
        vector3d = fov_plane.matrix_world @ vertax.co
        polygon.append((vector3d.x, vector3d.y))
    
    # Reorder to correct winding order (if necessary)
    tmp1, tmp2, tmp3, tmp4 = polygon[:4]
    return [tmp1, tmp2, tmp4, tmp3]

def save_position_data(x, y, rotation):
    """
    Append the current (x, y, rotation) state of the object to a text file.

    Args:
        x (float): X coordinate.
        y (float): Y coordinate.
        rotation (float): Rotation in degrees.
    """
    with open(output_folder + "PositionData.txt", "a") as file:
        file.write(f"{x}, {y}, {rotation}\n")

def render_frame(frame_counter):
    """
    Render and save the current frame.

    Args:
        frame_counter (int): Used for naming the image file.
    """
    bpy.context.scene.render.filepath = output_folder + f"Images/render_{frame_counter}.jpg"
    bpy.ops.render.render(write_still=True)

# Get the field of view polygon
polygon = find_vertices_positions()

# Compute the bounding box around the polygon
max_x = max(polygon, key=lambda point: point[0])[0]
min_x = min(polygon, key=lambda point: point[0])[0]
max_y = max(polygon, key=lambda point: point[1])[1]
min_y = min(polygon, key=lambda point: point[1])[1]

# Step sizes for position and rotation
step_length = 0.05                # Grid step in Blender units
rotation_step_length = 5         # Rotation step in degrees

# Counters and timing setup
current_iteration = 0
start_time = time.time()

# Estimate total number of iterations for progress tracking
total_positions = len(np.arange(min_x, max_x, step_length)) * len(np.arange(min_y, max_y, step_length))
total_rotations = 360 // rotation_step_length
total_iterations = total_positions * total_rotations

# Main loop: scan through (x, y) positions inside polygon, apply rotations
for x in np.arange(min_x, max_x, step_length):
    for y in np.arange(min_y, max_y, step_length):
        point = (x, y)
        if is_point_in_polygon(point, polygon):
            for rotation in range(0, 360, rotation_step_length):
                # Move object to new location and set rotation
                target_obj.location = mathutils.Vector((x, y, target_obj.location.z))
                target_obj.rotation_euler.z = math.radians(rotation)

                # Save position and rotation to file
                save_position_data(x, y, rotation)

                # Render and save image
                render_frame(current_iteration)

                # Update progress bar in terminal
                progress = int(100 * (current_iteration + 1) / total_iterations)
                elapsed_time = time.time() - start_time
                iterations_left = total_iterations - current_iteration + 1
                time_per_iteration = elapsed_time / (current_iteration + 1)
                eta = iterations_left * time_per_iteration / 60.0
                update_progress(progress, eta)

                # Increment frame count
                current_iteration += 1

### This script scans a 2D area defined by a plane and for each valid (x, y) location inside it, rotates the object (a CONE) in steps,
### rendering and logging every transformation. The result is a large set of systematically varied object renderings and pose data.