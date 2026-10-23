"""
Organizes and distributes all 66+ Sector 09 static meshes and 2K PBR textures into the exact
folder structure specified in Section 2:
Assets/
├── Meshes/
│   ├── Architecture/
│   ├── Floors/
│   ├── Doors/
│   ├── Industrial/
│   ├── Pipes/
│   ├── Railings/
│   ├── Machinery/
│   ├── Props/
│   └── SciFi/
└── Textures/
    ├── BaseColor/
    ├── Normal/
    ├── Roughness/
    ├── Metallic/
    ├── Emissive/
    ├── Masks/
    └── Decals/
"""

import os
import shutil
import glob

REPO_ROOT = r"d:\unreal engine"
SRC_MESH_DIR = os.path.join(REPO_ROOT, "Assets", "Level_1")
SRC_TEX_DIR = os.path.join(REPO_ROOT, "Assets", "Level_1", "Textures")
TARGET_ASSETS = os.path.join(REPO_ROOT, "Assets")

# Mesh mapping
MESH_MAPPING = {
    # Architecture
    "SM_01_Wall_Panel_A.fbx": ("Architecture", "SM_WallPanel_A.fbx"),
    "SM_01_Wall_Panel_B_Pipes.fbx": ("Architecture", "SM_WallPanel_B_Pipes.fbx"),
    "SM_01_Wall_Panel_C_Vent.fbx": ("Architecture", "SM_WallPanel_C_Vent.fbx"),
    "SM_01_Corner_Wall.fbx": ("Architecture", "SM_Corner_Wall.fbx"),
    "SM_01_Window_Panel.fbx": ("Architecture", "SM_Window_Panel.fbx"),
    "SM_03_Horizontal_Beam.fbx": ("Architecture", "SM_Support_Beam.fbx"),
    "SM_03_Large_Vertical_Panel.fbx": ("Architecture", "SM_Lift_Shaft_Wall.fbx"),
    "SM_CeilingPanel.fbx": ("Architecture", "SM_CeilingPanel.fbx"),
    "SM_CityView_WindowFrame.fbx": ("Architecture", "SM_CityView_WindowFrame.fbx"),
    "SM_Window_Glass.fbx": ("Architecture", "SM_Window_Glass.fbx"),

    # Floors
    "SM_02_Floor_Tile_A.fbx": ("Floors", "SM_FloorTile_A.fbx"),
    "SM_02_Floor_Tile_B_Grate.fbx": ("Floors", "SM_FloorTile_B_Grate.fbx"),
    "SM_02_Floor_Tile_C.fbx": ("Floors", "SM_FloorTile_C.fbx"),
    "SM_02_Floor_Tile_D_Corner.fbx": ("Floors", "SM_FloorTile_D_Corner.fbx"),
    "SM_02_Floor_Tile_E_Ramp.fbx": ("Floors", "SM_Floor_Ramp.fbx"),
    "SM_02_Platform_Module.fbx": ("Floors", "SM_Platform_Module.fbx"),
    "SM_02_Stair_Module.fbx": ("Floors", "SM_Stair_Module.fbx"),
    "SM_Floor_Edge_Module.fbx": ("Floors", "SM_Floor_Edge_Module.fbx"),
    "SM_Lift_Landing.fbx": ("Floors", "SM_Lift_Landing.fbx"),

    # Doors
    "SM_01_Industrial_Door.fbx": ("Doors", "SM_Industrial_Door.fbx"),
    "SM_01_Door_Frame.fbx": ("Doors", "SM_Door_Frame.fbx"),
    "SM_01_Large_Gate.fbx": ("Doors", "SM_Large_Gate.fbx"),

    # Industrial
    "SM_03_Cable_Tray.fbx": ("Industrial", "SM_Cable_Tray.fbx"),
    "SM_05_Electrical_Box.fbx": ("Industrial", "SM_Electrical_Box.fbx"),
    "SM_05_Access_Panel.fbx": ("Industrial", "SM_Access_Panel.fbx"),
    "SM_06_Duct_Cover.fbx": ("Industrial", "SM_Duct_Cover.fbx"),

    # Pipes
    "SM_03_Pipe_Straight.fbx": ("Pipes", "SM_Pipe_Straight.fbx"),
    "SM_03_Pipe_Elbow.fbx": ("Pipes", "SM_Pipe_Elbow.fbx"),
    "SM_03_Pipe_Junction_T.fbx": ("Pipes", "SM_Pipe_Junction_T.fbx"),
    "SM_03_Pipe_Set_Wall.fbx": ("Pipes", "SM_Pipe_Set_Wall.fbx"),

    # Railings
    "SM_02_Railing_Straight.fbx": ("Railings", "SM_Railing_Straight.fbx"),
    "SM_02_Railing_Corner.fbx": ("Railings", "SM_Railing_Corner.fbx"),

    # Machinery
    "SM_05_AC_Unit_Generator.fbx": ("Machinery", "SM_AC_Unit.fbx"),
    "SM_05_Vent_Unit.fbx": ("Machinery", "SM_Vent_Unit.fbx"),
    "SM_03_Lift_Platform.fbx": ("Machinery", "SM_LiftPlatform.fbx"),
    "SM_03_Elevator_Shaft_Module.fbx": ("Machinery", "SM_Elevator_Shaft_Module.fbx"),
    "SM_Industrial_Generator.fbx": ("Machinery", "SM_Industrial_Generator.fbx"),

    # Props
    "SM_04_Crate_Small.fbx": ("Props", "SM_Crate_Small.fbx"),
    "SM_04_Crate_Medium.fbx": ("Props", "SM_Crate_Medium.fbx"),
    "SM_04_Crate_Large.fbx": ("Props", "SM_Crate_Large.fbx"),
    "SM_04_Stacked_Crates.fbx": ("Props", "SM_Stacked_Crates.fbx"),
    "SM_04_Barrel.fbx": ("Props", "SM_Barrel.fbx"),
    "SM_04_Barrier_Low.fbx": ("Props", "SM_Barrier_Low.fbx"),
    "SM_04_Barrier_Tall.fbx": ("Props", "SM_Barrier_Tall.fbx"),
    "SM_04_Construction_Barrier.fbx": ("Props", "SM_Construction_Barrier.fbx"),
    "SM_04_Pallet.fbx": ("Props", "SM_Pallet.fbx"),
    "SM_06_Trash_Bin_A.fbx": ("Props", "SM_Trash_Bin_A.fbx"),
    "SM_06_Trash_Bin_B.fbx": ("Props", "SM_Trash_Bin_B.fbx"),
    "SM_06_Computer_Desk.fbx": ("Props", "SM_Computer_Desk.fbx"),
    "SM_06_Chair.fbx": ("Props", "SM_Chair.fbx"),

    # SciFi & Technology & Lighting
    "SM_05_Security_Camera.fbx": ("SciFi", "SM_SurveillanceCamera.fbx"),
    "SM_05_Server_Rack.fbx": ("SciFi", "SM_Server_Rack.fbx"),
    "SM_05_Control_Terminal.fbx": ("SciFi", "SM_ControlTerminal.fbx"),
    "SM_05_Info_Terminal_Glitch.fbx": ("SciFi", "SM_Info_Terminal_Glitch.fbx"),
    "SM_06_Monitor_Screen.fbx": ("SciFi", "SM_Monitor_Screen.fbx"),
    "SM_05_Hanging_Light.fbx": ("SciFi", "SM_Hanging_Light.fbx"),
    "SM_06_Ceiling_Light.fbx": ("SciFi", "SM_Ceiling_Light.fbx"),
    "SM_06_Wall_Light_Warm.fbx": ("SciFi", "SM_Wall_Light_Warm.fbx"),
    "SM_06_Neon_Light_Cyan.fbx": ("SciFi", "SM_Neon_Light_Cyan.fbx"),
    "SM_06_Neon_Light_Purple.fbx": ("SciFi", "SM_Neon_Light_Purple.fbx"),
    "SM_06_Emergency_Light_Red.fbx": ("SciFi", "SM_Emergency_Light_Red.fbx"),
    "SM_06_Street_Light_Indoor.fbx": ("SciFi", "SM_Street_Light_Indoor.fbx"),
    "SM_LiftControlPanel.fbx": ("SciFi", "SM_LiftControlPanel.fbx"),
    "SM_Shaft_Lighting_Assembly.fbx": ("SciFi", "SM_Shaft_Lighting_Assembly.fbx"),
    "SM_Computer_Workstation.fbx": ("SciFi", "SM_Computer_Workstation.fbx"),
    "SM_Server_Equipment.fbx": ("SciFi", "SM_Server_Equipment.fbx")
}

