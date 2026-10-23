# 🏭 SECTOR 09 — Level 1 Modular 3D Asset Kit

All 56 assets were procedurally modeled in Blender and exported with **Unreal Engine 5** standards:
- **Units**: 1 Unreal Unit = 1 cm (`100x` FBX scale factor applied).
- **Coordinate axes**: `-Z` Forward, `Y` Up.
- **Pivots**: Grounded at the base `Z=0` and modular grid snap edges.
- **Material Slots**: Multi-material slots assigned per mesh for easy master material swapping in UE5.
- **Locations**:
  - FBX: `Blender/FBX/Sector09/`
  - UE Project Import: `UE Projects/MyProject/Content/Sector09/`
  - Master Blender Scene: `Blender/Blend/Sector09_Level1_Kit.blend`

---

## 📋 Asset Catalog (56 Total)

### Group 01 — Walls, Doors & Gates (8 Assets)
| Asset Name | Dimensions (WxDxH cm) | Reference Image | Key Materials |
|---|---|---|---|
| `SM_01_Wall_Panel_A.fbx` | 200 x 20 x 300 | `01_Wall_Panel_A.png` | Dark Metal, Metal Panel, Neon Cyan |
| `SM_01_Wall_Panel_B_Pipes.fbx` | 200 x 30 x 300 | `01_Wall_Panel_B_Pipes.png` | Bright Metal, Rust, Hazard Yellow |
| `SM_01_Wall_Panel_C_Vent.fbx` | 200 x 25 x 300 | `01_Wall_Panel_C_Vent.png` | Dark Metal, Bright Metal, Hazard Yellow |
| `SM_01_Corner_Wall.fbx` | 60 x 60 x 300 | `01_Corner_Wall.png` | Dark Metal, Hazard Yellow, Neon Cyan |
| `SM_01_Door_Frame.fbx` | 230 x 40 x 320 | `01_Door_Frame.png` | Dark Metal, Bright Metal, Neon Cyan |
| `SM_01_Industrial_Door.fbx` | 180 x 15 x 280 | `01_Industrial_Door.png` | Metal Panel, Tinted Glass, Hazard Yellow |
| `SM_01_Large_Gate.fbx` | 360 x 35 x 340 | `01_Large_Gate.png` | Metal Dark, Hazard Yellow, Neon Red |
| `SM_01_Window_Panel.fbx` | 200 x 25 x 300 | `01_Window_Panel.png` | Metal Panel, Tinted Glass, Dark Metal |

---

### Group 02 — Floors, Stairs & Railings (9 Assets)
| Asset Name | Dimensions (WxDxH cm) | Reference Image | Key Materials |
|---|---|---|---|
| `SM_02_Floor_Tile_A.fbx` | 200 x 200 x 15 | `02_Floor_Tile_A.png` | Metal Panel, Metal Dark, Bolt Metal |
| `SM_02_Floor_Tile_B_Grate.fbx` | 200 x 200 x 15 | `02_Floor_Tile_B_Grate.png` | Dark Metal, Sump Rust, Grate Metal |
| `SM_02_Floor_Tile_C.fbx` | 200 x 200 x 15 | `02_Floor_Tile_C.png` | Hazard Yellow Border, Panel, Bright Metal |
| `SM_02_Floor_Tile_D_Corner.fbx` | 200 x 200 x 15 | `02_Floor_Tile_D_Corner.png` | Metal Panel, Chamfer Yellow, Conduit Dark |
| `SM_02_Floor_Tile_E_Ramp.fbx` | 200 x 200 x 40 | `02_Floor_Tile_E_Ramp.png` | Incline Deck, Anti-Slip Ribs, Yellow Lip |
| `SM_02_Stair_Module.fbx` | 200 x 200 x 120 | `02_Stair_Module.png` | 4 Steps, Hazard Tread Nose, Stringers |
| `SM_02_Platform_Module.fbx` | 200 x 200 x 40 | `02_Platform_Module.png` | Catwalk Deck, Underslung I-Beams |
| `SM_02_Railing_Straight.fbx` | 200 x 15 x 110 | `02_Railing_Straight.png` | Hazard Yellow Handrail, Stanchions |
| `SM_02_Railing_Corner.fbx` | 100 x 100 x 110 | `02_Railing_Corner.png` | Corner Stanchion, 90° Elbow Handrails |

