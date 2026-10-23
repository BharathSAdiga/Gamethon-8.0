# 🎮 Gamethon 8.0 — Cyberpunk Game

> A cyberpunk-themed Unreal Engine 5 game developed for Gamethon 8.0.

---

## 📁 Repository Structure

```
unreal engine/
│
├── UE Projects/
│   └── MyProject/               ← Main UE5 Project
│       └── Content/
│           ├── Assets/          ← Synchronized game assets (Meshes, Textures, Materials, Blueprints)
│           ├── Audio/           ← Sound FX & cues (A_Door_Slide, A_Gate_Alarm, A_Terminal_Beep, etc.)
│           ├── Characters/      ← Character meshes, rigs, anims
│           ├── Environments/    ← Layered backgrounds (City, Indoor, Outdoor, Railway)
│           ├── Input/           ← Enhanced input actions and contexts
│           ├── LevelPrototyping/← Prototyping meshes and materials
│           ├── ThirdPerson/     ← Third-person game mode and blueprints
│           ├── UI/              ← Cyberpunk HUD & widget textures (crosshair, health/energy bars, prompts)
│           ├── Variant_Platforming/ ← Platforming character and mechanics
│           └── VFX/             ← Niagara particle systems & textures (sparks, smoke, holo glitch, rings)
│
├── Assets/                      ← Raw / source art assets
│   ├── Audio/                   ← Master 16-bit 44.1kHz WAV SFX
│   ├── Backgrounds/             ← 2D background art (City, Indoor, Outdoor, Railway)
│   ├── Blueprints/              ← Blueprint actors & schemas (Doors, Interactive, Lift, Lighting, Environmental)
│   ├── Concepts/                ← Concept art (Characters, Environments, UI)
│   ├── Documentation/           ← Asset manifests, setup guides & assembly reports
│   ├── Game_Assets/             ← Prefabs, props, and reference packs
│   ├── Images/                  ← Sprites & SECTOR 09 reference crops
│   ├── Level_1/                 ← 66 Unreal-ready Level 1 modular FBX assets & catalog
│   ├── Materials/               ← Master materials & material instances
│   ├── Meshes/                  ← 66 modular static meshes + 4 superstructures (Architecture, Floors, Doors, etc.)
│   ├── Reference/               ← Blueprint schematics, layout diagrams, and asset sheets
│   ├── Textures/                ← 2K PBR texture sets (BaseColor, Normal, Roughness, Metallic, Emissive, Masks, Decals)
│   ├── UI/                      ← HUD textures, interaction prompts & dialogue boxes
│   └── VFX/                     ← Particle textures (sparks, smoke, glitch, neon rings)
│
├── Blender/                     ← Blender source files
│   ├── Characters/
│   ├── Environments/
│   ├── Props/
│   ├── Structures/              ← Cyberpunk structure .blend files
│   └── Scripts/
│
├── Docs/                        ← Documentation
│   ├── Design/GDD/              ← Game Design Document
│   ├── Design/ArtDirection/
│   ├── Design/LevelDesign/
│   └── Technical/
│
└── Pipeline/                    ← Tools and automation scripts
    └── Scripts/
        ├── Blender/             ← Blender Python generation scripts
        ├── Unreal/
        └── Automation/
```

---

## 🗂️ UE Content Naming Conventions

| Prefix | Asset Type             |
|--------|------------------------|
| BP_    | Blueprint              |
| SM_    | Static Mesh            |
| SK_    | Skeletal Mesh          |
| M_     | Material               |
| MI_    | Material Instance      |
| MF_    | Material Function      |
| T_     | Texture                |
| A_     | Audio / Sound Cue      |
| NS_    | Niagara System         |
| ABP_   | Animation Blueprint    |
| AM_    | Animation Montage      |
| BS_    | Blendspace             |
| DT_    | Data Table             |
| DA_    | Data Asset             |
| WBP_   | Widget Blueprint       |
| LVL_   | Level / Map            |
| PS_    | Physical Surface       |
| BT_    | Behavior Tree          |
| BB_    | Blackboard             |

---

## 🚀 Quick Start

1. Open `UE Projects/MyProject/MyProject.uproject` in Unreal Engine 5
2. All 3D FBX files are in `Blender/FBX/`
3. 2D Level 1 Assets are in `Assets/Images/SECTOR09_Level1_Assets/`
4. Background art is organized under `Assets/Backgrounds/`

---

## 🛠️ Tech Stack

- Engine: Unreal Engine 5
- 3D Modelling: Blender
- Scripting: Python (Blender automation), Blueprint (UE5)
- Version Control: Git + Git LFS