def distribute_meshes():
    count = 0
    for src_name, (category, target_name) in MESH_MAPPING.items():
        src_path = os.path.join(SRC_MESH_DIR, src_name)
        if os.path.exists(src_path):
            dst_dir = os.path.join(TARGET_ASSETS, "Meshes", category)
            os.makedirs(dst_dir, exist_ok=True)
            dst_path = os.path.join(dst_dir, target_name)
            shutil.copy2(src_path, dst_path)
            count += 1
        else:
            print(f"Warning: source mesh {src_name} not found!")
    print(f"Distributed {count} static meshes into Assets/Meshes/ categories.")

def distribute_textures():
    count = 0
    for f in glob.glob(os.path.join(SRC_TEX_DIR, "*.png")):
        filename = os.path.basename(f)
        subfolder = None
        if "BaseColor" in filename:
            subfolder = "BaseColor"
        elif "Normal" in filename:
            subfolder = "Normal"
        elif "Roughness" in filename:
            subfolder = "Roughness"
        elif "Metallic" in filename:
            subfolder = "Metallic"
        elif "Emissive" in filename:
            subfolder = "Emissive"
        elif "Mask" in filename:
            subfolder = "Masks"
        elif "Decal" in filename:
            subfolder = "Decals"
        
        if subfolder:
            dst_dir = os.path.join(TARGET_ASSETS, "Textures", subfolder)
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy2(f, os.path.join(dst_dir, filename))
            count += 1
    print(f"Distributed {count} textures into Assets/Textures/ categories.")

if __name__ == "__main__":
    distribute_meshes()
    distribute_textures()
