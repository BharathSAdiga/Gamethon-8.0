"""
LAST SECOND — SECTOR 09 | LEVEL 1: WAKE UP CALL
Master 3D Environment Assembly Script for Blender 5.x / 4.x
Imports actual FBX assets from Assets/Meshes/, reconnects 2K PBR textures,
assembles the complete 5-zone playable building environment, configures lighting,
creates 8 cameras, saves Sector09_Level1_Final.blend, and renders presentation views.
"""

import os
import sys
import math
import glob
import bpy
from mathutils import Vector, Euler

# ---------------------------------------------------------------------------
# Path Configuration
# ---------------------------------------------------------------------------
REPO_ROOT = r"d:\unreal engine"
ASSETS_DIR = os.path.join(REPO_ROOT, "Assets")
MESHES_DIR = os.path.join(ASSETS_DIR, "Meshes")
TEXTURES_DIR = os.path.join(ASSETS_DIR, "Textures")
SCRIPTS_DIR = os.path.join(ASSETS_DIR, "Scripts")
REF_DIR = os.path.join(ASSETS_DIR, "Reference")
LAYOUT_DIR = os.path.join(REF_DIR, "Layout")
DOCS_DIR = os.path.join(ASSETS_DIR, "Documentation")

BLEND_OUTPUT = os.path.join(ASSETS_DIR, "Sector09_Level1_Final.blend")
BLEND_BACKUP = os.path.join(REPO_ROOT, "Blender", "Blend", "Sector09_Level1_Final.blend")

RENDER_ISO = os.path.join(REF_DIR, "Sector09_Level1_Isometric.png")
RENDER_TOP = os.path.join(REF_DIR, "Sector09_Level1_TopView.png")
RENDER_SIDE = os.path.join(REF_DIR, "Sector09_Level1_SideView.png")

for d in [SCRIPTS_DIR, REF_DIR, LAYOUT_DIR, DOCS_DIR, os.path.dirname(BLEND_BACKUP)]:
    os.makedirs(d, exist_ok=True)