---

### Group 03 — Heavy Structure, Beams & Pipe Networks (9 Assets)
| Asset Name | Dimensions (WxDxH cm) | Reference Image | Key Materials |
|---|---|---|---|
| `SM_03_Lift_Platform.fbx` | 225 x 225 x 35 | `03_Lift_Platform.png` | Metal Panel, Hazard Rim, Hoist Shackles |
| `SM_03_Elevator_Shaft_Module.fbx` | 240 x 240 x 300 | `03_Elevator_Shaft_Module.png` | 4 Corner Columns, Guide Rails, Yellow |
| `SM_03_Large_Vertical_Panel.fbx` | 80 x 40 x 400 | `03_Large_Vertical_Panel.png` | Heavy Pillar, Conduit Bundle, Neon Purple |
| `SM_03_Horizontal_Beam.fbx` | 400 x 30 x 40 | `03_Horizontal_Beam.png` | Structural I-Beam, End Bolt Plates |
| `SM_03_Pipe_Straight.fbx` | 200 x 25 x 25 | `03_Pipe_Straight.png` | Bright Steel Conduit, End Flanges |
| `SM_03_Pipe_Elbow.fbx` | 60 x 60 x 25 | `03_Pipe_Elbow.png` | 90° Bend, Bolted Flanges |
| `SM_03_Pipe_Junction_T.fbx` | 80 x 50 x 25 | `03_Pipe_Junction_T.png` | 3-Way T-Junction, Red Shutoff Wheel |
| `SM_03_Pipe_Set_Wall.fbx` | 200 x 25 x 60 | `03_Pipe_Set_Wall.png` | Triple Pipe Run, Wall Strut Brackets |
| `SM_03_Cable_Tray.fbx` | 200 x 40 x 15 | `03_Cable_Tray.png` | Wire-Mesh Tray, 4 Cable Runs |

---

### Group 04 — Industrial Containers & Barriers (9 Assets)
| Asset Name | Dimensions (WxDxH cm) | Reference Image | Key Materials |
|---|---|---|---|
| `SM_04_Crate_Large.fbx` | 200 x 120 x 120 | `04_Crate_Large.png` | Corner Castings, Corrugated, RFID Cyan |
| `SM_04_Crate_Medium.fbx` | 100 x 100 x 100 | `04_Crate_Medium.png` | Side Handles, Hazard Placard, Dark Metal |
| `SM_04_Crate_Small.fbx` | 62 x 42 x 40 | `04_Crate_Small.png` | Technician Box, Clamps, Rubber Grip |
| `SM_04_Stacked_Crates.fbx` | 180 x 140 x 160 | `04_Stacked_Crates.png` | 3 Crate Cluster, Angled Top, Tie-Down Strap |
| `SM_04_Barrel.fbx` | 68 x 68 x 95 | `04_Barrel.png` | Dual Hoop Ribs, Chimes, Hazmat Label |
| `SM_04_Barrier_Low.fbx` | 200 x 50 x 80 | `04_Barrier_Low.png` | Concrete Jersey Barrier, Hazard Reflectors |
| `SM_04_Barrier_Tall.fbx` | 200 x 40 x 200 | `04_Barrier_Tall.png` | Steel Blast Shield, Viewport, Buttresses |
| `SM_04_Construction_Barrier.fbx` | 150 x 40 x 100 | `04_Construction_Barrier.png` | A-Frame Barricade, Hazard Board, Strobe |
| `SM_04_Pallet.fbx` | 120 x 100 x 16 | `04_Pallet.png` | Forklift Channels, Composite Deck |

---

