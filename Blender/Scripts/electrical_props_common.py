"""
Shared Procedural Material Library and Parametric Modeling Helpers
for Industrial Electrical Substation and Pillar Props in Blender 4.x / 5.x.
"""

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
# Procedural Shader Builders
# ---------------------------------------------------------------------------

def _build_yellow_paint_mat(mat, nodes, links, bsdf):
    """Vibrant industrial yellow enamel paint with edge scratches and grunge."""
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)

    # Scratches noise
    noise_scratches = nodes.new('ShaderNodeTexNoise')
    noise_scratches.location = (-700, 100)
    noise_scratches.inputs['Scale'].default_value = 32.0
    noise_scratches.inputs['Detail'].default_value = 8.0
    noise_scratches.inputs['Roughness'].default_value = 0.8
    links.new(tex_coord.outputs['Object'], noise_scratches.inputs['Vector'])

    # Scratch color ramp: 92% vibrant yellow, 8% dark scratched steel
    ramp_color = nodes.new('ShaderNodeValToRGB')
    ramp_color.location = (-400, 100)
    ramp_color.color_ramp.elements[0].position = 0.70
    ramp_color.color_ramp.elements[0].color = (0.98, 0.66, 0.05, 1.0)  # Pure Industrial Yellow
    ramp_color.color_ramp.elements[1].position = 0.78
    ramp_color.color_ramp.elements[1].color = (0.12, 0.12, 0.14, 1.0)  # Dark bare scratched steel
    links.new(noise_scratches.outputs['Fac'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf.inputs['Base Color'])

    # Metallic: paint is 0.08, scratches are 0.85
    ramp_metal = nodes.new('ShaderNodeValToRGB')
    ramp_metal.location = (-400, -100)
    ramp_metal.color_ramp.elements[0].position = 0.70
    ramp_metal.color_ramp.elements[0].color = (0.08, 0.08, 0.08, 1.0)
    ramp_metal.color_ramp.elements[1].position = 0.78
    ramp_metal.color_ramp.elements[1].color = (0.85, 0.85, 0.85, 1.0)
    links.new(noise_scratches.outputs['Fac'], ramp_metal.inputs['Fac'])
    links.new(ramp_metal.outputs['Color'], bsdf.inputs['Metallic'])

    _set_bsdf_input(bsdf, 'Roughness', 0.40)
    _set_bsdf_input(bsdf, 'Specular', 0.5)

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-100, -200)
    bump.inputs['Strength'].default_value = 0.02
    links.new(noise_scratches.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])


def _build_cyan_paint_mat(mat, nodes, links, bsdf):
    """Vibrant industrial cyan/teal enamel paint with subtle edge scratches."""
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-1000, 0)

    noise_scratches = nodes.new('ShaderNodeTexNoise')
    noise_scratches.location = (-700, 100)
    noise_scratches.inputs['Scale'].default_value = 32.0
    noise_scratches.inputs['Detail'].default_value = 8.0
    noise_scratches.inputs['Roughness'].default_value = 0.8
    links.new(tex_coord.outputs['Object'], noise_scratches.inputs['Vector'])

    # Scratch ramp: 92% vibrant cyan, 8% dark scratched steel
    ramp_color = nodes.new('ShaderNodeValToRGB')
    ramp_color.location = (-400, 100)
    ramp_color.color_ramp.elements[0].position = 0.70
    ramp_color.color_ramp.elements[0].color = (0.04, 0.78, 0.90, 1.0)  # Pure Vibrant Cyan / Teal
    ramp_color.color_ramp.elements[1].position = 0.78
    ramp_color.color_ramp.elements[1].color = (0.10, 0.12, 0.14, 1.0)  # Dark bare scratched steel
    links.new(noise_scratches.outputs['Fac'], ramp_color.inputs['Fac'])
    links.new(ramp_color.outputs['Color'], bsdf.inputs['Base Color'])

    ramp_metal = nodes.new('ShaderNodeValToRGB')
    ramp_metal.location = (-400, -100)
    ramp_metal.color_ramp.elements[0].position = 0.70
    ramp_metal.color_ramp.elements[0].color = (0.10, 0.10, 0.10, 1.0)
    ramp_metal.color_ramp.elements[1].position = 0.78
    ramp_metal.color_ramp.elements[1].color = (0.85, 0.85, 0.85, 1.0)
    links.new(noise_scratches.outputs['Fac'], ramp_metal.inputs['Fac'])
    links.new(ramp_metal.outputs['Color'], bsdf.inputs['Metallic'])

    _set_bsdf_input(bsdf, 'Roughness', 0.38)
    _set_bsdf_input(bsdf, 'Specular', 0.55)

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-100, -200)
    bump.inputs['Strength'].default_value = 0.02
    links.new(noise_scratches.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])


