"""
SECTOR 09 — Level 1 Modular 3D Asset Kit Generator for Blender 4.x / 5.x
Generates all 56 production-ready, Unreal Engine 5 optimized cyberpunk assets
based on reference crops in Assets/Images/SECTOR09_Level1_Assets/.
"""

import os
import sys
import math
import bpy
import bmesh
from mathutils import Vector, Euler

# Base directories
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BLEND_OUTPUT_PATH = os.path.join(REPO_ROOT, "Blender", "Blend", "Sector09_Level1_Kit.blend")
FBX_OUTPUT_DIR = os.path.join(REPO_ROOT, "Blender", "FBX", "Sector09")
UE_CONTENT_DIR = os.path.join(REPO_ROOT, "UE Projects", "MyProject", "Content", "Sector09")

os.makedirs(os.path.dirname(BLEND_OUTPUT_PATH), exist_ok=True)
os.makedirs(FBX_OUTPUT_DIR, exist_ok=True)
os.makedirs(UE_CONTENT_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# Shader & Material System
# ---------------------------------------------------------------------------

def safe_set_bsdf(bsdf, socket_name, value):
    if socket_name in bsdf.inputs:
        bsdf.inputs[socket_name].default_value = value
    elif socket_name == 'Specular' and 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = value
    elif socket_name == 'Emission' and 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = value


def create_pbr_material(name, base_color, metallic=0.0, roughness=0.5, emission_color=None, emission_strength=0.0):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out = nodes.new('ShaderNodeOutputMaterial')
    out.location = (400, 0)
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (0, 0)
    links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])

    safe_set_bsdf(bsdf, 'Base Color', base_color)
    safe_set_bsdf(bsdf, 'Metallic', metallic)
    safe_set_bsdf(bsdf, 'Roughness', roughness)
    safe_set_bsdf(bsdf, 'Specular', 0.5)

    if emission_color:
        safe_set_bsdf(bsdf, 'Emission Color', emission_color)
        safe_set_bsdf(bsdf, 'Emission', emission_color)
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission_strength

    return mat


def get_material_library():
    return {
        'metal_dark': create_pbr_material('M_Cyberpunk_Metal_Dark', (0.04, 0.04, 0.05, 1.0), metallic=0.9, roughness=0.4),
        'metal_panel': create_pbr_material('M_Cyberpunk_Metal_Panel', (0.09, 0.12, 0.16, 1.0), metallic=0.75, roughness=0.35),
        'metal_bright': create_pbr_material('M_Cyberpunk_Metal_Bright', (0.35, 0.38, 0.42, 1.0), metallic=0.95, roughness=0.25),
        'metal_rust': create_pbr_material('M_Cyberpunk_Metal_Rust', (0.18, 0.08, 0.05, 1.0), metallic=0.4, roughness=0.85),
        'concrete': create_pbr_material('M_Cyberpunk_Concrete', (0.15, 0.16, 0.17, 1.0), metallic=0.05, roughness=0.9),
        'hazard_yellow': create_pbr_material('M_Cyberpunk_Hazard_Yellow', (0.95, 0.72, 0.05, 1.0), metallic=0.1, roughness=0.45),
        'hazard_black': create_pbr_material('M_Cyberpunk_Hazard_Black', (0.02, 0.02, 0.02, 1.0), metallic=0.2, roughness=0.55),
        'rubber': create_pbr_material('M_Cyberpunk_Rubber', (0.03, 0.03, 0.03, 1.0), metallic=0.0, roughness=0.8),
        'neon_cyan': create_pbr_material('M_Cyberpunk_Neon_Cyan', (0.0, 0.9, 1.0, 1.0), metallic=0.0, roughness=0.1,
                                         emission_color=(0.0, 0.9, 1.0, 1.0), emission_strength=12.0),
        'neon_purple': create_pbr_material('M_Cyberpunk_Neon_Purple', (0.85, 0.05, 0.95, 1.0), metallic=0.0, roughness=0.1,
                                           emission_color=(0.85, 0.05, 0.95, 1.0), emission_strength=12.0),
        'neon_red': create_pbr_material('M_Cyberpunk_Neon_Red', (1.0, 0.03, 0.03, 1.0), metallic=0.0, roughness=0.1,
                                        emission_color=(1.0, 0.03, 0.03, 1.0), emission_strength=15.0),
        'neon_amber': create_pbr_material('M_Cyberpunk_Neon_Amber', (1.0, 0.45, 0.02, 1.0), metallic=0.0, roughness=0.2,
                                          emission_color=(1.0, 0.45, 0.02, 1.0), emission_strength=8.0),
        'screen_glitch': create_pbr_material('M_Cyberpunk_Screen_Glitch', (0.05, 0.85, 0.6, 1.0), metallic=0.1, roughness=0.2,
                                             emission_color=(0.05, 0.85, 0.6, 1.0), emission_strength=10.0),
        'glass_tinted': create_pbr_material('M_Cyberpunk_Glass_Tinted', (0.05, 0.1, 0.15, 0.8), metallic=0.2, roughness=0.1)
    }

# ---------------------------------------------------------------------------
# Mesh Helpers
# ---------------------------------------------------------------------------

def create_cube(name, size=(1.0, 1.0, 1.0), location=(0, 0, 0), rotation=(0, 0, 0), material=None, parent=None):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = size
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def create_cylinder(name, radius=0.5, depth=1.0, vertices=16, location=(0, 0, 0), rotation=(0, 0, 0), material=None, parent=None):
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=depth, vertices=vertices, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def add_bevel(obj, width=0.015, segments=2):
    mod = obj.modifiers.new(name="Bevel", type='BEVEL')
    mod.width = width
    mod.segments = segments
    mod.limit_method = 'ANGLE'
    mod.angle_limit = math.radians(35.0)


def create_empty(name, location=(0, 0, 0)):
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.empty_display_size = 0.5
    empty.location = location
    bpy.context.scene.collection.objects.link(empty)
    return empty


def join_objects_to_single_mesh(root_empty, final_name):
    children = [child for child in root_empty.children if child.type == 'MESH']
    if not children:
        return None

    bpy.ops.object.select_all(action='DESELECT')
    for child in children:
        child.select_set(True)
    bpy.context.view_layer.objects.active = children[0]

    for child in children:
        bpy.context.view_layer.objects.active = child
        for mod in list(child.modifiers):
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception:
                pass

    bpy.ops.object.select_all(action='DESELECT')
    for child in children:
        child.select_set(True)
    bpy.context.view_layer.objects.active = children[0]
    bpy.ops.object.join()

    final_mesh = bpy.context.active_object
    final_mesh.name = final_name
    final_mesh.parent = None

    saved_cursor = bpy.context.scene.cursor.location.copy()
    bpy.context.scene.cursor.location = root_empty.location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    bpy.context.scene.cursor.location = saved_cursor

    bpy.data.objects.remove(root_empty, do_unlink=True)
    return final_mesh


def export_fbx(mesh_obj, export_paths):
    bpy.ops.object.select_all(action='DESELECT')
    mesh_obj.select_set(True)
    bpy.context.view_layer.objects.active = mesh_obj

    for path in export_paths:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        bpy.ops.export_scene.fbx(
            filepath=path,
            use_selection=True,
            global_scale=1.0,
            apply_unit_scale=True,
            apply_scale_options='FBX_SCALE_ALL',
            axis_forward='-Z',
            axis_up='Y',
            bake_space_transform=True,
            mesh_smooth_type='FACE',
            use_mesh_modifiers=True,
            add_leaf_bones=False
        )
    print(f"  -> Exported: {mesh_obj.name}.fbx")

# ---------------------------------------------------------------------------
# ASSET BUILDERS: GROUP 01 — WALLS, DOORS & GATES
# ---------------------------------------------------------------------------

