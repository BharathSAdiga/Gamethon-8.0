# LAST SECOND — SECTOR 09 | LEVEL 1 — WAKE UP CALL
## Comprehensive Asset, Material, Texture & Blueprint Manifest
### Engine Target: Unreal Engine 5.6 | PBR Metallic/Roughness Workflow

---

## 1. Directory Structure Overview
```
Assets/
├── Meshes/
│   ├── Architecture/       (10 Static Meshes: Wall panels, corners, beams, window frames, glass)
│   ├── Floors/             (9 Static Meshes: Solid tiles, grates, ramps, platforms, stairs, landings)
│   ├── Doors/              (3 Static Meshes: Industrial doors, door frames, massive blast gates)
│   ├── Industrial/         (4 Static Meshes: Cable trays, electrical boxes, access panels, duct covers)
│   ├── Pipes/              (4 Static Meshes: Straight, elbow, T-junction, wall-mounted conduit sets)
│   ├── Railings/           (2 Static Meshes: Straight security railing, corner railing)
│   ├── Machinery/          (5 Static Meshes: AC units, vent turbines, lift platform, shaft modules, generators)
│   ├── Props/              (13 Static Meshes: Small/med/large crates, barrels, barriers, desks, chairs)
│   └── SciFi/              (16 Static Meshes: Cameras, server racks, control terminals, monitors, neon lights)
│
├── Blueprints/
│   ├── Doors/              (BP_IndustrialDoor, BP_LockedGate)
│   ├── Interactive/        (BP_ControlTerminal, BP_InteractablePanel)
│   ├── Lift/               (BP_LiftPlatform)
│   ├── Lighting/           (BP_NeonLight)
│   └── Environmental/      (BP_SurveillanceCamera)
│
├── Materials/
│   ├── MasterMaterials/    (M_IndustrialMetal_Master, M_Emissive_Master, M_DarkGlass_Master)
│   ├── Metal/              (MI_WornMetal, MI_MetalFloor, MI_VentilationMetal)
│   ├── Concrete/           (MI_DarkConcrete)
│   ├── Glass/              (MI_DarkGlass, MI_ScreenGlass)
│   ├── Emissive/           (MI_CyanEmissive, MI_PurpleEmissive, MI_RedWarningEmissive)
│   └── SpecialEffects/     (MI_MetalGrate, MI_IndustrialPaint)
│
├── Textures/
│   ├── BaseColor/          (6 x 2048x2048 sRGB PBR BaseColor Maps)
│   ├── Normal/             (6 x 2048x2048 Linear DirectX Tangent Normal Maps)
│   ├── Roughness/          (6 x 2048x2048 Linear Grayscale Roughness Maps)
│   ├── Metallic/           (6 x 2048x2048 Linear Grayscale Metallic Maps)
│   ├── Emissive/           (6 x 2048x2048 sRGB Emissive Glow Maps)
│   ├── Masks/              (3 x 2048x2048 Edge wear, grime, and hexagonal grate masks)
│   └── Decals/             (4 x 2048x2048 Caution hazard, Sector 09 stencils, lock symbols, bio-scans)
│
├── Reference/
│   ├── Blueprints/         (7 x 2560x1440 High-Res Technical Blueprint Schematics)
│   ├── AssetSheets/        (Modular Kit reference and kit showroom)
│   └── Layout/             (Level 1 room-by-room architectural blockout guides)
│
└── Documentation/
    ├── LEVEL_1_ASSET_MANIFEST.md (This document)
    └── UE5_SETUP_GUIDE.md        (Step-by-step UE 5.6 import & assembly guide)
```

---

## 2. Static Mesh Catalog (66 Assets)