def _build_concrete_mat(mat, nodes, links, bsdf):
    """Poured concrete foundation slab with stone aggregate noise."""
    tex_coord = nodes.new('ShaderNodeTexCoord')
    tex_coord.location = (-800, 0)

    noise = nodes.new('ShaderNodeTexNoise')
    noise.location = (-550, 0)
    noise.inputs['Scale'].default_value = 35.0
    noise.inputs['Detail'].default_value = 8.0
    noise.inputs['Roughness'].default_value = 0.85
    links.new(tex_coord.outputs['Object'], noise.inputs['Vector'])

    ramp = nodes.new('ShaderNodeValToRGB')
    ramp.location = (-300, 100)
    ramp.color_ramp.elements[0].position = 0.25
    ramp.color_ramp.elements[0].color = (0.50, 0.46, 0.42, 1.0)
    ramp.color_ramp.elements[1].position = 0.75
    ramp.color_ramp.elements[1].color = (0.68, 0.64, 0.60, 1.0)
    links.new(noise.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], bsdf.inputs['Base Color'])

    bump = nodes.new('ShaderNodeBump')
    bump.location = (-100, -100)
    bump.inputs['Strength'].default_value = 0.12
    bump.inputs['Distance'].default_value = 0.02
    links.new(noise.outputs['Fac'], bump.inputs['Height'])
    links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    _set_bsdf_input(bsdf, 'Metallic', 0.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.88)


def _build_dark_trim_mat(mat, nodes, links, bsdf):
    """Dark charcoal steel for trim gaskets, base borders, and louver slats."""
    _set_bsdf_input(bsdf, 'Base Color', (0.12, 0.13, 0.15, 1.0))
    _set_bsdf_input(bsdf, 'Metallic', 0.85)
    _set_bsdf_input(bsdf, 'Roughness', 0.42)
    _set_bsdf_input(bsdf, 'Specular', 0.6)


def _build_red_led_mat(mat, nodes, links, bsdf):
    """High-intensity glowing crimson red LED indicator diode."""
    color = (1.0, 0.02, 0.02, 1.0)
    _set_bsdf_input(bsdf, 'Base Color', color)
    _set_bsdf_input(bsdf, 'Emission Color', color)
    _set_bsdf_input(bsdf, 'Emission Strength', 35.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.1)


def _build_display_bezel_mat(mat, nodes, links, bsdf):
    """Recessed dark display backing chamber."""
    _set_bsdf_input(bsdf, 'Base Color', (0.04, 0.04, 0.05, 1.0))
    _set_bsdf_input(bsdf, 'Metallic', 0.2)
    _set_bsdf_input(bsdf, 'Roughness', 0.6)


def _build_black_decal_mat(mat, nodes, links, bsdf):
    """Matte black stencil graphic print for SYSTEM, CAUTION, and hazard borders."""
    _set_bsdf_input(bsdf, 'Base Color', (0.04, 0.04, 0.05, 1.0))
    _set_bsdf_input(bsdf, 'Metallic', 0.0)
    _set_bsdf_input(bsdf, 'Roughness', 0.85)


def _build_btn_red_mat(mat, nodes, links, bsdf):
    _set_bsdf_input(bsdf, 'Base Color', (0.85, 0.10, 0.10, 1.0))
    _set_bsdf_input(bsdf, 'Metallic', 0.2)
    _set_bsdf_input(bsdf, 'Roughness', 0.3)


def _build_btn_green_mat(mat, nodes, links, bsdf):
    _set_bsdf_input(bsdf, 'Base Color', (0.10, 0.75, 0.20, 1.0))
    _set_bsdf_input(bsdf, 'Metallic', 0.2)
    _set_bsdf_input(bsdf, 'Roughness', 0.3)


