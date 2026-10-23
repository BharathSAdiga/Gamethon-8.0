# LAST SECOND — SECTOR 09
## Level 1 — WAKE UP CALL: Unreal Engine 5.6 Setup & Integration Guide

This guide details how to import, configure, and assemble all Sector 09 Level 1 modular assets, materials, textures, and Blueprints inside Unreal Engine 5.6.

---

## 1. Opening the Project
1. Launch **Unreal Engine 5.6**.
2. Open the existing project located at:
   `d:\unreal engine\UE Projects\MyProject\MyProject.uproject`
3. The project is pre-configured with:
   - `ModelingToolsEditorMode` enabled.
   - `PythonScriptPlugin` and `EditorScriptingUtilities` enabled.
   - Nanite & Lumen support ready.

---

## 2. Directory Locations Inside Unreal Content Browser
All resources are organized inside the project's `Content/Assets/` folder:
- **Meshes**: `/Game/Assets/Meshes/{Architecture, Floors, Doors, Industrial, Pipes, Railings, Machinery, Props, SciFi}`
- **Materials**: `/Game/Assets/Materials/{MasterMaterials, Metal, Concrete, Glass, Emissive, SpecialEffects}`
- **Textures**: `/Game/Assets/Textures/{BaseColor, Normal, Roughness, Metallic, Emissive, Masks, Decals}`
- **Blueprints**: `/Game/Assets/Blueprints/{Doors, Interactive, Lift, Lighting, Environmental}`
- **Technical References**: `/Game/Assets/Reference/Blueprints/` (7 high-res 2560x1440 schematics)

---

## 3. Automated Asset Import & Creation via Python
An automated Python pipeline is provided in `Content/Python/build_sector09_ue5_assets.py`.

### How to Run in Unreal Editor:
1. Open Unreal Editor 5.6 with `MyProject`.
2. Open the **Output Log** (`Window -> Output Log`).
3. In the command bar at the bottom, select **Python** (or type `py`) and run:
   ```python
   import build_sector09_ue5_assets
   build_sector09_ue5_assets.run_all()
   ```
4. The script will automatically:
   - Import all 66+ FBX meshes with unified pivot points and collision settings.
   - Import all 2K textures with correct compression settings (`Default (DXT1/5)` for BaseColor/Emissive, `Normalmap (BC5)` for Normals, `Masks/Grayscale (BC4)` for Roughness/Metallic).
   - Create Master Materials and instantiate the 12 material instances.
   - Assign materials to all mesh slots.
   - Create the 7 native Blueprint actors in `/Game/Assets/Blueprints/`.

---

## 4. Manual FBX Import Settings (If Importing Manually)
If you prefer dragging and dropping FBX files into the Content Browser:

| Setting | Recommended Value | Reason |
|:---|:---:|:---|
| **Import Uniform Scale** | `1.0` | Models are already 1:1 scaled (1 cm = 1 Unreal Unit) |
| **Convert Scene** | `True` | Ensures proper coordinate system orientation |
| **Import Meshes in Folder Hierarchy** | `True` | Preserves category folder structure |
| **Generate Missing Collision** | `True` | Automatically builds simple box/convex hulls |
| **Vertex Override Color** | `Ignore` | Clean PBR vertex shading |
| **Material Import Method** | `Do Not Create Material` | Use the dedicated `Assets/Materials` library |

---

## 5. Collision Configuration Guidelines
- **Modular Wall Panels & Floors**:
  - Keep default **Simple Collision** (`BlockAll`).
  - For floor grates with gaps (`SM_FloorTile_B_Grate`), set Collision Complexity to **Project Default** or simple box.
- **Ramp & Stairs (`SM_Floor_Ramp`, `SM_Stair_Module`)**:
  - Use an invisible angled box/wedge collision so character movement is completely smooth without stepping stutter.
- **Pipes & Conduits**:
  - Simple Capsule collision or `NoCollision` for small ceiling pipes to optimize CPU collision queries.
- **Door Panels & Gates**:
  - Use `BlockAllDynamic` so that when sliding open, characters and projectiles immediately pass through.

---

## 6. Blueprint Wiring & Level Construction Checklist

### 1. Reusable Doors (`BP_IndustrialDoor`)
- Drag `BP_IndustrialDoor` into any doorway in Sector 09.
- The door is self-contained. It contains its own trigger volume and timeline.
- Test interaction by walking up and pressing [E] or calling `BPI_Interactable.OnInteract`.

### 2. Climax Blast Gate & Terminal Integration (`BP_LockedGate` & `BP_ControlTerminal`)
1. Place `BP_LockedGate` at the Level 1 sector exit threshold.
2. Place `BP_ControlTerminal` on the wall or floor right beside it.
3. In the Details Panel of `BP_ControlTerminal`:
   - Locate the variable **`TargetGateRef`**.
   - Use the eyedropper tool to pick the `BP_LockedGate` instance in the viewport.
4. When the player hacks/interacts with the terminal, it will automatically call `UnlockAndOpenGate()` on the gate, triggering sirens, cyan clearance strobes, and retracting the blast leaves.

### 3. Vertical Lift Platform (`BP_LiftPlatform`)
1. Place `BP_LiftPlatform` inside the elevator shaft opening.
2. Set `TravelDistance` to match your floor height delta (default: `1200.0` cm = 12m).
3. Place `SM_LiftControlPanel` at the top and bottom landings. Wire each button to call `BP_LiftPlatform.CallLift()`.

### 4. Surveillance Cameras (`BP_SurveillanceCamera`)
1. Mount to ceilings or walls overlooking main transit corridors.
2. In Details panel, adjust `SweepAngleMax` (e.g. `45.0` to `60.0` degrees) and `RotationSpeed` (`20.0` deg/s).
3. Light beam will illuminate volumetric dust in the air.

### 5. Neon Strips (`BP_NeonLight`)
- Place along catwalk edges and ceiling conduit channels.
- In Details panel, choose:
  - **Cyan Tech**: `(R=0.0, G=0.9, B=1.0)`
  - **Purple Atmospheric**: `(R=0.85, G=0.05, B=0.95)`
  - **Red Alert / Danger**: `(R=1.0, G=0.03, B=0.03)`
- Emissive intensity is pre-tuned for Lumen screen-space bounce lighting.

---

## 7. Technical Reference Diagrams
For in-depth node graphs, variable tables, component hierarchies, and expected in-game results, refer to the high-resolution images in:
`Assets/Reference/Blueprints/`
- [BP_IndustrialDoor_Reference.png](file:///d:/unreal%20engine/Assets/Reference/Blueprints/BP_IndustrialDoor_Reference.png)
- [BP_LockedGate_Reference.png](file:///d:/unreal%20engine/Assets/Reference/Blueprints/BP_LockedGate_Reference.png)
- [BP_ControlTerminal_Reference.png](file:///d:/unreal%20engine/Assets/Reference/Blueprints/BP_ControlTerminal_Reference.png)
- [BP_LiftPlatform_Reference.png](file:///d:/unreal%20engine/Assets/Reference/Blueprints/BP_LiftPlatform_Reference.png)
- [BP_SurveillanceCamera_Reference.png](file:///d:/unreal%20engine/Assets/Reference/Blueprints/BP_SurveillanceCamera_Reference.png)
- [BP_InteractablePanel_Reference.png](file:///d:/unreal%20engine/Assets/Reference/Blueprints/BP_InteractablePanel_Reference.png)
- [BP_NeonLight_Reference.png](file:///d:/unreal%20engine/Assets/Reference/Blueprints/BP_NeonLight_Reference.png)
