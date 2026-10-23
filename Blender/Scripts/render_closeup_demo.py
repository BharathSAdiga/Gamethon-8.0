"""
Render Close-up Demo for Sector09 Props & Terminals
"""

import os
import math
import bpy

REPO_ROOT = r"D:\unreal engine"
BLEND_FILE = os.path.join(REPO_ROOT, "Blender", "Blend", "Sector09_Level1_Kit.blend")
OUTPUT_RENDER = os.path.join(REPO_ROOT, "Blender", "Sector09_Closeup_Render.png")

bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

# Focus on terminal and prop row (Row 4/5: around Y=-14 to -18, X=0 to 12)
cam = bpy.context.scene.camera
if not cam:
    cam_data = bpy.data.cameras.new("Closeup_Camera")
    cam = bpy.data.objects.new("Closeup_Camera", cam_data)
    bpy.context.scene.collection.objects.link(cam)
    bpy.context.scene.camera = cam

cam.data.lens = 50
cam.location = (1.5, -20.0, 3.2)
cam.rotation_euler = (math.radians(75), 0, math.radians(-15))

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.filepath = OUTPUT_RENDER

bpy.ops.render.render(write_still=True)
print("Closeup render complete!")
