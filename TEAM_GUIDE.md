# 👥 TEAM GUIDE — Gamethon 8.0

A quick reference for every team member. Read this before adding anything to the repo.

---

## 📁 Where to Put Your Files

### If you work in Blender
| What you made | Where to save it |
|---|---|
| `.blend` file | `Blender/Blend/` |
| Exported `.fbx` | `Blender/FBX/` |
| Python script | `Blender/Scripts/` |

### If you work in Unreal Engine (UE5 project is `UE Projects/Lastsecond/`)
| What you made | Where to save it |
|---|---|
| Background / environment image | `UE Projects/Lastsecond/Content/Environments/City/` or `Railway/` or `Indoor/` or `Outdoor/` |
| Character mesh, rig, animation | `UE Projects/Lastsecond/Content/Characters/Player/` or `NPCs/` |
| Blueprint | `UE Projects/Lastsecond/Content/Blueprints/` |
| Material / texture | `UE Projects/Lastsecond/Content/Materials/` or `Textures/` |
| VFX (Niagara) | `UE Projects/Lastsecond/Content/VFX/Niagara/` |
| Sound / music | `UE Projects/Lastsecond/Content/Audio/` |
| UI widget | `UE Projects/Lastsecond/Content/UI/` |
| Game level / map | `UE Projects/Lastsecond/Content/Maps/Levels/` |

### If you have raw assets, concept art, or reference images
| What | Where |
|---|---|
| Asset images / sprites / decals | `Assets/Images/` |
| Game assets / props / prefabs | `Assets/Game_Assets/` |
| Concept art | `Assets/Concepts/` |
| Reference images | `Assets/Reference/` |
| Background images (raw) | `Assets/Backgrounds/` |


---

## 🏷️ Naming Your Files

Always use these prefixes so everyone knows what the file is at a glance:

| Prefix | Means |
|---|---|
| `SM_` | Static Mesh (e.g. `SM_CyberpunkTower`) |
| `SK_` | Skeletal Mesh (character body) |
| `BP_` | Blueprint |
| `M_` | Material |
| `MI_` | Material Instance |
| `T_` | Texture |
| `NS_` | Niagara VFX System |
| `ABP_` | Animation Blueprint |
| `WBP_` | Widget Blueprint (UI) |
| `A_` | Audio / Sound Cue |
| `DT_` | Data Table |

**Rules:**
- No spaces in file names — use underscores: `SM_My_Asset` ✅ not `SM My Asset` ❌
- Be descriptive: `SM_Cyberpunk_Lattice_Tower` ✅ not `SM_Tower1` ❌

---

## 🔄 Git Workflow (How to Push Your Work)

### First time setup
```bash
git clone https://github.com/BharathSAdiga/Gamethon-8.0.git
cd Gamethon-8.0
git lfs install
```

### Every time you add or change files
```bash
git pull origin main          # always pull first
git add .                     # stage your changes
git commit -m "your message"  # write what you did
git push origin main          # push to GitHub
```

### Commit message examples
```
asset: add SM_Cyberpunk_Pillar blender and FBX
asset: add BG_City_Rain background image
feat: create player jump animation
fix: fix material on telecom tower
```

---

## ⚠️ Rules

1. **Always `git pull` before you start working** — avoid conflicts
2. **Never commit to `main` directly during crunch** — tell the team before pushing
3. **Never put files in `UE Projects/MyProject/` or `MyProject2/`** — those are old templates, ignored
4. **Large files (FBX, PNG, blend) are handled by Git LFS automatically** — just `git add` normally
5. **Don't commit the `Saved/`, `Intermediate/`, or `DerivedDataCache/` folders** — already in gitignore

---

## 📞 Quick Reference

| Repo | https://github.com/BharathSAdiga/Gamethon-8.0 |
|---|---|
| Main UE Project | `UE Projects/Lastsecond/` |
| Blender files | `Blender/` |
| Background art | `Assets/Backgrounds/` |
| Team guide | This file (`TEAM_GUIDE.md`) |

