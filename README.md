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
│           ├── Characters/      ← Character meshes, rigs, anims
│           ├── Input/           ← Enhanced input actions and contexts
│           ├── LevelPrototyping/← Prototyping meshes and materials
│           ├── ThirdPerson/     ← Third-person game mode and blueprints
│           └── Variant_Platforming/ ← Platforming character and mechanics
│
├── Assets/                      ← Raw / source art assets
│   ├── Level_1/                 ← 56 Unreal-ready Level 1 modular FBX assets & catalog
│   ├── Images/                  ← 2D images, sprites, SECTOR09 reference crops
│   ├── Game_Assets/             ← Prefabs, props, and asset packs
│   ├── Backgrounds/             ← 2D background images (City, Railway, etc.)
│   ├── Concepts/                ← Concept art (Characters, Environments, UI)
│   ├── Reference/               ← Art and technical references
│   └── Exports/                 ← Final exports

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
