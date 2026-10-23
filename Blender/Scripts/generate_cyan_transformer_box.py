"""
Asset Script: Cyan Industrial Power Substation / Transformer Box
Features:
- Heavy poured concrete foundation slab with stone aggregate texture.
- Wide industrial enclosure cabinet in weathered vibrant cyan enamel paint.
- Dual vertical cooling louver columns with angled ventilation slats on left face.
- Overhanging stepped flat roof / lid with beveled rim and dark recessed lip.
- Front panel:
  - High-voltage lightning bolt warning triangle.
  - Dual red glowing LED dot-matrix indicator displays (2x4 array each = 16 glowing diodes).
  - 'CAUTION' industrial hazard sign.
  - 'WARNING' label and flammable fire hazard symbol.
- Procedural weathered cyan enamel shader with realistic chipped metal scratches.
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
    root = epc.create_root_empty("Prop_Cyan_Transformer_Box", location=location)
    if parent:
        root.parent = parent

    # -----------------------------------------------------------------------
    # 1. Concrete Foundation Pad
    # -----------------------------------------------------------------------
    pad_w, pad_d, pad_h = 1.76, 1.76, 0.16
    pad = epc.create_cube(
        "Transformer_Concrete_Pad",
        size=(pad_w, pad_d, pad_h),
        location=(0, 0, pad_h / 2.0),
        material=mats['concrete'],
        parent=root
    )
    epc.add_bevel_modifier(pad, width=0.015, segments=2)

    # -----------------------------------------------------------------------
    # 2. Recessed Base Collar / Kickplate
    # -----------------------------------------------------------------------
    collar_w, collar_d, collar_h = 1.44, 1.44, 0.05
    collar_z = pad_h + collar_h / 2.0
    epc.create_cube(
        "Transformer_Base_Collar",
        size=(collar_w, collar_d, collar_h),
        location=(0, 0, collar_z),
        material=mats['dark_trim'],
        parent=root
    )

    # -----------------------------------------------------------------------
    # 3. Main Enclosure Body
    # -----------------------------------------------------------------------
    body_w, body_d, body_h = 1.48, 1.48, 1.15
    body_z = pad_h + collar_h + body_h / 2.0

    body = epc.create_cube(
        "Transformer_Main_Body",
        size=(body_w, body_d, body_h),
        location=(0, 0, body_z),
        material=mats['cyan_paint'],
        parent=root
    )
    epc.add_bevel_modifier(body, width=0.015, segments=2)

    # Corner Seam Reinforcement Strips
    for cx in [-body_w/2, body_w/2]:
        for cy in [-body_d/2, body_d/2]:
            epc.create_cube(
                f"Corner_Seam_{cx:.1f}_{cy:.1f}",
                size=(0.04, 0.04, body_h),
                location=(cx, cy, body_z),
                material=mats['dark_trim'],
                parent=root
            )

    # -----------------------------------------------------------------------
    # 4. Front Panel Instrumentation & Decals
    # -----------------------------------------------------------------------
    front_y = -body_d / 2.0 - 0.006

    # A. Top High-Voltage Warning Triangle with Lightning Bolt
    epc.create_warning_triangle(
        name="Transformer_Warning_Triangle",
        size=0.36,
        location=(0.0, front_y, body_z + 0.26),
        rotation=(math.radians(90.0), 0, 0),
        material=mats['black_decal'],
        parent=root
    )

    # B. Dual Red LED Indicator Displays (Left & Right units)
    # Each unit has a 2x4 dot matrix
    led_spacing = 0.16
    for idx, lx in enumerate([-led_spacing, led_spacing]):
        epc.create_led_dot_matrix(
            name=f"Transformer_Display_{idx}",
            rows=2,
            cols=4,
            dot_radius=0.012,
            spacing_x=0.034,
            spacing_y=0.034,
            location=(lx, front_y - 0.004, body_z - 0.02),
            parent=root,
            led_mat=mats['red_led'],
            bezel_mat=mats['display_bezel']
        )

    # C. 'CAUTION' Industrial Placard (Below LEDs)
    caution_y = front_y - 0.002
    caution_z = body_z - 0.18
    # Outer Border
    epc.create_cube(
        "Transformer_Caution_Border",
        size=(0.28, 0.006, 0.15),
        location=(0, caution_y, caution_z),
        material=mats['black_decal'],
        parent=root
    )
    # Inner Plate
    epc.create_cube(
        "Transformer_Caution_Plate",
        size=(0.26, 0.007, 0.13),
        location=(0, caution_y - 0.001, caution_z),
        material=mats['cyan_paint'],
        parent=root
    )
    # Text
    epc.create_text_mesh(
        "Transformer_Caution_Text",
        text="CAUTION",
        size=0.036,
        extrude=0.003,
        location=(0, caution_y - 0.005, caution_z),
        rotation=(math.radians(90.0), 0, 0),
        material=mats['black_decal'],
        parent=root
    )

    # D. Lower Left: 'WARNING' Badge
    warn_x = -0.16
    warn_z = body_z - 0.35
    epc.create_cube(
        "Transformer_Warn_Plate",
        size=(0.18, 0.006, 0.08),
        location=(warn_x, front_y, warn_z),
        material=mats['black_decal'],
        parent=root
    )
    epc.create_text_mesh(
        "Transformer_Warn_Text",
        text="WARNING",
        size=0.025,
        extrude=0.003,
        location=(warn_x, front_y - 0.005, warn_z),
        rotation=(math.radians(90.0), 0, 0),
        material=mats['cyan_paint'],
        parent=root
    )

    # E. Lower Right: Flammable Flame Symbol
    flame_x = 0.16
    flame_z = body_z - 0.33
    epc.create_flame_symbol(
        name="Transformer_Flame_Icon",
        size=0.14,
        location=(flame_x, front_y, flame_z),
        rotation=(math.radians(90.0), 0, 0),
        material=mats['black_decal'],
        parent=root
    )

    # -----------------------------------------------------------------------
    # 5. Left Face: Dual Vertical Louver Ventilation Columns
    # -----------------------------------------------------------------------
    louver_y_offsets = [-0.28, 0.28]
    left_x = -body_w / 2.0 - 0.01

    for li, ly in enumerate(louver_y_offsets):
        epc.create_louver_vent_column(
            name=f"Transformer_Louver_{li}",
            width=0.26,
            height=0.88,
            num_slats=16,
            depth=0.04,
            location=(left_x, ly, body_z),
            rotation=(0, 0, math.radians(-90.0)),
            parent=root,
            louver_mat=mats['dark_trim'],
            frame_mat=mats['dark_trim']
        )

    # -----------------------------------------------------------------------
    # 6. Stepped Overhang Top Lid / Roof Cap
    # -----------------------------------------------------------------------
    top_z = pad_h + collar_h + body_h

    # Recessed Dark Under-Lip
    epc.create_cube(
        "Transformer_Roof_Lip",
        size=(body_w + 0.04, body_d + 0.04, 0.04),
        location=(0, 0, top_z + 0.02),
        material=mats['dark_trim'],
        parent=root
    )

    # Overhanging Flat Top Lid
    lid_w, lid_d, lid_h = body_w + 0.12, body_d + 0.12, 0.09
    lid = epc.create_cube(
        "Transformer_Top_Lid",
        size=(lid_w, lid_d, lid_h),
        location=(0, 0, top_z + 0.04 + lid_h / 2.0),
        material=mats['cyan_paint'],
        parent=root
    )
    epc.add_bevel_modifier(lid, width=0.015, segments=2)

    return root


if __name__ == '__main__':
    for obj in bpy.context.scene.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    build_prop()
    print("Cyan Transformer Box prop generated successfully.")
