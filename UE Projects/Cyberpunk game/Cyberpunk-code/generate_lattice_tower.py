"""
Procedural Generator for Modular Industrial Lattice Truss Tower (Asset 2).
Features:
- Poured concrete pedestal foundation with notched expansion joints
- Heavy flanged steel corner shoe boots anchored to concrete
- 4 vertical structural corner box-girders with top column caps
- 5 vertical tiers/modules of perimeter horizontal tie beams
- Iconic cross X-bracing on all 4 faces with circular center reinforcement hub discs
- Internal service ladder and conduit trunk
- Cyberpunk status lights: lower amber/orange LED box and mid-level cyan LED unit
- Top corner antenna pegs and spires
- Pivot at (0, 0, 0) at ground level for Unreal Engine snapping
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
    """Construct the complete Modular Lattice Truss Tower prop hierarchy."""
    mats = csc.get_materials()
    root = csc.create_root_empty("SM_Cyberpunk_Lattice_Tower", location=location)
    root.rotation_euler = rotation
    if parent:
        root.parent = parent

    loc_x, loc_y, loc_z = location

    # -----------------------------------------------------------------------
    # 1. Poured Concrete Foundation Pedestal
    # -----------------------------------------------------------------------
    plinth_w = 2.45
    plinth_h = 1.05
    plinth = csc.create_cube("Concrete_Foundation_Plinth",
                             size=(plinth_w, plinth_w, plinth_h),
                             location=(loc_x, loc_y, loc_z + plinth_h * 0.5),
                             material=mats['concrete'], parent=root)
    csc.add_bevel_modifier(plinth, width=0.035, segments=2)

    # Recessed horizontal groove / panel notch around concrete
    notch_h = 0.08
    for face_x, face_y, rot in [
        (0, -plinth_w * 0.5 - 0.005, 0),
        (0,  plinth_w * 0.5 + 0.005, 0),
        (-plinth_w * 0.5 - 0.005, 0, math.radians(90.0)),
        ( plinth_w * 0.5 + 0.005, 0, math.radians(90.0)),
    ]:
        csc.create_cube("Concrete_Expansion_Joint",
                        size=(plinth_w * 0.90, 0.02, notch_h),
                        location=(loc_x + face_x, loc_y + face_y, loc_z + plinth_h * 0.45),
                        rotation=(0, 0, rot), material=mats['steel_dark'], parent=root)

    # -----------------------------------------------------------------------
    # 2. Corner Shoe Brackets (Steel Anchor Boots)
    # -----------------------------------------------------------------------
    half_span = 0.95
    corners = [
        Vector((-half_span, -half_span, 0)),
        Vector(( half_span, -half_span, 0)),
        Vector(( half_span,  half_span, 0)),
        Vector((-half_span,  half_span, 0)),
    ]

    for i, c in enumerate(corners):
        shoe_pos = (loc_x + c.x, loc_y + c.y, loc_z + plinth_h + 0.12)
        shoe = csc.create_cube(f"Shoe_Bracket_{i}", size=(0.32, 0.32, 0.24),
                               location=shoe_pos, material=mats['steel_dark'], parent=root)
        csc.add_bevel_modifier(shoe, width=0.015, segments=1)

        # Flange base plate
        csc.create_cube(f"Shoe_BasePlate_{i}", size=(0.42, 0.42, 0.05),
                        location=(shoe_pos[0], shoe_pos[1], loc_z + plinth_h + 0.025),
                        material=mats['steel_dark'], parent=root)

    # -----------------------------------------------------------------------
    # 3. 4 Main Corner Vertical Columns (Box Girders)
    # -----------------------------------------------------------------------
    tower_h = 11.80  # Height above concrete
    col_size = 0.18
    col_total_h = tower_h + 0.70  # Extend past top horizontal beam

    for i, c in enumerate(corners):
        col_pos = (loc_x + c.x, loc_y + c.y, loc_z + plinth_h + col_total_h * 0.5)
        col = csc.create_cube(f"Corner_Column_{i}", size=(col_size, col_size, col_total_h),
                              location=col_pos, material=mats['steel_main'], parent=root)
        csc.add_bevel_modifier(col, width=0.012, segments=1)

        # Top Column Cap & Antenna Spire Peg
        cap_pos = (loc_x + c.x, loc_y + c.y, loc_z + plinth_h + col_total_h)
        cap = csc.create_cube(f"Column_Top_Cap_{i}", size=(col_size * 1.25, col_size * 1.25, 0.08),
                              location=cap_pos, material=mats['steel_dark'], parent=root)
        csc.add_bevel_modifier(cap, width=0.008, segments=1)

        # Top vertical antenna peg / rod spike
        csc.create_cylinder(f"Top_Antenna_Spike_{i}", radius=0.02, depth=0.65,
                            location=(cap_pos[0], cap_pos[1], cap_pos[2] + 0.35),
                            vertices=12, material=mats['steel_dark'], parent=root)

    # -----------------------------------------------------------------------
    # 4. Multi-Tier Lattice Framework (5 Vertical Bays)
    # -----------------------------------------------------------------------
    num_tiers = 5
    tier_height = tower_h / num_tiers  # ~2.36m per tier

    for tier in range(num_tiers):
        z_bottom = loc_z + plinth_h + tier * tier_height
        z_top = z_bottom + tier_height

        # Horizontal Perimeter Tie Beams at the tier levels
        tie_beam_size = (col_size * 0.75, col_size * 0.75)
        for i in range(4):
            c1 = corners[i]
            c2 = corners[(i + 1) % 4]

            # Bottom tie beam (skip ground level as it has shoe brackets, but place at tier boundaries)
            if tier > 0:
                p_b1 = Vector((loc_x + c1.x, loc_y + c1.y, z_bottom))
                p_b2 = Vector((loc_x + c2.x, loc_y + c2.y, z_bottom))
                beam = csc.create_angled_beam(f"Tie_Beam_T{tier}_Btm_{i}", p_b1, p_b2,
                                              size_xy=tie_beam_size, material=mats['steel_main'], parent=root)
                csc.add_bevel_modifier(beam, width=0.008, segments=1)

            # Top tie beam of the top tier
            if tier == num_tiers - 1:
                p_t1 = Vector((loc_x + c1.x, loc_y + c1.y, z_top))
                p_t2 = Vector((loc_x + c2.x, loc_y + c2.y, z_top))
                beam = csc.create_angled_beam(f"Tie_Beam_Top_{i}", p_t1, p_t2,
                                              size_xy=tie_beam_size, material=mats['steel_main'], parent=root)
                csc.add_bevel_modifier(beam, width=0.008, segments=1)

        # Cross X-Braces on all 4 faces of this tier
        brace_size = (0.08, 0.08)
        for i in range(4):
            c1 = corners[i]
            c2 = corners[(i + 1) % 4]

            # 4 Corner Points for this face
            p_bl = Vector((loc_x + c1.x, loc_y + c1.y, z_bottom + 0.12))
            p_br = Vector((loc_x + c2.x, loc_y + c2.y, z_bottom + 0.12))
            p_tl = Vector((loc_x + c1.x, loc_y + c1.y, z_top - 0.12))
            p_tr = Vector((loc_x + c2.x, loc_y + c2.y, z_top - 0.12))

            # Diagonal Strut 1: Bottom-Left to Top-Right
            d1 = csc.create_angled_beam(f"Lattice_X1_T{tier}_F{i}", p_bl, p_tr,
                                        size_xy=brace_size, material=mats['steel_main'], parent=root)
            csc.add_bevel_modifier(d1, width=0.006, segments=1)

            # Diagonal Strut 2: Bottom-Right to Top-Left
            d2 = csc.create_angled_beam(f"Lattice_X2_T{tier}_F{i}", p_br, p_tl,
                                        size_xy=brace_size, material=mats['steel_main'], parent=root)
            csc.add_bevel_modifier(d2, width=0.006, segments=1)

            # Center Reinforcement Hub Disc at X intersection
            center_pt = (p_bl + p_br + p_tl + p_tr) * 0.25
            face_dir = (p_br - p_bl).cross(Vector((0, 0, 1))).normalized()

            # Front-facing disc on this face
            rot_quat = face_dir.to_track_quat('Z', 'Y')
            disc = csc.create_cylinder(f"X_Hub_Disc_T{tier}_F{i}", radius=0.17, depth=0.06,
                                       location=(center_pt.x + face_dir.x * 0.04,
                                                 center_pt.y + face_dir.y * 0.04,
                                                 center_pt.z),
                                       rotation=rot_quat.to_euler(),
                                       vertices=16, material=mats['steel_dark'], parent=root)
            csc.add_bevel_modifier(disc, width=0.006, segments=1)

            # Center bolt on hub disc
            csc.create_cylinder(f"X_Hub_Bolt_T{tier}_F{i}", radius=0.035, depth=0.09,
                                location=(center_pt.x + face_dir.x * 0.06,
                                          center_pt.y + face_dir.y * 0.06,
                                          center_pt.z),
                                rotation=rot_quat.to_euler(),
                                vertices=12, material=mats['steel_dark'], parent=root)

    # -----------------------------------------------------------------------
    # 5. Internal Service Ladder & Central Conduit Spine
    # -----------------------------------------------------------------------
    ladder_x = loc_x
    ladder_y = loc_y + half_span * 0.65
    ladder_rail_dx = 0.22

    # Vertical ladder stringers
    for dx in [-ladder_rail_dx, ladder_rail_dx]:
        csc.create_cube(f"Ladder_Rail_{dx}", size=(0.04, 0.05, tower_h),
                        location=(ladder_x + dx, ladder_y, loc_z + plinth_h + tower_h * 0.5),
                        material=mats['steel_dark'], parent=root)

    # Ladder Rungs
    num_rungs = int(tower_h / 0.35)
    for r in range(num_rungs):
        rung_z = loc_z + plinth_h + 0.30 + r * 0.35
        csc.create_cylinder(f"Ladder_Rung_{r}", radius=0.015, depth=ladder_rail_dx * 2.0,
                            location=(ladder_x, ladder_y, rung_z),
                            rotation=(0, math.radians(90.0), 0),
                            vertices=8, material=mats['steel_dark'], parent=root)

    # Central heavy vertical power/conduit trunk
    csc.create_cylinder("Core_Conduit_Trunk", radius=0.06, depth=tower_h + 0.8,
                        location=(loc_x, loc_y, loc_z + plinth_h + tower_h * 0.5),
                        vertices=16, material=mats['cable'], parent=root)

    # -----------------------------------------------------------------------
    # 6. Cyberpunk Indicator Lights Matching Reference
    # -----------------------------------------------------------------------
    # Lower right corner amber/orange indicator light box (Z ~ 2.2m)
    amber_box_pos = (loc_x + half_span + 0.12, loc_y - half_span + 0.05, loc_z + plinth_h + 1.25)
    csc.create_cube("Status_Box_Amber", size=(0.14, 0.12, 0.22),
                    location=amber_box_pos, material=mats['steel_dark'], parent=root)
    # Glowing orange lens
    csc.create_cube("Status_Lens_Orange", size=(0.04, 0.08, 0.14),
                    location=(amber_box_pos[0] + 0.06, amber_box_pos[1], amber_box_pos[2]),
                    material=mats['orange_glow'], parent=root)

    # Mid-level cyan indicator module (Z ~ 6.5m on column)
    cyan_mod_pos = (loc_x + half_span + 0.12, loc_y + 0.10, loc_z + plinth_h + 5.5)
    csc.create_cube("Status_Box_Cyan", size=(0.12, 0.12, 0.18),
                    location=cyan_mod_pos, material=mats['steel_dark'], parent=root)
    csc.create_cube("Status_Lens_Cyan", size=(0.04, 0.07, 0.10),
                    location=(cyan_mod_pos[0] + 0.05, cyan_mod_pos[1], cyan_mod_pos[2]),
                    material=mats['cyan_glow'], parent=root)

    print(f"[Prop Built] Lattice Tower created at {location}")
    return root


if __name__ == '__main__':
    # Test standalone generation
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    build_prop()