def get_materials():
    """Dictionary of all prepared procedural materials."""
    return {
        'yellow_paint': get_or_create_material('M_Yellow_Weathered_Paint', _build_yellow_paint_mat),
        'cyan_paint': get_or_create_material('M_Cyan_Weathered_Paint', _build_cyan_paint_mat),
        'concrete': get_or_create_material('M_Concrete_Foundation', _build_concrete_mat),
        'dark_trim': get_or_create_material('M_Dark_Metal_Trim', _build_dark_trim_mat),
        'red_led': get_or_create_material('M_Emissive_Red_LED', _build_red_led_mat),
        'display_bezel': get_or_create_material('M_Display_Bezel_Black', _build_display_bezel_mat),
        'black_decal': get_or_create_material('M_Black_Decal_Text', _build_black_decal_mat),
        'btn_red': get_or_create_material('M_Button_Red', _build_btn_red_mat),
        'btn_green': get_or_create_material('M_Button_Green', _build_btn_green_mat),
    }


# ---------------------------------------------------------------------------
# Modeling Utility Primitives
# ---------------------------------------------------------------------------

def create_root_empty(name, location=(0, 0, 0)):
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = 'PLAIN_AXES'
    empty.empty_display_size = 0.5
    empty.location = location
    bpy.context.collection.objects.link(empty)
    return empty


def create_cube(name, size, location=(0, 0, 0), rotation=(0, 0, 0), material=None, parent=None):
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
    if obj and obj.type == 'MESH':
        mod = obj.modifiers.new(name="Bevel", type='BEVEL')
        mod.width = width
        mod.segments = segments
        mod.limit_method = 'ANGLE'
        mod.angle_limit = math.radians(35.0)


def create_text_mesh(name, text, size=0.08, extrude=0.004, location=(0,0,0), rotation=(0,0,0), material=None, parent=None):
    curve_data = bpy.data.curves.new(name=f"{name}_Data", type='FONT')
    curve_data.body = text
    curve_data.size = size
    curve_data.extrude = extrude
    curve_data.align_x = 'CENTER'
    curve_data.align_y = 'CENTER'

    obj = bpy.data.objects.new(name, curve_data)
    obj.location = location
    obj.rotation_euler = rotation
    bpy.context.collection.objects.link(obj)

    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def create_warning_triangle(name, size=0.25, location=(0,0,0), rotation=(0,0,0), material=None, parent=None):
    mesh = bpy.data.meshes.new(name=f"{name}_Mesh")
    bm = bmesh.new()

    h = size * (math.sqrt(3) / 2.0)
    half_w = size / 2.0
    r_inner = 0.78

    v1 = bm.verts.new((-half_w, -h/3.0, 0))
    v2 = bm.verts.new((half_w, -h/3.0, 0))
    v3 = bm.verts.new((0, 2.0 * h / 3.0, 0))

    v1_in = bm.verts.new((-half_w * r_inner, -h/3.0 * r_inner, 0))
    v2_in = bm.verts.new((half_w * r_inner, -h/3.0 * r_inner, 0))
    v3_in = bm.verts.new((0, (2.0 * h / 3.0) * r_inner, 0))

    bm.faces.new((v1, v2, v2_in, v1_in))
    bm.faces.new((v2, v3, v3_in, v2_in))
    bm.faces.new((v3, v1, v1_in, v3_in))

    lb_w = size * 0.12
    lb_h = size * 0.45
    lv1 = bm.verts.new((-lb_w*0.5, lb_h*0.4, 0))
    lv2 = bm.verts.new((lb_w*0.7, lb_h*0.4, 0))
    lv3 = bm.verts.new((-lb_w*0.1, 0, 0))
    lv4 = bm.verts.new((lb_w*0.6, 0, 0))
    lv5 = bm.verts.new((-lb_w*0.6, -lb_h*0.5, 0))
    lv6 = bm.verts.new((lb_w*0.1, -lb_h*0.1, 0))
    lv7 = bm.verts.new((-lb_w*0.4, -lb_h*0.1, 0))

    bm.faces.new((lv1, lv2, lv3))
    bm.faces.new((lv3, lv4, lv6, lv7))
    bm.faces.new((lv6, lv5, lv7))

    bmesh.ops.extrude_face_region(bm, geom=bm.faces)
    bmesh.ops.translate(bm, vec=Vector((0, 0, 0.005)), verts=[v for v in bm.verts if v.co.z == 0])

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    bpy.context.collection.objects.link(obj)

    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def create_flame_symbol(name, size=0.14, location=(0,0,0), rotation=(0,0,0), material=None, parent=None):
    mesh = bpy.data.meshes.new(name=f"{name}_Mesh")
    bm = bmesh.new()

    s = size / 2.0
    pts = [
        (0.0, s),
        (s*0.35, s*0.4),
        (s*0.75, s*0.1),
        (s*0.8, -s*0.5),
        (s*0.4, -s*0.85),
        (0.0, -s),
        (-s*0.4, -s*0.85),
        (-s*0.8, -s*0.5),
        (-s*0.75, s*0.1),
        (-s*0.35, s*0.4),
    ]
    verts = [bm.verts.new((x, y, 0)) for x, y in pts]
    bm.faces.new(verts)

    bmesh.ops.extrude_face_region(bm, geom=bm.faces)
    bmesh.ops.translate(bm, vec=Vector((0, 0, 0.005)), verts=[v for v in bm.verts if v.co.z == 0])

    bm.to_mesh(mesh)
    bm.free()

    obj = bpy.data.objects.new(name, mesh)
    obj.location = location
    obj.rotation_euler = rotation
    bpy.context.collection.objects.link(obj)

    if material:
        obj.data.materials.append(material)
    if parent:
        obj.parent = parent
    return obj


