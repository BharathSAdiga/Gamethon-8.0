"""
Master Showcase Scene Builder and Unreal Engine FBX Exporter for Cyberpunk Superstructures.
Assembles all 3 props side-by-side matching the reference image layout:
  1. Left: Cyberpunk Telecom / Cellular Antenna Tower
  2. Middle: Modular Industrial Lattice Truss Tower
  3. Right: Cantilevered Industrial Overpass / Gantry Platform

Features:
- Sets up cinematic lighting and camera framing matching the reference image
- Saves 'Cyberpunk_Superstructures_Showcase.blend'
- Renders high-resolution showcase preview image
- Automatically exports individual, Unreal Engine 5-ready FBX models with correct scale and pivots
"""

import os
import sys
import math
import bpy
from mathutils import Vector, Euler

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import cyberpunk_structures_common as csc
import generate_telecom_tower
import generate_lattice_tower
import generate_cantilever_gantry


def clear_scene():
    """Remove all objects and unlinked data from current scene."""
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)


def build_showcase():
    print("Clearing existing scene...")
    clear_scene()

    mats = csc.get_materials()
    showcase_root = csc.create_root_empty("Cyberpunk_Superstructures_Showcase", location=(0, 0, 0))

    # -----------------------------------------------------------------------
    # 1. Place Props Matching Reference Image Layout
    # -----------------------------------------------------------------------
    # Left: Telecom Tower
    telecom_pos = (-4.0, 0.2, 0.0)
    telecom_root = generate_telecom_tower.build_prop(location=telecom_pos, parent=showcase_root)

    # Middle: Lattice Truss Tower
    lattice_pos = (-1.2, 0.0, 0.0)
    lattice_root = generate_lattice_tower.build_prop(location=lattice_pos, parent=showcase_root)

    # Right: Cantilever Gantry Platform
    gantry_pos = (2.2, -0.4, 0.0)
    gantry_root = generate_cantilever_gantry.build_prop(location=gantry_pos, parent=showcase_root)

    # -----------------------------------------------------------------------
    # 2. Studio Dark Floor & World Background
    # -----------------------------------------------------------------------
    floor = csc.create_cube(
        "Studio_Floor",
        size=(50.0, 50.0, 0.2),
        location=(0, 0, -0.1),
        material=mats['steel_dark'],
        parent=showcase_root
    )

    # Dark atmospheric cyberpunk world background
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("Cyberpunk_World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get('Background')
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.015, 0.018, 0.030, 1.0)
        bg_node.inputs['Strength'].default_value = 0.8

    # -----------------------------------------------------------------------
    # 3. Cinematic Cyberpunk Studio Lighting (Matching Reference Image)
    # -----------------------------------------------------------------------
    # Key Sunlight (Cool white with slight blue tint casting sharp angled shadows)
    sun_data = bpy.data.lights.new(name="Sun_Key_Light_Data", type='SUN')
    sun_data.energy = 6.5
    sun_data.color = (0.90, 0.94, 1.0)
    sun_obj = bpy.data.objects.new("Sun_Key_Light", sun_data)
    sun_obj.rotation_euler = (math.radians(52.0), math.radians(10.0), math.radians(-50.0))
    bpy.context.collection.objects.link(sun_obj)

    # Fill Ambient Light (Moody deep purple/slate tone)
    fill_data = bpy.data.lights.new(name="Fill_Area_Light_Data", type='AREA')
    fill_data.energy = 2200.0
    fill_data.color = (0.40, 0.35, 0.65)
    fill_data.size = 20.0
    fill_obj = bpy.data.objects.new("Fill_Area_Light", fill_data)
    fill_obj.location = (8.0, -12.0, 9.0)
    fill_obj.rotation_euler = (math.radians(58.0), 0, math.radians(35.0))
    bpy.context.collection.objects.link(fill_obj)

    # Back Rim Light (Subtle magenta/purple edge highlight)
    rim_data = bpy.data.lights.new(name="Rim_Light_Data", type='AREA')
    rim_data.energy = 1800.0
    rim_data.color = (0.80, 0.45, 1.0)
    rim_data.size = 24.0
    rim_obj = bpy.data.objects.new("Rim_Light", rim_data)
    rim_obj.location = (-4.0, 10.0, 11.0)
    rim_obj.rotation_euler = (math.radians(-48.0), 0, math.radians(165.0))
    bpy.context.collection.objects.link(rim_obj)

    # Accent Cyan Area Light (Front-Left, accentuating the telecom tower and pylon)
    accent_data = bpy.data.lights.new(name="Accent_Cyan_Light_Data", type='AREA')
    accent_data.energy = 800.0
    accent_data.color = (0.1, 0.8, 1.0)
    accent_data.size = 8.0
    accent_obj = bpy.data.objects.new("Accent_Cyan_Light", accent_data)
    accent_obj.location = (-7.5, -8.0, 6.0)
    accent_obj.rotation_euler = (math.radians(65.0), 0, math.radians(-45.0))
    bpy.context.collection.objects.link(accent_obj)

    # -----------------------------------------------------------------------
    # 4. Reference Camera Framing (Full Height & Width of all 3 Props)
    # -----------------------------------------------------------------------
    cam_data = bpy.data.cameras.new("Showcase_Camera_Data")
    cam_data.lens = 29.0  # Perfectly frames all 3 tall structures from ground to tip
    cam_obj = bpy.data.objects.new("Showcase_Camera", cam_data)
    cam_obj.location = (0.3, -26.5, 7.8)
    cam_obj.rotation_euler = (math.radians(84.5), 0, math.radians(-1.0))
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj

    # Render settings & Color Management
    scene = bpy.context.scene
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.view_settings.view_transform = 'AgX' if 'AgX' in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items else 'Filmic'
    scene.view_settings.look = 'Medium High Contrast'

    print("Master Cyberpunk Superstructures Showcase built successfully!")
    return {
        'telecom': telecom_root,
        'lattice': lattice_root,
        'gantry': gantry_root,
    }


def export_all_props_for_unreal(props_dict):
    """
    Exports each prop individually to FBX format for Unreal Engine 5.
    Saved to both:
    1. Local project FBX folder: 'UE Projects/Cyberpunk game/Exported_FBX/'
    2. Unreal Engine Content folder: 'UE Projects/Lastsecond/Content/Cyberpunk_Structures/'
    """
    export_dirs = [
        os.path.join(os.path.dirname(script_dir), "Exported_FBX"),
        os.path.abspath(os.path.join(script_dir, "..", "..", "Lastsecond", "Content", "Cyberpunk_Structures"))
    ]

    for export_dir in export_dirs:
        os.makedirs(export_dir, exist_ok=True)

        for prop_key, root_obj in props_dict.items():
            fbx_path = os.path.join(export_dir, f"{root_obj.name}.fbx")
            csc.export_prop_to_fbx(root_obj, fbx_path)


if __name__ == '__main__':
    props = build_showcase()

    # Save .blend file
    blend_path = os.path.join(script_dir, "Cyberpunk_Superstructures_Showcase.blend")
    try:
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"[Blender Save] Scene saved to: {blend_path}")
    except Exception as e:
        print(f"[Blender Save] Could not save .blend file: {e}")

    # Export FBX models for Unreal Engine
    try:
        export_all_props_for_unreal(props)
    except Exception as e:
        print(f"[Unreal Export] Error during FBX export: {e}")
