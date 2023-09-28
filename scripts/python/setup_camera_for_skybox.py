import bpy
import os
from math import radians

def setup_camera_for_skybox():
    # Check if a camera exists or create one
    if "SkyboxCamera" in bpy.data.cameras:
        camera = bpy.data.cameras["SkyboxCamera"]
        cam_obj = bpy.data.objects["SkyboxCamera"]
    else:
        bpy.ops.object.camera_add(location=(0, 0, 0))
        cam_obj = bpy.context.active_object
        cam_obj.name = "SkyboxCamera"
        camera = cam_obj.data
        camera.name = "SkyboxCamera"
    
    # Set camera to perspective with a 90-degree field of view
    camera.type = 'PERSP'
    camera.angle = 1.5708  # This is 90 degrees in radians

    # Set render resolution (can be adjusted)
    bpy.context.scene.render.resolution_x = 2048
    bpy.context.scene.render.resolution_y = 2048
    bpy.context.scene.cycles.samples = 50
    # Enabling denoising
    bpy.context.scene.cycles.use_denoising = True
    bpy.context.scene.cycles.denoiser = 'OPENIMAGEDENOISE'    
    #bpy.context.scene.cycles.device = 'GPU'
    

    return cam_obj


def render_skybox(output_path):
    orientations = [
        ("pz", (90, 0, 0)),      # forward
        ("px", (90, 0, -90)),   # right
        ("nz", (-90, 180, 0)),    # backward
        ("nx", (90, 0, 90)),    # left
        ("py", (0, -180, 180)),    # up
        ("ny", (0, 0, 0))       # down
    ]
    
    camera = setup_camera_for_skybox()

    # Ensure output path exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    for name, rotation in orientations:
        camera.rotation_euler = [radians(angle) for angle in rotation]
        filepath = os.path.join(output_path, f"{name}.png")
        bpy.context.scene.render.filepath = filepath
        bpy.ops.render.render(write_still=True)

# Set the path where you want the images to be saved
output_path = "/Users/smielniczuk/Documents/works/ic/xr-midas-threejs/design/skybox"

# Render skybox
render_skybox(output_path)
