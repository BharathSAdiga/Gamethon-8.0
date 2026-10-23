"""
Blender script to model and export the additional specialized meshes for Level 1 Sector 09.
All models follow Unreal Engine standards:
- 1 Blender unit = 1 Unreal unit (1 cm)
- Forward: -Y in Blender (transferred to +X in Unreal FBX export)
- UV Unwrapped with clean seams & lightmap friendly margins
- Standard PBR material slots
"""

import os
import sys
import math
import bpy
import bmesh
from mathutils import Vector, Euler

REPO_ROOT = r"d:\unreal engine"
FBX_DIR = os.path.join(REPO_ROOT, "Assets", "Level_1")
os.makedirs(FBX_DIR, exist_ok=True)

def reset_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    if bpy.context.scene.collection.objects:
        for obj in list(bpy.context.scene.collection.objects):
            bpy.data.objects.remove(obj, do_unlink=True)

def apply_transform(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

def unwrap_mesh(obj):
    bpy.context.view_layer.objects.active = obj
    obj.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=66.0, island_margin=0.02)
    bpy.ops.object.mode_set(mode='OBJECT')

def assign_material(obj, mat_name):
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
        mat.use_nodes = True
    if len(obj.data.materials) == 0:
        obj.data.materials.append(mat)
    else:
        obj.data.materials[0] = mat

def export_fbx(obj, filename):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    path = os.path.join(FBX_DIR, filename)
    bpy.ops.export_scene.fbx(
        filepath=path,
        use_selection=True,
        apply_unit_scale=True,
        apply_scale_options='FBX_SCALE_ALL',
        axis_forward='-Z',
        axis_up='Y',
        bake_space_transform=True,
        mesh_smooth_type='FACE'
    )
    print(f"Exported: {filename}")

# 1. SM_CeilingPanel (300 x 300 x 20 cm)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 10))
panel = bpy.context.active_object
panel.scale = (300, 300, 20)
apply_transform(panel)
# Add recessed lighting slots
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 5))
recess = bpy.context.active_object
recess.scale = (220, 180, 12)
apply_transform(recess)
mod = panel.modifiers.new('Recess', 'BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = recess
bpy.context.view_layer.objects.active = panel
bpy.ops.object.modifier_apply(modifier='Recess')
bpy.data.objects.remove(recess, do_unlink=True)
unwrap_mesh(panel)
assign_material(panel, "M_IndustrialMetal_Master")
export_fbx(panel, "SM_CeilingPanel.fbx")

# 2. SM_Floor_Edge_Module (300 x 60 x 30 cm)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 15))
edge = bpy.context.active_object
edge.scale = (300, 60, 30)
apply_transform(edge)
# Add hazard beveled curb lip
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 25, 32))
curb = bpy.context.active_object
curb.scale = (300, 10, 8)
apply_transform(curb)
# Join
bpy.ops.object.select_all(action='DESELECT')
edge.select_set(True)
curb.select_set(True)
bpy.context.view_layer.objects.active = edge
bpy.ops.object.join()
unwrap_mesh(edge)
assign_material(edge, "M_MetalFloor")
export_fbx(edge, "SM_Floor_Edge_Module.fbx")

# 3. SM_CityView_WindowFrame (400 x 30 x 300 cm)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 150))
frame = bpy.context.active_object
frame.scale = (400, 30, 300)
apply_transform(frame)
# Punch out window opening
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 150))
hole = bpy.context.active_object
hole.scale = (360, 40, 260)
apply_transform(hole)
mod = frame.modifiers.new('Hole', 'BOOLEAN')
mod.operation = 'DIFFERENCE'
mod.object = hole
bpy.context.view_layer.objects.active = frame
bpy.ops.object.modifier_apply(modifier='Hole')
bpy.data.objects.remove(hole, do_unlink=True)
# Add center mullion
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 150))
mullion = bpy.context.active_object
mullion.scale = (15, 26, 260)
apply_transform(mullion)
frame.select_set(True)
bpy.context.view_layer.objects.active = frame
bpy.ops.object.join()
unwrap_mesh(frame)
assign_material(frame, "M_IndustrialMetal_Master")
export_fbx(frame, "SM_CityView_WindowFrame.fbx")

# 4. SM_Window_Glass (360 x 5 x 260 cm)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 150))
glass = bpy.context.active_object
glass.scale = (360, 5, 260)
apply_transform(glass)
unwrap_mesh(glass)
assign_material(glass, "M_DarkGlass")
export_fbx(glass, "SM_Window_Glass.fbx")

