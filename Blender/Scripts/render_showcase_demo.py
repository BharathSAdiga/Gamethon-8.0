"""
Render Showcase Demo for Sector09_Level1_Kit.blend
Sets up camera, cyberpunk dramatic lighting, and renders a high-res demonstration view.
"""

import os
import math
import bpy

REPO_ROOT = r"D:\unreal engine"
BLEND_FILE = os.path.join(REPO_ROOT, "Blender", "Blend", "Sector09_Level1_Kit.blend")
OUTPUT_RENDER = os.path.join(REPO_ROOT, "Blender", "Sector09_Demo_Render.png")

# Open the blend file
bpy.ops.wm.open_mainfile(filepath=BLEND_FILE)

# Setup world background (dark cyberpunk slate)
world = bpy.context.scene.world
if not world:
    world = bpy.data.worlds.new("Cyberpunk_World")
    bpy.context.scene.world = world
world.use_nodes = True
bg_node = world.node_tree.nodes.get("Background")
if bg_node:
    bg_node.inputs['Color'].default_value = (0.02, 0.025, 0.035, 1.0)
    bg_node.inputs['Strength'].default_value = 0.5

# Setup dark metallic floor ground plane
bpy.ops.mesh.primitive_plane_add(size=120.0, location=(12.0, -12.0, -0.01))
ground = bpy.context.active_object
ground.name = "Showcase_Ground"
ground_mat = bpy.data.materials.new("M_Showcase_Ground")
ground_mat.use_nodes = True
g_bsdf = ground_mat.node_tree.nodes.get("Principled BSDF")
if g_bsdf:
    g_bsdf.inputs['Base Color'].default_value = (0.03, 0.035, 0.04, 1.0)
    g_bsdf.inputs['Roughness'].default_value = 0.25
    g_bsdf.inputs['Metallic'].default_value = 0.8
ground.data.materials.append(ground_mat)

# Add dramatic lighting:
# 1. Warm overhead sun/key
light_data_sun = bpy.data.lights.new(name="Sun_Key", type='SUN')
light_data_sun.energy = 2.5
light_data_sun.color = (0.85, 0.9, 1.0)
sun_obj = bpy.data.objects.new(name="Sun_Key", object_data=light_data_sun)
sun_obj.rotation_euler = (math.radians(50), math.radians(20), math.radians(-40))
bpy.context.scene.collection.objects.link(sun_obj)

# 2. Cyan area fill light
light_data_fill = bpy.data.lights.new(name="Cyan_Fill", type='AREA')
light_data_fill.energy = 5000.0
light_data_fill.size = 15.0
light_data_fill.color = (0.0, 0.8, 1.0)
fill_obj = bpy.data.objects.new(name="Cyan_Fill", object_data=light_data_fill)
fill_obj.location = (-5.0, 5.0, 12.0)
fill_obj.rotation_euler = (math.radians(45), math.radians(-30), math.radians(20))
bpy.context.scene.collection.objects.link(fill_obj)

# 3. Magenta rim light
light_data_rim = bpy.data.lights.new(name="Magenta_Rim", type='AREA')
light_data_rim.energy = 6000.0
light_data_rim.size = 20.0
light_data_rim.color = (0.9, 0.1, 0.8)
rim_obj = bpy.data.objects.new(name="Magenta_Rim", object_data=light_data_rim)
rim_obj.location = (30.0, -30.0, 10.0)
rim_obj.rotation_euler = (math.radians(-45), math.radians(30), math.radians(-120))
bpy.context.scene.collection.objects.link(rim_obj)

# Setup Camera for an elevated perspective overview
cam_data = bpy.data.cameras.new("Showcase_Camera")
cam_data.lens = 32
cam_obj = bpy.data.objects.new("Showcase_Camera", cam_data)
cam_obj.location = (12.0, -36.0, 22.0)
cam_obj.rotation_euler = (math.radians(58), 0, math.radians(0))
bpy.context.scene.collection.objects.link(cam_obj)
bpy.context.scene.camera = cam_obj

scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'


scene.render.resolution_x = 1920
scene.render.resolution_y = 1080
scene.render.resolution_percentage = 100
scene.render.filepath = OUTPUT_RENDER
scene.render.image_settings.file_format = 'PNG'

# Render
print(f"Rendering showcase to {OUTPUT_RENDER}...")
bpy.ops.render.render(write_still=True)
print("Render complete!")

# Also re-save blend file with camera, ground, and lights configured
bpy.ops.wm.save_as_mainfile(filepath=BLEND_FILE)
print("Updated blend file saved.")