def create_led_dot_matrix(name, rows=2, cols=4, dot_radius=0.013, spacing_x=0.038, spacing_y=0.038,
                          location=(0,0,0), parent=None, led_mat=None, bezel_mat=None):
    """Create a recessed dot matrix LED display unit."""
    bezel_w = cols * spacing_x + 0.04
    bezel_h = rows * spacing_y + 0.04
    bezel_d = 0.025

    bezel = create_cube(
        f"{name}_Bezel",
        size=(bezel_w, bezel_d, bezel_h),
        location=location,
        material=bezel_mat,
        parent=parent
    )
    add_bevel_modifier(bezel, width=0.004, segments=1)

    for r in range(rows):
        for c in range(cols):
            ox = (c - (cols - 1) / 2.0) * spacing_x
            oz = ((rows - 1) / 2.0 - r) * spacing_y
            dot_pos = (location[0] + ox, location[1] - bezel_d / 2.0 - 0.004, location[2] + oz)

            create_cylinder(
                f"{name}_LED_{r}_{c}",
                radius=dot_radius,
                depth=0.008,
                location=dot_pos,
                rotation=(math.radians(90.0), 0, 0),
                material=led_mat,
                parent=parent
            )

    return bezel


def create_louver_vent_column(name, width=0.18, height=0.75, num_slats=14, depth=0.04,
                              location=(0,0,0), rotation=(0,0,0), parent=None,
                              louver_mat=None, frame_mat=None):
    """Create a vertical recessed cooling louver vent strip with angled slats."""
    # Create the recess frame parented to the prop parent
    frame = create_cube(
        f"{name}_Recess",
        size=(width, depth, height),
        location=location,
        rotation=rotation,
        material=frame_mat,
        parent=parent
    )

    slat_spacing = height / num_slats
    slat_w = width * 0.90
    slat_h = slat_spacing * 0.75
    rot_mat = Euler(rotation).to_matrix()
    up_norm = rot_mat @ Vector((0, 0, 1))
    forward_norm = rot_mat @ Vector((0, -depth/2 - 0.005, 0))

    # Parent slats to parent directly using world position (avoids double transform)
    for i in range(num_slats):
        offset_z = ((num_slats - 1) / 2.0 - i) * slat_spacing
        pos = Vector(location) + forward_norm + (up_norm * offset_z)

        create_cube(
            f"{name}_Slat_{i}",
            size=(slat_w, 0.012, slat_h),
            location=(pos.x, pos.y, pos.z),
            rotation=(rotation[0] + math.radians(35.0), rotation[1], rotation[2]),
            material=louver_mat,
            parent=parent
        )

    return frame