# 5. SM_Lift_Landing (300 x 300 x 35 cm threshold platform)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 17.5))
landing = bpy.context.active_object
landing.scale = (300, 300, 35)
apply_transform(landing)
# Add interlocking teeth at the threshold
for i in range(-2, 3):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(i * 50, 152, 28))
    tooth = bpy.context.active_object
    tooth.scale = (25, 8, 12)
    apply_transform(tooth)
    landing.select_set(True)
    bpy.context.view_layer.objects.active = landing
    bpy.ops.object.join()
unwrap_mesh(landing)
assign_material(landing, "M_MetalGrate")
export_fbx(landing, "SM_Lift_Landing.fbx")

# 6. SM_LiftControlPanel (40 x 12 x 100 cm)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 120))
panel_box = bpy.context.active_object
panel_box.scale = (40, 12, 100)
apply_transform(panel_box)
# Add angled display bezel
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -6, 140))
screen = bpy.context.active_object
screen.scale = (28, 4, 35)
apply_transform(screen)
# Add lift arrow buttons
bpy.ops.mesh.primitive_cylinder_add(radius=4, depth=3, location=(0, -6, 100))
btn = bpy.context.active_object
btn.rotation_euler = (math.radians(90), 0, 0)
apply_transform(btn)
# Join
for obj in [panel_box, screen, btn]:
    obj.select_set(True)
bpy.context.view_layer.objects.active = panel_box
bpy.ops.object.join()
unwrap_mesh(panel_box)
assign_material(panel_box, "M_IndustrialMetal_Master")
export_fbx(panel_box, "SM_LiftControlPanel.fbx")

# 7. SM_Shaft_Lighting_Assembly (35 x 35 x 280 cm)
reset_scene()
bpy.ops.mesh.primitive_cylinder_add(radius=4, depth=280, location=(0, 0, 140))
pole = bpy.context.active_object
apply_transform(pole)
# Cage rings
for z in [40, 100, 160, 220, 270]:
    bpy.ops.mesh.primitive_torus_add(major_radius=14, minor_radius=1.5, location=(0, 0, z))
    ring = bpy.context.active_object
    apply_transform(ring)
    pole.select_set(True)
    bpy.context.view_layer.objects.active = pole
    bpy.ops.object.join()
unwrap_mesh(pole)
assign_material(pole, "M_IndustrialMetal_Master")
export_fbx(pole, "SM_Shaft_Lighting_Assembly.fbx")

# 8. SM_Computer_Workstation (220 x 110 x 130 cm)
reset_scene()
# Desk surface
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 75))
desk = bpy.context.active_object
desk.scale = (220, 100, 6)
apply_transform(desk)
# Desk legs
for x in [-95, 95]:
    for y in [-40, 40]:
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x, y, 36))
        leg = bpy.context.active_object
        leg.scale = (8, 8, 72)
        apply_transform(leg)
        desk.select_set(True)
        bpy.context.view_layer.objects.active = desk
        bpy.ops.object.join()
# Dual curved monitors
for x_off, rot in [(-45, -15), (45, 15)]:
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(x_off, 10, 110))
    mon = bpy.context.active_object
    mon.scale = (65, 6, 42)
    mon.rotation_euler = (0, 0, math.radians(rot))
    apply_transform(mon)
    desk.select_set(True)
    bpy.context.view_layer.objects.active = desk
    bpy.ops.object.join()
unwrap_mesh(desk)
assign_material(desk, "M_IndustrialMetal_Master")
export_fbx(desk, "SM_Computer_Workstation.fbx")

# 9. SM_Server_Equipment (110 x 90 x 240 cm)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 120))
rack = bpy.context.active_object
rack.scale = (110, 90, 240)
apply_transform(rack)
# Server blades
for z in range(30, 220, 25):
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, -46, z))
    blade = bpy.context.active_object
    blade.scale = (96, 4, 18)
    apply_transform(blade)
    rack.select_set(True)
    bpy.context.view_layer.objects.active = rack
    bpy.ops.object.join()
unwrap_mesh(rack)
assign_material(rack, "M_IndustrialMetal_Master")
export_fbx(rack, "SM_Server_Equipment.fbx")

# 10. SM_Industrial_Generator (240 x 140 x 170 cm)
reset_scene()
bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0, 0, 85))
gen = bpy.context.active_object
gen.scale = (240, 140, 170)
apply_transform(gen)
# Add dual turbine exhaust hoods on top
for x in [-60, 60]:
    bpy.ops.mesh.primitive_cylinder_add(radius=30, depth=40, location=(x, 0, 180))
    turb = bpy.context.active_object
    apply_transform(turb)
    gen.select_set(True)
    bpy.context.view_layer.objects.active = gen
    bpy.ops.object.join()
unwrap_mesh(gen)
assign_material(gen, "M_IndustrialMetal_Master")
export_fbx(gen, "SM_Industrial_Generator.fbx")

print("All missing specialized Level 1 meshes generated and exported to FBX successfully.")
