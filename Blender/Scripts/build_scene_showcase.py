"""
Master Showcase Scene Builder for Yellow System Pillar & Cyan Transformer Box.
Assembles both props side-by-side, sets up reference lighting & camera framing,
saves 'Electrical_Props_Showcase.blend', and renders a showcase image.
"""

import os
import sys
import math
import bpy
from mathutils import Vector, Euler

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import electrical_props_common as epc
import generate_yellow_system_pillar
import generate_cyan_transformer_box


def clear_scene():
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def build_showcase():
    print("Clearing existing scene...")
    clear_scene()

    mats = epc.get_materials()
    showcase_root = epc.create_root_empty("Industrial_Electrical_Showcase", location=(0, 0, 0))

    # 1. Place Props matching the reference image layout:
    # Left: Yellow Pillar
    # Right: Wide Cyan Transformer Box
    pillar_pos = (-1.25, 0.15, 0.0)
    trans_pos = (0.95, -0.10, 0.0)

    # Slight rotation to match 3/4 perspective in reference image
    generate_yellow_system_pillar.build_prop(location=pillar_pos, parent=showcase_root)
    generate_cyan_transformer_box.build_prop(location=trans_pos, parent=showcase_root)

    # 2. Dark Ground Plane
    ground = epc.create_cube(
        "Studio_Ground",
        size=(18.0, 18.0, 0.1),
        location=(0, 0, -0.05),
        material=mats['display_bezel'],
        parent=showcase_root
    )

    # 3. Studio Lighting Matching the Reference Image
    # Main Key Light: Warm bright sunlight from Front-Left high, casting sharp dark shadows to back-right
    key_light_data = bpy.data.lights.new(name="Key_Sun_Light_Data", type='SUN')
    key_light_data.energy = 5.5
    key_light_data.color = (1.0, 0.96, 0.90)
    key_light_obj = bpy.data.objects.new("Key_Sun_Light", key_light_data)
    key_light_obj.rotation_euler = (math.radians(52.0), math.radians(15.0), math.radians(-55.0))
    bpy.context.collection.objects.link(key_light_obj)

    # Fill Light: Soft cool ambient light from opposite side
    fill_light_data = bpy.data.lights.new(name="Fill_Light_Data", type='AREA')
    fill_light_data.energy = 600.0
    fill_light_data.color = (0.7, 0.85, 1.0)
    fill_light_data.size = 6.0
    fill_light_obj = bpy.data.objects.new("Fill_Light", fill_light_data)
    fill_light_obj.location = (4.0, -5.0, 3.5)
    fill_light_obj.rotation_euler = (math.radians(65.0), 0, math.radians(40.0))
    bpy.context.collection.objects.link(fill_light_obj)

    # Top Cyan Glow Accent Light (reflecting cyan brilliance on transformer top)
    top_light_data = bpy.data.lights.new(name="Top_Cyan_Light_Data", type='AREA')
    top_light_data.energy = 400.0
    top_light_data.color = (0.1, 0.9, 1.0)
    top_light_data.size = 3.0
    top_light_obj = bpy.data.objects.new("Top_Cyan_Light", top_light_data)
    top_light_obj.location = (1.0, -0.2, 3.5)
    top_light_obj.rotation_euler = (0, 0, 0)
    bpy.context.collection.objects.link(top_light_obj)

    # 4. Camera Setup Matching Reference Image View
    # Perspective camera framing both props completely with ground and roof margin
    cam_data = bpy.data.cameras.new("Reference_Camera_Data")
    cam_data.lens = 36.0
    cam_obj = bpy.data.objects.new("Reference_Camera", cam_data)
    cam_obj.location = (-0.15, -6.8, 1.35)
    cam_obj.rotation_euler = (math.radians(78.0), 0, math.radians(-2.0))
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # Render settings
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080

    print("Electrical Props Showcase built successfully!")


if __name__ == '__main__':
    build_showcase()

    blend_path = os.path.join(script_dir, "Electrical_Props_Showcase.blend")
    try:
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"Showcase scene saved to: {blend_path}")
    except Exception as e:
        print(f"Could not save .blend file: {e}")
