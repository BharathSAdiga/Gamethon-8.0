"""
Asset Script: Yellow Industrial "SYSTEM" Electrical Terminal Pillar
Features:
- Poured concrete foundation plinth with aggregate texture.
- Lower skirt section with CAUTION warning placards and hazard frame.
- Main cabinet body with bold stencil 'SYSTEM' header.
- Recessed 2x4 red glowing dot-matrix LED indicator panel.
- Vertical 3-button control switch strip.
- High-voltage lightning bolt warning triangle.
- Left and right vertical ventilation louver columns with angled slats.
- Gabled / pitched roof cap with dark trim overhang and side WARNING badges.
- Procedural weathered yellow enamel paint with realistic chipped metal edges.
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


def build_prop(location=(0, 0, 0), parent=None):
    mats = epc.get_materials()
    root = epc.create_root_empty("Prop_Yellow_System_Pillar", location=location)
    if parent:
        root.parent = parent

    # -----------------------------------------------------------------------
    # 1. Concrete Foundation Plinth
    # -----------------------------------------------------------------------
    base_w, base_d, base_h = 0.68, 0.68, 0.16
    base_pad = epc.create_cube(
        "Pillar_Concrete_Base",
        size=(base_w, base_d, base_h),
        location=(0, 0, base_h / 2.0),
        material=mats['concrete'],
        parent=root
    )
    epc.add_bevel_modifier(base_pad, width=0.015, segments=2)

    # -----------------------------------------------------------------------
    # 2. Lower Skirt Section
    # -----------------------------------------------------------------------
    skirt_w, skirt_d, skirt_h = 0.58, 0.58, 0.44
    skirt_z = base_h + skirt_h / 2.0

    skirt = epc.create_cube(
        "Pillar_Lower_Skirt",
        size=(skirt_w, skirt_d, skirt_h),
        location=(0, 0, skirt_z),
        material=mats['yellow_paint'],
        parent=root
    )
    epc.add_bevel_modifier(skirt, width=0.012, segments=2)

    # Lower Skirt CAUTION placards (Front and Left Side)
    # Front Placard Border & Text
    epc.create_cube(
        "Skirt_Caution_Border_F",
        size=(0.34, 0.006, 0.22),
        location=(0, -skirt_d/2 - 0.004, skirt_z - 0.02),
        material=mats['black_decal'],
        parent=root
    )
    epc.create_cube(
        "Skirt_Caution_Inner_F",
        size=(0.32, 0.007, 0.20),
        location=(0, -skirt_d/2 - 0.005, skirt_z - 0.02),
        material=mats['yellow_paint'],
        parent=root
    )
    epc.create_text_mesh(
        "Skirt_Caution_Text_F",
        text="CAUTION",
        size=0.045,
        extrude=0.003,
        location=(0, -skirt_d/2 - 0.010, skirt_z - 0.02),
        rotation=(math.radians(90.0), 0, 0),
        material=mats['black_decal'],
        parent=root
    )

    # Left Side CAUTION Placard
    epc.create_cube(
        "Skirt_Caution_Border_L",
        size=(0.006, 0.34, 0.22),
        location=(-skirt_w/2 - 0.004, 0, skirt_z - 0.02),
        material=mats['black_decal'],
        parent=root
    )
    epc.create_cube(
        "Skirt_Caution_Inner_L",
        size=(0.007, 0.32, 0.20),
        location=(-skirt_w/2 - 0.005, 0, skirt_z - 0.02),
        material=mats['yellow_paint'],
        parent=root
    )
    epc.create_text_mesh(
        "Skirt_Caution_Text_L",
        text="CAUTION",
        size=0.045,
        extrude=0.003,
        location=(-skirt_w/2 - 0.010, 0, skirt_z - 0.02),
        rotation=(math.radians(90.0), 0, math.radians(-90.0)),
        material=mats['black_decal'],
        parent=root
    )

    # -----------------------------------------------------------------------
    # 3. Horizontal Seam Trim / Gasket
    # -----------------------------------------------------------------------
    seam_z = base_h + skirt_h
    epc.create_cube(
        "Pillar_Mid_Gasket",
        size=(skirt_w + 0.02, skirt_d + 0.02, 0.025),
        location=(0, 0, seam_z + 0.0125),
        material=mats['dark_trim'],
        parent=root
    )

    # -----------------------------------------------------------------------
    # 4. Main Body Cabinet
    # -----------------------------------------------------------------------
    body_w, body_d, body_h = 0.54, 0.54, 0.88
    body_z = seam_z + 0.025 + body_h / 2.0

    body = epc.create_cube(
        "Pillar_Main_Body",
        size=(body_w, body_d, body_h),
        location=(0, 0, body_z),
        material=mats['yellow_paint'],
        parent=root
    )
    epc.add_bevel_modifier(body, width=0.012, segments=2)

    # Front Face Details:
    # A. Header Text: 'SYSTEM'
    epc.create_text_mesh(
        "Pillar_Text_SYSTEM",
        text="SYSTEM",
        size=0.062,
        extrude=0.003,
        location=(-0.04, -body_d/2 - 0.006, body_z + body_h/2 - 0.12),
        rotation=(math.radians(90.0), 0, 0),
        material=mats['black_decal'],
        parent=root
    )

    # B. Recessed 2x4 Red Glowing LED Matrix Display
    epc.create_led_dot_matrix(
        name="Pillar_Display",
        rows=2,
        cols=4,
        dot_radius=0.013,
        spacing_x=0.038,
        spacing_y=0.038,
        location=(-0.06, -body_d/2 - 0.008, body_z + body_h/2 - 0.28),
        parent=root,
        led_mat=mats['red_led'],
        bezel_mat=mats['display_bezel']
    )

    # C. Right Button Strip (3 buttons stacked vertically)
    btn_x = body_w/2 - 0.08
    btn_y = -body_d/2 - 0.006
    # Vertical recess bar
    epc.create_cube(
        "Pillar_Button_Recess",
        size=(0.045, 0.015, 0.20),
        location=(btn_x, btn_y, body_z + body_h/2 - 0.35),
        material=mats['display_bezel'],
        parent=root
    )
    # 3 square buttons
    for bi, bz_off in enumerate([0.06, 0.0, -0.06]):
        b_mat = mats['btn_red'] if bi == 0 else (mats['btn_green'] if bi == 1 else mats['dark_trim'])
        epc.create_cube(
            f"Pillar_Button_{bi}",
            size=(0.025, 0.01, 0.025),
            location=(btn_x, btn_y - 0.008, body_z + body_h/2 - 0.35 + bz_off),
            material=b_mat,
            parent=root
        )

    # D. High Voltage Warning Triangle with Lightning Bolt
    epc.create_warning_triangle(
        name="Pillar_Warning_Triangle",
        size=0.28,
        location=(0, -body_d/2 - 0.008, body_z - 0.15),
        rotation=(math.radians(90.0), 0, 0),
        material=mats['black_decal'],
        parent=root
    )

    # Side Faces: Vertical Louvered Vents
    # Left Side Louver
    epc.create_louver_vent_column(
        name="Pillar_Louver_L",
        width=0.18,
        height=0.62,
        num_slats=12,
        depth=0.035,
        location=(-body_w/2 - 0.01, 0, body_z - 0.04),
        rotation=(0, 0, math.radians(-90.0)),
        parent=root,
        louver_mat=mats['dark_trim'],
        frame_mat=mats['dark_trim']
    )

    # Right Side Louver
    epc.create_louver_vent_column(
        name="Pillar_Louver_R",
        width=0.18,
        height=0.62,
        num_slats=12,
        depth=0.035,
        location=(body_w/2 + 0.01, 0, body_z - 0.04),
        rotation=(0, 0, math.radians(90.0)),
        parent=root,
        louver_mat=mats['dark_trim'],
        frame_mat=mats['dark_trim']
    )

    # -----------------------------------------------------------------------
    # 5. Upper Fascia Collar Band
    # -----------------------------------------------------------------------
    fascia_z = body_z + body_h / 2.0
    fascia_h = 0.12
    fascia = epc.create_cube(
        "Pillar_Fascia_Band",
        size=(body_w + 0.03, body_d + 0.03, fascia_h),
        location=(0, 0, fascia_z + fascia_h / 2.0),
        material=mats['yellow_paint'],
        parent=root
    )
    epc.add_bevel_modifier(fascia, width=0.01, segments=1)

    # Side WARNING Placard on Fascia Band
    epc.create_cube(
        "Fascia_Warning_Plate_L",
        size=(0.006, 0.18, 0.06),
        location=(-(body_w + 0.03)/2 - 0.004, 0, fascia_z + fascia_h / 2.0),
        material=mats['black_decal'],
        parent=root
    )
    epc.create_text_mesh(
        "Fascia_Warning_Text_L",
        text="WARNING",
        size=0.025,
        extrude=0.003,
        location=(-(body_w + 0.03)/2 - 0.008, 0, fascia_z + fascia_h / 2.0),
        rotation=(math.radians(90.0), 0, math.radians(-90.0)),
        material=mats['yellow_paint'],
        parent=root
    )

    # -----------------------------------------------------------------------
    # 6. Pitched / Gabled Protective Roof Cap
    # -----------------------------------------------------------------------
    cap_z = fascia_z + fascia_h
    roof_w, roof_d, roof_h = 0.64, 0.64, 0.14

    # Underside dark lip
    epc.create_cube(
        "Roof_Underside_Lip",
        size=(roof_w - 0.02, roof_d - 0.02, 0.03),
        location=(0, 0, cap_z + 0.015),
        material=mats['dark_trim'],
        parent=root
    )

    # Main gabled top roof (slanted towards front and back)
    # Build using pyramid / gabled mesh
    roof_mesh = bpy.data.meshes.new(name="Pillar_Gabled_Roof_Mesh")
    bm = bpy.data.meshes.new(name="temp")
    import bmesh
    bm = bmesh.new()

    hw = roof_w / 2.0
    hd = roof_d / 2.0
    hz_bot = 0.0
    hz_top = roof_h

    # Bottom 4 corners
    v_b1 = bm.verts.new((-hw, -hd, hz_bot))
    v_b2 = bm.verts.new(( hw, -hd, hz_bot))
    v_b3 = bm.verts.new(( hw,  hd, hz_bot))
    v_b4 = bm.verts.new((-hw,  hd, hz_bot))

    # Top ridge corners (pitched along X axis)
    ridge_w = hw * 0.85
    ridge_d = 0.04
    v_t1 = bm.verts.new((-ridge_w, -ridge_d, hz_top))
    v_t2 = bm.verts.new(( ridge_w, -ridge_d, hz_top))
    v_t3 = bm.verts.new(( ridge_w,  ridge_d, hz_top))
    v_t4 = bm.verts.new((-ridge_w,  ridge_d, hz_top))

    # Faces
    bm.faces.new((v_b1, v_b2, v_b3, v_b4)) # Bottom
    bm.faces.new((v_t1, v_t2, v_t3, v_t4)) # Top ridge
    bm.faces.new((v_b1, v_b2, v_t2, v_t1)) # Front slope
    bm.faces.new((v_b3, v_b4, v_t4, v_t3)) # Back slope
    bm.faces.new((v_b4, v_b1, v_t1, v_t4)) # Left gable
    bm.faces.new((v_b2, v_b3, v_t3, v_t2)) # Right gable

    bm.to_mesh(roof_mesh)
    bm.free()

    roof_obj = bpy.data.objects.new("Pillar_Gabled_Roof", roof_mesh)
    roof_obj.location = (0, 0, cap_z + 0.03)
    bpy.context.collection.objects.link(roof_obj)
    roof_obj.data.materials.append(mats['yellow_paint'])
    roof_obj.parent = root
    epc.add_bevel_modifier(roof_obj, width=0.012, segments=2)

    return root


if __name__ == '__main__':
    for obj in bpy.context.scene.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    build_prop()
    print("Yellow System Pillar prop generated successfully.")
