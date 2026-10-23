# 🎨 Sector 09 — 2048x2048 High-Definition PBR Texture Sets

All 56 modular assets are mapped with dedicated 2K PBR texture sets located here:

---

## 📦 Included Texture Sets:

1. **`T_Cyberpunk_Wall_Panel`**:
   - Used by: Wall Panels, Doors, Frames, Gates, Windows, Corner Columns
   - Features: Gunmetal steel panels, beveled seams, rivet matrices, caution hazard chevrons, stencil text (`SECTOR 09`, `RESTRICTED`), cyan conduit lines.

2. **`T_Cyberpunk_Floor_Grate`**:
   - Used by: Floor Slabs, Grates, Ramps, Catwalks, Stairs, Railings
   - Features: Industrial diamond-plate grips, galvanized steel drainage grates, yellow perimeter hazard borders, non-slip tread edges.

3. **`T_Cyberpunk_Pipes_Conduit`**:
   - Used by: Heavy Beams, Straight/Elbow/T-Junction Pipes, Flanges, Cable Trays
   - Features: Brushed industrial steel, bolted flange rings, high-pressure steam/coolant warning stripes, cylindrical depth normals.

4. **`T_Cyberpunk_Container_Crate`**:
   - Used by: Large/Medium/Small Crates, Stacked Crates, Barrels, Jersey Barriers, Pallets
   - Features: Weathered blue-grey enamel paint, corrugated accordion siding, corner casting hoist brackets, RFID digital locks, hazmat hazard diamonds.

5. **`T_Cyberpunk_Terminal_Console`**:
   - Used by: Control Workstations, Information Kiosks, Access Panels, Server Blades, Security Cameras, Desks
   - Features: Glowing cyan/green telemetry radar & waveform displays, scanlines, terminal hexadecimal code, keyboard matrix, biometric palm scanner, indicator LEDs.

6. **`T_Cyberpunk_Neon_Lights`**:
   - Used by: Neon Light Bars, Ceiling Troffers, Emergency Beacons, Street Lights, Monitor Screens
   - Features: High-intensity neon glow (electric cyan, ultraviolet purple, crimson warning red, warm amber).

---

## ⚙️ Unreal Engine 5 Texture Settings:

| Map | Compression Settings | sRGB Checkbox | Texture Group |
|---|---|---|---|
| `_BaseColor.png` | **Default (DXT1/5, BC1/3)** | ✅ **Checked (sRGB ON)** | World |
| `_Normal.png` | **Normalmap (DXT5, BC5)** | ❌ **Unchecked (sRGB OFF)** | WorldNormalMap |
| `_Roughness.png` | **Masks / Grayscale (R8)** | ❌ **Unchecked (sRGB OFF)** | World |
| `_Metallic.png` | **Masks / Grayscale (R8)** | ❌ **Unchecked (sRGB OFF)** | World |
| `_Emissive.png` | **Default (DXT1/5, BC1/3)** | ✅ **Checked (sRGB ON)** | World |

---

## 🔗 FBX Texture Embedding:
Every `.fbx` exported in `Assets/Level_1/` and `Blender/FBX/Sector09/` has its materials linked and UV unwrapped. When you drag and drop into Unreal Engine, check **Import Materials** and **Import Textures**.