### Architecture (`Assets/Meshes/Architecture/`)
| Mesh Name | Asset Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_WallPanel_A` | 300 x 30 x 300 | BlockAll | `M_IndustrialMetal_Master` | Standard modular blue-grey industrial wall panel |
| `SM_WallPanel_B_Pipes` | 300 x 45 x 300 | BlockAll | `M_IndustrialMetal_Master` | Wall panel with integrated conduit runners |
| `SM_WallPanel_C_Vent` | 300 x 40 x 300 | BlockAll | `M_VentilationMetal` | Wall panel with intake louvers & vent grate |
| `SM_Corner_Wall` | 300 x 300 x 300 | BlockAll | `M_IndustrialMetal_Master` | 90-degree reinforced structural corner module |
| `SM_Window_Panel` | 300 x 30 x 300 | BlockAll | `M_IndustrialMetal_Master` | Wall panel with central cutout for observation glass |
| `SM_CityView_WindowFrame` | 400 x 30 x 300 | BlockAll | `M_IndustrialMetal_Master` | Large observation room panorama frame |
| `SM_Window_Glass` | 360 x 5 x 260 | BlockAll | `M_DarkGlass` | Bullet-resistant observation window glass |
| `SM_CeilingPanel` | 300 x 300 x 20 | BlockAll | `M_IndustrialMetal_Master` | Modular ceiling panel with recessed lighting troughs |
| `SM_Support_Beam` | 40 x 40 x 300 | BlockAll | `M_WornMetal` | Heavy structural I-beam with bolt flanges |
| `SM_Lift_Shaft_Wall` | 300 x 30 x 600 | BlockAll | `M_DarkConcrete` | Double-height reinforced elevator shaft wall |

### Floors & Catwalks (`Assets/Meshes/Floors/`)
| Mesh Name | Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_FloorTile_A` | 300 x 300 x 20 | BlockAll | `M_MetalFloor` | Solid diamond-tread industrial floor tile |
| `SM_FloorTile_B_Grate` | 300 x 300 x 20 | BlockAll | `M_MetalGrate` | Hexagonal perforated drainage grate |
| `SM_FloorTile_C` | 300 x 300 x 20 | BlockAll | `M_MetalFloor` | Metal tile with perimeter utility trough |
| `SM_FloorTile_D_Corner` | 300 x 300 x 20 | BlockAll | `M_MetalFloor` | Corner floor tile with yellow hazard trim |
| `SM_Floor_Ramp` | 300 x 300 x 75 | BlockAll | `M_MetalFloor` | 15-degree ADA industrial transition ramp |
| `SM_Platform_Module` | 300 x 300 x 100 | BlockAll | `M_MetalFloor` | Elevated catwalk platform module |
| `SM_Stair_Module` | 300 x 240 x 150 | BlockAll (Ramp) | `M_MetalFloor` | Industrial stairway with non-slip treads |
| `SM_Floor_Edge_Module` | 300 x 60 x 30 | BlockAll | `M_IndustrialPaint` | Grated edge module with hazard lip |
| `SM_Lift_Landing` | 300 x 300 x 35 | BlockAll | `M_MetalGrate` | Heavy threshold with mechanical interlocking teeth |

### Doors & Blast Gates (`Assets/Meshes/Doors/`)
| Mesh Name | Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_Industrial_Door` | 140 x 15 x 240 | BlockAllDynamic | `M_WornMetal` | Vertical sliding hydraulic door panel |
| `SM_Door_Frame` | 180 x 40 x 270 | BlockAll | `M_IndustrialMetal_Master` | Rigid reinforced door jamb with light socket |
| `SM_Large_Gate` | 400 x 60 x 350 | BlockAll | `M_WornMetal` | Armored Level 1 climax blast gate |

### Pipes & Conduits (`Assets/Meshes/Pipes/`)
| Mesh Name | Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_Pipe_Straight` | 40 x 40 x 300 | Simple Capsule | `M_WornMetal` | 3m straight industrial utility pipe |
| `SM_Pipe_Elbow` | 80 x 80 x 40 | Simple Capsule | `M_WornMetal` | 90-degree pipe elbow with seal flange |
| `SM_Pipe_Junction_T` | 100 x 60 x 60 | Simple Capsule | `M_WornMetal` | T-junction pipe splitter |
| `SM_Pipe_Set_Wall` | 300 x 40 x 80 | BlockAll | `M_WornMetal` | Wall-clamped bundle of 4 utility conduits |

