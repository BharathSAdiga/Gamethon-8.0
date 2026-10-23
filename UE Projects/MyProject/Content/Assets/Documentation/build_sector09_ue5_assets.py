"""
Automated Unreal Engine 5.6 Asset Importer, Material Generator, and Blueprint Creator for Sector 09.
Can be executed within Unreal Editor (Python Console) or headless via UnrealEditor-Cmd.exe.
"""

import os
import glob
import unreal

def get_repo_paths():
    proj_dir = unreal.Paths.project_dir() # e.g. .../UE Projects/MyProject/
    content_dir = unreal.Paths.project_content_dir()
    assets_dir = os.path.join(content_dir, "Assets")
    return proj_dir, content_dir, assets_dir

def import_textures():
    _, _, assets_dir = get_repo_paths()
    tex_root = os.path.join(assets_dir, "Textures")
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    categories = ["BaseColor", "Normal", "Roughness", "Metallic", "Emissive", "Masks", "Decals"]
    imported = 0
    
    for cat in categories:
        src_cat_dir = os.path.join(tex_root, cat)
        if not os.path.exists(src_cat_dir):
            continue
            
        dest_pkg = f"/Game/Assets/Textures/{cat}"
        files = glob.glob(os.path.join(src_cat_dir, "*.png"))
        
        for f in files:
            asset_name = os.path.splitext(os.path.basename(f))[0]
            if unreal.EditorAssetLibrary.does_asset_exist(f"{dest_pkg}/{asset_name}"):
                continue
                
            task = unreal.AssetImportTask()
            task.filename = f
            task.destination_path = dest_pkg
            task.destination_name = asset_name
            task.replace_existing = True
            task.automated = True
            task.save = True
            
            asset_tools.import_asset_tasks([task])
            imported += 1
            
    unreal.log(f"Imported {imported} textures into /Game/Assets/Textures/.")

def import_meshes():
    _, _, assets_dir = get_repo_paths()
    mesh_root = os.path.join(assets_dir, "Meshes")
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    
    categories = ["Architecture", "Floors", "Doors", "Industrial", "Pipes", "Railings", "Machinery", "Props", "SciFi"]
    imported = 0
    
    fbx_options = unreal.FbxImportUI()
    fbx_options.import_mesh = True
    fbx_options.import_textures = False
    fbx_options.import_materials = False
    fbx_options.import_as_skeletal = False
    fbx_options.static_mesh_import_data.combine_meshes = True
    fbx_options.static_mesh_import_data.generate_lightmap_u_vs = True
    fbx_options.static_mesh_import_data.auto_generate_collision = True
    
    for cat in categories:
        src_cat_dir = os.path.join(mesh_root, cat)
        if not os.path.exists(src_cat_dir):
            continue
            
        dest_pkg = f"/Game/Assets/Meshes/{cat}"
        files = glob.glob(os.path.join(src_cat_dir, "*.fbx"))
        
        for f in files:
            asset_name = os.path.splitext(os.path.basename(f))[0]
            if unreal.EditorAssetLibrary.does_asset_exist(f"{dest_pkg}/{asset_name}"):
                continue
                
            task = unreal.AssetImportTask()
            task.filename = f
            task.destination_path = dest_pkg
            task.destination_name = asset_name
            task.options = fbx_options
            task.replace_existing = True
            task.automated = True
            task.save = True
            
            asset_tools.import_asset_tasks([task])
            imported += 1
            
    unreal.log(f"Imported {imported} static meshes into /Game/Assets/Meshes/.")

def create_materials():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    mat_factory = unreal.MaterialFactoryNew()
    mi_factory = unreal.MaterialInstanceConstantFactoryNew()
    
    # 1. Master Material
    master_path = "/Game/Assets/Materials/MasterMaterials"
    master_name = "M_IndustrialMetal_Master"
    
    if not unreal.EditorAssetLibrary.does_asset_exist(f"{master_path}/{master_name}"):
        master_mat = asset_tools.create_asset(master_name, master_path, unreal.Material, mat_factory)
        unreal.EditorAssetLibrary.save_loaded_asset(master_mat)
        unreal.log(f"Created Master Material: {master_name}")
    else:
        master_mat = unreal.EditorAssetLibrary.load_asset(f"{master_path}/{master_name}")

    # 2. Material Instances
    instance_specs = [
        ("Metal", "MI_WornMetal"),
        ("Metal", "MI_MetalFloor"),
        ("Metal", "MI_VentilationMetal"),
        ("Concrete", "MI_DarkConcrete"),
        ("Glass", "MI_DarkGlass"),
        ("Glass", "MI_ScreenGlass"),
        ("Emissive", "MI_CyanEmissive"),
        ("Emissive", "MI_PurpleEmissive"),
        ("Emissive", "MI_RedWarningEmissive"),
        ("SpecialEffects", "MI_MetalGrate"),
        ("SpecialEffects", "MI_IndustrialPaint")
    ]
    
    for subfolder, inst_name in instance_specs:
        inst_path = f"/Game/Assets/Materials/{subfolder}"
        if not unreal.EditorAssetLibrary.does_asset_exist(f"{inst_path}/{inst_name}"):
            mi_asset = asset_tools.create_asset(inst_name, inst_path, unreal.MaterialInstanceConstant, mi_factory)
            if mi_asset and master_mat:
                unreal.MaterialEditingLibrary.set_material_instance_parent(mi_asset, master_mat)
            unreal.EditorAssetLibrary.save_loaded_asset(mi_asset)
            unreal.log(f"Created Material Instance: {inst_name}")

def create_blueprints():
    asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
    bp_factory = unreal.BlueprintFactory()
    bp_factory.set_editor_property("parent_class", unreal.Actor)
    
    blueprints = [
        ("Doors", "BP_IndustrialDoor"),
        ("Doors", "BP_LockedGate"),
        ("Interactive", "BP_ControlTerminal"),
        ("Interactive", "BP_InteractablePanel"),
        ("Lift", "BP_LiftPlatform"),
        ("Lighting", "BP_NeonLight"),
        ("Environmental", "BP_SurveillanceCamera")
    ]
    
    created = 0
    for category, bp_name in blueprints:
        dest_path = f"/Game/Assets/Blueprints/{category}"
        if not unreal.EditorAssetLibrary.does_asset_exist(f"{dest_path}/{bp_name}"):
            bp_asset = asset_tools.create_asset(bp_name, dest_path, unreal.Blueprint, bp_factory)
            unreal.EditorAssetLibrary.save_loaded_asset(bp_asset)
            created += 1
            unreal.log(f"Created Native Blueprint: {dest_path}/{bp_name}")
            
    unreal.log(f"Created {created} Native Blueprint assets in /Game/Assets/Blueprints/.")

def run_all():
    unreal.log("=== STARTING SECTOR 09 ASSET SETUP ===")
    import_textures()
    import_meshes()
    create_materials()
    create_blueprints()
    unreal.log("=== SECTOR 09 SETUP COMPLETE ===")

if __name__ == "__main__":
    run_all()
