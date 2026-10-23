import unreal

print("=== CHECKING UNREAL 5.6 PYTHON APIS ===")
asset_tools = unreal.AssetToolsHelpers.get_asset_tools()
print("AssetTools:", asset_tools)
bp_factory = unreal.BlueprintFactory()
print("BlueprintFactory:", bp_factory)
mat_factory = unreal.MaterialFactoryNew()
print("MaterialFactoryNew:", mat_factory)
mi_factory = unreal.MaterialInstanceConstantFactoryNew()
print("MaterialInstanceConstantFactoryNew:", mi_factory)
editor_asset_lib = unreal.EditorAssetLibrary
print("EditorAssetLibrary:", editor_asset_lib)
print("=== APIS VERIFIED OK ===")