def build_01_wall_panel_a(mats, pos):
    root = create_empty("SM_Wall_Panel_A_Root", pos)
    # Frame 200x20x300cm
    create_cube("Frame", (2.0, 0.2, 3.0), (pos[0], pos[1], pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    create_cube("Inner_Panel", (1.7, 0.16, 2.7), (pos[0], pos[1] - 0.01, pos[2] + 1.5), material=mats['metal_panel'], parent=root)
    # Louver slats
    for i in range(5):
        create_cube(f"Louver_{i}", (1.4, 0.04, 0.06), (pos[0], pos[1] - 0.09, pos[2] + 2.3 + i * 0.1), material=mats['metal_dark'], parent=root)
    # Bottom conduit & neon groove
    create_cylinder("Conduit", radius=0.03, depth=1.8, vertices=12, location=(pos[0], pos[1] - 0.11, pos[2] + 0.25), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    create_cube("Neon_Stripe", (1.6, 0.02, 0.03), (pos[0], pos[1] - 0.09, pos[2] + 1.8), material=mats['neon_cyan'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Wall_Panel_A")


def build_01_wall_panel_b_pipes(mats, pos):
    root = create_empty("SM_Wall_Panel_B_Pipes_Root", pos)
    create_cube("Frame", (2.0, 0.2, 3.0), (pos[0], pos[1], pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    create_cube("Inner_Panel", (1.7, 0.16, 2.7), (pos[0], pos[1] - 0.01, pos[2] + 1.5), material=mats['metal_panel'], parent=root)
    # Dual vertical industrial pipes
    create_cylinder("Pipe_Left", radius=0.06, depth=3.0, vertices=16, location=(pos[0] - 0.5, pos[1] - 0.15, pos[2] + 1.5), material=mats['metal_bright'], parent=root)
    create_cylinder("Pipe_Right", radius=0.04, depth=3.0, vertices=16, location=(pos[0] - 0.35, pos[1] - 0.15, pos[2] + 1.5), material=mats['metal_rust'], parent=root)
    # Pipe brackets & pressure gauge
    for z in [0.8, 1.8, 2.6]:
        create_cube(f"Bracket_{z}", (0.35, 0.08, 0.06), (pos[0] - 0.42, pos[1] - 0.13, pos[2] + z), material=mats['metal_dark'], parent=root)
    create_cylinder("Gauge", radius=0.1, depth=0.08, vertices=16, location=(pos[0] - 0.5, pos[1] - 0.22, pos[2] + 1.5), rotation=(math.pi/2, 0, 0), material=mats['hazard_yellow'], parent=root)
    # Hazard stripe panel
    create_cube("Hazard_Plate", (0.8, 0.02, 0.3), (pos[0] + 0.4, pos[1] - 0.09, pos[2] + 1.5), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Wall_Panel_B_Pipes")


def build_01_wall_panel_c_vent(mats, pos):
    root = create_empty("SM_Wall_Panel_C_Vent_Root", pos)
    create_cube("Frame", (2.0, 0.2, 3.0), (pos[0], pos[1], pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    create_cube("Inner_Panel", (1.7, 0.16, 2.7), (pos[0], pos[1] - 0.01, pos[2] + 1.5), material=mats['metal_panel'], parent=root)
    # Circular intake vent
    create_cylinder("Vent_Housing", radius=0.55, depth=0.12, vertices=24, location=(pos[0], pos[1] - 0.09, pos[2] + 2.0), rotation=(math.pi/2, 0, 0), material=mats['metal_dark'], parent=root)
    create_cylinder("Vent_Core", radius=0.48, depth=0.14, vertices=24, location=(pos[0], pos[1] - 0.09, pos[2] + 2.0), rotation=(math.pi/2, 0, 0), material=mats['metal_bright'], parent=root)
    create_cylinder("Vent_Fan_Hub", radius=0.14, depth=0.18, vertices=16, location=(pos[0], pos[1] - 0.09, pos[2] + 2.0), rotation=(math.pi/2, 0, 0), material=mats['hazard_yellow'], parent=root)
    # Lower service access door
    create_cube("Access_Hatch", (0.8, 0.04, 0.7), (pos[0], pos[1] - 0.1, pos[2] + 0.6), material=mats['metal_dark'], parent=root)
    create_cube("Hatch_Handle", (0.04, 0.06, 0.2), (pos[0] + 0.3, pos[1] - 0.14, pos[2] + 0.6), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Wall_Panel_C_Vent")


def build_01_corner_wall(mats, pos):
    root = create_empty("SM_Corner_Wall_Root", pos)
    # Corner 60x60x300cm
    create_cube("Corner_Col_X", (0.6, 0.2, 3.0), (pos[0] + 0.1, pos[1] - 0.1, pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    create_cube("Corner_Col_Y", (0.2, 0.6, 3.0), (pos[0] - 0.1, pos[1] + 0.1, pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    # Beveled bumper strip along outer edge
    create_cube("Corner_Buffer", (0.12, 0.12, 2.95), (pos[0] - 0.18, pos[1] - 0.18, pos[2] + 1.5), rotation=(0, 0, math.pi/4), material=mats['hazard_yellow'], parent=root)
    # Vertical cyan neon accent
    create_cube("Neon_Corner", (0.04, 0.04, 2.6), (pos[0] - 0.21, pos[1] - 0.21, pos[2] + 1.5), rotation=(0, 0, math.pi/4), material=mats['neon_cyan'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Corner_Wall")


def build_01_door_frame(mats, pos):
    root = create_empty("SM_Door_Frame_Root", pos)
    # Left & Right posts
    create_cube("Post_L", (0.3, 0.35, 3.2), (pos[0] - 1.0, pos[1], pos[2] + 1.6), material=mats['metal_dark'], parent=root)
    create_cube("Post_R", (0.3, 0.35, 3.2), (pos[0] + 1.0, pos[1], pos[2] + 1.6), material=mats['metal_dark'], parent=root)
    # Header lintel
    create_cube("Header", (2.3, 0.4, 0.4), (pos[0], pos[1], pos[2] + 3.0), material=mats['metal_dark'], parent=root)
    # Floor threshold
    create_cube("Threshold", (2.0, 0.4, 0.06), (pos[0], pos[1], pos[2] + 0.03), material=mats['metal_bright'], parent=root)
    # Hydraulic cylinder details
    create_cylinder("Hydraulic_L", radius=0.05, depth=0.6, vertices=12, location=(pos[0] - 0.75, pos[1] - 0.15, pos[2] + 2.7), rotation=(0, 0, math.pi/6), material=mats['metal_bright'], parent=root)
    create_cylinder("Hydraulic_R", radius=0.05, depth=0.6, vertices=12, location=(pos[0] + 0.75, pos[1] - 0.15, pos[2] + 2.7), rotation=(0, 0, -math.pi/6), material=mats['metal_bright'], parent=root)
    # Overhead status light
    create_cube("Status_Light", (0.6, 0.06, 0.08), (pos[0], pos[1] - 0.21, pos[2] + 2.95), material=mats['neon_cyan'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Door_Frame")


def build_01_industrial_door(mats, pos):
    root = create_empty("SM_Industrial_Door_Root", pos)
    # Door slab 180x15x280cm
    create_cube("Door_Slab", (1.8, 0.14, 2.8), (pos[0], pos[1], pos[2] + 1.4), material=mats['metal_panel'], parent=root)
    # Cross diagonal ribs
    create_cube("Rib_Diag1", (2.2, 0.06, 0.12), (pos[0], pos[1] - 0.08, pos[2] + 1.4), rotation=(0, math.atan2(2.8, 1.8), 0), material=mats['metal_dark'], parent=root)
    create_cube("Rib_Diag2", (2.2, 0.06, 0.12), (pos[0], pos[1] - 0.08, pos[2] + 1.4), rotation=(0, -math.atan2(2.8, 1.8), 0), material=mats['metal_dark'], parent=root)
    # Center viewing port / grille
    create_cube("Viewport_Frame", (0.5, 0.08, 0.4), (pos[0], pos[1] - 0.08, pos[2] + 1.8), material=mats['metal_dark'], parent=root)
    create_cube("Viewport_Glass", (0.42, 0.02, 0.32), (pos[0], pos[1] - 0.08, pos[2] + 1.8), material=mats['glass_tinted'], parent=root)
    # Bottom hazard stripes
    create_cube("Hazard_Strip", (1.6, 0.04, 0.25), (pos[0], pos[1] - 0.08, pos[2] + 0.2), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Industrial_Door")


def build_01_large_gate(mats, pos):
    root = create_empty("SM_Large_Gate_Root", pos)
    # Double-wide gate 360x35x340cm
    create_cube("Top_Rail", (3.6, 0.45, 0.4), (pos[0], pos[1], pos[2] + 3.2), material=mats['metal_dark'], parent=root)
    create_cube("Door_Left", (1.65, 0.2, 2.9), (pos[0] - 0.85, pos[1], pos[2] + 1.5), material=mats['metal_panel'], parent=root)
    create_cube("Door_Right", (1.65, 0.2, 2.9), (pos[0] + 0.85, pos[1], pos[2] + 1.5), material=mats['metal_panel'], parent=root)
    # Reinforcement vertical beams on each leaf
    for x in [-1.4, -0.9, -0.4, 0.4, 0.9, 1.4]:
        create_cube(f"Beam_{x}", (0.12, 0.08, 2.8), (pos[0] + x, pos[1] - 0.11, pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    # Center interlocking teeth & hazard chevron line
    create_cube("Center_Seam", (0.08, 0.24, 2.9), (pos[0], pos[1], pos[2] + 1.5), material=mats['metal_bright'], parent=root)
    create_cube("Hazard_Left", (1.4, 0.04, 0.3), (pos[0] - 0.85, pos[1] - 0.11, pos[2] + 0.4), material=mats['hazard_yellow'], parent=root)
    create_cube("Hazard_Right", (1.4, 0.04, 0.3), (pos[0] + 0.85, pos[1] - 0.11, pos[2] + 0.4), material=mats['hazard_yellow'], parent=root)
    create_cylinder("Beacon_L", radius=0.08, depth=0.16, vertices=12, location=(pos[0] - 1.5, pos[1] - 0.2, pos[2] + 3.3), material=mats['neon_red'], parent=root)
    create_cylinder("Beacon_R", radius=0.08, depth=0.16, vertices=12, location=(pos[0] + 1.5, pos[1] - 0.2, pos[2] + 3.3), material=mats['neon_red'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Large_Gate")


def build_01_window_panel(mats, pos):
    root = create_empty("SM_Window_Panel_Root", pos)
    create_cube("Outer_Wall", (2.0, 0.2, 3.0), (pos[0], pos[1], pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    # Reinforced observation window frame
    create_cube("Win_Frame", (1.4, 0.26, 1.5), (pos[0], pos[1], pos[2] + 1.6), material=mats['metal_panel'], parent=root)
    create_cube("Glass_Pane", (1.2, 0.06, 1.3), (pos[0], pos[1], pos[2] + 1.6), material=mats['glass_tinted'], parent=root)
    # Diagonal security brace
    create_cube("Brace_1", (1.8, 0.04, 0.08), (pos[0], pos[1] - 0.14, pos[2] + 1.6), rotation=(0, math.atan2(1.3, 1.2), 0), material=mats['metal_dark'], parent=root)
    create_cube("Sill_Ledge", (1.5, 0.3, 0.08), (pos[0], pos[1] - 0.05, pos[2] + 0.8), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Window_Panel")

# ---------------------------------------------------------------------------
# ASSET BUILDERS: GROUP 02 — FLOORS, STAIRS & RAILINGS
# ---------------------------------------------------------------------------

def build_02_floor_tile_a(mats, pos):
    root = create_empty("SM_Floor_Tile_A_Root", pos)
    create_cube("Slab", (2.0, 2.0, 0.15), (pos[0], pos[1], pos[2] + 0.075), material=mats['metal_panel'], parent=root)
    # Perimeter rim
    create_cube("Rim_X1", (2.0, 0.1, 0.16), (pos[0], pos[1] + 0.95, pos[2] + 0.08), material=mats['metal_dark'], parent=root)
    create_cube("Rim_X2", (2.0, 0.1, 0.16), (pos[0], pos[1] - 0.95, pos[2] + 0.08), material=mats['metal_dark'], parent=root)
    create_cube("Rim_Y1", (0.1, 1.8, 0.16), (pos[0] + 0.95, pos[1], pos[2] + 0.08), material=mats['metal_dark'], parent=root)
    create_cube("Rim_Y2", (0.1, 1.8, 0.16), (pos[0] - 0.95, pos[1], pos[2] + 0.08), material=mats['metal_dark'], parent=root)
    # 4 Corner bolt wells
    for cx in [-0.85, 0.85]:
        for cy in [-0.85, 0.85]:
            create_cylinder(f"Bolt_{cx}_{cy}", radius=0.04, depth=0.06, vertices=8, location=(pos[0] + cx, pos[1] + cy, pos[2] + 0.14), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Floor_Tile_A")


def build_02_floor_tile_b_grate(mats, pos):
    root = create_empty("SM_Floor_Tile_B_Grate_Root", pos)
    create_cube("Outer_Rim", (2.0, 2.0, 0.15), (pos[0], pos[1], pos[2] + 0.075), material=mats['metal_dark'], parent=root)
    # Recessed drain sump
    create_cube("Sump_Pit", (1.5, 1.5, 0.14), (pos[0], pos[1], pos[2] + 0.03), material=mats['metal_rust'], parent=root)
    # Grate bars
    for i in range(-6, 7):
        create_cube(f"Bar_{i}", (1.45, 0.04, 0.06), (pos[0], pos[1] + i * 0.1, pos[2] + 0.12), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Floor_Tile_B_Grate")


def build_02_floor_tile_c(mats, pos):
    root = create_empty("SM_Floor_Tile_C_Root", pos)
    create_cube("Slab", (2.0, 2.0, 0.15), (pos[0], pos[1], pos[2] + 0.075), material=mats['metal_panel'], parent=root)
    # Yellow hazard perimeter
    create_cube("Hazard_Border", (1.8, 1.8, 0.155), (pos[0], pos[1], pos[2] + 0.078), material=mats['hazard_yellow'], parent=root)
    create_cube("Inner_Floor", (1.5, 1.5, 0.16), (pos[0], pos[1], pos[2] + 0.08), material=mats['metal_dark'], parent=root)
    # Access hatch in center
    create_cube("Hatch", (0.8, 0.8, 0.04), (pos[0], pos[1], pos[2] + 0.17), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Floor_Tile_C")


def build_02_floor_tile_d_corner(mats, pos):
    root = create_empty("SM_Floor_Tile_D_Corner_Root", pos)
    create_cube("Slab", (2.0, 2.0, 0.15), (pos[0], pos[1], pos[2] + 0.075), material=mats['metal_panel'], parent=root)
    # Diagonal corner chamfer feature
    create_cube("Chamfer_Pad", (0.8, 0.8, 0.16), (pos[0] + 0.7, pos[1] + 0.7, pos[2] + 0.08), rotation=(0, 0, math.pi/4), material=mats['hazard_yellow'], parent=root)
    create_cube("Conduit_Trough", (1.2, 0.12, 0.06), (pos[0] - 0.2, pos[1] + 0.8, pos[2] + 0.13), material=mats['metal_dark'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Floor_Tile_D_Corner")


def build_02_floor_tile_e_ramp(mats, pos):
    root = create_empty("SM_Floor_Tile_E_Ramp_Root", pos)
    # 200x200cm ramp rising from 0 to 40cm
    rot_angle = math.atan2(0.4, 2.0)
    ramp_len = math.sqrt(2.0**2 + 0.4**2)
    create_cube("Ramp_Deck", (2.0, ramp_len, 0.08), (pos[0], pos[1], pos[2] + 0.2), rotation=(-rot_angle, 0, 0), material=mats['metal_panel'], parent=root)
    # Anti-slip ribs
    for step in range(6):
        y_loc = (step - 2.5) * 0.3
        z_loc = 0.2 - y_loc * math.tan(rot_angle) + 0.045
        create_cube(f"Grip_Rib_{step}", (1.8, 0.04, 0.02), (pos[0], pos[1] + y_loc, pos[2] + z_loc), rotation=(-rot_angle, 0, 0), material=mats['metal_dark'], parent=root)
    # Yellow warning lip at bottom edge
    create_cube("Warning_Lip", (2.0, 0.08, 0.04), (pos[0], pos[1] - 0.96, pos[2] + 0.02), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Floor_Tile_E_Ramp")


def build_02_stair_module(mats, pos):
    root = create_empty("SM_Stair_Module_Root", pos)
    # 4 Steps: 200cm wide, 200cm total run, 120cm rise (30cm rise x 50cm run per step)
    for i in range(4):
        step_z = (i + 1) * 0.3
        step_y = (i - 1.5) * 0.5
        # Tread slab
        create_cube(f"Tread_{i}", (2.0, 0.52, 0.08), (pos[0], pos[1] + step_y, pos[2] + step_z - 0.04), material=mats['metal_panel'], parent=root)
        # Riser plate
        create_cube(f"Riser_{i}", (1.96, 0.04, 0.3), (pos[0], pos[1] + step_y - 0.24, pos[2] + step_z - 0.15), material=mats['metal_dark'], parent=root)
        # Hazard tread nose
        create_cube(f"Tread_Nose_{i}", (1.98, 0.04, 0.03), (pos[0], pos[1] + step_y - 0.25, pos[2] + step_z), material=mats['hazard_yellow'], parent=root)
    # Side stringers
    create_cube("Stringer_L", (0.08, 2.2, 0.3), (pos[0] - 0.98, pos[1], pos[2] + 0.6), rotation=(math.atan2(1.2, 2.0), 0, 0), material=mats['metal_dark'], parent=root)
    create_cube("Stringer_R", (0.08, 2.2, 0.3), (pos[0] + 0.98, pos[1], pos[2] + 0.6), rotation=(math.atan2(1.2, 2.0), 0, 0), material=mats['metal_dark'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Stair_Module")


def build_02_platform_module(mats, pos):
    root = create_empty("SM_Platform_Module_Root", pos)
    create_cube("Deck", (2.0, 2.0, 0.12), (pos[0], pos[1], pos[2] + 0.34), material=mats['metal_panel'], parent=root)
    # Underslung I-beams
    create_cube("I_Beam_1", (0.15, 2.0, 0.28), (pos[0] - 0.7, pos[1], pos[2] + 0.14), material=mats['metal_dark'], parent=root)
    create_cube("I_Beam_2", (0.15, 2.0, 0.28), (pos[0] + 0.7, pos[1], pos[2] + 0.14), material=mats['metal_dark'], parent=root)
    # Cross tie plate
    create_cube("Cross_Tie", (1.6, 0.15, 0.08), (pos[0], pos[1], pos[2] + 0.04), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Platform_Module")


def build_02_railing_straight(mats, pos):
    root = create_empty("SM_Railing_Straight_Root", pos)
    # Top handrail 200cm, height 110cm
    create_cylinder("Handrail_Top", radius=0.03, depth=2.0, vertices=12, location=(pos[0], pos[1], pos[2] + 1.1), rotation=(0, math.pi/2, 0), material=mats['hazard_yellow'], parent=root)
    create_cylinder("Mid_Rail", radius=0.02, depth=2.0, vertices=12, location=(pos[0], pos[1], pos[2] + 0.6), rotation=(0, math.pi/2, 0), material=mats['metal_dark'], parent=root)
    # Kickplate
    create_cube("Kickplate", (2.0, 0.02, 0.15), (pos[0], pos[1], pos[2] + 0.075), material=mats['metal_dark'], parent=root)
    # 3 Stanchion posts
    for x in [-0.95, 0.0, 0.95]:
        create_cylinder(f"Post_{x}", radius=0.03, depth=1.1, vertices=12, location=(pos[0] + x, pos[1], pos[2] + 0.55), material=mats['metal_bright'], parent=root)
        create_cube(f"Base_Plate_{x}", (0.12, 0.12, 0.02), (pos[0] + x, pos[1], pos[2] + 0.01), material=mats['metal_dark'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Railing_Straight")


def build_02_railing_corner(mats, pos):
    root = create_empty("SM_Railing_Corner_Root", pos)
    # Corner post at (0, 0)
    create_cylinder("Corner_Post", radius=0.04, depth=1.1, vertices=12, location=(pos[0], pos[1], pos[2] + 0.55), material=mats['metal_bright'], parent=root)
    # Arm X
    create_cylinder("Rail_X_Top", radius=0.03, depth=1.0, vertices=12, location=(pos[0] + 0.5, pos[1], pos[2] + 1.1), rotation=(0, math.pi/2, 0), material=mats['hazard_yellow'], parent=root)
    create_cylinder("Rail_X_Mid", radius=0.02, depth=1.0, vertices=12, location=(pos[0] + 0.5, pos[1], pos[2] + 0.6), rotation=(0, math.pi/2, 0), material=mats['metal_dark'], parent=root)
    create_cube("Kick_X", (1.0, 0.02, 0.15), (pos[0] + 0.5, pos[1], pos[2] + 0.075), material=mats['metal_dark'], parent=root)
    create_cylinder("Post_X_End", radius=0.03, depth=1.1, vertices=12, location=(pos[0] + 1.0, pos[1], pos[2] + 0.55), material=mats['metal_bright'], parent=root)
    # Arm Y
    create_cylinder("Rail_Y_Top", radius=0.03, depth=1.0, vertices=12, location=(pos[0], pos[1] + 0.5, pos[2] + 1.1), rotation=(math.pi/2, 0, 0), material=mats['hazard_yellow'], parent=root)
    create_cylinder("Rail_Y_Mid", radius=0.02, depth=1.0, vertices=12, location=(pos[0], pos[1] + 0.5, pos[2] + 0.6), rotation=(math.pi/2, 0, 0), material=mats['metal_dark'], parent=root)
    create_cube("Kick_Y", (0.02, 1.0, 0.15), (pos[0], pos[1] + 0.5, pos[2] + 0.075), material=mats['metal_dark'], parent=root)
    create_cylinder("Post_Y_End", radius=0.03, depth=1.1, vertices=12, location=(pos[0], pos[1] + 1.0, pos[2] + 0.55), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Railing_Corner")

# ---------------------------------------------------------------------------
# ASSET BUILDERS: GROUP 03 — HEAVY STRUCTURE, BEAMS & PIPES
# ---------------------------------------------------------------------------

def build_03_lift_platform(mats, pos):
    root = create_empty("SM_Lift_Platform_Root", pos)
    create_cube("Deck", (2.2, 2.2, 0.2), (pos[0], pos[1], pos[2] + 0.1), material=mats['metal_panel'], parent=root)
    create_cube("Hazard_Rim", (2.25, 2.25, 0.18), (pos[0], pos[1], pos[2] + 0.1), material=mats['hazard_yellow'], parent=root)
    for cx in [-0.95, 0.95]:
        for cy in [-0.95, 0.95]:
            create_cube(f"Lug_{cx}_{cy}", (0.16, 0.16, 0.25), (pos[0] + cx, pos[1] + cy, pos[2] + 0.25), material=mats['metal_dark'], parent=root)
            create_cylinder(f"Eyelet_{cx}_{cy}", radius=0.04, depth=0.18, vertices=8, location=(pos[0] + cx, pos[1] + cy, pos[2] + 0.32), rotation=(math.pi/2, 0, 0), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Lift_Platform")


def build_03_elevator_shaft_module(mats, pos):
    root = create_empty("SM_Elevator_Shaft_Module_Root", pos)
    # 4 Corner column rails 240x240x300cm
    for cx in [-1.1, 1.1]:
        for cy in [-1.1, 1.1]:
            create_cube(f"Column_{cx}_{cy}", (0.18, 0.18, 3.0), (pos[0] + cx, pos[1] + cy, pos[2] + 1.5), material=mats['metal_dark'], parent=root)
    # Horizontal bracing rings
    for z in [0.2, 1.5, 2.9]:
        create_cube(f"Ring_X1_{z}", (2.2, 0.08, 0.08), (pos[0], pos[1] + 1.1, pos[2] + z), material=mats['metal_bright'], parent=root)
        create_cube(f"Ring_X2_{z}", (2.2, 0.08, 0.08), (pos[0], pos[1] - 1.1, pos[2] + z), material=mats['metal_bright'], parent=root)
        create_cube(f"Ring_Y1_{z}", (0.08, 2.2, 0.08), (pos[0] + 1.1, pos[1], pos[2] + z), material=mats['metal_bright'], parent=root)
        create_cube(f"Ring_Y2_{z}", (0.08, 2.2, 0.08), (pos[0] - 1.1, pos[1], pos[2] + z), material=mats['metal_bright'], parent=root)
    # Center guide rails
    create_cube("Guide_Rail_L", (0.06, 0.12, 3.0), (pos[0] - 1.1, pos[1], pos[2] + 1.5), material=mats['hazard_yellow'], parent=root)
    create_cube("Guide_Rail_R", (0.06, 0.12, 3.0), (pos[0] + 1.1, pos[1], pos[2] + 1.5), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Elevator_Shaft_Module")


def build_03_large_vertical_panel(mats, pos):
    root = create_empty("SM_Large_Vertical_Panel_Root", pos)
    create_cube("Pillar", (0.8, 0.4, 4.0), (pos[0], pos[1], pos[2] + 2.0), material=mats['metal_dark'], parent=root)
    create_cube("Center_Recess", (0.5, 0.38, 3.8), (pos[0], pos[1] - 0.02, pos[2] + 2.0), material=mats['metal_panel'], parent=root)
    create_cylinder("Cable_Bundle", radius=0.08, depth=3.8, vertices=12, location=(pos[0], pos[1] - 0.18, pos[2] + 2.0), material=mats['rubber'], parent=root)
    create_cube("Emissive_Stripe", (0.04, 0.02, 3.2), (pos[0] - 0.3, pos[1] - 0.21, pos[2] + 2.0), material=mats['neon_purple'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Large_Vertical_Panel")


def build_03_horizontal_beam(mats, pos):
    root = create_empty("SM_Horizontal_Beam_Root", pos)
    # I-Beam 400x30x40cm
    create_cube("Web", (4.0, 0.06, 0.36), (pos[0], pos[1], pos[2] + 0.2), material=mats['metal_dark'], parent=root)
    create_cube("Flange_Top", (4.0, 0.3, 0.05), (pos[0], pos[1], pos[2] + 0.38), material=mats['metal_dark'], parent=root)
    create_cube("Flange_Bot", (4.0, 0.3, 0.05), (pos[0], pos[1], pos[2] + 0.02), material=mats['metal_dark'], parent=root)
    for x in [-1.98, 1.98]:
        create_cube(f"End_Plate_{x}", (0.05, 0.36, 0.46), (pos[0] + x, pos[1], pos[2] + 0.2), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Horizontal_Beam")


def build_03_pipe_straight(mats, pos):
    root = create_empty("SM_Pipe_Straight_Root", pos)
    create_cylinder("Main_Pipe", radius=0.12, depth=2.0, vertices=16, location=(pos[0], pos[1], pos[2] + 0.15), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    for x in [-0.98, 0.98]:
        create_cylinder(f"Flange_{x}", radius=0.16, depth=0.06, vertices=16, location=(pos[0] + x, pos[1], pos[2] + 0.15), rotation=(0, math.pi/2, 0), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Pipe_Straight")


def build_03_pipe_elbow(mats, pos):
    root = create_empty("SM_Pipe_Elbow_Root", pos)
    create_cylinder("Pipe_Arm_X", radius=0.12, depth=0.45, vertices=16, location=(pos[0] + 0.22, pos[1], pos[2] + 0.15), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    create_cylinder("Pipe_Arm_Y", radius=0.12, depth=0.45, vertices=16, location=(pos[0], pos[1] + 0.22, pos[2] + 0.15), rotation=(math.pi/2, 0, 0), material=mats['metal_bright'], parent=root)
    create_cube("Corner_Joint", (0.26, 0.26, 0.26), (pos[0], pos[1], pos[2] + 0.15), material=mats['metal_dark'], parent=root)
    create_cylinder("Flange_X", radius=0.16, depth=0.06, vertices=16, location=(pos[0] + 0.45, pos[1], pos[2] + 0.15), rotation=(0, math.pi/2, 0), material=mats['hazard_yellow'], parent=root)
    create_cylinder("Flange_Y", radius=0.16, depth=0.06, vertices=16, location=(pos[0], pos[1] + 0.45, pos[2] + 0.15), rotation=(math.pi/2, 0, 0), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Pipe_Elbow")


def build_03_pipe_junction_t(mats, pos):
    root = create_empty("SM_Pipe_Junction_T_Root", pos)
    create_cylinder("Main_Run", radius=0.12, depth=0.8, vertices=16, location=(pos[0], pos[1], pos[2] + 0.15), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    create_cylinder("Branch_Run", radius=0.12, depth=0.45, vertices=16, location=(pos[0], pos[1] + 0.22, pos[2] + 0.15), rotation=(math.pi/2, 0, 0), material=mats['metal_bright'], parent=root)
    create_cube("T_Box", (0.28, 0.28, 0.28), (pos[0], pos[1], pos[2] + 0.15), material=mats['metal_dark'], parent=root)
    # Valve wheel on branch
    create_cylinder("Valve_Shaft", radius=0.02, depth=0.15, vertices=8, location=(pos[0], pos[1] + 0.48, pos[2] + 0.15), rotation=(math.pi/2, 0, 0), material=mats['metal_dark'], parent=root)
    create_cylinder("Valve_Wheel", radius=0.14, depth=0.03, vertices=16, location=(pos[0], pos[1] + 0.55, pos[2] + 0.15), rotation=(math.pi/2, 0, 0), material=mats['neon_red'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Pipe_Junction_T")


def build_03_pipe_set_wall(mats, pos):
    root = create_empty("SM_Pipe_Set_Wall_Root", pos)
    create_cube("Strut_L", (0.06, 0.25, 0.6), (pos[0] - 0.7, pos[1], pos[2] + 0.3), material=mats['metal_dark'], parent=root)
    create_cube("Strut_R", (0.06, 0.25, 0.6), (pos[0] + 0.7, pos[1], pos[2] + 0.3), material=mats['metal_dark'], parent=root)
    # 3 Pipes (Large, Medium, Small)
    create_cylinder("Pipe_Large", radius=0.09, depth=2.0, vertices=16, location=(pos[0], pos[1] - 0.1, pos[2] + 0.48), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    create_cylinder("Pipe_Med", radius=0.06, depth=2.0, vertices=16, location=(pos[0], pos[1] - 0.1, pos[2] + 0.3), rotation=(0, math.pi/2, 0), material=mats['hazard_yellow'], parent=root)
    create_cylinder("Pipe_Small", radius=0.04, depth=2.0, vertices=16, location=(pos[0], pos[1] - 0.1, pos[2] + 0.15), rotation=(0, math.pi/2, 0), material=mats['metal_rust'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Pipe_Set_Wall")


def build_03_cable_tray(mats, pos):
    root = create_empty("SM_Cable_Tray_Root", pos)
    create_cube("Tray_Base", (2.0, 0.4, 0.04), (pos[0], pos[1], pos[2] + 0.02), material=mats['metal_dark'], parent=root)
    create_cube("Tray_Lip_Y1", (2.0, 0.03, 0.12), (pos[0], pos[1] + 0.18, pos[2] + 0.07), material=mats['metal_dark'], parent=root)
    create_cube("Tray_Lip_Y2", (2.0, 0.03, 0.12), (pos[0], pos[1] - 0.18, pos[2] + 0.07), material=mats['metal_dark'], parent=root)
    # 4 Bundled cables inside
    for i, y_off in enumerate([-0.12, -0.04, 0.04, 0.12]):
        mat = mats['rubber'] if i % 2 == 0 else mats['hazard_yellow']
        create_cylinder(f"Cable_{i}", radius=0.025, depth=2.0, vertices=8, location=(pos[0], pos[1] + y_off, pos[2] + 0.06), rotation=(0, math.pi/2, 0), material=mat, parent=root)
    return join_objects_to_single_mesh(root, "SM_Cable_Tray")

# ---------------------------------------------------------------------------
# ASSET BUILDERS: GROUP 04 — INDUSTRIAL CONTAINERS & BARRIERS
# ---------------------------------------------------------------------------

def build_04_crate_large(mats, pos):
    root = create_empty("SM_Crate_Large_Root", pos)
    # 200x120x120cm
    create_cube("Body", (2.0, 1.2, 1.2), (pos[0], pos[1], pos[2] + 0.6), material=mats['metal_panel'], parent=root)
    # 8 Corner protective castings
    for cx in [-0.98, 0.98]:
        for cy in [-0.58, 0.58]:
            for cz in [0.08, 1.12]:
                create_cube(f"Corner_{cx}_{cy}_{cz}", (0.12, 0.12, 0.14), (pos[0] + cx, pos[1] + cy, pos[2] + cz), material=mats['metal_dark'], parent=root)
    # Corrugation ribs
    for x in [-0.6, -0.2, 0.2, 0.6]:
        create_cube(f"Rib_F_{x}", (0.08, 0.04, 1.0), (pos[0] + x, pos[1] - 0.61, pos[2] + 0.6), material=mats['metal_dark'], parent=root)
        create_cube(f"Rib_B_{x}", (0.08, 0.04, 1.0), (pos[0] + x, pos[1] + 0.61, pos[2] + 0.6), material=mats['metal_dark'], parent=root)
    # Electronic RFID lock & hazard tag
    create_cube("Lock_Panel", (0.16, 0.04, 0.12), (pos[0], pos[1] - 0.62, pos[2] + 0.7), material=mats['neon_cyan'], parent=root)
    create_cube("Hazard_Tag", (0.3, 0.02, 0.25), (pos[0] + 0.6, pos[1] - 0.61, pos[2] + 0.7), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Crate_Large")


def build_04_crate_medium(mats, pos):
    root = create_empty("SM_Crate_Medium_Root", pos)
    create_cube("Body", (1.0, 1.0, 1.0), (pos[0], pos[1], pos[2] + 0.5), material=mats['metal_panel'], parent=root)
    # Recessed frame
    create_cube("Inner_Well", (0.84, 0.84, 0.96), (pos[0], pos[1], pos[2] + 0.5), material=mats['metal_dark'], parent=root)
    create_cube("Top_Cap", (1.04, 1.04, 0.08), (pos[0], pos[1], pos[2] + 0.98), material=mats['metal_dark'], parent=root)
    create_cube("Handle_L", (0.04, 0.18, 0.06), (pos[0] - 0.52, pos[1], pos[2] + 0.55), material=mats['metal_bright'], parent=root)
    create_cube("Handle_R", (0.04, 0.18, 0.06), (pos[0] + 0.52, pos[1], pos[2] + 0.55), material=mats['metal_bright'], parent=root)
    create_cube("Hazard_Symbol", (0.22, 0.02, 0.22), (pos[0], pos[1] - 0.51, pos[2] + 0.55), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Crate_Medium")


def build_04_crate_small(mats, pos):
    root = create_empty("SM_Crate_Small_Root", pos)
    create_cube("Case", (0.6, 0.4, 0.4), (pos[0], pos[1], pos[2] + 0.2), material=mats['metal_dark'], parent=root)
    create_cube("Lid", (0.62, 0.42, 0.06), (pos[0], pos[1], pos[2] + 0.38), material=mats['metal_panel'], parent=root)
    create_cube("Latch_L", (0.04, 0.03, 0.08), (pos[0] - 0.18, pos[1] - 0.21, pos[2] + 0.35), material=mats['metal_bright'], parent=root)
    create_cube("Latch_R", (0.04, 0.03, 0.08), (pos[0] + 0.18, pos[1] - 0.21, pos[2] + 0.35), material=mats['metal_bright'], parent=root)
    create_cube("Grip_Handle", (0.18, 0.04, 0.03), (pos[0], pos[1] - 0.23, pos[2] + 0.24), material=mats['rubber'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Crate_Small")


def build_04_stacked_crates(mats, pos):
    root = create_empty("SM_Stacked_Crates_Root", pos)
    # Crate 1 bottom left
    create_cube("Crate_1", (1.0, 1.0, 0.8), (pos[0] - 0.45, pos[1], pos[2] + 0.4), material=mats['metal_panel'], parent=root)
    # Crate 2 bottom right
    create_cube("Crate_2", (0.8, 0.8, 0.8), (pos[0] + 0.5, pos[1] + 0.05, pos[2] + 0.4), material=mats['metal_dark'], parent=root)
    # Crate 3 atop angled
    create_cube("Crate_3", (0.8, 0.8, 0.7), (pos[0] - 0.1, pos[1] - 0.05, pos[2] + 1.15), rotation=(0, 0, math.radians(18.0)), material=mats['hazard_yellow'], parent=root)
    # Securing strap
    create_cube("Strap", (0.04, 1.1, 1.55), (pos[0] - 0.1, pos[1], pos[2] + 0.78), material=mats['rubber'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Stacked_Crates")


def build_04_barrel(mats, pos):
    root = create_empty("SM_Barrel_Root", pos)
    create_cylinder("Drum", radius=0.32, depth=0.95, vertices=20, location=(pos[0], pos[1], pos[2] + 0.475), material=mats['metal_panel'], parent=root)
    # Two rolling hoop ribs
    create_cylinder("Hoop_1", radius=0.34, depth=0.04, vertices=20, location=(pos[0], pos[1], pos[2] + 0.32), material=mats['metal_dark'], parent=root)
    create_cylinder("Hoop_2", radius=0.34, depth=0.04, vertices=20, location=(pos[0], pos[1], pos[2] + 0.64), material=mats['metal_dark'], parent=root)
    # Chime top & bottom rim
    create_cylinder("Chime_Top", radius=0.33, depth=0.04, vertices=20, location=(pos[0], pos[1], pos[2] + 0.94), material=mats['metal_dark'], parent=root)
    create_cylinder("Chime_Bot", radius=0.33, depth=0.04, vertices=20, location=(pos[0], pos[1], pos[2] + 0.02), material=mats['metal_dark'], parent=root)
    create_cylinder("Bung_Cap", radius=0.04, depth=0.04, vertices=12, location=(pos[0] + 0.16, pos[1], pos[2] + 0.96), material=mats['metal_bright'], parent=root)
    create_cube("Hazmat_Sticker", (0.16, 0.02, 0.16), (pos[0], pos[1] - 0.33, pos[2] + 0.48), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Barrel")


def build_04_barrier_low(mats, pos):
    root = create_empty("SM_Barrier_Low_Root", pos)
    # Concrete Jersey barrier 200x50x80cm
    create_cube("Base_Flange", (2.0, 0.5, 0.2), (pos[0], pos[1], pos[2] + 0.1), material=mats['concrete'], parent=root)
    create_cube("Stem", (2.0, 0.25, 0.6), (pos[0], pos[1], pos[2] + 0.5), material=mats['concrete'], parent=root)
    # Yellow hazard reflector strips
    create_cube("Reflector_1", (0.25, 0.02, 0.1), (pos[0] - 0.6, pos[1] - 0.14, pos[2] + 0.6), material=mats['hazard_yellow'], parent=root)
    create_cube("Reflector_2", (0.25, 0.02, 0.1), (pos[0] + 0.6, pos[1] - 0.14, pos[2] + 0.6), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Barrier_Low")


def build_04_barrier_tall(mats, pos):
    root = create_empty("SM_Barrier_Tall_Root", pos)
    create_cube("Blast_Shield", (2.0, 0.16, 2.0), (pos[0], pos[1], pos[2] + 1.0), material=mats['metal_dark'], parent=root)
    # Concrete footer
    create_cube("Footer", (2.0, 0.45, 0.3), (pos[0], pos[1], pos[2] + 0.15), material=mats['concrete'], parent=root)
    # Viewport slit
    create_cube("Slit_Glass", (0.8, 0.04, 0.12), (pos[0], pos[1], pos[2] + 1.5), material=mats['glass_tinted'], parent=root)
    # Rear buttress supports
    create_cube("Buttress_L", (0.08, 0.4, 1.2), (pos[0] - 0.7, pos[1] + 0.2, pos[2] + 0.7), rotation=(-math.radians(20.0), 0, 0), material=mats['metal_dark'], parent=root)
    create_cube("Buttress_R", (0.08, 0.4, 1.2), (pos[0] + 0.7, pos[1] + 0.2, pos[2] + 0.7), rotation=(-math.radians(20.0), 0, 0), material=mats['metal_dark'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Barrier_Tall")


def build_04_construction_barrier(mats, pos):
    root = create_empty("SM_Construction_Barrier_Root", pos)
    create_cube("Cross_Board", (1.5, 0.04, 0.25), (pos[0], pos[1], pos[2] + 0.75), material=mats['hazard_yellow'], parent=root)
    create_cube("Bottom_Board", (1.5, 0.04, 0.2), (pos[0], pos[1], pos[2] + 0.35), material=mats['hazard_black'], parent=root)
    # A-Frame legs
    for x in [-0.65, 0.65]:
        create_cube(f"Leg_F_{x}", (0.06, 0.06, 1.0), (pos[0] + x, pos[1] - 0.15, pos[2] + 0.5), rotation=(math.radians(12.0), 0, 0), material=mats['metal_dark'], parent=root)
        create_cube(f"Leg_B_{x}", (0.06, 0.06, 1.0), (pos[0] + x, pos[1] + 0.15, pos[2] + 0.5), rotation=(-math.radians(12.0), 0, 0), material=mats['metal_dark'], parent=root)
    create_cylinder("Strobe_Light", radius=0.06, depth=0.12, vertices=12, location=(pos[0], pos[1], pos[2] + 0.95), material=mats['neon_amber'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Construction_Barrier")


def build_04_pallet(mats, pos):
    root = create_empty("SM_Pallet_Root", pos)
    # 120x100x16cm
    for i in range(5):
        create_cube(f"Top_Plank_{i}", (1.2, 0.14, 0.03), (pos[0], pos[1] + (i - 2) * 0.22, pos[2] + 0.145), material=mats['metal_dark'], parent=root)
    # 3 Stringers
    for y in [-0.42, 0.0, 0.42]:
        create_cube(f"Stringer_{y}", (1.2, 0.08, 0.1), (pos[0], pos[1] + y, pos[2] + 0.08), material=mats['metal_panel'], parent=root)
    # Bottom skids
    for y in [-0.42, 0.0, 0.42]:
        create_cube(f"Bot_Plank_{y}", (1.2, 0.12, 0.03), (pos[0], pos[1] + y, pos[2] + 0.015), material=mats['metal_dark'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Pallet")

# ---------------------------------------------------------------------------
# ASSET BUILDERS: GROUP 05 — CYBERPUNK TERMINALS & ELECTRONICS
# ---------------------------------------------------------------------------

def build_05_control_terminal(mats, pos):
    root = create_empty("SM_Control_Terminal_Root", pos)
    # Pedestal base
    create_cube("Base", (0.7, 0.6, 0.1), (pos[0], pos[1], pos[2] + 0.05), material=mats['metal_dark'], parent=root)
    create_cube("Pillar", (0.4, 0.3, 0.8), (pos[0], pos[1], pos[2] + 0.5), material=mats['metal_dark'], parent=root)
    # Angled console deck
    create_cube("Console_Bed", (0.9, 0.55, 0.12), (pos[0], pos[1] - 0.05, pos[2] + 0.95), rotation=(math.radians(25.0), 0, 0), material=mats['metal_panel'], parent=root)
    # Keyboard & dials
    create_cube("Keyboard", (0.5, 0.22, 0.02), (pos[0], pos[1] - 0.12, pos[2] + 0.94), rotation=(math.radians(25.0), 0, 0), material=mats['rubber'], parent=root)
    # Main tilted monitor display
    create_cube("Screen_Frame", (0.8, 0.06, 0.45), (pos[0], pos[1] + 0.12, pos[2] + 1.25), rotation=(-math.radians(15.0), 0, 0), material=mats['metal_dark'], parent=root)
    create_cube("Screen_Glow", (0.74, 0.02, 0.39), (pos[0], pos[1] + 0.09, pos[2] + 1.25), rotation=(-math.radians(15.0), 0, 0), material=mats['screen_glitch'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Control_Terminal")


def build_05_info_terminal_glitch(mats, pos):
    root = create_empty("SM_Info_Terminal_Glitch_Root", pos)
    create_cube("Foot", (0.6, 0.5, 0.08), (pos[0], pos[1], pos[2] + 0.04), material=mats['metal_dark'], parent=root)
    create_cube("Kiosk_Body", (0.55, 0.35, 1.7), (pos[0], pos[1], pos[2] + 0.93), material=mats['metal_dark'], parent=root)
    # Dual stacked portrait touchscreens
    create_cube("Screen_Upper", (0.44, 0.02, 0.6), (pos[0], pos[1] - 0.18, pos[2] + 1.35), material=mats['screen_glitch'], parent=root)
    create_cube("Screen_Lower", (0.44, 0.02, 0.4), (pos[0], pos[1] - 0.18, pos[2] + 0.78), material=mats['neon_cyan'], parent=root)
    create_cube("Side_Jack_Bay", (0.04, 0.2, 0.4), (pos[0] + 0.28, pos[1], pos[2] + 1.1), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Info_Terminal_Glitch")


def build_05_access_panel(mats, pos):
    root = create_empty("SM_Access_Panel_Root", pos)
    create_cube("Housing", (0.4, 0.08, 0.6), (pos[0], pos[1], pos[2] + 0.3), material=mats['metal_dark'], parent=root)
    # Keypad grid
    create_cube("Keypad_Face", (0.22, 0.02, 0.24), (pos[0], pos[1] - 0.045, pos[2] + 0.36), material=mats['rubber'], parent=root)
    # Biometric scanner plate
    create_cube("Scanner_Glass", (0.2, 0.02, 0.12), (pos[0], pos[1] - 0.045, pos[2] + 0.14), material=mats['neon_cyan'], parent=root)
    # LED Indicator dots
    create_cylinder("LED_Red", radius=0.015, depth=0.02, vertices=8, location=(pos[0] - 0.12, pos[1] - 0.045, pos[2] + 0.53), rotation=(math.pi/2, 0, 0), material=mats['neon_red'], parent=root)
    create_cylinder("LED_Green", radius=0.015, depth=0.02, vertices=8, location=(pos[0] + 0.12, pos[1] - 0.045, pos[2] + 0.53), rotation=(math.pi/2, 0, 0), material=mats['neon_cyan'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Access_Panel")


def build_05_electrical_box(mats, pos):
    root = create_empty("SM_Electrical_Box_Root", pos)
    create_cube("Cabinet", (0.6, 0.3, 0.8), (pos[0], pos[1], pos[2] + 0.4), material=mats['metal_panel'], parent=root)
    create_cube("Door_Rim", (0.58, 0.04, 0.78), (pos[0], pos[1] - 0.16, pos[2] + 0.4), material=mats['metal_dark'], parent=root)
    # Throw switch handle on right
    create_cylinder("Switch_Axle", radius=0.02, depth=0.08, vertices=8, location=(pos[0] + 0.32, pos[1] - 0.05, pos[2] + 0.45), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    create_cube("Switch_Arm", (0.04, 0.15, 0.03), (pos[0] + 0.35, pos[1] - 0.1, pos[2] + 0.5), rotation=(math.radians(35.0), 0, 0), material=mats['neon_red'], parent=root)
    # Lightning hazard warning
    create_cube("Hazard_Triangle", (0.18, 0.02, 0.18), (pos[0], pos[1] - 0.19, pos[2] + 0.55), material=mats['hazard_yellow'], parent=root)
    # Bottom conduit gland fittings
    for x in [-0.18, 0.0, 0.18]:
        create_cylinder(f"Gland_{x}", radius=0.035, depth=0.08, vertices=12, location=(pos[0] + x, pos[1], pos[2] - 0.04), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Electrical_Box")


def build_05_server_rack(mats, pos):
    root = create_empty("SM_Server_Rack_Root", pos)
    create_cube("Outer_Chassis", (0.8, 0.9, 2.0), (pos[0], pos[1], pos[2] + 1.0), material=mats['metal_dark'], parent=root)
    # 8 Server blade modules
    for i in range(8):
        z_blade = 0.25 + i * 0.22
        create_cube(f"Blade_{i}", (0.74, 0.04, 0.18), (pos[0], pos[1] - 0.44, pos[2] + z_blade), material=mats['metal_panel'], parent=root)
        # Blinking LED cluster
        create_cylinder(f"LED_1_{i}", radius=0.015, depth=0.02, vertices=8, location=(pos[0] - 0.28, pos[1] - 0.47, pos[2] + z_blade), rotation=(math.pi/2, 0, 0), material=mats['neon_cyan'], parent=root)
        create_cylinder(f"LED_2_{i}", radius=0.015, depth=0.02, vertices=8, location=(pos[0] - 0.23, pos[1] - 0.47, pos[2] + z_blade), rotation=(math.pi/2, 0, 0), material=mats['neon_purple'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Server_Rack")


def build_05_vent_unit(mats, pos):
    root = create_empty("SM_Vent_Unit_Root", pos)
    create_cube("Housing", (0.9, 0.5, 0.9), (pos[0], pos[1], pos[2] + 0.45), material=mats['metal_dark'], parent=root)
    # Recessed duct cowl
    create_cylinder("Cowl", radius=0.38, depth=0.15, vertices=24, location=(pos[0], pos[1] - 0.22, pos[2] + 0.45), rotation=(math.pi/2, 0, 0), material=mats['metal_panel'], parent=root)
    create_cylinder("Fan_Hub", radius=0.1, depth=0.18, vertices=16, location=(pos[0], pos[1] - 0.22, pos[2] + 0.45), rotation=(math.pi/2, 0, 0), material=mats['hazard_yellow'], parent=root)
    # Protective grille crossbars
    create_cube("Grille_H", (0.7, 0.02, 0.04), (pos[0], pos[1] - 0.28, pos[2] + 0.45), material=mats['metal_bright'], parent=root)
    create_cube("Grille_V", (0.04, 0.02, 0.7), (pos[0], pos[1] - 0.28, pos[2] + 0.45), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Vent_Unit")


def build_05_ac_unit_generator(mats, pos):
    root = create_empty("SM_AC_Unit_Generator_Root", pos)
    create_cube("Base_Frame", (1.6, 1.0, 0.12), (pos[0], pos[1], pos[2] + 0.06), material=mats['metal_dark'], parent=root)
    create_cube("Main_Housing", (1.5, 0.9, 0.9), (pos[0], pos[1], pos[2] + 0.55), material=mats['metal_panel'], parent=root)
    # Twin rooftop turbine exhaust fans
    for x in [-0.42, 0.42]:
        create_cylinder(f"Exhaust_{x}", radius=0.32, depth=0.12, vertices=20, location=(pos[0] + x, pos[1], pos[2] + 1.05), material=mats['metal_dark'], parent=root)
        create_cylinder(f"Fan_Core_{x}", radius=0.1, depth=0.16, vertices=12, location=(pos[0] + x, pos[1], pos[2] + 1.05), material=mats['hazard_yellow'], parent=root)
    # Copper cooling fins along front
    create_cube("Cooling_Fins", (1.2, 0.06, 0.6), (pos[0], pos[1] - 0.46, pos[2] + 0.55), material=mats['metal_rust'], parent=root)
    return join_objects_to_single_mesh(root, "SM_AC_Unit_Generator")


def build_05_security_camera(mats, pos):
    root = create_empty("SM_Security_Camera_Root", pos)
    # Wall plate
    create_cube("Wall_Plate", (0.15, 0.04, 0.2), (pos[0], pos[1], pos[2] + 0.15), material=mats['metal_dark'], parent=root)
    # Cantilever arm
    create_cube("Arm", (0.05, 0.2, 0.05), (pos[0], pos[1] - 0.1, pos[2] + 0.15), material=mats['metal_dark'], parent=root)
    # Dome housing
    create_cylinder("Dome", radius=0.1, depth=0.14, vertices=16, location=(pos[0], pos[1] - 0.2, pos[2] + 0.08), material=mats['metal_panel'], parent=root)
    create_cylinder("Red_Lens", radius=0.035, depth=0.06, vertices=12, location=(pos[0], pos[1] - 0.28, pos[2] + 0.08), rotation=(math.pi/2, 0, 0), material=mats['neon_red'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Security_Camera")


def build_05_hanging_light(mats, pos):
    root = create_empty("SM_Hanging_Light_Root", pos)
    create_cylinder("Cord", radius=0.015, depth=0.4, vertices=8, location=(pos[0], pos[1], pos[2] + 0.5), material=mats['rubber'], parent=root)
    create_cylinder("Housing", radius=0.2, depth=0.15, vertices=16, location=(pos[0], pos[1], pos[2] + 0.25), material=mats['metal_dark'], parent=root)
    create_cylinder("Lamp_Bulb", radius=0.14, depth=0.1, vertices=16, location=(pos[0], pos[1], pos[2] + 0.15), material=mats['neon_amber'], parent=root)
    # Wire guard cage
    create_cylinder("Wire_Cage", radius=0.22, depth=0.2, vertices=12, location=(pos[0], pos[1], pos[2] + 0.12), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Hanging_Light")

# ---------------------------------------------------------------------------
# ASSET BUILDERS: GROUP 06 — LIGHTING, FURNITURE & DETAILS
# ---------------------------------------------------------------------------

def build_06_ceiling_light(mats, pos):
    root = create_empty("SM_Ceiling_Light_Root", pos)
    create_cube("Frame", (1.2, 0.3, 0.1), (pos[0], pos[1], pos[2] + 0.05), material=mats['metal_dark'], parent=root)
    create_cube("Diffuser", (1.08, 0.22, 0.03), (pos[0], pos[1], pos[2] + 0.015), material=mats['neon_cyan'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Ceiling_Light")


def build_06_neon_light_purple(mats, pos):
    root = create_empty("SM_Neon_Light_Purple_Root", pos)
    create_cube("Mount_Bar", (1.5, 0.06, 0.08), (pos[0], pos[1], pos[2] + 0.06), material=mats['metal_dark'], parent=root)
    create_cylinder("Neon_Tube", radius=0.025, depth=1.4, vertices=12, location=(pos[0], pos[1] - 0.05, pos[2] + 0.06), rotation=(0, math.pi/2, 0), material=mats['neon_purple'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Neon_Light_Purple")


def build_06_neon_light_cyan(mats, pos):
    root = create_empty("SM_Neon_Light_Cyan_Root", pos)
    create_cube("Mount_Bar", (1.5, 0.06, 0.08), (pos[0], pos[1], pos[2] + 0.06), material=mats['metal_dark'], parent=root)
    create_cylinder("Neon_Tube", radius=0.025, depth=1.4, vertices=12, location=(pos[0], pos[1] - 0.05, pos[2] + 0.06), rotation=(0, math.pi/2, 0), material=mats['neon_cyan'], parent=root)
    create_cube("Inverter_Box", (0.15, 0.08, 0.12), (pos[0] + 0.72, pos[1] - 0.02, pos[2] + 0.06), material=mats['metal_panel'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Neon_Light_Cyan")


def build_06_wall_light_warm(mats, pos):
    root = create_empty("SM_Wall_Light_Warm_Root", pos)
    create_cube("Sconce_Back", (0.3, 0.04, 0.4), (pos[0], pos[1], pos[2] + 0.2), material=mats['metal_dark'], parent=root)
    create_cube("Angled_Shade", (0.26, 0.2, 0.22), (pos[0], pos[1] - 0.1, pos[2] + 0.25), rotation=(-math.radians(20.0), 0, 0), material=mats['metal_panel'], parent=root)
    create_cube("Warm_Lamp", (0.22, 0.15, 0.03), (pos[0], pos[1] - 0.1, pos[2] + 0.16), material=mats['neon_amber'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Wall_Light_Warm")


def build_06_emergency_light_red(mats, pos):
    root = create_empty("SM_Emergency_Light_Red_Root", pos)
    create_cube("Base_Bracket", (0.5, 0.15, 0.08), (pos[0], pos[1], pos[2] + 0.04), material=mats['metal_dark'], parent=root)
    create_cylinder("Dome_L", radius=0.08, depth=0.14, vertices=16, location=(pos[0] - 0.15, pos[1], pos[2] + 0.15), material=mats['neon_red'], parent=root)
    create_cylinder("Dome_R", radius=0.08, depth=0.14, vertices=16, location=(pos[0] + 0.15, pos[1], pos[2] + 0.15), material=mats['neon_red'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Emergency_Light_Red")


def build_06_street_light_indoor(mats, pos):
    root = create_empty("SM_Street_Light_Indoor_Root", pos)
    create_cube("Base_Plate", (0.4, 0.4, 0.08), (pos[0], pos[1], pos[2] + 0.04), material=mats['metal_dark'], parent=root)
    # Pole 3.5m tall
    create_cylinder("Pole", radius=0.06, depth=3.2, vertices=16, location=(pos[0], pos[1], pos[2] + 1.6), material=mats['metal_dark'], parent=root)
    # Cantilever arm extending forward
    create_cube("Arm", (0.08, 0.8, 0.08), (pos[0], pos[1] - 0.4, pos[2] + 3.2), material=mats['metal_bright'], parent=root)
    # Dual floodlight heads
    for x in [-0.15, 0.15]:
        create_cube(f"Head_{x}", (0.16, 0.22, 0.1), (pos[0] + x, pos[1] - 0.75, pos[2] + 3.12), rotation=(math.radians(30.0), 0, 0), material=mats['metal_panel'], parent=root)
        create_cube(f"Lens_{x}", (0.13, 0.18, 0.02), (pos[0] + x, pos[1] - 0.75, pos[2] + 3.08), rotation=(math.radians(30.0), 0, 0), material=mats['neon_cyan'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Street_Light_Indoor")


def build_06_monitor_screen(mats, pos):
    root = create_empty("SM_Monitor_Screen_Root", pos)
    create_cube("Bezel", (1.1, 0.08, 0.65), (pos[0], pos[1], pos[2] + 0.35), material=mats['metal_dark'], parent=root)
    create_cube("Display", (1.02, 0.02, 0.58), (pos[0], pos[1] - 0.04, pos[2] + 0.35), material=mats['screen_glitch'], parent=root)
    create_cube("Wall_Mount", (0.2, 0.08, 0.2), (pos[0], pos[1] + 0.07, pos[2] + 0.35), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Monitor_Screen")


def build_06_computer_desk(mats, pos):
    root = create_empty("SM_Computer_Desk_Root", pos)
    create_cube("Desktop", (1.4, 0.7, 0.05), (pos[0], pos[1], pos[2] + 0.72), material=mats['metal_panel'], parent=root)
    # 4 Steel legs
    for lx in [-0.64, 0.64]:
        for ly in [-0.3, 0.3]:
            create_cylinder(f"Leg_{lx}_{ly}", radius=0.03, depth=0.7, vertices=12, location=(pos[0] + lx, pos[1] + ly, pos[2] + 0.35), material=mats['metal_dark'], parent=root)
    # Under-desk drawer unit
    create_cube("Drawer_Unit", (0.35, 0.55, 0.5), (pos[0] + 0.45, pos[1], pos[2] + 0.42), material=mats['metal_dark'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Computer_Desk")


def build_06_chair(mats, pos):
    root = create_empty("SM_Chair_Root", pos)
    # 5-Spoke base
    create_cylinder("Base_Hub", radius=0.08, depth=0.08, vertices=12, location=(pos[0], pos[1], pos[2] + 0.08), material=mats['metal_dark'], parent=root)
    for i in range(5):
        ang = i * (2 * math.pi / 5)
        create_cube(f"Spoke_{i}", (0.04, 0.26, 0.04), (pos[0] + math.sin(ang)*0.14, pos[1] + math.cos(ang)*0.14, pos[2] + 0.06), rotation=(0, 0, -ang), material=mats['metal_dark'], parent=root)
        create_cylinder(f"Caster_{i}", radius=0.03, depth=0.03, vertices=8, location=(pos[0] + math.sin(ang)*0.26, pos[1] + math.cos(ang)*0.26, pos[2] + 0.03), material=mats['rubber'], parent=root)
    # Piston
    create_cylinder("Piston", radius=0.035, depth=0.35, vertices=12, location=(pos[0], pos[1], pos[2] + 0.28), material=mats['metal_bright'], parent=root)
    # Seat & Backrest
    create_cube("Seat", (0.5, 0.5, 0.08), (pos[0], pos[1], pos[2] + 0.48), material=mats['rubber'], parent=root)
    create_cube("Backrest", (0.45, 0.06, 0.55), (pos[0], pos[1] + 0.22, pos[2] + 0.78), rotation=(-math.radians(10.0), 0, 0), material=mats['rubber'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Chair")


def build_06_trash_bin_a(mats, pos):
    root = create_empty("SM_Trash_Bin_A_Root", pos)
    create_cylinder("Body", radius=0.22, depth=0.85, vertices=20, location=(pos[0], pos[1], pos[2] + 0.425), material=mats['metal_panel'], parent=root)
    create_cylinder("Lid_Ring", radius=0.24, depth=0.08, vertices=20, location=(pos[0], pos[1], pos[2] + 0.84), material=mats['neon_cyan'], parent=root)
    create_cylinder("Swing_Flap", radius=0.16, depth=0.02, vertices=16, location=(pos[0], pos[1], pos[2] + 0.84), material=mats['metal_dark'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Trash_Bin_A")


def build_06_trash_bin_b(mats, pos):
    root = create_empty("SM_Trash_Bin_B_Root", pos)
    # Rectangular dumpster 120x70x95cm
    create_cube("Bin_Body", (1.2, 0.7, 0.8), (pos[0], pos[1], pos[2] + 0.5), material=mats['metal_dark'], parent=root)
    # Sloped split lids
    create_cube("Lid_L", (0.58, 0.74, 0.05), (pos[0] - 0.3, pos[1], pos[2] + 0.92), rotation=(0, -math.radians(8.0), 0), material=mats['hazard_yellow'], parent=root)
    create_cube("Lid_R", (0.58, 0.74, 0.05), (pos[0] + 0.3, pos[1], pos[2] + 0.92), rotation=(0, math.radians(8.0), 0), material=mats['hazard_yellow'], parent=root)
    # Side lift trunnion pins
    create_cylinder("Pin_L", radius=0.03, depth=0.15, vertices=12, location=(pos[0] - 0.66, pos[1], pos[2] + 0.55), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    create_cylinder("Pin_R", radius=0.03, depth=0.15, vertices=12, location=(pos[0] + 0.66, pos[1], pos[2] + 0.55), rotation=(0, math.pi/2, 0), material=mats['metal_bright'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Trash_Bin_B")


def build_06_duct_cover(mats, pos):
    root = create_empty("SM_Duct_Cover_Root", pos)
    create_cube("Rim", (0.6, 0.06, 0.6), (pos[0], pos[1], pos[2] + 0.3), material=mats['metal_dark'], parent=root)
    # Louver vanes
    for i in range(7):
        create_cube(f"Vane_{i}", (0.5, 0.04, 0.03), (pos[0], pos[1] - 0.02, pos[2] + 0.12 + i * 0.06), rotation=(-math.radians(35.0), 0, 0), material=mats['metal_bright'], parent=root)
    # 4 Corner mounting screws
    for sx in [-0.26, 0.26]:
        for sz in [0.06, 0.54]:
            create_cylinder(f"Screw_{sx}_{sz}", radius=0.015, depth=0.03, vertices=8, location=(pos[0] + sx, pos[1] - 0.035, pos[2] + sz), rotation=(math.pi/2, 0, 0), material=mats['hazard_yellow'], parent=root)
    return join_objects_to_single_mesh(root, "SM_Duct_Cover")

# ---------------------------------------------------------------------------
# REGISTRY OF ALL 56 ASSETS
# ---------------------------------------------------------------------------

ASSET_REGISTRY = [
    # Group 01
    ("01_Wall_Panel_A", build_01_wall_panel_a),
    ("01_Wall_Panel_B_Pipes", build_01_wall_panel_b_pipes),
    ("01_Wall_Panel_C_Vent", build_01_wall_panel_c_vent),
    ("01_Corner_Wall", build_01_corner_wall),
    ("01_Door_Frame", build_01_door_frame),
    ("01_Industrial_Door", build_01_industrial_door),
    ("01_Large_Gate", build_01_large_gate),
    ("01_Window_Panel", build_01_window_panel),

    # Group 02
    ("02_Floor_Tile_A", build_02_floor_tile_a),
    ("02_Floor_Tile_B_Grate", build_02_floor_tile_b_grate),
    ("02_Floor_Tile_C", build_02_floor_tile_c),
    ("02_Floor_Tile_D_Corner", build_02_floor_tile_d_corner),
    ("02_Floor_Tile_E_Ramp", build_02_floor_tile_e_ramp),
    ("02_Stair_Module", build_02_stair_module),
    ("02_Platform_Module", build_02_platform_module),
    ("02_Railing_Straight", build_02_railing_straight),
    ("02_Railing_Corner", build_02_railing_corner),

    # Group 03
    ("03_Lift_Platform", build_03_lift_platform),
    ("03_Elevator_Shaft_Module", build_03_elevator_shaft_module),
    ("03_Large_Vertical_Panel", build_03_large_vertical_panel),
    ("03_Horizontal_Beam", build_03_horizontal_beam),
    ("03_Pipe_Straight", build_03_pipe_straight),
    ("03_Pipe_Elbow", build_03_pipe_elbow),
    ("03_Pipe_Junction_T", build_03_pipe_junction_t),
    ("03_Pipe_Set_Wall", build_03_pipe_set_wall),
    ("03_Cable_Tray", build_03_cable_tray),

    # Group 04
    ("04_Crate_Large", build_04_crate_large),
    ("04_Crate_Medium", build_04_crate_medium),
    ("04_Crate_Small", build_04_crate_small),
    ("04_Stacked_Crates", build_04_stacked_crates),
    ("04_Barrel", build_04_barrel),
    ("04_Barrier_Low", build_04_barrier_low),
    ("04_Barrier_Tall", build_04_barrier_tall),
    ("04_Construction_Barrier", build_04_construction_barrier),
    ("04_Pallet", build_04_pallet),

    # Group 05
    ("05_Control_Terminal", build_05_control_terminal),
    ("05_Info_Terminal_Glitch", build_05_info_terminal_glitch),
    ("05_Access_Panel", build_05_access_panel),
    ("05_Electrical_Box", build_05_electrical_box),
    ("05_Server_Rack", build_05_server_rack),
    ("05_Vent_Unit", build_05_vent_unit),
    ("05_AC_Unit_Generator", build_05_ac_unit_generator),
    ("05_Security_Camera", build_05_security_camera),
    ("05_Hanging_Light", build_05_hanging_light),

    # Group 06
    ("06_Ceiling_Light", build_06_ceiling_light),
    ("06_Neon_Light_Purple", build_06_neon_light_purple),
    ("06_Neon_Light_Cyan", build_06_neon_light_cyan),
    ("06_Wall_Light_Warm", build_06_wall_light_warm),
    ("06_Emergency_Light_Red", build_06_emergency_light_red),
    ("06_Street_Light_Indoor", build_06_street_light_indoor),
    ("06_Monitor_Screen", build_06_monitor_screen),
    ("06_Computer_Desk", build_06_computer_desk),
    ("06_Chair", build_06_chair),
    ("06_Trash_Bin_A", build_06_trash_bin_a),
    ("06_Trash_Bin_B", build_06_trash_bin_b),
    ("06_Duct_Cover", build_06_duct_cover)
]

# ---------------------------------------------------------------------------
# MAIN PIPELINE EXECUTION
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("  SECTOR 09 — LEVEL 1 MODULAR ASSET KIT GENERATOR")
    print(f"  Target Asset Count: {len(ASSET_REGISTRY)}")
    print("=" * 70)

    # Reset scene
    bpy.ops.wm.read_factory_settings(use_empty=True)

    mats = get_material_library()
    generated_meshes = []

    # Grid spacing for showcase placement in master blend
    grid_cols = 8
    spacing_x = 3.5
    spacing_y = 3.5

    for idx, (raw_name, builder_func) in enumerate(ASSET_REGISTRY):
        col = idx % grid_cols
        row = idx // grid_cols
        grid_pos = (col * spacing_x, -row * spacing_y, 0.0)

        # Build asset
        mesh = builder_func(mats, grid_pos)
        if not mesh:
            print(f"[ERROR] Failed to build {raw_name}")
            continue

        clean_name = f"SM_{raw_name}"
        mesh.name = clean_name
        generated_meshes.append(mesh)

        # Export individual FBX to both Blender/FBX and UE Projects Content
        fbx_name = f"{clean_name}.fbx"
        export_paths = [
            os.path.join(FBX_OUTPUT_DIR, fbx_name),
            os.path.join(UE_CONTENT_DIR, fbx_name)
        ]
        export_fbx(mesh, export_paths)

    # Save Master Blender Showcase
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUTPUT_PATH)
    print(f"\n[SUCCESS] Master showcase scene saved: {BLEND_OUTPUT_PATH}")
    print(f"[SUCCESS] Exported {len(generated_meshes)} FBX assets to:\n  - {FBX_OUTPUT_DIR}\n  - {UE_CONTENT_DIR}")
    print("=" * 70)


if __name__ == "__main__":
    main()
