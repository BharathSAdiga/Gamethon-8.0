# 🎮 Gamethon 8.0 — Cyberpunk Game

> A cyberpunk-themed Unreal Engine 5 game developed for Gamethon 8.0.

---

## 📁 Repository Structure

```
unreal engine/
│
├── UE Projects/
│   └── Lastsecond/              ← Main UE5 Project
│       └── Content/
│           ├── Blueprints/      ← All Blueprint classes
│           ├── Characters/      ← Character meshes, rigs, anims, materials
│           ├── Environments/    ← Level environment assets
│           ├── StaticMeshes/    ← Architecture, props, vehicles
│           ├── Cyberpunk_Structures/ ← Cyberpunk-specific structures
│           ├── Materials/       ← Master materials, instances, functions
│           ├── Textures/        ← All textures by category
│           ├── VFX/             ← Niagara particles and VFX materials
│           ├── Audio/           ← Music, SFX, dialogue, ambience
│           ├── Animations/      ← Anim blueprints, montages, blendspaces
│           ├── UI/              ← HUD, menus, widgets, icons
│           ├── Maps/            ← Levels and streaming maps
│           ├── Data/            ← DataTables, DataAssets, Curves, Enums
│           ├── Cinematics/      ← Sequences and cutscenes
│           ├── Physics/         ← Physics materials and surfaces
│           ├── AI/              ← Behavior trees, blackboards, EQS
│           ├── SourceAssets/    ← Raw FBX and source files for import
│           └── ThirdParty/      ← Marketplace and plugin assets
│
├── Assets/                      ← Raw / source art assets
│   ├── Backgrounds/             ← 2D background images (City, Railway, etc.)
│   ├── Concepts/                ← Concept art (Characters, Environments, UI)
│   ├── Reference/               ← Art and technical references
│   └── Exports/                 ← Final FBX/OBJ/Texture exports
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

1. Open UE Projects/Lastsecond/Lastsecond.uproject in Unreal Engine 5
2. Import FBX structures from Content/SourceAssets/FBX/Structures/ into Cyberpunk_Structures/Meshes/
3. Background images are pre-sorted under Environments/(City|Railway|Indoor|Outdoor)/Backgrounds/

---

## 🛠️ Tech Stack

- Engine: Unreal Engine 5
- 3D Modelling: Blender
- Scripting: Python (Blender automation), Blueprint (UE5)
- Version Control: Git + Git LFS
