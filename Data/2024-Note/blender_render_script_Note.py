# Import necessary libraries
from matplotlib import path                     # Used for point-in-polygon test
import bpy                                     # Blender Python API
from bpy import context
import numpy as np                             # For numerical operations like range
import mathutils                               # For Blender's math types like vectors
import sys
import time

# Set the target object whose position will be updated and rendered
target_obj = bpy.data.objects['RING']

# Set the reference object that defines the Field Of View (FOV) as a plane
fov_plane = bpy.data.objects['Plane']

# Define the output folder for saving rendered images and position data
output_folder = "your_output_folder"

def is_point_in_polygon(point, polygon):
    """
    Check if a 2D point lies within a polygon.
    
    Args:
        point (tuple): The (x, y) coordinates of the point.
        polygon (list): List of (x, y) tuples defining the polygon's vertices.
    
    Returns:
        bool: True if the point is inside the polygon, False otherwise.
    """
    p = path.Path(polygon)
    return p.contains_points([point])

def find_vertices_positions():
    """
    Get the world-space (x, y) coordinates of the plane's 4 vertices.
    
    Returns:
        list: A list of tuples representing the polygon that defines the plane.
    """
    polygon = []

    # Get the vertex coordinates in world space
    v = fov_plane.data.vertices
    for vertax in v:
        vector3d = fov_plane.matrix_world @ vertax.co
        polygon.append((vector3d.x, vector3d.y))

    # Reorder vertices to ensure consistent winding (avoids rendering issues)
    tmp1 = polygon[0]
    tmp2 = polygon[1]
    tmp3 = polygon[2]
    tmp4 = polygon[3]
    polygon = [tmp1, tmp2, tmp4, tmp3]
    
    return polygon

def save_position_data():
    """
    Append the current (x, y) position of the target object to a text file.
    """
    with open(output_folder + "PositionData.txt", "a") as file:
        x = target_obj.location.x
        y = target_obj.location.y
        file.write(f"{x}, {y}\n")  # Log position

def render_frame(frame_counter):
    """
    Render the current frame and save it along with the object's position.
    
    Args:
        frame_counter (int): A counter used to name the rendered image files.
    """
    save_position_data()  # Log object position to file

    # Set file path for rendering output
    bpy.context.scene.render.filepath = output_folder + "Images/" + "render_" + str(frame_counter) + ".jpg"
    
    # Trigger rendering and save as still image
    bpy.ops.render.render(write_still=True)

# Find the polygon of interest from the plane's vertices
polygon = find_vertices_positions()

# Determine bounding box of the polygon
max_x = max(polygon, key=lambda point: point[0])[0]
min_x = min(polygon, key=lambda point: point[0])[0]
max_y = max(polygon, key=lambda point: point[1])[1]
min_y = min(polygon, key=lambda point: point[1])[1]

# Step size for scanning the area
step_length = 0.05

# Initialize frame counter
current_iteration = 0

# Iterate through a grid of points in the bounding box
for x in np.arange(min_x, max_x, step_length):
    for y in np.arange(min_y, max_y, step_length):
        point = (x, y)
        
        # Only proceed if the point lies inside the polygon
        if is_point_in_polygon(point, polygon):
            # Move the target object to the new position
            target_obj.location = mathutils.Vector((x, y, target_obj.location.z))
            
            # Render and save the frame
            render_frame(current_iteration)
            
            # Increment the frame counter
            current_iteration += 1


### This script essentially loops over a grid of (x, y) positions inside a defined polygon (from the Plane object),
### moves the RING object to each of those points, renders a frame, and saves both the image and the position data.