### Group 05 — Cyberpunk Terminals & Electronics (9 Assets)
| Asset Name | Dimensions (WxDxH cm) | Reference Image | Key Materials |
|---|---|---|---|
| `SM_05_Control_Terminal.fbx` | 100 x 70 x 125 | `05_Control_Terminal.png` | Angled Deck, Keyboard, Holographic Screen |
| `SM_05_Info_Terminal_Glitch.fbx` | 60 x 50 x 180 | `05_Info_Terminal_Glitch.png` | Dual Vertical Screens, Glitch Cyan |
| `SM_05_Access_Panel.fbx` | 40 x 10 x 60 | `05_Access_Panel.png` | Keypad, Biometric Scanner, Status LEDs |
| `SM_05_Electrical_Box.fbx` | 60 x 30 x 80 | `05_Electrical_Box.png` | Throw Switch, Conduits, Lightning Decal |
| `SM_05_Server_Rack.fbx` | 80 x 90 x 200 | `05_Server_Rack.png` | 8 Blade Modules, Blinking LEDs |
| `SM_05_Vent_Unit.fbx` | 90 x 50 x 90 | `05_Vent_Unit.png` | Cowled Turbine, Protective Grille |
| `SM_05_AC_Unit_Generator.fbx` | 160 x 100 x 115 | `05_AC_Unit_Generator.png` | Dual Rooftop Fans, Copper Heat Fins |
| `SM_05_Security_Camera.fbx` | 35 x 25 x 30 | `05_Security_Camera.png` | Cantilever Arm, Dome, Glowing Red Lens |
| `SM_05_Hanging_Light.fbx` | 40 x 40 x 60 | `05_Hanging_Light.png` | Low-Bay Lamp, Wire Guard Cage, Amber |

---

### Group 06 — Lighting, Furniture & Details (12 Assets)
| Asset Name | Dimensions (WxDxH cm) | Reference Image | Key Materials |
|---|---|---|---|
| `SM_06_Ceiling_Light.fbx` | 120 x 30 x 12 | `06_Ceiling_Light.png` | Flush Troffer, Cyan/White Diffuser |
| `SM_06_Neon_Light_Purple.fbx` | 150 x 12 x 12 | `06_Neon_Light_Purple.png` | Horizontal Neon Tube, Purple Glow |
| `SM_06_Neon_Light_Cyan.fbx` | 150 x 12 x 12 | `06_Neon_Light_Cyan.png` | Horizontal Neon Tube, Electric Cyan, Inverter |
| `SM_06_Wall_Light_Warm.fbx` | 30 x 25 x 40 | `06_Wall_Light_Warm.png` | Bulkhead Sconce, Downward Louvers, Amber |
| `SM_06_Emergency_Light_Red.fbx` | 50 x 20 x 25 | `06_Emergency_Light_Red.png` | Dual Rotating Strobe Domes, Crimson |
| `SM_06_Street_Light_Indoor.fbx` | 60 x 120 x 350 | `06_Street_Light_Indoor.png` | 3.5m Pole, Cantilever Arm, Dual Floodlights |
| `SM_06_Monitor_Screen.fbx` | 110 x 15 x 65 | `06_Monitor_Screen.png` | Wall Display, Rear Bracket, Glitch Green |
| `SM_06_Computer_Desk.fbx` | 140 x 70 x 75 | `06_Computer_Desk.png` | Steel Workstation, Drawer Unit |
| `SM_06_Chair.fbx` | 60 x 60 x 95 | `06_Chair.png` | 5-Spoke Caster Base, Piston, Bucket Seat |
| `SM_06_Trash_Bin_A.fbx` | 45 x 45 x 85 | `06_Trash_Bin_A.png` | Stainless Cylinder, Swing Flap, Cyan Rim |
| `SM_06_Trash_Bin_B.fbx` | 120 x 70 x 95 | `06_Trash_Bin_B.png` | Industrial Dumpster, Split Yellow Lids |
| `SM_06_Duct_Cover.fbx` | 60 x 8 x 60 | `06_Duct_Cover.png` | Directional Louver Register, 4 Screw Wells |