# ---------------------------------------------------------------------------
# Scene Reset & Collection Hierarchy
# ---------------------------------------------------------------------------
def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if bpy.context.scene.collection.objects:
        for obj in list(bpy.context.scene.collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

COLLECTION_NAMES = [
    "L1_Architecture",
    "L1_Floors",
    "L1_Doors",
    "L1_Pipes",
    "L1_Railings",
    "L1_Props",
    "L1_ObservationRoom",
    "L1_VerticalLift",
    "L1_LockedTerminal",
    "L1_Lighting",
    "L1_Cameras",
    "L1_Placeholders"
]

COLLECTIONS = {}

def setup_collections():
    root = bpy.context.scene.collection
    for name in COLLECTION_NAMES:
        col = bpy.data.collections.get(name)
        if not col:
            col = bpy.data.collections.new(name)
            root.children.link(col)
        COLLECTIONS[name] = col

# ---------------------------------------------------------------------------
# PBR Material & Texture System
# ---------------------------------------------------------------------------
MATERIALS = {}

def safe_set_bsdf(bsdf, socket_name, value):
    if socket_name in bsdf.inputs:
        bsdf.inputs[socket_name].default_value = value
    elif socket_name == 'Specular' and 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = value
    elif socket_name == 'Emission' and 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = value

def create_pbr_mat(name, base_color=(0.1, 0.12, 0.15, 1.0), metallic=0.8, roughness=0.4,
                   tex_prefix=None, emission_color=None, emission_strength=0.0, is_glass=False):
    mat = bpy.data.materials.get(name)
    if mat:
        MATERIALS[name] = mat
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

    if is_glass:
        safe_set_bsdf(bsdf, 'Roughness', 0.08)
        safe_set_bsdf(bsdf, 'Transmission Weight', 0.85)
        if 'Transmission' in bsdf.inputs:
            bsdf.inputs['Transmission'].default_value = 0.85
        if 'IOR' in bsdf.inputs:
            bsdf.inputs['IOR'].default_value = 1.33
        if hasattr(mat, 'blend_method'):
            mat.blend_method = 'BLEND'

    if emission_color:
        safe_set_bsdf(bsdf, 'Emission Color', emission_color)
        safe_set_bsdf(bsdf, 'Emission', emission_color)
        if 'Emission Strength' in bsdf.inputs:
            bsdf.inputs['Emission Strength'].default_value = emission_strength

    if tex_prefix:
        bc_path = os.path.join(TEXTURES_DIR, "BaseColor", f"{tex_prefix}_BaseColor.png")
        if os.path.exists(bc_path):
            img_bc = bpy.data.images.load(bc_path)
            node_bc = nodes.new('ShaderNodeTexImage')
            node_bc.location = (-400, 200)
            node_bc.image = img_bc
            links.new(node_bc.outputs['Color'], bsdf.inputs['Base Color'])

        n_path = os.path.join(TEXTURES_DIR, "Normal", f"{tex_prefix}_Normal.png")
        if os.path.exists(n_path):
            img_n = bpy.data.images.load(n_path)
            img_n.colorspace_settings.name = 'Non-Color'
            node_n = nodes.new('ShaderNodeTexImage')
            node_n.location = (-600, -200)
            node_n.image = img_n
            node_norm = nodes.new('ShaderNodeNormalMap')
            node_norm.location = (-200, -200)
            node_norm.inputs['Strength'].default_value = 1.0
            links.new(node_n.outputs['Color'], node_norm.inputs['Color'])
            links.new(node_norm.outputs['Normal'], bsdf.inputs['Normal'])

        r_path = os.path.join(TEXTURES_DIR, "Roughness", f"{tex_prefix}_Roughness.png")
        if os.path.exists(r_path):
            img_r = bpy.data.images.load(r_path)
            img_r.colorspace_settings.name = 'Non-Color'
            node_r = nodes.new('ShaderNodeTexImage')
            node_r.location = (-400, -50)
            node_r.image = img_r
            links.new(node_r.outputs['Color'], bsdf.inputs['Roughness'])

        m_path = os.path.join(TEXTURES_DIR, "Metallic", f"{tex_prefix}_Metallic.png")
        if os.path.exists(m_path):
            img_m = bpy.data.images.load(m_path)
            img_m.colorspace_settings.name = 'Non-Color'
            node_m = nodes.new('ShaderNodeTexImage')
            node_m.location = (-400, -350)
            node_m.image = img_m
            links.new(node_m.outputs['Color'], bsdf.inputs['Metallic'])

        e_path = os.path.join(TEXTURES_DIR, "Emissive", f"{tex_prefix}_Emissive.png")
        if os.path.exists(e_path) and emission_color:
            img_e = bpy.data.images.load(e_path)
            node_e = nodes.new('ShaderNodeTexImage')
            node_e.location = (-400, -500)
            node_e.image = img_e
            if 'Emission Color' in bsdf.inputs:
                links.new(node_e.outputs['Color'], bsdf.inputs['Emission Color'])
            elif 'Emission' in bsdf.inputs:
                links.new(node_e.outputs['Color'], bsdf.inputs['Emission'])

    MATERIALS[name] = mat
    return mat

def build_material_library():
    create_pbr_mat('M_IndustrialMetal_Master', (0.09, 0.12, 0.16, 1.0), metallic=0.85, roughness=0.35, tex_prefix='T_Cyberpunk_Wall_Panel')
    create_pbr_mat('M_WornMetal', (0.12, 0.14, 0.18, 1.0), metallic=0.9, roughness=0.45, tex_prefix='T_Cyberpunk_Pipes_Conduit')
    create_pbr_mat('M_DarkConcrete', (0.08, 0.09, 0.10, 1.0), metallic=0.05, roughness=0.9, tex_prefix='T_Cyberpunk_Floor_Grate')
    create_pbr_mat('M_MetalFloor', (0.15, 0.17, 0.20, 1.0), metallic=0.95, roughness=0.35, tex_prefix='T_Cyberpunk_Floor_Grate')
    create_pbr_mat('M_MetalGrate', (0.12, 0.14, 0.16, 1.0), metallic=0.9, roughness=0.4, tex_prefix='T_Cyberpunk_Floor_Grate')
    create_pbr_mat('M_DarkGlass', (0.03, 0.06, 0.10, 0.4), metallic=0.2, roughness=0.08, is_glass=True)
    create_pbr_mat('M_CyanEmissive', (0.0, 0.90, 1.0, 1.0), metallic=0.0, roughness=0.1,
                   emission_color=(0.0, 0.90, 1.0, 1.0), emission_strength=15.0, tex_prefix='T_Cyberpunk_Neon_Lights')
    create_pbr_mat('M_PurpleEmissive', (0.85, 0.05, 0.95, 1.0), metallic=0.0, roughness=0.1,
                   emission_color=(0.85, 0.05, 0.95, 1.0), emission_strength=14.0, tex_prefix='T_Cyberpunk_Neon_Lights')
    create_pbr_mat('M_RedWarningEmissive', (1.0, 0.03, 0.03, 1.0), metallic=0.0, roughness=0.1,
                   emission_color=(1.0, 0.03, 0.03, 1.0), emission_strength=18.0, tex_prefix='T_Cyberpunk_Neon_Lights')
    create_pbr_mat('M_ScreenGlass', (0.05, 0.85, 0.65, 1.0), metallic=0.1, roughness=0.2,
                   emission_color=(0.05, 0.85, 0.65, 1.0), emission_strength=10.0, tex_prefix='T_Cyberpunk_Terminal_Console')
    create_pbr_mat('M_IndustrialPaint', (0.95, 0.72, 0.05, 1.0), metallic=0.1, roughness=0.45, tex_prefix='T_Cyberpunk_Wall_Panel')
    create_pbr_mat('M_VentilationMetal', (0.35, 0.38, 0.42, 1.0), metallic=0.92, roughness=0.3, tex_prefix='T_Cyberpunk_Wall_Panel')

# -----------------------------------------------------------
# FBX Asset Loader & Normalizer
# -----------------------------------------------------------
ASSET_CACHE = {}

def load_fbx_asset(category, filename):
    key = f"{category}/{filename}"
    if key in ASSET_CACHE:
        return ASSET_CACHE[key]

    path = os.path.join(MESHES_DIR, category, filename)
    if not os.path.exists(path):
        print(f"Warning: {path} not found!")
        return None

    # Import FBX into temporary isolation
    bpy.ops.import_scene.fbx(filepath=path)
    imported = bpy.context.selected_objects
    if not imported:
        return None

    obj = imported[0]
    # Apply rotation and check scale
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.transform_apply(rotation=True)

    # If dimensions indicate centimeters (>20m for props/panels), normalize to meters
    if obj.dimensions.x > 30.0 or obj.dimensions.z > 30.0:
        obj.scale = (0.01, 0.01, 0.01)
        bpy.ops.object.transform_apply(scale=True)

    # Unlink from initial collection
    for col in obj.users_collection:
        col.objects.unlink(obj)

    ASSET_CACHE[key] = obj
    return obj

def spawn_instance(category, filename, instance_name, target_collection_name,
                   loc=(0, 0, 0), rot_deg=(0, 0, 0), scale=(1, 1, 1), override_mat=None):
    base_obj = load_fbx_asset(category, filename)
    if not base_obj:
        return None

    # Create linked duplicate object sharing mesh datablock
    new_obj = bpy.data.objects.new(instance_name, base_obj.data)
    new_obj.location = loc
    new_obj.rotation_euler = Euler((math.radians(rot_deg[0]), math.radians(rot_deg[1]), math.radians(rot_deg[2])), 'XYZ')
    new_obj.scale = scale

    if override_mat and override_mat in MATERIALS:
        if len(new_obj.data.materials) == 0:
            new_obj.data.materials.append(MATERIALS[override_mat])
        else:
            new_obj.data.materials[0] = MATERIALS[override_mat]

    col = COLLECTIONS.get(target_collection_name, bpy.context.scene.collection)
    col.objects.link(new_obj)
    return new_obj

# ---------------------------------------------------------------------------
# Zone Assembly System
# ---------------------------------------------------------------------------

def assemble_zone1_start_area():
    """Zone 1: Start Area (Far Left, X: -16m to -10m, Y: -4m to +2m, Z: 0m)"""
    # Floors (3x3 grid: X from -15 to -11 by 2m, Y from -3 to +1 by 2m)
    f_idx = 1
    for x in [-15.0, -13.0, -11.0]:
        for y in [-3.0, -1.0, 1.0]:
            tile_name = "SM_FloorTile_C.fbx" if (x == -15.0 and y == -1.0) else "SM_FloorTile_A.fbx"
            spawn_instance("Floors", tile_name, f"L1_Start_Floor_{f_idx:02d}", "L1_Floors",
                           loc=(x, y, 0), override_mat="M_MetalFloor")
            f_idx += 1

    # West Entrance Wall (X = -16.0m) with Airlock Door in Center
    spawn_instance("Doors", "SM_Door_Frame.fbx", "L1_Start_DoorFrame_West", "L1_Doors",
                   loc=(-16.0, -1.0, 0), rot_deg=(0, 0, 90), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Doors", "SM_Industrial_Door.fbx", "L1_Start_Door_West", "L1_Doors",
                   loc=(-16.0, -1.0, 0.1), rot_deg=(0, 0, 90), override_mat="M_WornMetal")
    spawn_instance("Architecture", "SM_WallPanel_A.fbx", "L1_Start_Wall_W1", "L1_Architecture",
                   loc=(-16.0, -3.0, 0), rot_deg=(0, 0, 90), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Architecture", "SM_WallPanel_A.fbx", "L1_Start_Wall_W2", "L1_Architecture",
                   loc=(-16.0, 1.0, 0), rot_deg=(0, 0, 90), override_mat="M_IndustrialMetal_Master")

    # South Wall (Y = -4.0m, X: -16m to -10m)
    spawn_instance("Architecture", "SM_Corner_Wall.fbx", "L1_Start_Corner_SW", "L1_Architecture",
                   loc=(-16.0, -4.0, 0), rot_deg=(0, 0, 0), override_mat="M_IndustrialMetal_Master")
    for i, x in enumerate([-14.0, -12.0]):
        spawn_instance("Architecture", "SM_WallPanel_B_Pipes.fbx", f"L1_Start_Wall_S_{i+1}", "L1_Architecture",
                       loc=(x, -4.0, 0), rot_deg=(0, 0, 0), override_mat="M_IndustrialMetal_Master")

    # North Wall (Y = +2.0m, X: -16m to -10m)
    spawn_instance("Architecture", "SM_Corner_Wall.fbx", "L1_Start_Corner_NW", "L1_Architecture",
                   loc=(-16.0, 2.0, 0), rot_deg=(0, 0, 270), override_mat="M_IndustrialMetal_Master")
    for i, x in enumerate([-14.0, -12.0]):
        spawn_instance("Architecture", "SM_WallPanel_A.fbx", f"L1_Start_Wall_N_{i+1}", "L1_Architecture",
                       loc=(x, 2.0, 0), rot_deg=(0, 0, 180), override_mat="M_IndustrialMetal_Master")

    # Ceiling & Lighting
    spawn_instance("Architecture", "SM_CeilingPanel.fbx", "L1_Start_Ceiling", "L1_Architecture",
                   loc=(-13.0, -1.0, 3.2), scale=(1, 1, 1), override_mat="M_IndustrialMetal_Master")
    spawn_instance("SciFi", "SM_Ceiling_Light.fbx", "L1_Start_CeilingLight", "L1_Lighting",
                   loc=(-13.0, -1.0, 3.0), override_mat="M_CyanEmissive")

    # Start Area Props & Power Distribution
    spawn_instance("Industrial", "SM_Electrical_Box.fbx", "L1_Start_PowerBox", "L1_Props",
                   loc=(-13.0, 1.85, 1.2), rot_deg=(0, 0, 180), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Industrial", "SM_Access_Panel.fbx", "L1_Start_AccessPanel", "L1_Props",
                   loc=(-15.0, 1.9, 1.1), rot_deg=(0, 0, 180), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Props", "SM_Stacked_Crates.fbx", "L1_Start_StackedCrates", "L1_Props",
                   loc=(-15.0, -3.0, 0.1), rot_deg=(0, 0, 15), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Props", "SM_Crate_Small.fbx", "L1_Start_Crate_Small", "L1_Props",
                   loc=(-13.8, -3.2, 0.1), rot_deg=(0, 0, -10), override_mat="M_IndustrialMetal_Master")


def assemble_zone2_main_corridor():
    """Zone 2: Main Corridor (Central-Left, X: -10m to +2m, Y: -2m to +2m, Z: 0m)"""
    # Floors (6 tiles long x 2 tiles wide)
    f_idx = 1
    for i, x in enumerate([-9.0, -7.0, -5.0, -3.0, -1.0, 1.0]):
        # Alternate solid plates and grated panels for steam/drainage
        tile_south = "SM_FloorTile_B_Grate.fbx" if (i % 2 == 1) else "SM_FloorTile_A.fbx"
        spawn_instance("Floors", tile_south, f"L1_Corridor_Floor_S_{f_idx:02d}", "L1_Floors",
                       loc=(x, -1.0, 0), override_mat="M_MetalFloor")
        spawn_instance("Floors", "SM_FloorTile_A.fbx", f"L1_Corridor_Floor_N_{f_idx:02d}", "L1_Floors",
                       loc=(x, 1.0, 0), override_mat="M_MetalFloor")
        f_idx += 1

    # South Wall (Y = -2.0m, Continuous along entire corridor length)
    for i, x in enumerate([-9.0, -7.0, -5.0, -3.0, -1.0, 1.0]):
        panel_type = "SM_WallPanel_B_Pipes.fbx" if (i % 2 == 0) else "SM_WallPanel_C_Vent.fbx"
        spawn_instance("Architecture", panel_type, f"L1_Corridor_Wall_S_{i+1}", "L1_Architecture",
                       loc=(x, -2.0, 0), rot_deg=(0, 0, 0), override_mat="M_IndustrialMetal_Master")
        # Continuous conduit bundle along base of south wall
        spawn_instance("Pipes", "SM_Pipe_Set_Wall.fbx", f"L1_Corridor_Conduits_S_{i+1}", "L1_Pipes",
                       loc=(x, -1.85, 0.4), rot_deg=(0, 0, 0), override_mat="M_WornMetal")
        # Overhead cable trays
        spawn_instance("Industrial", "SM_Cable_Tray.fbx", f"L1_Corridor_CableTray_{i+1}", "L1_Pipes",
                       loc=(x, -1.6, 2.7), rot_deg=(0, 0, 0), override_mat="M_WornMetal")

    # North Wall (Y = +2.0m, from X = -10m to -2m; opening for Observation Room from X = -2m to +2m)
    for i, x in enumerate([-9.0, -7.0, -5.0, -3.0]):
        spawn_instance("Architecture", "SM_WallPanel_A.fbx", f"L1_Corridor_Wall_N_{i+1}", "L1_Architecture",
                       loc=(x, 2.0, 0), rot_deg=(0, 0, 180), override_mat="M_IndustrialMetal_Master")
        # Atmospheric Purple Neon Strip fixtures along north corridor wall
        spawn_instance("SciFi", "SM_Neon_Light_Purple.fbx", f"L1_Corridor_Neon_{i+1}", "L1_Lighting",
                       loc=(x, 1.9, 2.2), rot_deg=(0, 0, 180), override_mat="M_PurpleEmissive")

    # Corridor Environmental Props & Hazard Trim (Kept tight against south wall to preserve clear path)
    spawn_instance("Props", "SM_Barrel.fbx", "L1_Corridor_Barrel_01", "L1_Props",
                   loc=(-6.8, -1.6, 0.1), override_mat="M_WornMetal")
    spawn_instance("Props", "SM_Barrel.fbx", "L1_Corridor_Barrel_02", "L1_Props",
                   loc=(-6.3, -1.5, 0.1), override_mat="M_WornMetal")
    spawn_instance("Props", "SM_Crate_Medium.fbx", "L1_Corridor_Crate_01", "L1_Props",
                   loc=(-2.5, -1.5, 0.1), rot_deg=(0, 0, 20), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Railings", "SM_Railing_Straight.fbx", "L1_Corridor_Railing_01", "L1_Railings",
                   loc=(0.0, -1.8, 0.1), rot_deg=(0, 0, 0), override_mat="M_IndustrialMetal_Master")


def assemble_zone3_observation_room():
    """Zone 3: Observation Room (Upper-Middle, X: -2m to +6m, Y: +2m to +8m, Z: 0m)"""
    # Floors (4 tiles wide x 3 tiles deep)
    f_idx = 1
    for x in [-1.0, 1.0, 3.0, 5.0]:
        for y in [3.0, 5.0, 7.0]:
            spawn_instance("Floors", "SM_FloorTile_A.fbx", f"L1_Obs_Floor_{f_idx:02d}", "L1_Floors",
                           loc=(x, y, 0), override_mat="M_MetalFloor")
            f_idx += 1

    # North Wall (Y = +8.0m): Large Panoramic City-View Window overlooking Cyberpunk Skyline!
    spawn_instance("Architecture", "SM_CityView_WindowFrame.fbx", "L1_Obs_WindowFrame", "L1_ObservationRoom",
                   loc=(2.0, 8.0, 0), rot_deg=(0, 0, 180), scale=(1, 1, 1), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Architecture", "SM_Window_Glass.fbx", "L1_Obs_WindowGlass", "L1_ObservationRoom",
                   loc=(2.0, 8.0, 0), rot_deg=(0, 0, 180), scale=(1, 1, 1), override_mat="M_DarkGlass")
    # Flanking Wall Panels
    spawn_instance("Architecture", "SM_WallPanel_A.fbx", "L1_Obs_Wall_N_Left", "L1_ObservationRoom",
                   loc=(-1.0, 8.0, 0), rot_deg=(0, 0, 180), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Architecture", "SM_WallPanel_A.fbx", "L1_Obs_Wall_N_Right", "L1_ObservationRoom",
                   loc=(5.0, 8.0, 0), rot_deg=(0, 0, 180), override_mat="M_IndustrialMetal_Master")

    # West Wall (X = -2.0m, Y: +2m to +8m)
    for i, y in enumerate([3.0, 5.0, 7.0]):
        spawn_instance("Architecture", "SM_WallPanel_A.fbx", f"L1_Obs_Wall_W_{i+1}", "L1_ObservationRoom",
                       loc=(-2.0, y, 0), rot_deg=(0, 0, 90), override_mat="M_IndustrialMetal_Master")

    # East Wall (X = +6.0m, Y: +2m to +8m)
    for i, y in enumerate([3.0, 5.0, 7.0]):
        spawn_instance("Architecture", "SM_WallPanel_B_Pipes.fbx", f"L1_Obs_Wall_E_{i+1}", "L1_ObservationRoom",
                       loc=(6.0, y, 0), rot_deg=(0, 0, 270), override_mat="M_IndustrialMetal_Master")

    # Observation Room Equipment (Desk facing North window!)
    spawn_instance("Props", "SM_Computer_Desk.fbx", "L1_Obs_Desk", "L1_ObservationRoom",
                   loc=(2.0, 6.8, 0.1), rot_deg=(0, 0, 180), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Props", "SM_Chair.fbx", "L1_Obs_Chair", "L1_ObservationRoom",
                   loc=(2.0, 5.8, 0.1), rot_deg=(0, 0, 0), override_mat="M_IndustrialMetal_Master")
    spawn_instance("SciFi", "SM_Monitor_Screen.fbx", "L1_Obs_Monitor", "L1_ObservationRoom",
                   loc=(2.0, 6.8, 0.85), rot_deg=(0, 0, 180), override_mat="M_ScreenGlass")

    # Server Racks & Diagnostics along West Wall
    spawn_instance("SciFi", "SM_Server_Rack.fbx", "L1_Obs_ServerRack_01", "L1_ObservationRoom",
                   loc=(-1.5, 6.0, 0.1), rot_deg=(0, 0, 90), override_mat="M_WornMetal")
    spawn_instance("SciFi", "SM_Server_Rack.fbx", "L1_Obs_ServerRack_02", "L1_ObservationRoom",
                   loc=(-1.5, 4.5, 0.1), rot_deg=(0, 0, 90), override_mat="M_WornMetal")
    spawn_instance("SciFi", "SM_Info_Terminal_Glitch.fbx", "L1_Obs_GlitchTerminal", "L1_ObservationRoom",
                   loc=(-1.4, 3.2, 0.1), rot_deg=(0, 0, 90), override_mat="M_ScreenGlass")


def assemble_zone4_vertical_lift():
    """Zone 4: Vertical Lift (Recessed Right-Middle, X: +2m to +8m, Y: -6m to -2m, Shaft Depth Z: -8m to 0m)"""
    # Preserved Recessed Shaft Walls (Z = -4.0m to 0m and down to -8m)
    for z_lvl in [-6.0, -3.0, 0.0]:
        spawn_instance("Machinery", "SM_Elevator_Shaft_Module.fbx", f"L1_Lift_ShaftRing_Z{abs(int(z_lvl))}", "L1_VerticalLift",
                       loc=(4.0, -4.0, z_lvl), override_mat="M_DarkConcrete")

    # Lift Platform inside the shaft
    spawn_instance("Machinery", "SM_LiftPlatform.fbx", "L1_Lift_Platform_Active", "L1_VerticalLift",
                   loc=(4.0, -4.0, -3.5), override_mat="M_MetalGrate")

    # Upper Landing (Walkway floor at Z = 0m, X: +2m to +8m along northern shaft edge)
    spawn_instance("Floors", "SM_Lift_Landing.fbx", "L1_Lift_Landing_Upper", "L1_VerticalLift",
                   loc=(4.0, -2.0, 0), scale=(1, 1, 1), override_mat="M_MetalGrate")

    # Safety Railings protecting the open vertical shaft pit
    spawn_instance("Railings", "SM_Railing_Straight.fbx", "L1_Lift_Railing_North_1", "L1_Railings",
                   loc=(3.0, -2.1, 0.1), rot_deg=(0, 0, 0), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Railings", "SM_Railing_Straight.fbx", "L1_Lift_Railing_North_2", "L1_Railings",
                   loc=(5.0, -2.1, 0.1), rot_deg=(0, 0, 0), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Railings", "SM_Railing_Straight.fbx", "L1_Lift_Railing_West", "L1_Railings",
                   loc=(2.1, -4.0, 0.1), rot_deg=(0, 0, 90), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Railings", "SM_Railing_Straight.fbx", "L1_Lift_Railing_East", "L1_Railings",
                   loc=(6.9, -4.0, 0.1), rot_deg=(0, 0, 90), override_mat="M_IndustrialMetal_Master")

    # Lift Control Interface & Shaft Lighting Assembly
    spawn_instance("SciFi", "SM_LiftControlPanel.fbx", "L1_Lift_ControlPanel", "L1_VerticalLift",
                   loc=(2.3, -2.0, 0.1), rot_deg=(0, 0, 90), scale=(1, 1, 1), override_mat="M_IndustrialMetal_Master")
    spawn_instance("SciFi", "SM_Shaft_Lighting_Assembly.fbx", "L1_Lift_ShaftBeacon_Pole", "L1_Lighting",
                   loc=(2.2, -5.8, -4.0), scale=(1, 1, 1), override_mat="M_IndustrialMetal_Master")
    spawn_instance("SciFi", "SM_Neon_Light_Purple.fbx", "L1_Lift_Neon_Vertical", "L1_Lighting",
                   loc=(5.8, -2.1, -2.0), rot_deg=(90, 0, 0), override_mat="M_PurpleEmissive")


def assemble_zone5_locked_terminal():
    """Zone 5: Locked Terminal (Far Upper-Right, X: +8m to +16m, Y: -1m to +6m, Z: 0m)"""
    # Floors (4 tiles wide x 3.5 tiles deep)
    f_idx = 1
    for x in [9.0, 11.0, 13.0, 15.0]:
        for y in [0.0, 2.0, 4.0]:
            tile_type = "SM_FloorTile_B_Grate.fbx" if (x == 15.0 and y == 2.0) else "SM_FloorTile_A.fbx"
            spawn_instance("Floors", tile_type, f"L1_Terminal_Floor_{f_idx:02d}", "L1_Floors",
                           loc=(x, y, 0), override_mat="M_MetalFloor")
            f_idx += 1

    # EAST WALL (X = +16.0m): The Primary Focal Point of Level 1 — Massive Blast Gate!
    spawn_instance("Doors", "SM_Large_Gate.fbx", "L1_Terminal_BlastGate_Exit", "L1_LockedTerminal",
                   loc=(16.0, 2.5, 0), rot_deg=(0, 0, 270), override_mat="M_WornMetal")
    # Wall panels flanking the large gate
    spawn_instance("Architecture", "SM_WallPanel_A.fbx", "L1_Terminal_Wall_E_Left", "L1_Architecture",
                   loc=(16.0, 0.0, 0), rot_deg=(0, 0, 270), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Architecture", "SM_WallPanel_A.fbx", "L1_Terminal_Wall_E_Right", "L1_Architecture",
                   loc=(16.0, 5.0, 0), rot_deg=(0, 0, 270), override_mat="M_IndustrialMetal_Master")

    # Interactive Security Console immediately beside the locked gate
    spawn_instance("SciFi", "SM_ControlTerminal.fbx", "L1_Terminal_GateOverrideConsole", "L1_LockedTerminal",
                   loc=(15.2, 0.8, 0.1), rot_deg=(0, 0, 250), override_mat="M_IndustrialMetal_Master")

    # Security Warning Lighting above the gate
    spawn_instance("SciFi", "SM_Emergency_Light_Red.fbx", "L1_Terminal_AlarmStrobe_Left", "L1_Lighting",
                   loc=(15.8, 1.2, 3.4), rot_deg=(0, 0, 270), override_mat="M_RedWarningEmissive")
    spawn_instance("SciFi", "SM_Emergency_Light_Red.fbx", "L1_Terminal_AlarmStrobe_Right", "L1_Lighting",
                   loc=(15.8, 3.8, 3.4), rot_deg=(0, 0, 270), override_mat="M_RedWarningEmissive")

    # Surveillance Camera monitoring the terminal approach
    spawn_instance("SciFi", "SM_SurveillanceCamera.fbx", "L1_Terminal_SecurityCam", "L1_LockedTerminal",
                   loc=(14.5, 4.8, 3.0), rot_deg=(25, 0, -120), override_mat="M_WornMetal")

    # North Wall (Y = +6.0m): Heavy Industrial Machinery & Generator Bank
    spawn_instance("Machinery", "SM_Industrial_Generator.fbx", "L1_Terminal_FusionGenerator", "L1_LockedTerminal",
                   loc=(10.0, 5.2, 0.1), scale=(1, 1, 1), override_mat="M_WornMetal")
    spawn_instance("Machinery", "SM_AC_Unit.fbx", "L1_Terminal_AC_Compressor", "L1_LockedTerminal",
                   loc=(12.8, 5.2, 0.1), override_mat="M_VentilationMetal")
    spawn_instance("Machinery", "SM_Vent_Unit.fbx", "L1_Terminal_VentTurbine", "L1_LockedTerminal",
                   loc=(14.8, 5.2, 0.1), override_mat="M_VentilationMetal")

    # Overhead Conduits & Cable Trays
    for i, x in enumerate([9.0, 11.0, 13.0, 15.0]):
        spawn_instance("Industrial", "SM_Cable_Tray.fbx", f"L1_Terminal_Trays_{i+1}", "L1_Pipes",
                       loc=(x, 5.0, 2.8), rot_deg=(0, 0, 0), override_mat="M_WornMetal")

    # Barricades & Logistics Crates
    spawn_instance("Props", "SM_Barrier_Low.fbx", "L1_Terminal_Barrier", "L1_Props",
                   loc=(9.0, -0.8, 0.1), rot_deg=(0, 0, 0), override_mat="M_IndustrialPaint")
    spawn_instance("Props", "SM_Crate_Large.fbx", "L1_Terminal_Crate_Large", "L1_Props",
                   loc=(11.5, -0.6, 0.1), rot_deg=(0, 0, 15), override_mat="M_IndustrialMetal_Master")
    spawn_instance("Props", "SM_Crate_Small.fbx", "L1_Terminal_Crate_Small", "L1_Props",
                   loc=(12.8, -0.5, 0.1), rot_deg=(0, 0, -25), override_mat="M_IndustrialMetal_Master")

# ---------------------------------------------------------------------------
# Lighting Setup
# ---------------------------------------------------------------------------
def setup_cinematic_lighting():
    lighting_col = COLLECTIONS["L1_Lighting"]

    # 1. World Background (Deep Cyberpunk Midnight)
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("L1_Cyberpunk_World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg_node = world.node_tree.nodes.get("Background")
    if bg_node:
        bg_node.inputs['Color'].default_value = (0.012, 0.016, 0.024, 1.0)
        bg_node.inputs['Strength'].default_value = 0.4

    # 2. Zone 1: Cyan Key & Warm Bulkhead Lamp
    l_z1_data = bpy.data.lights.new("Light_Zone1_CyanKey", type='POINT')
    l_z1_data.energy = 2200.0
    l_z1_data.color = (0.0, 0.85, 1.0)
    l_z1 = bpy.data.objects.new("Light_Zone1_CyanKey", l_z1_data)
    l_z1.location = (-13.0, -1.0, 2.6)
    lighting_col.objects.link(l_z1)

    l_z1_warm_data = bpy.data.lights.new("Light_Zone1_WarmAirlock", type='POINT')
    l_z1_warm_data.energy = 800.0
    l_z1_warm_data.color = (1.0, 0.65, 0.3)
    l_z1_warm = bpy.data.objects.new("Light_Zone1_WarmAirlock", l_z1_warm_data)
    l_z1_warm.location = (-15.5, -1.0, 2.4)
    lighting_col.objects.link(l_z1_warm)

    # 3. Zone 2: Main Corridor Purple Atmosphere Fill Lights
    for i, x in enumerate([-8.0, -4.0, 0.0]):
        l_cor_data = bpy.data.lights.new(f"Light_Zone2_Purple_{i+1}", type='POINT')
        l_cor_data.energy = 1600.0
        l_cor_data.color = (0.85, 0.08, 0.95)
        l_cor = bpy.data.objects.new(f"Light_Zone2_Purple_{i+1}", l_cor_data)
        l_cor.location = (x, 0.0, 2.5)
        lighting_col.objects.link(l_cor)

    # 4. Zone 3: Observation Room City Sky Rim & Desk Cyan Task Light
    l_obs_sky_data = bpy.data.lights.new("Light_Zone3_CityWindowRim", type='AREA')
    l_obs_sky_data.energy = 3500.0
    l_obs_sky_data.size = 6.0
    l_obs_sky_data.color = (0.75, 0.2, 1.0)
    l_obs_sky = bpy.data.objects.new("Light_Zone3_CityWindowRim", l_obs_sky_data)
    l_obs_sky.location = (2.0, 8.5, 2.5)
    l_obs_sky.rotation_euler = (math.radians(-90), 0, 0)
    lighting_col.objects.link(l_obs_sky)

    l_obs_desk_data = bpy.data.lights.new("Light_Zone3_DeskCyan", type='POINT')
    l_obs_desk_data.energy = 700.0
    l_obs_desk_data.color = (0.0, 0.9, 1.0)
    l_obs_desk = bpy.data.objects.new("Light_Zone3_DeskCyan", l_obs_desk_data)
    l_obs_desk.location = (2.0, 6.6, 1.4)
    lighting_col.objects.link(l_obs_desk)

    # 5. Zone 4: Vertical Lift Deep Purple Shaft Light
    l_lift_data = bpy.data.lights.new("Light_Zone4_ShaftPurple", type='SPOT')
    l_lift_data.energy = 5000.0
    l_lift_data.spot_size = math.radians(65)
    l_lift_data.color = (0.9, 0.05, 0.95)
    l_lift = bpy.data.objects.new("Light_Zone4_ShaftPurple", l_lift_data)
    l_lift.location = (4.0, -4.0, 2.0)
    l_lift.rotation_euler = (math.radians(180), 0, 0)
    lighting_col.objects.link(l_lift)

    # 6. Zone 5: Locked Terminal Red Warning Lights & Cyan Console Light
    l_term_red_data = bpy.data.lights.new("Light_Zone5_RedAlarm", type='POINT')
    l_term_red_data.energy = 3500.0
    l_term_red_data.color = (1.0, 0.02, 0.02)
    l_term_red = bpy.data.objects.new("Light_Zone5_RedAlarm", l_term_red_data)
    l_term_red.location = (15.5, 2.5, 3.2)
    lighting_col.objects.link(l_term_red)

    l_term_cyan_data = bpy.data.lights.new("Light_Zone5_TerminalCyan", type='POINT')
    l_term_cyan_data.energy = 1500.0
    l_term_cyan_data.color = (0.0, 0.95, 1.0)
    l_term_cyan = bpy.data.objects.new("Light_Zone5_TerminalCyan", l_term_cyan_data)
    l_term_cyan.location = (14.8, 1.0, 1.5)
    lighting_col.objects.link(l_term_cyan)

# ---------------------------------------------------------------------------
# Cameras System (8 Dedicated Views)
# ---------------------------------------------------------------------------
def setup_cameras():
    cam_col = COLLECTIONS["L1_Cameras"]

    cam_specs = [
        # 1. CAM_L1_Isometric: Elevated three-quarter complete building view framing full 32m layout
        {
            "name": "CAM_L1_Isometric",
            "type": 'PERSP',
            "lens": 24,
            "loc": (0.0, -26.0, 22.0),
            "rot": (54, 0, 0),
            "is_default": True
        },
        # 2. CAM_L1_Top: Orthographic true plan view of all 5 zones
        {
            "name": "CAM_L1_Top",
            "type": 'ORTHO',
            "ortho_scale": 40.0,
            "loc": (0.0, 1.5, 35.0),
            "rot": (0, 0, 0),
            "is_default": False
        },
        # 3. CAM_L1_Side: Orthographic side elevation showing route and lift depth
        {
            "name": "CAM_L1_Side",
            "type": 'ORTHO',
            "ortho_scale": 40.0,
            "loc": (0.0, -30.0, 0.0),
            "rot": (90, 0, 0),
            "is_default": False
        },
        # 4. CAM_L1_Start: Zone 1 Start Area & entry door
        {
            "name": "CAM_L1_Start",
            "type": 'PERSP',
            "lens": 24,
            "loc": (-10.5, -1.0, 1.8),
            "rot": (85, 0, -90),
            "is_default": False
        },
        # 5. CAM_L1_Corridor: Zone 2 Main Corridor looking east
        {
            "name": "CAM_L1_Corridor",
            "type": 'PERSP',
            "lens": 26,
            "loc": (-9.0, 0.0, 1.6),
            "rot": (88, 0, 90),
            "is_default": False
        },
        # 6. CAM_L1_Observation: Zone 3 Observation Room facing window & desk
        {
            "name": "CAM_L1_Observation",
            "type": 'PERSP',
            "lens": 24,
            "loc": (2.0, 3.2, 1.6),
            "rot": (86, 0, 0),
            "is_default": False
        },
        # 7. CAM_L1_Lift: Zone 4 Vertical Lift looking down into the shaft
        {
            "name": "CAM_L1_Lift",
            "type": 'PERSP',
            "lens": 24,
            "loc": (4.0, -1.2, 2.2),
            "rot": (60, 0, 180),
            "is_default": False
        },
        # 8. CAM_L1_Terminal: Zone 5 Locked Terminal framed on large gate
        {
            "name": "CAM_L1_Terminal",
            "type": 'PERSP',
            "lens": 26,
            "loc": (10.0, 2.0, 1.7),
            "rot": (88, 0, 90),
            "is_default": False
        }
    ]

    for spec in cam_specs:
        cdata = bpy.data.cameras.new(spec["name"])
        cdata.type = spec["type"]
        if spec["type"] == 'PERSP':
            cdata.lens = spec["lens"]
        else:
            cdata.ortho_scale = spec["ortho_scale"]

        cobj = bpy.data.objects.new(spec["name"], cdata)
        cobj.location = spec["loc"]
        cobj.rotation_euler = Euler((math.radians(spec["rot"][0]),
                                     math.radians(spec["rot"][1]),
                                     math.radians(spec["rot"][2])), 'XYZ')
        cam_col.objects.link(cobj)

        if spec["is_default"]:
            bpy.context.scene.camera = cobj

# ---------------------------------------------------------------------------
# Rendering & Export Execution
# ---------------------------------------------------------------------------
def render_presentation_views():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_WORKBENCH'
    scene.display.shading.color_type = 'TEXTURE'
    scene.display.shading.light = 'MATCAP'
    scene.display.render_aa = 'FXAA'

    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'

    render_tasks = [
        ("CAM_L1_Isometric", RENDER_ISO),
        ("CAM_L1_Top", RENDER_TOP),
        ("CAM_L1_Side", RENDER_SIDE)
    ]

    for cam_name, out_path in render_tasks:
        cam_obj = bpy.data.objects.get(cam_name)
        if cam_obj:
            scene.camera = cam_obj
            scene.render.filepath = out_path
            print(f"Rendering {cam_name} to {out_path}...")
            try:
                bpy.ops.render.render(write_still=True)
                print(f"Finished: {out_path}")
            except Exception as re:
                print(f"Render warning for {cam_name}: {re}")

# ---------------------------------------------------------------------------
# Master Execution Flow
# ---------------------------------------------------------------------------
def run_assembly():
    print("=== STARTING SECTOR 09 LEVEL 1 3D ENVIRONMENT ASSEMBLY ===")
    reset_scene()
    setup_collections()
    build_material_library()

    print("Building Zone 1: Start Area...")
    assemble_zone1_start_area()

    print("Building Zone 2: Main Corridor...")
    assemble_zone2_main_corridor()

    print("Building Zone 3: Observation Room...")
    assemble_zone3_observation_room()

    print("Building Zone 4: Vertical Lift...")
    assemble_zone4_vertical_lift()

    print("Building Zone 5: Locked Terminal...")
    assemble_zone5_locked_terminal()

    print("Configuring Cinematic Cyberpunk Lighting...")
    setup_cinematic_lighting()

    print("Configuring 8 Presentation Cameras...")
    setup_cameras()

    print(f"Saving final Blender scene: {BLEND_OUTPUT}...")
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUTPUT)

    print(f"Saving secondary backup: {BLEND_BACKUP}...")
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_BACKUP)

    print("Rendering isometric, top-down, and side-elevation presentation views...")
    render_presentation_views()

    print("=== SECTOR 09 LEVEL 1 ASSEMBLY COMPLETE ===")

if __name__ == "__main__":
    run_assembly()
