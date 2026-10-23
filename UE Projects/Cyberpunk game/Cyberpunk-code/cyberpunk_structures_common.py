"""
Shared Procedural Material Library, Modeling Primitives, and Unreal Engine FBX Exporter
for Cyberpunk Industrial Superstructure Props in Blender 4.x / 5.x.

Designed specifically for Unreal Engine 5 import readiness:
- Correct scale (1 unit = 1 meter, exported with FBX 100x scale for Unreal 1 unit = 1 cm)
- Base pivot point at (0, 0, 0)
- Clean, distinct Material Slots
- Standard coordinate axes (+X Forward, +Z Up)
"""

import os
import math
import bpy
import bmesh
from mathutils import Vector, Euler, Matrix


def _set_bsdf_input(bsdf, socket_name, value):
    """Safe setter for Principled BSDF across Blender socket naming variations."""
    if socket_name in bsdf.inputs:
        bsdf.inputs[socket_name].default_value = value
    elif socket_name == 'Specular' and 'Specular IOR Level' in bsdf.inputs:
        bsdf.inputs['Specular IOR Level'].default_value = value
    elif socket_name == 'Emission' and 'Emission Color' in bsdf.inputs:
        bsdf.inputs['Emission Color'].default_value = value
    elif socket_name == 'Roughness' and 'Roughness' in bsdf.inputs:
        bsdf.inputs['Roughness'].default_value = value
    elif socket_name == 'Metallic' and 'Metallic' in bsdf.inputs:
        bsdf.inputs['Metallic'].default_value = value


def get_or_create_material(mat_name, builder_func):
    """Retrieve existing material or construct a fresh procedural shader graph."""
    existing = bpy.data.materials.get(mat_name)
    if existing:
        return existing

    mat = bpy.data.materials.new(name=mat_name)
    try:
        mat.use_nodes = True
    except Exception:
        pass

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    out_node = nodes.new('ShaderNodeOutputMaterial')
    out_node.location = (600, 0)

    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    bsdf.location = (200, 0)
    links.new(bsdf.outputs['BSDF'], out_node.inputs['Surface'])

    builder_func(mat, nodes, links, bsdf)
    return mat


# ---------------------------------------------------------------------------
# Procedural Shader Builders Matching Reference Image Aesthetics
# ---------------------------------------------------------------------------

def _build_steel_purple_mat(mat, nodes, links, bsdf):
    """
    Primary cyberpunk weathered structural metal.
    Slate-blue/purple tinted steel panels with edge grunge and subtle grime.
    """
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)

    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-700, 100)
    noise.inputs['Scale'].default_value = 24.0
    noise.inputs['Detail'].default_value = 6.0
    noise.inputs['Roughness'].default_value = 0.75
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])

    # Slate/Purple-grey metal tones matching the reference lighting & metal
    ramp_color = nodes.new('ShaderNodeValToRGB')
    ramp_color.location = (-400, 100)
    ramp_color.color_ramp.elements[0].position = 0.20
    ramp_color.color_ramp.elements[0].color = (0.28, 0.29, 0.38, 1.0)  # Slate purple-blue steel
    ramp_color.color_ramp.elements[1].position = 0.80
    ramp_color.color_ramp.elements[1].color = (0.42, 0.44, 0.54, 1.0)  # Lighter lavender-steel panel
    links.new(noise.outputs['Fac'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf.inputs['Base Color'])

    _set_bsdf_input(bsdf, 'Metallic', 0.82)
    _set_bsdf_input(bsdf, 'Roughness', 0.45)
    _set_bsdf_input(bsdf, 'Specular', 0.55)

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-100, -150)
    bump.inputs['Strength'].default_value = 0.025
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])


def _build_steel_dark_mat(mat, nodes, links, bsdf):
    """Dark charcoal structural steel for brackets, joints, bolts, and inner framing."""
    _set_bsdf_input(bsdf, 'Base Color', (0.10, 0.11, 0.14, 1.0))
    _set_bsdf_input(bsdf, 'Metallic', 0.90)
    _set_bsdf_input(bsdf, 'Roughness', 0.38)
    _set_bsdf_input(bsdf, 'Specular', 0.6)


