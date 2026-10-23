"""
Generates high quality 2K Decals, Masks, and Ambient Occlusion textures for Sector 09.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO_ROOT = r"d:\unreal engine"
TEX_DIR = os.path.join(REPO_ROOT, "Assets", "Textures")
DECALS_DIR = os.path.join(TEX_DIR, "Decals")
MASKS_DIR = os.path.join(TEX_DIR, "Masks")
AO_DIR = os.path.join(TEX_DIR, "Roughness")  # or shared/ORM

os.makedirs(DECALS_DIR, exist_ok=True)
os.makedirs(MASKS_DIR, exist_ok=True)

RES = 2048

# 1. T_Decal_Sector09_Warning (Stenciled SECTOR 09 with warning chevron and cyan subtext)
img_sec09 = Image.new("RGBA", (RES, RES), (0, 0, 0, 0))
draw = ImageDraw.Draw(img_sec09)
# Outer box
draw.rectangle([100, 100, RES-100, RES-100], outline=(0, 220, 255, 230), width=16)
# Corner brackets
for x, y, dx, dy in [(140, 140, 200, 0), (140, 140, 0, 200), (RES-140, 140, -200, 0), (RES-140, 140, 0, 200),
                    (140, RES-140, 200, 0), (140, RES-140, 0, -200), (RES-140, RES-140, -200, 0), (RES-140, RES-140, 0, -200)]:
    draw.line([x, y, x+dx, y+dy], fill=(0, 220, 255, 255), width=24)
# Warning Chevrons top and bottom
for cx in range(250, RES-250, 150):
    draw.polygon([(cx, 160), (cx+70, 160), (cx+110, 230), (cx+40, 230)], fill=(255, 200, 0, 240))
    draw.polygon([(cx, RES-230), (cx+70, RES-230), (cx+110, RES-160), (cx+40, RES-160)], fill=(255, 200, 0, 240))
# Text
draw.text((RES//2 - 480, RES//2 - 220), "SECTOR 09", fill=(240, 245, 255, 255), font_size=160)
draw.text((RES//2 - 580, RES//2 + 20), "RESTRICTED ACCESS — LEVEL 01", fill=(0, 230, 255, 255), font_size=65)
draw.text((RES//2 - 380, RES//2 + 130), "AUTHORIZATION CODE: WAKE-UP-CALL", fill=(255, 70, 70, 255), font_size=40)
img_sec09.save(os.path.join(DECALS_DIR, "T_Decal_Sector09_Warning_BaseColor.png"))

# 2. T_Decal_Hazard_Stripe (Yellow & Black angled safety bands)
img_hazard = Image.new("RGBA", (RES, RES), (15, 15, 18, 255))
draw_h = ImageDraw.Draw(img_hazard)
stripe_w = 120
for x in range(-RES, RES*2, stripe_w * 2):
    draw_h.polygon([(x, 0), (x + stripe_w, 0), (x + stripe_w + RES, RES), (x + RES, RES)], fill=(240, 180, 5, 255))
# Grime and weathering overlay
noise = np.random.normal(0, 15, (RES, RES)).astype(np.int16)
arr_h = np.array(img_hazard, dtype=np.int16)
arr_h[..., :3] = np.clip(arr_h[..., :3] + noise[..., None], 0, 255)
Image.fromarray(arr_h.astype(np.uint8)).save(os.path.join(DECALS_DIR, "T_Decal_Hazard_Stripe_BaseColor.png"))

# 3. T_Decal_Locked_Gate_Symbol (Red Neon biometric / lock emblem)
img_lock = Image.new("RGBA", (RES, RES), (0, 0, 0, 0))
draw_l = ImageDraw.Draw(img_lock)
# Hexagon outline
hex_pts = []
for i in range(6):
    ang = i * (np.pi / 3) + np.pi/6
    hex_pts.append((RES//2 + int(600 * np.cos(ang)), RES//2 + int(600 * np.sin(ang))))
draw_l.polygon(hex_pts, outline=(255, 30, 30, 255), width=28)
# Padlock body
draw_l.rounded_rectangle([RES//2 - 250, RES//2 - 50, RES//2 + 250, RES//2 + 350], radius=40, fill=(255, 30, 30, 230))
# Padlock shackle
draw_l.arc([RES//2 - 180, RES//2 - 380, RES//2 + 180, RES//2 + 50], start=180, end=0, fill=(255, 30, 30, 230), width=60)
draw_l.text((RES//2 - 260, RES//2 + 420), "SECURITY LOCK ENGAGED", fill=(255, 50, 50, 255), font_size=42)
img_lock.save(os.path.join(DECALS_DIR, "T_Decal_Locked_Gate_Symbol.png"))

# 4. T_Decal_BioScan_Handprint (Cyan interactive hand scanner emblem)
img_hand = Image.new("RGBA", (RES, RES), (0, 0, 0, 0))
draw_hand = ImageDraw.Draw(img_hand)
# Concentric target circles
draw_hand.ellipse([RES//2 - 550, RES//2 - 550, RES//2 + 550, RES//2 + 550], outline=(0, 230, 255, 180), width=12)
draw_hand.ellipse([RES//2 - 400, RES//2 - 400, RES//2 + 400, RES//2 + 400], outline=(0, 230, 255, 230), width=18)
# Palm & fingers schematic
draw_hand.ellipse([RES//2 - 180, RES//2 - 50, RES//2 + 180, RES//2 + 250], fill=(0, 240, 255, 220))
# Fingers
finger_offsets = [(-140, -220, 45, 240), (-50, -280, 50, 290), (50, -270, 50, 280), (140, -200, 45, 220), (220, 30, 50, 160)]
for fx, fy, fw, fh in finger_offsets:
    draw_hand.rounded_rectangle([RES//2 + fx - fw//2, RES//2 + fy, RES//2 + fx + fw//2, RES//2 + fy + fh], radius=22, fill=(0, 240, 255, 220))
draw_hand.text((RES//2 - 280, RES//2 + 360), "BIOMETRIC IDENT SCANNER", fill=(0, 240, 255, 255), font_size=42)
img_hand.save(os.path.join(DECALS_DIR, "T_Decal_BioScan_Handprint.png"))

# 5. T_Mask_EdgeWear_Scratches (Roughness/Metallic mask for edge wear)
np.random.seed(42)
scratches = np.zeros((RES, RES), dtype=np.uint8)
img_scratch = Image.fromarray(scratches)
draw_sc = ImageDraw.Draw(img_scratch)
for _ in range(800):
    x1, y1 = np.random.randint(0, RES, 2)
    length = np.random.randint(30, 250)
    angle = np.random.uniform(0, 2 * np.pi)
    x2 = int(x1 + length * np.cos(angle))
    y2 = int(y1 + length * np.sin(angle))
    intensity = np.random.randint(60, 220)
    draw_sc.line([x1, y1, x2, y2], fill=intensity, width=np.random.randint(1, 4))
img_scratch = img_scratch.filter(ImageFilter.GaussianBlur(1.0))
img_scratch.save(os.path.join(MASKS_DIR, "T_Mask_EdgeWear_Scratches.png"))

# 6. T_Mask_Dirt_Grime (Perlin-like noise mask for ambient grime)
x = np.linspace(0, 8 * np.pi, RES)
y = np.linspace(0, 8 * np.pi, RES)
X, Y = np.meshgrid(x, y)
grime = (np.sin(X) * np.cos(Y) * 0.5 + 0.5) * 128
grime += (np.sin(2 * X + 1) * np.cos(2 * Y + 1) * 0.5 + 0.5) * 64
grime += np.random.normal(0, 18, (RES, RES))
grime = np.clip(grime, 0, 255).astype(np.uint8)
Image.fromarray(grime).save(os.path.join(MASKS_DIR, "T_Mask_Dirt_Grime.png"))

# 7. T_Mask_Hexagon_Grate (Hexagonal perforated mask for metal grate and ventilation)
img_hex = Image.new("L", (RES, RES), 0)
draw_hex = ImageDraw.Draw(img_hex)
r = 45
dx = int(r * 1.5)
dy = int(r * np.sqrt(3))
for col in range(-1, RES // dx + 2):
    for row in range(-1, RES // dy + 2):
        cx = col * dx
        cy = row * dy + (dx // 2 if col % 2 == 1 else 0)
        pts = [(cx + int(r * 0.7 * np.cos(a)), cy + int(r * 0.7 * np.sin(a))) for a in np.linspace(0, 2*np.pi, 7)[:-1]]
        draw_hex.polygon(pts, fill=255)
img_hex.save(os.path.join(MASKS_DIR, "T_Mask_Hexagon_Grate.png"))

print("Generated 4 Decals and 3 Masks in 2K resolution.")
