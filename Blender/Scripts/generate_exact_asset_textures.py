"""
Generates exact PBR texture sets (BaseColor, Normal, Roughness, Metallic, Emissive)
for all 56 individual asset references in Assets/Game_Assets/Individual_Asset_References/.
"""

import os
import glob
from PIL import Image, ImageFilter
import numpy as np
from scipy.signal import convolve2d

REPO_ROOT = r"d:\unreal engine"
REF_DIR = os.path.join(REPO_ROOT, "Assets", "Game_Assets", "Individual_Asset_References")
OUT_DIR = os.path.join(REPO_ROOT, "Assets", "Textures", "Individual")
os.makedirs(OUT_DIR, exist_ok=True)

# Also ensure subfolders exist for UE imports
os.makedirs(os.path.join(REPO_ROOT, "Assets", "Textures", "BaseColor"), exist_ok=True)
os.makedirs(os.path.join(REPO_ROOT, "Assets", "Textures", "Normal"), exist_ok=True)
os.makedirs(os.path.join(REPO_ROOT, "Assets", "Textures", "Roughness"), exist_ok=True)
os.makedirs(os.path.join(REPO_ROOT, "Assets", "Textures", "Metallic"), exist_ok=True)
os.makedirs(os.path.join(REPO_ROOT, "Assets", "Textures", "Emissive"), exist_ok=True)

def process_asset(ref_file):
    base_name = os.path.splitext(os.path.basename(ref_file))[0]
    img = Image.open(ref_file).convert("RGB")
    arr = np.array(img)
    h, w = arr.shape[:2]

    # Detect text banner at bottom
    text_start_row = int(h * 0.7)
    for r in range(int(h * 0.58), h):
        if (arr[r] > 190).sum() > 18:
            text_start_row = max(int(h * 0.55), r - 4)
            break

    crop = img.crop((0, 0, w, text_start_row))
    # Resize to clean 1024x1024 power-of-two texture
    base_color = crop.resize((1024, 1024), Image.Resampling.LANCZOS)
    bc_arr = np.array(base_color, dtype=np.float32)

    # 1. BaseColor
    bc_path = os.path.join(OUT_DIR, f"T_{base_name}_BaseColor.png")
    base_color.save(bc_path)
    base_color.save(os.path.join(REPO_ROOT, "Assets", "Textures", "BaseColor", f"T_{base_name}_BaseColor.png"))

    # 2. Normal Map (Sobel filter for surface depth)
    gray = base_color.convert("L")
    gray_arr = np.array(gray, dtype=np.float32)
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float32)
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float32)
    gx = convolve2d(gray_arr, sobel_x, mode='same', boundary='symm') / 8.0
    gy = convolve2d(gray_arr, sobel_y, mode='same', boundary='symm') / 8.0

    strength = 2.5
    nz = 255.0 / max(strength, 0.1)
    norm = np.sqrt(gx**2 + gy**2 + nz**2)
    nx = (-gx / norm * 127.5 + 128).clip(0, 255).astype(np.uint8)
    ny = (-gy / norm * 127.5 + 128).clip(0, 255).astype(np.uint8)
    nz_c = (nz / norm * 127.5 + 128).clip(0, 255).astype(np.uint8)

    normal_img = Image.fromarray(np.stack([nx, ny, nz_c], axis=-1))
    normal_img.save(os.path.join(OUT_DIR, f"T_{base_name}_Normal.png"))
    normal_img.save(os.path.join(REPO_ROOT, "Assets", "Textures", "Normal", f"T_{base_name}_Normal.png"))

    # 3. Emissive Map
    r, g, b = bc_arr[:,:,0], bc_arr[:,:,1], bc_arr[:,:,2]
    is_cyan = (b > 150) & (g > 130) & (b > r + 25)
    is_purple = (r > 140) & (b > 140) & (r > g + 35)
    is_red = (r > 175) & (g < 100) & (b < 100)
    is_yellow = (r > 190) & (g > 160) & (b < 80)
    is_white_screen = (r > 230) & (g > 230) & (b > 230)

    # Lights and screens should glow
    emissive_mask = np.zeros_like(r, dtype=np.float32)
    if "Light" in base_name or "Neon" in base_name or "Screen" in base_name or "Terminal" in base_name or "Camera" in base_name or "Emergency" in base_name:
        emissive_mask = (is_cyan | is_purple | is_red | is_white_screen).astype(np.float32)
    else:
        # Subtle accents on consoles/panels
        emissive_mask = (is_cyan | is_purple).astype(np.float32) * 0.8

    em_img = Image.fromarray((emissive_mask * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.0))
    em_rgb = (np.array(base_color) * (np.array(em_img)[:,:,None] / 255.0)).astype(np.uint8)
    Image.fromarray(em_rgb).save(os.path.join(OUT_DIR, f"T_{base_name}_Emissive.png"))
    Image.fromarray(em_rgb).save(os.path.join(REPO_ROOT, "Assets", "Textures", "Emissive", f"T_{base_name}_Emissive.png"))

    # 4. Metallic Map
    # Cyberpunk structural elements are metal; rubber, glass, painted panels are less metal
    lum = (r * 0.299 + g * 0.587 + b * 0.114)
    sat = (np.maximum(np.maximum(r, g), b) - np.minimum(np.minimum(r, g), b))
    # Metals typically have lower saturation unless colored alloy, and higher brightness
    metal_mask = ((sat < 50) & (lum > 40) & (lum < 220)).astype(np.float32) * 0.85
    # Non-metals
    metal_mask[is_cyan | is_purple | is_red | is_yellow] = 0.1
    met_img = Image.fromarray((metal_mask * 255).astype(np.uint8))
    met_img.save(os.path.join(OUT_DIR, f"T_{base_name}_Metallic.png"))
    met_img.save(os.path.join(REPO_ROOT, "Assets", "Textures", "Metallic", f"T_{base_name}_Metallic.png"))

    # 5. Roughness Map
    # Smooth surfaces: neon tubes, screens, polished chrome -> low roughness
    # Rough surfaces: concrete barriers, rubber grips, rusty pipes -> high roughness
    rough_val = np.full_like(lum, 140, dtype=np.uint8) # default industrial metallic roughness ~0.55
    rough_val[is_cyan | is_purple | is_white_screen] = 30 # glossy neons / screens
    if "Barrier" in base_name:
        rough_val[:] = 210 # matte concrete/composite
    elif "Grate" in base_name or "Rust" in base_name:
        rough_val = (lum * 0.5 + 100).clip(120, 230).astype(np.uint8)

    rough_img = Image.fromarray(rough_val)
    rough_img.save(os.path.join(OUT_DIR, f"T_{base_name}_Roughness.png"))
    rough_img.save(os.path.join(REPO_ROOT, "Assets", "Textures", "Roughness", f"T_{base_name}_Roughness.png"))

    print(f"Processed: {base_name}")

def main():
    files = sorted(glob.glob(os.path.join(REF_DIR, "*.png")))
    print(f"Found {len(files)} reference files to process.")
    for f in files:
        process_asset(f)
    print("All 56 PBR texture sets generated successfully!")

if __name__ == "__main__":
    main()
