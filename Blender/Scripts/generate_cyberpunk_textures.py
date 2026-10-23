"""
Cyberpunk 2048x2048 PBR Texture Generator
Generates production-grade PBR texture sets (BaseColor, Normal, Roughness, Metallic, Emissive)
for Sector 09 Level 1 assets using NumPy and PIL.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = r"D:\unreal engine"
TEXTURE_DIRS = [
    os.path.join(REPO_ROOT, "Assets", "Level_1", "Textures"),
    os.path.join(REPO_ROOT, "Blender", "FBX", "Sector09", "Textures")
]

for d in TEXTURE_DIRS:
    os.makedirs(d, exist_ok=True)

SIZE = 2048


def height_to_normal(height_map, strength=4.0):
    """Converts a normalized height map (0..1 float) into a tangent-space DirectX normal map."""
    gx, gy = np.gradient(height_map)
    gx *= strength
    gy *= strength
    nz = np.ones_like(height_map)
    norm = np.sqrt(gx**2 + gy**2 + nz**2)
    nx = -gx / norm
    ny = -gy / norm # Inverted for Unreal Engine DirectX format
    nz = nz / norm

    r = ((nx * 0.5 + 0.5) * 255.0).clip(0, 255).astype(np.uint8)
    g = ((ny * 0.5 + 0.5) * 255.0).clip(0, 255).astype(np.uint8)
    b = ((nz * 0.5 + 0.5) * 255.0).clip(0, 255).astype(np.uint8)
    return np.stack([r, g, b], axis=-1)


def save_texture_set(prefix, base_rgb, height_map, roughness, metallic, emissive_rgb=None):
    normal_rgb = height_to_normal(height_map, strength=5.0)

    img_base = Image.fromarray(base_rgb.astype(np.uint8))
    img_normal = Image.fromarray(normal_rgb)
    img_rough = Image.fromarray((roughness * 255.0).clip(0, 255).astype(np.uint8))
    img_metal = Image.fromarray((metallic * 255.0).clip(0, 255).astype(np.uint8))

    if emissive_rgb is not None:
        img_emissive = Image.fromarray(emissive_rgb.astype(np.uint8))
    else:
        img_emissive = Image.fromarray(np.zeros((SIZE, SIZE, 3), dtype=np.uint8))

    for d in TEXTURE_DIRS:
        img_base.save(os.path.join(d, f"{prefix}_BaseColor.png"))
        img_normal.save(os.path.join(d, f"{prefix}_Normal.png"))
        img_rough.save(os.path.join(d, f"{prefix}_Roughness.png"))
        img_metal.save(os.path.join(d, f"{prefix}_Metallic.png"))
        img_emissive.save(os.path.join(d, f"{prefix}_Emissive.png"))

    print(f"[TEXTURES GENERATED] {prefix} (2048x2048)")


# ---------------------------------------------------------------------------
# 1. THEME: WALL PANEL (Industrial Cyberpunk Wall Panels, Doors, Frames, Gates)
# ---------------------------------------------------------------------------

def generate_wall_panel_textures():
    print("Generating Wall Panel PBR Textures...")
    # Base dark slate metal
    base = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    base[:, :] = [28, 35, 45] # Gunmetal slate base

    # High-frequency brushed metal grain
    noise = np.random.normal(0, 7.0, (SIZE, SIZE))
    base += noise[:, :, None]

    height = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.5
    roughness = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.45
    metallic = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.8
    emissive = np.zeros((SIZE, SIZE, 3), dtype=np.float32)

    # Convert to PIL for crisp vector panel drawing
    pil_img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(pil_img)

    # 4 Large panel quadrants with beveled seams
    quads = [
        (64, 64, 980, 980),
        (1068, 64, 1984, 980),
        (64, 1068, 980, 1984),
        (1068, 1068, 1984, 1984)
    ]

    for (x1, y1, x2, y2) in quads:
        # Inner panel is lighter slate enamel
        draw.rectangle([x1, y1, x2, y2], fill=(42, 54, 70), outline=(15, 18, 24), width=12)
        height[y1:y2, x1:x2] = 0.65
        height[y1-6:y1+6, x1:x2] = 0.2 # Seam trench
        height[y2-6:y2+6, x1:x2] = 0.2
        height[y1:y2, x1-6:x1+6] = 0.2
        height[y1:y2, x2-6:x2+6] = 0.2

        # Rivets along panel perimeter
        for rx in range(x1 + 40, x2 - 40, 70):
            for ry in [y1 + 24, y2 - 24]:
                draw.ellipse([rx-8, ry-8, rx+8, ry+8], fill=(160, 175, 190), outline=(10, 12, 16))
                height[ry-8:ry+8, rx-8:rx+8] = 0.95
                metallic[ry-8:ry+8, rx-8:rx+8] = 0.95
                roughness[ry-8:ry+8, rx-8:rx+8] = 0.2

    # Hazard Chevron Stripe Bar across bottom quadrant
    stripe_w = 40
    for x in range(0, SIZE + 300, stripe_w * 2):
        pts = [(x, 1500), (x + stripe_w, 1500), (x + stripe_w - 200, 1700), (x - 200, 1700)]
        draw.polygon(pts, fill=(240, 185, 15)) # Vivid Caution Yellow
    for x in range(stripe_w, SIZE + 300, stripe_w * 2):
        pts = [(x, 1500), (x + stripe_w, 1500), (x + stripe_w - 200, 1700), (x - 200, 1700)]
        draw.polygon(pts, fill=(15, 15, 18)) # Carbon Black
    roughness[1500:1700, :] = 0.6
    metallic[1500:1700, :] = 0.1

    # Stencil technical lettering
    draw.text((120, 120), "SECTOR 09 — LEVEL 1", fill=(210, 220, 230))
    draw.text((120, 160), "HYDRAULIC BULKHEAD // MODULAR SECTION A", fill=(130, 145, 160))
    draw.text((1120, 120), "RESTRICTED PERSONNEL ONLY", fill=(240, 185, 15))
    draw.text((1120, 160), "AUTOMATIC LOCKDOWN ENABLED", fill=(180, 50, 40))

    # Glowing Cyan Neon Conduit Channel in center
    draw.rectangle([980, 100, 1068, 1948], fill=(10, 12, 16))
    draw.rectangle([1016, 120, 1032, 1928], fill=(0, 240, 255)) # Glowing cyan neon
    emissive[120:1928, 1016:1032] = [0.0, 240.0, 255.0]
    height[100:1948, 980:1068] = 0.3 # Recessed trench
    height[120:1928, 1016:1032] = 0.7

    base_final = np.array(pil_img, dtype=np.float32)
    save_texture_set("T_Cyberpunk_Wall_Panel", base_final, height, roughness, metallic, emissive)


# ---------------------------------------------------------------------------
# 2. THEME: FLOOR & GRATE (Industrial Diamond Plate, Drainage Grates, Walkways)
# ---------------------------------------------------------------------------

def generate_floor_grate_textures():
    print("Generating Floor & Grate PBR Textures...")
    base = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    base[:, :] = [35, 38, 42]

    height = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.4
    roughness = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.35
    metallic = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.95

    # Diamond plate raised grips
    grid_size = 32
    for y in range(0, SIZE, grid_size):
        for x in range(0, SIZE, grid_size):
            offset = (grid_size // 2) if (y // grid_size) % 2 == 1 else 0
            cx = (x + offset) % SIZE
            cy = y
            # Stamp diamond angle
            for d in range(-8, 9):
                w = 8 - abs(d)
                px = (cx + d) % SIZE
                for py_off in range(-w, w + 1):
                    py = (cy + py_off) % SIZE
                    height[py, px] = 0.75
                    base[py, px] = [85, 95, 105] # Highlights on diamond lips
                    roughness[py, px] = 0.2

    # Central heavy ventilation drainage grate (1024x1024)
    x1, y1, x2, y2 = 512, 512, 1536, 1536
    height[y1:y2, x1:x2] = 0.1 # Sunken sump
    base[y1:y2, x1:x2] = [15, 18, 22] # Dark pit
    roughness[y1:y2, x1:x2] = 0.8
    metallic[y1:y2, x1:x2] = 0.6

    # Steel grate bars across the sump
    bar_pitch = 40
    for gy in range(y1 + 20, y2 - 20, bar_pitch):
        height[gy-8:gy+8, x1:x2] = 0.6
        base[gy-8:gy+8, x1:x2] = [110, 120, 130] # Bright galvanized steel
        metallic[gy-8:gy+8, x1:x2] = 0.98
        roughness[gy-8:gy+8, x1:x2] = 0.25

    # Yellow Caution Border around Grate
    pil_img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(pil_img)
    draw.rectangle([x1-30, y1-30, x2+30, y2+30], outline=(245, 195, 20), width=24)
    height[y1-30:y1-6, x1-30:x2+30] = 0.55
    height[y2+6:y2+30, x1-30:x2+30] = 0.55
    height[y1-30:y2+30, x1-30:x1-6] = 0.55
    height[y1-30:y2+30, x2+6:x2+30] = 0.55

    base_final = np.array(pil_img, dtype=np.float32)
    save_texture_set("T_Cyberpunk_Floor_Grate", base_final, height, roughness, metallic)


# ---------------------------------------------------------------------------
# 3. THEME: PIPES & CONDUITS (Heavy Steel, Copper Heat Fins, Flanges, Valves)
# ---------------------------------------------------------------------------

def generate_pipes_textures():
    print("Generating Pipes & Conduits PBR Textures...")
    base = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    base[:, :] = [70, 75, 82] # Cast industrial steel

    height = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.5
    roughness = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.28
    metallic = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.92

    # Cylindrical curvature shading bands
    for x in range(SIZE):
        rad = math.sin((x / SIZE) * math.pi * 4)
        height[:, x] += rad * 0.15
        base[:, x] += rad * 20.0

    # Bolted Flange Ring bands
    for fy in [256, 768, 1280, 1792]:
        height[fy-35:fy+35, :] = 0.85
        base[fy-35:fy+35, :] = [135, 145, 155]
        roughness[fy-35:fy+35, :] = 0.2
        for bx in range(32, SIZE, 64):
            height[fy-12:fy+12, bx-12:bx+12] = 1.0
            base[fy-12:fy+12, bx-12:bx+12] = [210, 220, 230]

    # Stencil pipe markers
    pil_img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(pil_img)
    draw.rectangle([200, 480, 1848, 560], fill=(220, 60, 20)) # Red steam hazard band
    draw.text((300, 500), "HIGH PRESSURE STEAM // LINE 09-B // 350 PSI", fill=(255, 255, 255))
    draw.rectangle([200, 1500, 1848, 1580], fill=(20, 160, 230)) # Cyan coolant band
    draw.text((300, 1520), "CRYOGENIC SUB-COOLANT // DANGER LIQUID NITROGEN", fill=(255, 255, 255))

    base_final = np.array(pil_img, dtype=np.float32)
    save_texture_set("T_Cyberpunk_Pipes_Conduit", base_final, height, roughness, metallic)


# ---------------------------------------------------------------------------
# 4. THEME: CONTAINER CRATE (Corrugated Cargo Containers, RFID Locks, Barrels)
# ---------------------------------------------------------------------------

def generate_crate_textures():
    print("Generating Container Crate PBR Textures...")
    base = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    base[:, :] = [30, 48, 62] # Cyberpunk blue-grey enamel paint

    height = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.5
    roughness = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.4
    metallic = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.35
    emissive = np.zeros((SIZE, SIZE, 3), dtype=np.float32)

    # Corrugated accordion siding (vertical ridges)
    ridge_pitch = 64
    for x in range(0, SIZE, ridge_pitch):
        for w in range(ridge_pitch):
            prof = math.sin((w / ridge_pitch) * math.pi)
            height[:, x + w] = 0.35 + prof * 0.45
            base[:, x + w] += prof * 18.0

    # Heavy corner casting brackets
    pil_img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(pil_img)

    # 4 Corner steel casting plates
    corners = [(0, 0, 256, 256), (SIZE-256, 0, SIZE, 256), (0, SIZE-256, 256, SIZE), (SIZE-256, SIZE-256, SIZE, SIZE)]
    for (cx1, cy1, cx2, cy2) in corners:
        draw.rectangle([cx1, cy1, cx2, cy2], fill=(20, 22, 26), outline=(80, 85, 95), width=8)
        draw.ellipse([cx1+64, cy1+64, cx2-64, cy2-64], fill=(10, 12, 14)) # Hoist pocket
        height[cy1:cy2, cx1:cx2] = 0.9
        metallic[cy1:cy2, cx1:cx2] = 0.95
        roughness[cy1:cy2, cx1:cx2] = 0.3

    # High-Tech RFID Keyless Lock Panel in Center
    draw.rectangle([768, 768, 1280, 1280], fill=(15, 18, 22), outline=(100, 110, 120), width=10)
    draw.rectangle([832, 832, 1216, 1024], fill=(0, 220, 255)) # Glowing cyan display
    emissive[832:1024, 832:1216] = [0.0, 220.0, 255.0]
    draw.text((860, 880), "CARGO SECURED", fill=(0, 20, 30))
    draw.text((860, 930), "LOCK ID: #S09-8842", fill=(0, 20, 30))

    # Hazmat Diamond Warning Placard
    draw.polygon([(1024, 1080), (1140, 1160), (1024, 1240), (908, 1160)], fill=(240, 185, 15), outline=(0, 0, 0), width=6)
    draw.text((980, 1145), "BIO-03", fill=(0, 0, 0))

    base_final = np.array(pil_img, dtype=np.float32)
    save_texture_set("T_Cyberpunk_Container_Crate", base_final, height, roughness, metallic, emissive)


# ---------------------------------------------------------------------------
# 5. THEME: TERMINALS & CONSOLES (Holographic Screens, Keypads, Server Blades)
# ---------------------------------------------------------------------------

def generate_terminal_textures():
    print("Generating Terminal & Console PBR Textures...")
    base = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    base[:, :] = [18, 20, 24] # Matte charcoal technical chassis

    height = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.5
    roughness = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.3
    metallic = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.7
    emissive = np.zeros((SIZE, SIZE, 3), dtype=np.float32)

    pil_img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(pil_img)

    # 1. Main Holographic Monitor Screen (Top Half: 0 to 1024)
    draw.rectangle([64, 64, 1984, 980], fill=(5, 15, 20), outline=(50, 60, 75), width=16)
    height[64:980, 64:1984] = 0.35 # Glass recess
    roughness[64:980, 64:1984] = 0.1
    metallic[64:980, 64:1984] = 0.05

    # Glowing Telemetry Visuals (Cyan & Green Scanlines)
    pil_emiss = Image.fromarray(emissive.astype(np.uint8))
    draw_e = ImageDraw.Draw(pil_emiss)

    # Hex radar & circular telemetry
    draw_e.ellipse([200, 200, 800, 800], outline=(0, 240, 255), width=4)
    draw_e.ellipse([350, 350, 650, 650], outline=(0, 180, 220), width=2)
    draw_e.line([200, 500, 800, 500], fill=(0, 240, 255), width=2)
    draw_e.line([500, 200, 500, 800], fill=(0, 240, 255), width=2)

    # Sine waveform graph
    wave_pts = []
    for wx in range(900, 1900, 8):
        wy = 400 + int(math.sin(wx * 0.05) * 80 + math.cos(wx * 0.02) * 40)
        wave_pts.append((wx, wy))
    draw_e.line(wave_pts, fill=(50, 255, 120), width=4)

    # Terminal Code Readout Lines
    draw_e.text((900, 150), "> SECTOR 09 REACTOR SUBSYSTEM 4: ONLINE", fill=(0, 240, 255))
    draw_e.text((900, 200), "> CORE TEMP: 418.2 K // NEURAL SYNC: 99.4%", fill=(50, 255, 120))
    draw_e.text((900, 250), "> WARNING: GATEWAY 03 PRESSURE DEVIATION", fill=(255, 180, 20))
    draw_e.text((900, 600), "0x8849F2AA  0x00FF8129  0x99482100", fill=(0, 200, 230))
    draw_e.text((900, 650), "0x7721B300  0xA482C091  0x33100844", fill=(0, 200, 230))
    draw_e.text((900, 700), "0x110992FF  0x66542100  0x8849F2AA", fill=(0, 200, 230))

    # Scanlines across screen
    for sy in range(80, 960, 12):
        draw_e.line([80, sy, 1960, sy], fill=(0, 40, 60), width=1)

    # 2. Lower Half: Physical Keyboard, Dials, and Biometric Scanner
    # Keyboard Key Matrix
    key_w, key_h = 44, 44
    for ky in range(1120, 1500, 60):
        for kx in range(120, 1300, 56):
            draw.rectangle([kx, ky, kx + key_w, ky + key_h], fill=(30, 32, 38), outline=(60, 65, 75), width=2)
            height[ky:ky+key_h, kx:kx+key_w] = 0.75
            roughness[ky:ky+key_h, kx:kx+key_w] = 0.35

    # Biometric Palm Scanner Glass Plate
    draw.rectangle([1400, 1120, 1850, 1550], fill=(10, 40, 50), outline=(0, 240, 255), width=8)
    draw_e.rectangle([1408, 1128, 1842, 1542], fill=(0, 70, 90))
    # Glowing hand silhouette
    draw_e.ellipse([1560, 1240, 1690, 1430], outline=(0, 255, 255), width=6)
    draw_e.line([1580, 1240, 1570, 1170], fill=(0, 255, 255), width=6) # Finger 1
    draw_e.line([1610, 1240, 1610, 1150], fill=(0, 255, 255), width=6) # Finger 2
    draw_e.line([1640, 1240, 1645, 1155], fill=(0, 255, 255), width=6) # Finger 3
    draw_e.line([1670, 1240, 1680, 1180], fill=(0, 255, 255), width=6) # Finger 4
    draw_e.line([1560, 1330, 1500, 1300], fill=(0, 255, 255), width=6) # Thumb

    # Indicator LED Array along bottom (Green, Amber, Red)
    for idx, lx in enumerate(range(120, 1850, 90)):
        color = (0, 255, 120) if idx % 3 == 0 else ((255, 180, 10) if idx % 3 == 1 else (255, 30, 30))
        draw.ellipse([lx, 1750, lx + 36, 1786], fill=color, outline=(0, 0, 0), width=4)
        draw_e.ellipse([lx, 1750, lx + 36, 1786], fill=color)
        height[1750:1786, lx:lx+36] = 0.85

    base_final = np.array(pil_img, dtype=np.float32)
    emissive_final = np.array(pil_emiss, dtype=np.float32)
    save_texture_set("T_Cyberpunk_Terminal_Console", base_final, height, roughness, metallic, emissive_final)


# ---------------------------------------------------------------------------
# 6. THEME: NEON LIGHTS (Vibrant Electric Emissive Tubes & Strobe Fixtures)
# ---------------------------------------------------------------------------

def generate_neon_textures():
    print("Generating Neon Light PBR Textures...")
    base = np.zeros((SIZE, SIZE, 3), dtype=np.float32)
    base[:, :] = [15, 15, 18]

    height = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.5
    roughness = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.15
    metallic = np.zeros((SIZE, SIZE), dtype=np.float32) + 0.2
    emissive = np.zeros((SIZE, SIZE, 3), dtype=np.float32)

    pil_img = Image.fromarray(base.clip(0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(pil_img)
    pil_emiss = Image.fromarray(emissive.astype(np.uint8))
    draw_e = ImageDraw.Draw(pil_emiss)

    # 4 Colored neon tube rows (Cyan, Magenta/Purple, Crimson Red, Warm Amber)
    colors = [
        ("Cyan", (0, 240, 255), 180),
        ("Purple", (220, 20, 255), 680),
        ("Red", (255, 25, 25), 1180),
        ("Amber", (255, 150, 15), 1680)
    ]

    for name, col, y_pos in colors:
        # Fixture mounting bar
        draw.rectangle([100, y_pos - 60, 1948, y_pos + 60], fill=(25, 28, 35), outline=(70, 75, 85), width=8)
        height[y_pos-60:y_pos+60, 100:1948] = 0.7
        # Glass neon tube in center
        draw.rectangle([140, y_pos - 24, 1908, y_pos + 24], fill=col)
        draw_e.rectangle([140, y_pos - 24, 1908, y_pos + 24], fill=col)
        height[y_pos-24:y_pos+24, 140:1908] = 0.95
        roughness[y_pos-24:y_pos+24, 140:1908] = 0.05

    base_final = np.array(pil_img, dtype=np.float32)
    emissive_final = np.array(pil_emiss, dtype=np.float32)
    save_texture_set("T_Cyberpunk_Neon_Lights", base_final, height, roughness, metallic, emissive_final)


if __name__ == "__main__":
    print("=" * 70)
    print("  CYBERPUNK 2048x2048 PBR TEXTURE PACK GENERATOR")
    print("=" * 70)
    generate_wall_panel_textures()
    generate_floor_grate_textures()
    generate_pipes_textures()
    generate_crate_textures()
    generate_terminal_textures()
    generate_neon_textures()
    print("=" * 70)
    print("  ALL 6 THEMATIC 2K PBR TEXTURE SETS GENERATED SUCCESSFULLY!")
    print("=" * 70)