### Railings (`Assets/Meshes/Railings/`)
| Mesh Name | Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_Railing_Straight` | 300 x 15 x 110 | BlockAll | `M_IndustrialMetal_Master` | Standard industrial steel safety railing |
| `SM_Railing_Corner` | 150 x 150 x 110 | BlockAll | `M_IndustrialMetal_Master` | 90-degree corner safety railing |

### Industrial & Machinery (`Assets/Meshes/Industrial/` & `Machinery/`)
| Mesh Name | Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_Cable_Tray` | 300 x 50 x 25 | BlockAll | `M_WornMetal` | Overhead suspended wireway / tray |
| `SM_Electrical_Box` | 80 x 30 x 120 | BlockAll | `M_IndustrialMetal_Master` | High-voltage breaker cabinet with dial gauges |
| `SM_Access_Panel` | 60 x 15 x 90 | BlockAll | `M_IndustrialMetal_Master` | Wall-mount utility panel with indicator light |
| `SM_Duct_Cover` | 120 x 20 x 80 | BlockAll | `M_VentilationMetal` | Exhaust hood with louvered baffle |
| `SM_AC_Unit` | 160 x 100 x 120 | BlockAll | `M_VentilationMetal` | Heavy compressor with cooling ribs |
| `SM_Vent_Unit` | 200 x 120 x 140 | BlockAll | `M_VentilationMetal` | Roof/wall ventilation blower with spinning turbine |
| `SM_LiftPlatform` | 280 x 280 x 40 | BlockAll | `M_MetalGrate` | Elevator cage base with safety perimeter |
| `SM_Elevator_Shaft_Module` | 320 x 320 x 300 | BlockAll | `M_DarkConcrete` | Enclosed structural shaft framing segment |
| `SM_Industrial_Generator` | 240 x 140 x 170 | BlockAll | `M_WornMetal` | Auxiliary fusion/diesel generator unit |

