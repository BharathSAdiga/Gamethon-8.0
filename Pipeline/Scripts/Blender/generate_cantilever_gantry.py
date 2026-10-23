"""
Procedural Generator for Cyberpunk Cantilevered Industrial Overpass / Gantry Platform (Asset 3).
Features:
- Brutalist segmented vertical column pylon with armor plates and vertical conduit grooves
- Inset vertical glowing amber/orange status LED indicator strip near pillar base
- Heavy diagonal boxed cantilever strut (knee brace) with reinforcement gusset brackets
- Cantilevered observation deck / walkway platform with modular underside joists
- Dual horizontal glowing neon light bars on platform fascia (one cyan, one violet-white)
- Industrial safety perimeter railings (stanchions, handrails, kickplates)
- Drooping catenary conduit cables hanging under the cantilever arm
- Pivot at (0, 0, 0) at the base of the pillar for Unreal Engine snapping
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
    """Construct the complete Cantilevered Gantry Platform prop hierarchy."""
    mats = csc.get_materials()
    root = csc.create_root_empty("SM_Cyberpunk_Cantilever_Gantry", location=location)
    root.rotation_euler = rotation
    if parent:
        root.parent = parent

    loc_x, loc_y, loc_z = location

    # -----------------------------------------------------------------------
    # 1. Main Vertical Column / Pylon Assembly (Z: 0 to 8.2m)
    # -----------------------------------------------------------------------
    pylon_center_x = loc_x - 1.0
    pylon_center_y = loc_y
    pylon_w = 1.35   # X width
    pylon_d = 1.45   # Y depth
    pylon_h = 8.20   # Total height to deck underside

    # Base Footing Shoe (Heavy flanged base)
    base_shoe = csc.create_cube("Pylon_Base_Shoe", size=(pylon_w + 0.35, pylon_d + 0.35, 0.45),
                                location=(pylon_center_x, pylon_center_y, loc_z + 0.225),
                                material=mats['steel_dark'], parent=root)
    csc.add_bevel_modifier(base_shoe, width=0.03, segments=2)

    # Main Segmented Pylon Shaft
    pylon_body = csc.create_cube("Pylon_Main_Shaft", size=(pylon_w, pylon_d, pylon_h - 0.45),
                                 location=(pylon_center_x, pylon_center_y, loc_z + 0.45 + (pylon_h - 0.45) * 0.5),
                                 material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(pylon_body, width=0.025, segments=2)

    # Modular Horizontal Armor Seams / Banding along Pylon height
    for seam_z in [2.40, 4.20, 6.00]:
        seam_band = csc.create_cube(f"Pylon_Seam_Band_Z{int(seam_z*10)}",
                                    size=(pylon_w + 0.08, pylon_d + 0.08, 0.16),
                                    location=(pylon_center_x, pylon_center_y, loc_z + seam_z),
                                    material=mats['steel_dark'], parent=root)
        csc.add_bevel_modifier(seam_band, width=0.012, segments=1)

    # Vertical Conduit Channel Ribs on Front Face (Y-)
    front_y = pylon_center_y - pylon_d * 0.5
    for rib_x in [-0.42, 0.42]:
        rib = csc.create_cube(f"Pylon_Vertical_Rib_{rib_x}",
                              size=(0.20, 0.12, pylon_h - 0.60),
                              location=(pylon_center_x + rib_x, front_y - 0.05, loc_z + 0.45 + (pylon_h - 0.60)*0.5),
                              material=mats['steel_dark'], parent=root)
        csc.add_bevel_modifier(rib, width=0.01, segments=1)

    # Vertical Glowing Orange / Amber LED Strip Lights near base (Z: 0.7m to 2.1m)
    amber_strip_z = loc_z + 1.40
    for ox in [-0.22, 0.22]:
        # Recessed dark housing
        csc.create_cube(f"Amber_Housing_{ox}", size=(0.14, 0.08, 1.40),
                        location=(pylon_center_x + ox, front_y - 0.04, amber_strip_z),
                        material=mats['steel_dark'], parent=root)
        # Glowing vertical amber neon light bar
        csc.create_cube(f"Amber_LED_Strip_{ox}", size=(0.06, 0.02, 1.20),
                        location=(pylon_center_x + ox, front_y - 0.085, amber_strip_z),
                        material=mats['orange_glow'], parent=root)

    # Hydraulic / Conduit Piston Cylinder running vertically on side of column
    csc.create_cylinder("Pylon_Hydraulic_Cylinder", radius=0.08, depth=3.80,
                        location=(pylon_center_x + pylon_w * 0.5 + 0.06, pylon_center_y - 0.25, loc_z + 4.2),
                        vertices=16, material=mats['steel_dark'], parent=root)
    # Piston collars
    for cz in [2.35, 4.25, 6.05]:
        csc.create_cylinder(f"Hydraulic_Collar_{int(cz*10)}", radius=0.11, depth=0.12,
                            location=(pylon_center_x + pylon_w * 0.5 + 0.06, pylon_center_y - 0.25, loc_z + cz),
                            vertices=16, material=mats['steel_main'], parent=root)

    # Secondary Support Column behind pylon (depth dimension)
    rear_col_x = pylon_center_x + 0.60
    rear_col_y = pylon_center_y + 1.25
    rear_col = csc.create_cube("Rear_Support_Column", size=(0.60, 0.60, pylon_h * 0.85),
                               location=(rear_col_x, rear_col_y, loc_z + (pylon_h * 0.85) * 0.5),
                               material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(rear_col, width=0.02, segments=1)

    # Rear column foot
    csc.create_cube("Rear_Column_Foot", size=(0.85, 0.85, 0.35),
                    location=(rear_col_x, rear_col_y, loc_z + 0.175),
                    material=mats['steel_dark'], parent=root)

    # -----------------------------------------------------------------------
    # 2. Diagonal Cantilever Strut (Knee Brace Arm)
    # -----------------------------------------------------------------------
    # Diagonal beam spanning from (pylon_center_x + 0.4, pylon_center_y, 4.4) to (pylon_center_x + 3.8, pylon_center_y, 8.1)
    strut_start = Vector((pylon_center_x + 0.45, pylon_center_y, loc_z + 4.30))
    strut_end   = Vector((pylon_center_x + 3.85, pylon_center_y, loc_z + pylon_h - 0.15))

    strut_arm = csc.create_angled_beam("Cantilever_Knee_Strut", strut_start, strut_end,
                                       size_xy=(0.42, 0.48), material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(strut_arm, width=0.02, segments=2)

    # Lower Gusset Bracket at Pillar Connection
    lower_bracket_pos = (pylon_center_x + 0.45, pylon_center_y, loc_z + 4.30)
    lower_bracket = csc.create_cube("Strut_Lower_Gusset", size=(0.55, 0.58, 0.70),
                                    location=lower_bracket_pos, material=mats['steel_dark'], parent=root)
    csc.add_bevel_modifier(lower_bracket, width=0.02, segments=1)

    # Upper Gusset Bracket at Deck Connection
    upper_bracket_pos = (pylon_center_x + 3.85, pylon_center_y, loc_z + pylon_h - 0.20)
    upper_bracket = csc.create_cube("Strut_Upper_Gusset", size=(0.60, 0.58, 0.55),
                                    location=upper_bracket_pos, material=mats['steel_dark'], parent=root)
    csc.add_bevel_modifier(upper_bracket, width=0.02, segments=1)

    # Secondary internal diagonal brace strut
    sub_start = Vector((pylon_center_x + 0.45, pylon_center_y, loc_z + 6.20))
    sub_end   = Vector((pylon_center_x + 2.20, pylon_center_y, loc_z + pylon_h - 0.20))
    sub_arm = csc.create_angled_beam("Cantilever_Sub_Strut", sub_start, sub_end,
                                     size_xy=(0.28, 0.32), material=mats['steel_dark'], parent=root)
    csc.add_bevel_modifier(sub_arm, width=0.015, segments=1)

    # -----------------------------------------------------------------------
    # 3. Cantilevered Walkway / Observation Deck Platform (Z: 8.2 to 9.2m)
    # -----------------------------------------------------------------------
    # Deck extends from X = pylon_center_x - 0.8 to X = pylon_center_x + 6.5
    deck_length = 7.30
    deck_width  = 2.40
    deck_thick  = 0.75
    deck_center_x = pylon_center_x + 2.85
    deck_center_y = pylon_center_y
    deck_top_z    = loc_z + pylon_h + deck_thick

    # Main Deck Girder Structure
    deck_box = csc.create_cube("Gantry_Deck_Main", size=(deck_length, deck_width, deck_thick),
                               location=(deck_center_x, deck_center_y, loc_z + pylon_h + deck_thick * 0.5),
                               material=mats['steel_main'], parent=root)
    csc.add_bevel_modifier(deck_box, width=0.035, segments=2)

    # Underside Transverse Structural Ribs (Joists)
    num_ribs = 7
    rib_spacing = (deck_length - 0.8) / (num_ribs - 1)
    for r in range(num_ribs):
        rx = (deck_center_x - deck_length * 0.5 + 0.4) + r * rib_spacing
        csc.create_cube(f"Deck_Under_Rib_{r}", size=(0.14, deck_width + 0.08, 0.18),
                        location=(rx, deck_center_y, loc_z + pylon_h - 0.09),
                        material=mats['steel_dark'], parent=root)

    # Cantilever Overhang Nose Bevel / End Cap (Far Right)
    nose_x = deck_center_x + deck_length * 0.5
    nose_cap = csc.create_cube("Deck_Nose_Cap", size=(0.35, deck_width + 0.05, deck_thick * 0.85),
                               location=(nose_x - 0.15, deck_center_y, loc_z + pylon_h + deck_thick * 0.5),
                               material=mats['steel_dark'], parent=root)
    csc.add_bevel_modifier(nose_cap, width=0.02, segments=1)

    # -----------------------------------------------------------------------
    # 4. Glowing Neon Light Bars on Platform Fascia (Front Edge)
    # -----------------------------------------------------------------------
    # Side panel of deck facing camera (Y = deck_center_y - deck_width*0.5)
    fascia_y = deck_center_y - deck_width * 0.5 - 0.015
    light_z  = loc_z + pylon_h + deck_thick * 0.65

    # Light 1: Glowing Cyan Neon Strip (Left segment)
    cyan_strip_x = deck_center_x - 0.85
    cyan_strip_len = 0.85
    # Bezel housing
    csc.create_cube("Gantry_Cyan_Light_Bezel", size=(cyan_strip_len + 0.12, 0.06, 0.18),
                    location=(cyan_strip_x, fascia_y - 0.02, light_z),
                    material=mats['steel_dark'], parent=root)
    # Glowing Cyan Bar
    csc.create_cube("Gantry_Neon_Cyan_Strip", size=(cyan_strip_len, 0.02, 0.09),
                    location=(cyan_strip_x, fascia_y - 0.055, light_z),
                    material=mats['cyan_glow'], parent=root)

    # Light 2: Glowing Violet-White Neon Strip (Right segment)
    purple_strip_x = deck_center_x + 2.25
    purple_strip_len = 0.95
    # Bezel housing
    csc.create_cube("Gantry_Purple_Light_Bezel", size=(purple_strip_len + 0.12, 0.06, 0.18),
                    location=(purple_strip_x, fascia_y - 0.02, light_z),
                    material=mats['steel_dark'], parent=root)
    # Glowing Violet-White Bar
    csc.create_cube("Gantry_Neon_Purple_Strip", size=(purple_strip_len, 0.02, 0.09),
                    location=(purple_strip_x, fascia_y - 0.055, light_z),
                    material=mats['purple_glow'], parent=root)

    # -----------------------------------------------------------------------
    # 5. Industrial Safety Perimeter Railings (Z: 8.95m to 10.15m)
    # -----------------------------------------------------------------------
    rail_h = 1.15
    stanchion_size = 0.06
    deck_floor_z = deck_top_z

    # Front Edge Railing Stanchions
    num_posts = 8
    post_spacing = (deck_length - 0.4) / (num_posts - 1)
    for p in range(num_posts):
        px = (deck_center_x - deck_length * 0.5 + 0.2) + p * post_spacing
        post_y = deck_center_y - deck_width * 0.5 + 0.08
        csc.create_cube(f"Front_Rail_Post_{p}", size=(stanchion_size, stanchion_size, rail_h),
                        location=(px, post_y, deck_floor_z + rail_h * 0.5),
                        material=mats['steel_dark'], parent=root)

    # Front Top Handrail (Horizontal Tube)
    csc.create_cylinder("Front_Top_Handrail", radius=0.028, depth=deck_length - 0.3,
                        location=(deck_center_x, deck_center_y - deck_width * 0.5 + 0.08, deck_floor_z + rail_h),
                        rotation=(0, math.radians(90.0), 0),
                        vertices=12, material=mats['steel_dark'], parent=root)

    # Front Mid Safety Rail (Horizontal Tube)
    csc.create_cylinder("Front_Mid_Safety_Rail", radius=0.018, depth=deck_length - 0.3,
                        location=(deck_center_x, deck_center_y - deck_width * 0.5 + 0.08, deck_floor_z + rail_h * 0.52),
                        rotation=(0, math.radians(90.0), 0),
                        vertices=12, material=mats['steel_dark'], parent=root)

    # Front Kickplate / Toeboard
    csc.create_cube("Front_Kickplate", size=(deck_length - 0.3, 0.025, 0.16),
                    location=(deck_center_x, deck_center_y - deck_width * 0.5 + 0.08, deck_floor_z + 0.08),
                    material=mats['steel_dark'], parent=root)

    # Far Right End Railing (Nose end of platform)
    right_x = deck_center_x + deck_length * 0.5 - 0.08
    csc.create_cylinder("Right_Top_Handrail", radius=0.028, depth=deck_width - 0.2,
                        location=(right_x, deck_center_y, deck_floor_z + rail_h),
                        rotation=(math.radians(90.0), 0, 0),
                        vertices=12, material=mats['steel_dark'], parent=root)
    csc.create_cylinder("Right_Mid_Safety_Rail", radius=0.018, depth=deck_width - 0.2,
                        location=(right_x, deck_center_y, deck_floor_z + rail_h * 0.52),
                        rotation=(math.radians(90.0), 0, 0),
                        vertices=12, material=mats['steel_dark'], parent=root)

    # Rear Edge Handrail (Top & Mid)
    rear_rail_y = deck_center_y + deck_width * 0.5 - 0.08
    csc.create_cylinder("Rear_Top_Handrail", radius=0.028, depth=deck_length - 0.3,
                        location=(deck_center_x, rear_rail_y, deck_floor_z + rail_h),
                        rotation=(0, math.radians(90.0), 0),
                        vertices=12, material=mats['steel_dark'], parent=root)
    csc.create_cylinder("Rear_Mid_Safety_Rail", radius=0.018, depth=deck_length - 0.3,
                        location=(deck_center_x, rear_rail_y, deck_floor_z + rail_h * 0.52),
                        rotation=(0, math.radians(90.0), 0),
                        vertices=12, material=mats['steel_dark'], parent=root)
    for p in range(num_posts):
        px = (deck_center_x - deck_length * 0.5 + 0.2) + p * post_spacing
        csc.create_cube(f"Rear_Rail_Post_{p}", size=(stanchion_size, stanchion_size, rail_h),
                        location=(px, rear_rail_y, deck_floor_z + rail_h * 0.5),
                        material=mats['steel_dark'], parent=root)

    # -----------------------------------------------------------------------
    # 6. Hanging Cyberpunk Conduit Cables (Catenary Droop under Cantilever)
    # -----------------------------------------------------------------------
    # Cable 1: Hanging from outer deck underside back to main pillar mid-height
    c1_start = (deck_center_x + 2.5, deck_center_y - 0.45, loc_z + pylon_h - 0.15)
    c1_end   = (pylon_center_x + 0.55, deck_center_y - 0.40, loc_z + 4.90)
    csc.create_catenary_cable("Cantilever_Cable_1", c1_start, c1_end,
                              sag=0.55, radius=0.038, material=mats['cable'], parent=root)

    # Cable 2: Second bundle swooping with slightly different droop
    c2_start = (deck_center_x + 2.9, deck_center_y - 0.30, loc_z + pylon_h - 0.15)
    c2_end   = (pylon_center_x + 0.55, deck_center_y - 0.25, loc_z + 4.60)
    csc.create_catenary_cable("Cantilever_Cable_2", c2_start, c2_end,
                              sag=0.75, radius=0.030, material=mats['cable'], parent=root)

    # Cable 3: Inner cable loop
    c3_start = (deck_center_x + 1.4, deck_center_y - 0.48, loc_z + pylon_h - 0.15)
    c3_end   = (pylon_center_x + 0.55, deck_center_y - 0.48, loc_z + 5.20)
    csc.create_catenary_cable("Cantilever_Cable_3", c3_start, c3_end,
                              sag=0.35, radius=0.032, material=mats['cable'], parent=root)

    print(f"[Prop Built] Cantilever Gantry created at {location}")
    return root


if __name__ == '__main__':
    # Test standalone generation
    for obj in list(bpy.context.scene.objects):
        bpy.data.objects.remove(obj, do_unlink=True)
    build_prop()