def _build_concrete_foundation_mat(mat, nodes, links, bsdf):
    """Heavy concrete foundation block for lattice tower pedestal."""
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-550, 0)
    noise.inputs['Scale'].default_value = 30.0
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.85
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])

    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-300, 100)
    ramp.color_ramp.elements[0].position = 0.25
    ramp.color_ramp.elements[0].color = (0.35, 0.36, 0.42, 1.0)  # Bluish concrete
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.55, 0.56, 0.60, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-100, -100)
    bump.inputs['Strength'].default_value = 0.10
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    _set_bsdf_input(bsdf, 'Metallic', 0.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.92)


def _build_emissive_cyan_mat(mat, nodes, links, bsdf):
    """High-intensity neon cyan LED light bar and telecom indicator panel."""
    color = (0.05, 0.75, 1.0, 1.0)
    _set_bsdf_input(bsdf, 'Base Color', color)
    _set_bsdf_input(bsdf, 'Emission Color', color)
    _set_bsdf_input(bsdf, 'Emission Strength', 30.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.1)


def _build_emissive_orange_mat(mat, nodes, links, bsdf):
    """High-intensity neon amber / orange LED strip and status block."""
    color = (1.0, 0.45, 0.02, 1.0)
    _set_bsdf_input(bsdf, 'Base Color', color)
    _set_bsdf_input(bsdf, 'Emission Color', color)
    _set_bsdf_input(bsdf, 'Emission Strength', 30.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.1)


def _build_emissive_purple_mat(mat, nodes, links, bsdf):
    """High-intensity neon violet / magenta-white strip light."""
    color = (0.85, 0.70, 1.0, 1.0)
    _set_bsdf_input(bsdf, 'Base Color', color)
    _set_bsdf_input(bsdf, 'Emission Color', color)
    _set_bsdf_input(bsdf, 'Emission Strength', 25.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.1)


def _build_emissive_red_mat(mat, nodes, links, bsdf):
    """Beacon warning light."""
    color = (1.0, 0.03, 0.03, 1.0)
    _set_bsdf_input(bsdf, 'Base Color', color)
    _set_bsdf_input(bsdf, 'Emission Color', color)
    _set_bsdf_input(bsdf, 'Emission Strength', 25.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.1)


def _build_cable_rubber_mat(mat, nodes, links, bsdf):
    """Matte dark rubber / flex conduit for heavy industrial cable harnesses."""
    _set_bsdf_input(bsdf, 'Base Color', (0.05, 0.05, 0.06, 1.0))
    _set_bsdf_input(bsdf, 'Metallic', 0.05)
    _set_bsdf_input(bsdf, 'Roughness', 0.70)
    _set_bsdf_input(bsdf, 'Specular', 0.3)


def get_materials():
    """Retrieve dictionary of all required procedural materials."""
    return {
        'steel_main': get_or_create_material('M_Cyberpunk_Steel_Main', _build_steel_purple_mat),
        'steel_dark': get_or_create_material('M_Cyberpunk_Steel_Dark', _build_steel_dark_mat),
        'concrete': get_or_create_material('M_Cyberpunk_Concrete', _build_concrete_foundation_mat),
        'cyan_glow': get_or_create_material('M_Emissive_Cyan', _build_emissive_cyan_mat),
        'orange_glow': get_or_create_material('M_Emissive_Orange', _build_emissive_orange_mat),
        'purple_glow': get_or_create_material('M_Emissive_Purple', _build_emissive_purple_mat),
        'red_glow': get_or_create_material('M_Emissive_Red', _build_emissive_red_mat),
        'cable': get_or_create_material('M_Cable_Rubber', _build_cable_rubber_mat),
    }


# ---------------------------------------------------------------------------
# Procedural Modeling Utilities
# ---------------------------------------------------------------------------

def create_root_empty(name, location=(0, 0, 0)):
    """Create a root empty display node for organizing asset hierarchies."""
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.empty_display_size = 0.5
    empty.location = location
    bpy.context.collection.objects.link(empty)
    return empty