### Props & Furniture (`Assets/Meshes/Props/`)
| Mesh Name | Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_Crate_Small` | 60 x 60 x 60 | BlockAll | `M_IndustrialMetal_Master` | Stackable cargo cube with corner protectors |
| `SM_Crate_Medium` | 100 x 100 x 100 | BlockAll | `M_IndustrialMetal_Master` | Standard shipping container |
| `SM_Crate_Large` | 160 x 120 x 140 | BlockAll | `M_IndustrialMetal_Master` | Heavy logistics container with digital manifest |
| `SM_Stacked_Crates` | 180 x 140 x 210 | BlockAll | `M_IndustrialMetal_Master` | Realistic pre-arranged cargo stack |
| `SM_Barrel` | 60 x 60 x 95 | Simple Cylinder | `M_WornMetal` | Ribbed chemical drum with hazard decals |
| `SM_Barrier_Low` | 200 x 40 x 90 | BlockAll | `M_IndustrialPaint` | Low concrete/metal crowd barrier |
| `SM_Barrier_Tall` | 240 x 40 x 200 | BlockAll | `M_IndustrialPaint` | Security barricade with reinforced wire |
| `SM_Construction_Barrier` | 200 x 30 x 110 | BlockAll | `M_IndustrialPaint` | Striped hazard barrier |
| `SM_Pallet` | 120 x 80 x 15 | BlockAll | `M_DarkConcrete` | Heavy plastic industrial logistics pallet |
| `SM_Trash_Bin_A` | 45 x 45 x 85 | BlockAll | `M_IndustrialMetal_Master` | Cyberpunk waste receptacle |
| `SM_Trash_Bin_B` | 50 x 50 x 90 | BlockAll | `M_IndustrialMetal_Master` | Cylindrical waste recycler |
| `SM_Computer_Desk` | 160 x 80 x 75 | BlockAll | `M_IndustrialMetal_Master` | Ergonomic observation room desk |
| `SM_Chair` | 60 x 60 x 95 | Simple Box | `M_IndustrialMetal_Master` | Pneumatic swivel operator chair |

### SciFi, Lighting & Electronics (`Assets/Meshes/SciFi/`)
| Mesh Name | Dimensions (cm) | Target Collision | Material Slot | Description |
|:---|:---:|:---:|:---:|:---|
| `SM_SurveillanceCamera` | 35 x 30 x 25 | Simple Box | `M_WornMetal` | Security camera with lens & pivot joint |
| `SM_Server_Rack` | 90 x 80 x 220 | BlockAll | `M_WornMetal` | Dual blade server rack with fiber optic LEDs |
| `SM_ControlTerminal` | 70 x 60 x 115 | BlockAll | `M_IndustrialMetal_Master` | Free-standing angled console terminal |
| `SM_Info_Terminal_Glitch` | 70 x 60 x 115 | BlockAll | `M_ScreenGlass` | Wall info kiosk with glitch screen |
| `SM_Monitor_Screen` | 65 x 8 x 45 | Simple Box | `M_ScreenGlass` | Curved 16:9 widescreen terminal monitor |
| `SM_Hanging_Light` | 40 x 40 x 180 | NoCollision | `M_IndustrialMetal_Master` | Ceiling pendant lamp with protective cage |
| `SM_Ceiling_Light` | 120 x 40 x 15 | NoCollision | `M_CyanEmissive` | Recessed fluorescent lighting panel |
| `SM_Wall_Light_Warm` | 30 x 20 x 40 | NoCollision | `M_IndustrialMetal_Master` | Low-glare incandescent bulkhead light |
| `SM_Neon_Light_Cyan` | 200 x 8 x 8 | NoCollision | `M_CyanEmissive` | 2m cyan tech strip neon fixture |
| `SM_Neon_Light_Purple` | 200 x 8 x 8 | NoCollision | `M_PurpleEmissive` | 2m atmospheric purple neon fixture |
| `SM_Emergency_Light_Red` | 25 x 25 x 20 | NoCollision | `M_RedWarningEmissive` | Revolving emergency beacon |
| `SM_Street_Light_Indoor` | 60 x 60 x 350 | BlockAll | `M_WornMetal` | Tall industrial stanchion floodlight |
| `SM_LiftControlPanel` | 40 x 12 x 100 | BlockAll | `M_IndustrialMetal_Master` | Wall-mount lift call terminal with arrow diodes |
| `SM_Shaft_Lighting_Assembly` | 35 x 35 x 280 | BlockAll | `M_IndustrialMetal_Master` | Vertical caged beacon strip for elevator shaft |
| `SM_Computer_Workstation` | 220 x 110 x 130 | BlockAll | `M_IndustrialMetal_Master` | Multi-screen observation command desk |
| `SM_Server_Equipment` | 110 x 90 x 240 | BlockAll | `M_WornMetal` | Heavy enterprise compute blade cabinet |

---

## 3. Coordinated PBR Material Library (12 Materials)

| Material Name | Type | Blend Mode | Shading Model | Texture Set / Parameters |
|:---|:---:|:---:|:---:|:---|
| `M_IndustrialMetal_Master` | Master | Opaque | DefaultLit | BaseColor, Normal, Roughness, Metallic, Emissive |
| `M_WornMetal` | Instance | Opaque | DefaultLit | High roughness (0.65), gunmetal tint (0.12, 0.14, 0.18) |
| `M_DarkConcrete` | Instance | Opaque | DefaultLit | Roughness (0.9), Metallic (0.05), UVTile (2.0) |
| `M_MetalFloor` | Instance | Opaque | DefaultLit | Diamond tread normal, Roughness (0.35), Metallic (0.95) |
| `M_MetalGrate` | Instance | Masked | DefaultLit | Perforated Hexagon Grate Mask, Two-Sided |
| `M_DarkGlass` | Master | Translucent | DefaultLit | Opacity (0.45), Refraction (1.33), Roughness (0.08) |
| `M_CyanEmissive` | Master | Opaque | Unlit | Cyan Vector `(0, 0.9, 1.0)`, Multiplier 15.0 |
| `M_PurpleEmissive` | Master | Opaque | Unlit | Purple Vector `(0.85, 0.05, 0.95)`, Multiplier 14.0 |
| `M_RedWarningEmissive` | Master | Opaque | Unlit | Red Vector `(1.0, 0.03, 0.03)`, Multiplier 18.0 |
| `M_IndustrialPaint` | Instance | Opaque | DefaultLit | Hazard yellow-black caution stripe texture |
| `M_VentilationMetal` | Instance | Opaque | DefaultLit | Zinc-coated galvanized metal, Metallic 0.92 |
| `M_ScreenGlass` | Master | Translucent | DefaultLit | Glitch GUI terminal phosphor scanlines, Emissive 10.0 |

---

## 4. Texture Library (37 Texture Maps)

All textures are 2048 x 2048 high resolution, seamlessly tileable or atlas-mapped:
- **BaseColor (6 Maps)**: Full PBR color calibration, zero baked shadows.
- **Normal (6 Maps)**: DirectX format (R=X+, G=Y-, B=Z+), 16-bit smooth tangent vectors.
- **Roughness (6 Maps)**: Linear grayscale with realistic micro-surface variance.
- **Metallic (6 Maps)**: Clean binary/dielectric separation (0 = non-metal, 255 = raw alloy).
- **Emissive (6 Maps)**: Precise masked glow channels for neons, terminals, diodes.
- **Masks (3 Maps)**: Procedural scratches, perlin surface grime, hexagonal perforation.
- **Decals (4 Maps)**: SECTOR 09 stencils, hazard bands, bio-scans, locked gate sirens.

---

## 5. Technical Blueprint Actors (7 Actors)

1. **`BP_IndustrialDoor`**:
   - **Components**: `USceneComponent` (Root), `UStaticMeshComponent` (Frame), `UStaticMeshComponent` (Panel), `UPointLightComponent`, `UBoxComponent`, `UAudioComponent`, `UTimelineComponent`.
   - **Behavior**: Smooth vertical sliding door triggered via `BPI_Interactable`. Prevents re-trigger during motion. Red/Cyan indicator.

2. **`BP_LockedGate`**:
   - **Components**: Frame, dual horizontal retracting leaves, flashing red emergency strobe, siren audio, timeline.
   - **Behavior**: End-of-level exit gate. Locked until `UnlockAndOpenGate` is called by terminal.

3. **`BP_ControlTerminal`**:
   - **Components**: Pedestal mesh, monitor screen, sphere trigger, cyan keyboard wash light, widget component.
   - **Behavior**: Interactive console beside blast gate. Pressing interact triggers access sequence and unlocks `BP_LockedGate`.

4. **`BP_LiftPlatform`**:
   - **Components**: Platform grate, safety railings, underglow light, winch motor audio, 5.0s timeline.
   - **Behavior**: Transports player 12m vertically between lower maintenance floor and upper observation overlook.

5. **`BP_SurveillanceCamera`**:
   - **Components**: Wall mount, swivel joint scene root, camera housing mesh, volumetric spot light (cone 45°).
   - **Behavior**: Sweeps back and forth across corridor in a 120° arc. Turns red if triggered; can be disabled.

6. **`BP_InteractablePanel`**:
   - **Components**: Flush wall console, indicator diode, box trigger, toggle switch audio.
   - **Behavior**: Universal interaction point for breaker resets and vent overrides.

7. **`BP_NeonLight`**:
   - **Components**: Strip bracket mesh, tube mesh, point/rect light.
   - **Behavior**: Configurable cyan, purple, or red accent light with dynamic material instances.
