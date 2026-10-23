"""
Procedural Generator for Cyberpunk Telecom / Cellular Antenna Tower (Asset 1).
Features:
- Angled A-frame 4-legged lattice truss base with anchor footings
- Segmented cylindrical mast with mounting collars and flanges
- Upper array of cellular panel antennas (radomes) with mounting brackets
- Side-mounted microwave drum antenna
- Avionics junction box with glowing neon cyan LED indicator display
- Conduit cable runs and red warning beacon
- Top lightning rod / sensor spire
- Pivot at (0, 0, 0) at the ground base for Unreal Engine snapping
"""

import os
import sys
import math
import bpy
from mathutils import Vector, Euler

script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir not in sys.path:
    sys.path.append(script_dir)

import cyberpunk_structures_common as csc


def build_prop(location=(0, 0, 0), rotation=(0, 0, 0), parent=None):
    """Construct the complete Telecom Tower prop hierarchy."""
    mats = csc.get_materials()
    root = csc.create_root_empty("SM_Cyberpunk_Telecom_Tower", location=location)
    root.rotation_euler = rotation
    if parent:
        root.parent = parent

    loc_x, loc_y, loc_z = location

    # -----------------------------------------------------------------------
    # 1. Base Pedestal (A-Frame 4-Legged Truss)
    # -----------------------------------------------------------------------
    base_half_w = 0.75
    top_half_w = 0.28
    base_h = 2.40

    leg_bottoms = [
        Vector((-base_half_w, -base_half_w, 0.0)),
        Vector(( base_half_w, -base_half_w, 0.0)),
        Vector(( base_half_w,  base_half_w, 0.0)),
        Vector((-base_half_w,  base_half_w, 0.0)),
    ]
    leg_tops = [
        Vector((-top_half_w, -top_half_w, base_h)),
        Vector(( top_half_w, -top_half_w, base_h)),
        Vector(( top_half_w,  top_half_w, base_h)),
        Vector((-top_half_w,  top_half_w, base_h)),
    ]

    # 4 Main Angled Corner Legs
    for i in range(4):
        p1 = leg_bottoms[i] + Vector(location)
        p2 = leg_tops[i] + Vector(location)
        leg = csc.create_angled_beam(f"Tower_Leg_{i}", p1, p2, size_xy=(0.10, 0.10),
                                     material=mats['steel_main'], parent=root)
        csc.add_bevel_modifier(leg, width=0.01, segments=1)

        # Footing Anchor Pad at each leg base
        foot_pos = (p1.x, p1.y, p1.z + 0.03)
        foot = csc.create_cube(f"Tower_Foot_{i}", size=(0.28, 0.28, 0.06), location=foot_pos,
                               material=mats['steel_dark'], parent=root)
        csc.add_bevel_modifier(foot, width=0.008, segments=1)

        # 4 Anchor Bolts on foot
        for bx in [-0.09, 0.09]:
            for by in [-0.09, 0.09]:
                csc.create_cylinder(f"Bolt_{i}_{bx}_{by}", radius=0.016, depth=0.04,
                                    location=(foot_pos[0] + bx, foot_pos[1] + by, foot_pos[2] + 0.035),
                                    material=mats['steel_dark'], parent=root)

    # Horizontal Tie Braces between legs at Z = 0.6m and Z = 1.6m
    for z_level, factor in [(0.60, 0.60 / base_h), (1.60, 1.60 / base_h)]:
        half_w = base_half_w + (top_half_w - base_half_w) * factor
        pts = [
            Vector((-half_w, -half_w, z_level)) + Vector(location),
            Vector(( half_w, -half_w, z_level)) + Vector(location),
            Vector(( half_w,  half_w, z_level)) + Vector(location),
            Vector((-half_w,  half_w, z_level)) + Vector(location),
        ]
        for i in range(4):
            p_a = pts[i]
            p_b = pts[(i + 1) % 4]
            csc.create_angled_beam(f"Base_Tie_Z{z_level}_{i}", p_a, p_b, size_xy=(0.06, 0.06),
                                   material=mats['steel_main'], parent=root)

    # Diagonal Cross Braces (X-bracing) on all 4 faces
    for i in range(4):
        b1 = leg_bottoms[i] + Vector(location) + Vector((0, 0, 0.60))
        b2 = leg_bottoms[(i + 1) % 4] + Vector(location) + Vector((0, 0, 0.60))
        t1 = leg_tops[i] + Vector(location) - Vector((0, 0, 0.30))
        t2 = leg_tops[(i + 1) % 4] + Vector(location) - Vector((0, 0, 0.30))

        csc.create_angled_beam(f"Base_X_A_{i}", b1, t2, size_xy=(0.045, 0.045),
                               material=mats['steel_dark'], parent=root)
        csc.create_angled_beam(f"Base_X_B_{i}", b2, t1, size_xy=(0.045, 0.045),
                               material=mats['steel_dark'], parent=root)

    # Base Top Collar / Sleeve Clamp
    collar = csc.create_cylinder("Base_Top_Collar", radius=0.32, depth=0.35,
                                 location=(loc_x, loc_y, loc_z + base_h),
                                 vertices=16, material=mats['steel_dark'], parent=root)
    csc.add_bevel_modifier(collar, width=0.015, segments=1)

    # -----------------------------------------------------------------------
    # 2. Main Central Mast Column
    # -----------------------------------------------------------------------
    # Lower Mast (Z: 2.3m to 6.0m)
    lower_mast = csc.create_cylinder("Mast_Lower", radius=0.17, depth=3.8,
                                     location=(loc_x, loc_y, loc_z + 4.2),
                                     vertices=24, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(lower_mast, width=0.01, segments=1)

    # Flange Ring Collar 1 at Z = 6.0m
    flange_1 = csc.create_cylinder("Mast_Flange_Mid", radius=0.23, depth=0.12,
                                   location=(loc_x, loc_y, loc_z + 6.1),
                                   vertices=24, material=mats['steel_dark'], parent=root)
    csc.add_bevel_modifier(flange_1, width=0.008, segments=1)

    # Upper Mast (Z: 6.1m to 12.0m)
    upper_mast = csc.create_cylinder("Mast_Upper", radius=0.13, depth=5.9,
                                     location=(loc_x, loc_y, loc_z + 9.05),
                                     vertices=24, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(upper_mast, width=0.008, segments=1)

    # Flange Ring Collar 2 at Z = 9.2m
    flange_2 = csc.create_cylinder("Mast_Flange_Top", radius=0.19, depth=0.10,
                                   location=(loc_x, loc_y, loc_z + 9.2),
                                   vertices=24, material=mats['steel_dark'], parent=root)

    # -----------------------------------------------------------------------
    # 3. Mid-Level Equipment (Junction Box, Beacon, Microwave Dish)
    # -----------------------------------------------------------------------
    # Avionics / Signal Control Enclosure (Junction Box with Cyan Screen)
    box_pos = (loc_x - 0.05, loc_y - 0.32, loc_z + 4.60)
    jbox = csc.create_cube("Signal_Junction_Box", size=(0.34, 0.22, 0.62),
                           location=box_pos, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(jbox, width=0.012, segments=1)

    # Glowing Cyan Screen / Status Indicator on Front Face
    screen_pos = (box_pos[0], box_pos[1] - 0.112, box_pos[2] + 0.08)
    csc.create_cube("Junction_Box_Screen_Cyan", size=(0.20, 0.015, 0.28),
                    location=screen_pos, material=mats['cyan_glow'], parent=root)

    # Mounting Clamp Bracket attaching box to mast
    bracket_pos = (box_pos[0], box_pos[1] + 0.12, box_pos[2])
    csc.create_cube("JBox_Mount_Bracket", size=(0.18, 0.12, 0.40),
                    location=bracket_pos, material=mats['steel_dark'], parent=root)

    # Conduit from bottom of box
    csc.create_cylinder("JBox_Conduit_Bottom", radius=0.035, depth=0.45,
                        location=(box_pos[0], box_pos[1], box_pos[2] - 0.45),
                        material=mats['cable'], parent=root)

    # Microwave Drum Antenna (Side-Mounted)
    dish_center = (loc_x - 0.42, loc_y + 0.08, loc_z + 6.80)
    dish_arm = csc.create_cube("Microwave_Mount_Arm", size=(0.35, 0.08, 0.08),
                               location=(loc_x - 0.24, loc_y + 0.08, loc_z + 6.80),
                               material=mats['steel_dark'], parent=root)

    # Drum dish cylinder facing angled left
    dish_drum = csc.create_cylinder("Microwave_Drum_Dish", radius=0.25, depth=0.18,
                                    location=dish_center,
                                    rotation=(0, math.radians(90.0), math.radians(-25.0)),
                                    vertices=24, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(dish_drum, width=0.01, segments=1)

    # Warning Red Beacon Light on Mast Collar
    beacon_pos = (loc_x + 0.22, loc_y - 0.08, loc_z + 5.30)
    csc.create_cube("Beacon_Bracket", size=(0.14, 0.06, 0.05),
                    location=(loc_x + 0.14, loc_y - 0.08, loc_z + 5.30),
                    material=mats['steel_dark'], parent=root)
    csc.create_cylinder("Beacon_Housing", radius=0.045, depth=0.06,
                        location=beacon_pos, material=mats['steel_dark'], parent=root)
    csc.create_cylinder("Beacon_Red_Lens", radius=0.035, depth=0.08,
                        location=(beacon_pos[0], beacon_pos[1], beacon_pos[2] + 0.06),
                        material=mats['red_glow'], parent=root)

    # -----------------------------------------------------------------------
    # 4. Upper Array of Sector Panel Antennas (Radomes)
    # -----------------------------------------------------------------------
    # Panel 1: Lower Front Panel
    p1_pos = (loc_x - 0.04, loc_y - 0.34, loc_z + 8.10)
    p1 = csc.create_cube("Panel_Antenna_Lower_Front", size=(0.30, 0.14, 1.70),
                         location=p1_pos, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(p1, width=0.015, segments=1)
    # Mounting Brackets to Mast
    csc.create_cube("P1_Bracket_Top", size=(0.08, 0.20, 0.06),
                    location=(p1_pos[0], p1_pos[1] + 0.14, p1_pos[2] + 0.60),
                    material=mats['steel_dark'], parent=root)
    csc.create_cube("P1_Bracket_Btm", size=(0.08, 0.20, 0.06),
                    location=(p1_pos[0], p1_pos[1] + 0.14, p1_pos[2] - 0.60),
                    material=mats['steel_dark'], parent=root)

    # Panel 2: Upper Main Front-Right Panel (Tallest prominent panel in reference)
    p2_pos = (loc_x + 0.18, loc_y - 0.28, loc_z + 10.45)
    p2 = csc.create_cube("Panel_Antenna_Upper_Front", size=(0.32, 0.15, 2.20),
                         location=p2_pos, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(p2, width=0.015, segments=1)
    csc.create_cube("P2_Bracket_Top", size=(0.14, 0.18, 0.06),
                    location=(p2_pos[0] - 0.07, p2_pos[1] + 0.12, p2_pos[2] + 0.80),
                    material=mats['steel_dark'], parent=root)
    csc.create_cube("P2_Bracket_Btm", size=(0.14, 0.18, 0.06),
                    location=(p2_pos[0] - 0.07, p2_pos[1] + 0.12, p2_pos[2] - 0.80),
                    material=mats['steel_dark'], parent=root)

    # Panel 3: Left Rear-Side Panel
    p3_pos = (loc_x - 0.32, loc_y - 0.05, loc_z + 10.10)
    p3 = csc.create_cube("Panel_Antenna_Upper_Left", size=(0.14, 0.30, 1.90),
                         location=p3_pos, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(p3, width=0.015, segments=1)
    csc.create_cube("P3_Bracket_Top", size=(0.18, 0.08, 0.06),
                    location=(p3_pos[0] + 0.14, p3_pos[1], p3_pos[2] + 0.70),
                    material=mats['steel_dark'], parent=root)
    csc.create_cube("P3_Bracket_Btm", size=(0.18, 0.08, 0.06),
                    location=(p3_pos[0] + 0.14, p3_pos[1], p3_pos[2] - 0.70),
                    material=mats['steel_dark'], parent=root)

    # Panel 4: Back Right Panel
    p4_pos = (loc_x + 0.12, loc_y + 0.28, loc_z + 10.80)
    p4 = csc.create_cube("Panel_Antenna_Upper_Back", size=(0.28, 0.14, 1.80),
                         location=p4_pos, material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(p4, width=0.015, segments=1)

    # -----------------------------------------------------------------------
    # 5. Conduit Cable Runs
    # -----------------------------------------------------------------------
    # Main trunk running from panel array down to junction box
    csc.create_catenary_cable("Cable_Run_Main",
                              (loc_x + 0.08, loc_y - 0.18, loc_z + 9.5),
                              (loc_x - 0.02, loc_y - 0.24, loc_z + 4.9),
                              sag=0.06, radius=0.025, material=mats['cable'], parent=root)
    # Cable from dish to mast
    csc.create_catenary_cable("Cable_Run_Dish",
                              (dish_center[0] + 0.1, dish_center[1], dish_center[2] - 0.1),
                              (loc_x - 0.12, loc_y, loc_z + 6.3),
                              sag=0.08, radius=0.020, material=mats['cable'], parent=root)
    # Cable from junction box down to base leg
    csc.create_catenary_cable("Cable_Run_Base",
                              (box_pos[0], box_pos[1], box_pos[2] - 0.3),
                              (loc_x - base_half_w * 0.8, loc_y - base_half_w * 0.8, loc_z + 0.5),
                              sag=0.10, radius=0.028, material=mats['cable'], parent=root)

    # -----------------------------------------------------------------------
    # 6. Top Apex Spire / Lightning Arrester Rod
    # -----------------------------------------------------------------------
    top_cap = csc.create_cylinder("Mast_Top_Cap", radius=0.15, depth=0.15,
                                  location=(loc_x, loc_y, loc_z + 12.0),
                                  vertices=16, material=mats['steel_dark'], parent=root)

    # Lightning Rod Spire
    spire = csc.create_cylinder("Lightning_Rod_Spire", radius=0.025, depth=2.4,
                                location=(loc_x, loc_y, loc_z + 13.2),
                                vertices=12, material=mats['steel_dark'], parent=root)

    # Small aerial whip needles / cross arms near tip
    csc.create_cylinder("Spire_Cross_Arm_1", radius=0.008, depth=0.35,
                        location=(loc_x, loc_y, loc_z + 13.8),
                        rotation=(math.radians(90.0), 0, 0),
                        vertices=8, material=mats['steel_dark'], parent=root)
    csc.create_cylinder("Spire_Cross_Arm_2", radius=0.008, depth=0.35,
                        location=(loc_x, loc_y, loc_z + 13.8),
                        rotation=(0, math.radians(90.0), 0),
                        vertices=8, material=mats['steel_dark'], parent=root)

    print(f"[Prop Built] Telecom Tower created at {location}")
    return root


if __name__ == '__main__':
    # Test standalone generation
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    build_prop()