def create_cube(name, size, location=(0, 0, 0), rotation=(0, 0, 0), material=None, parent=None):
    """Create a scaled cube primitive with transforms applied."""
    bpy.ops.mesh.primitive_cube_add(size=1.0, location=location, rotation=rotation)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (size[0], size[1], size[2])
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def create_cylinder(name, radius, depth, location=(0, 0, 0), rotation=(0, 0, 0), vertices=24, material=None, parent=None):
    """Create a cylinder primitive with specified dimensions and orientation."""
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=vertices,
        radius=radius,
        depth=depth,
        location=location,
        rotation=rotation
    )
    obj = bpy.context.active_object
    obj.name = name
    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def add_bevel_modifier(obj, width=0.015, segments=2):
    """Add a non-destructive bevel modifier to soften industrial hard edges."""
    if obj and obj.type == 'MESH':
        mod = obj.modifiers.new(name="Bevel", type='BEVEL')
        mod.width = width
        mod.segments = segments
        mod.limit_method = 'ANGLE'
        mod.angle_limit = math.radians(35.0)


def create_catenary_cable(name, p1, p2, sag=0.3, radius=0.03, resolution=16, material=None, parent=None):
    """
    Create a drooping bezier curve representing hanging power/data cables,
    converted to a clean 3D mesh with material applied.
    """
    curve_data = bpy.data.curves.new(name=f"{name}_Curve", type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.bevel_depth = radius
    curve_data.bevel_resolution = 4
    curve_data.fill_mode = 'FULL'

    spline = curve_data.splines.new(type='BEZIER')
    spline.bezier_points.add(2)  # Total 3 points: start, droop-midpoint, end

    pt0 = spline.bezier_points[0]
    pt1 = spline.bezier_points[1]
    pt2 = spline.bezier_points[2]

    v1 = Vector(p1)
    v2 = Vector(p2)
    v_mid = (v1 + v2) * 0.5
    v_mid.z -= sag

    # Point 0: Start
    pt0.co = v1
    pt0.handle_left_type = 'AUTO'
    pt0.handle_right_type = 'AUTO'

    # Point 1: Mid drooping point
    pt1.co = v_mid
    pt1.handle_left_type = 'AUTO'
    pt1.handle_right_type = 'AUTO'

    # Point 2: End
    pt2.co = v2
    pt2.handle_left_type = 'AUTO'
    pt2.handle_right_type = 'AUTO'

    curve_obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(curve_obj)

    # Convert curve to mesh for consistent FBX export and material assignment
    bpy.context.view_layer.objects.active = curve_obj
    curve_obj.select_set(True)
    bpy.ops.object.convert(target='MESH')
    mesh_obj = bpy.context.active_object

    if material:
        mesh_obj.data.materials.append(material)
    if parent:
        mesh_obj.parent = parent

    return mesh_obj


def create_angled_beam(name, p1, p2, size_xy=(0.08, 0.08), material=None, parent=None):
    """
    Create a straight structural beam spanning between two 3D points p1 and p2.
    """
    v1 = Vector(p1)
    v2 = Vector(p2)
    direction = v2 - v1
    length = direction.length
    if length < 1e-5:
        return None

    mid = (v1 + v2) * 0.5
    rot_quat = direction.to_track_quat('Z', 'Y')

    beam = create_cube(
        name,
        size=(size_xy[0], size_xy[1], length),
        location=mid,
        rotation=rot_quat.to_euler(),
        material=material,
        parent=parent
    )
    return beam


# ---------------------------------------------------------------------------
# Unreal Engine 5 FBX Exporter Helper
# ---------------------------------------------------------------------------

def export_prop_to_fbx(root_obj, fbx_filepath):
    """
    Exports a prop hierarchy to an FBX file optimized for Unreal Engine 5:
    - 1 unit = 100cm scale
    - Pivot centered at base
    - Standard axis conventions (-Z Forward, Y Up)
    - Materials and mesh data preserved
    """
    os.makedirs(os.path.dirname(os.path.abspath(fbx_filepath)), exist_ok=True)

    # Deselect all
    bpy.ops.object.select_all(action='DESELECT')

    # Select root and all children
    root_obj.select_set(True)
    for child in root_obj.children_recursive:
        child.select_set(True)

    bpy.context.view_layer.objects.active = root_obj

    try:
        bpy.ops.export_scene.fbx(
            filepath=fbx_filepath,
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
        print(f"[Unreal Export] Saved FBX: {fbx_filepath}")
        return True
    except Exception as e:
        print(f"[Unreal Export] Failed to export FBX: {e}")
        return False
