"""
Generates complete technical material specification files for all 12 Sector 09 materials
under Assets/Materials/.
"""

import os
import json

REPO_ROOT = r"d:\unreal engine"
MAT_ROOT = os.path.join(REPO_ROOT, "Assets", "Materials")

MATERIALS = [
    # 1. M_IndustrialMetal_Master
    {
        "path": ("MasterMaterials", "M_IndustrialMetal_Master.json"),
        "name": "M_IndustrialMetal_Master",
        "type": "MasterMaterial",
        "shading_model": "DefaultLit",
        "blend_mode": "Opaque",
        "two_sided": False,
        "description": "Primary architectural and industrial master shader for Sector 09 with metallic, roughness, and normal inputs.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 1.0,
                "RoughnessMultiplier": 1.0,
                "NormalStrength": 1.0,
                "EmissiveIntensity": 0.0,
                "UVTile": 1.0
            },
            "vector": {
                "BaseColorTint": [0.85, 0.9, 0.95, 1.0],
                "EmissiveTint": [0.0, 0.0, 0.0, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/BaseColor/T_Cyberpunk_Wall_Panel_BaseColor",
                "NormalMap": "/Game/Assets/Textures/Normal/T_Cyberpunk_Wall_Panel_Normal",
                "RoughnessMap": "/Game/Assets/Textures/Roughness/T_Cyberpunk_Wall_Panel_Roughness",
                "MetallicMap": "/Game/Assets/Textures/Metallic/T_Cyberpunk_Wall_Panel_Metallic",
                "EmissiveMap": "/Game/Assets/Textures/Emissive/T_Cyberpunk_Wall_Panel_Emissive"
            }
        }
    },
    # 2. M_WornMetal (Instance of Master)
    {
        "path": ("Metal", "MI_WornMetal.json"),
        "name": "MI_WornMetal",
        "parent": "M_IndustrialMetal_Master",
        "type": "MaterialInstance",
        "description": "Scratched gunmetal with visible edge scuffs for corridors and structural columns.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 0.88,
                "RoughnessMultiplier": 1.25,
                "NormalStrength": 1.2,
                "EmissiveIntensity": 0.0,
                "UVTile": 1.0
            },
            "vector": {
                "BaseColorTint": [0.12, 0.14, 0.18, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/BaseColor/T_Cyberpunk_Pipes_Conduit_BaseColor",
                "NormalMap": "/Game/Assets/Textures/Normal/T_Cyberpunk_Pipes_Conduit_Normal",
                "RoughnessMap": "/Game/Assets/Textures/Roughness/T_Cyberpunk_Pipes_Conduit_Roughness",
                "MetallicMap": "/Game/Assets/Textures/Metallic/T_Cyberpunk_Pipes_Conduit_Metallic"
            }
        }
    },
    # 3. M_DarkConcrete
    {
        "path": ("Concrete", "MI_DarkConcrete.json"),
        "name": "MI_DarkConcrete",
        "parent": "M_IndustrialMetal_Master",
        "type": "MaterialInstance",
        "description": "Reinforced dark blue-grey brutalist concrete for subfloors, elevator foundations, and loadbearing pilasters.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 0.05,
                "RoughnessMultiplier": 1.45,
                "NormalStrength": 1.5,
                "EmissiveIntensity": 0.0,
                "UVTile": 2.0
            },
            "vector": {
                "BaseColorTint": [0.10, 0.12, 0.15, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/BaseColor/T_Cyberpunk_Floor_Grate_BaseColor",
                "NormalMap": "/Game/Assets/Textures/Normal/T_Cyberpunk_Floor_Grate_Normal",
                "RoughnessMap": "/Game/Assets/Textures/Roughness/T_Cyberpunk_Floor_Grate_Roughness"
            }
        }
    },
    # 4. M_MetalFloor
    {
        "path": ("Metal", "MI_MetalFloor.json"),
        "name": "MI_MetalFloor",
        "parent": "M_IndustrialMetal_Master",
        "type": "MaterialInstance",
        "description": "Diamond tread and ribbed industrial metal plates with reflective highlights and scuff marks.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 0.95,
                "RoughnessMultiplier": 0.85,
                "NormalStrength": 1.3,
                "UVTile": 1.0
            },
            "vector": {
                "BaseColorTint": [0.18, 0.20, 0.24, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/BaseColor/T_Cyberpunk_Floor_Grate_BaseColor",
                "NormalMap": "/Game/Assets/Textures/Normal/T_Cyberpunk_Floor_Grate_Normal",
                "RoughnessMap": "/Game/Assets/Textures/Roughness/T_Cyberpunk_Floor_Grate_Roughness",
                "MetallicMap": "/Game/Assets/Textures/Metallic/T_Cyberpunk_Floor_Grate_Metallic"
            }
        }
    },
    # 5. M_MetalGrate
    {
        "path": ("SpecialEffects", "MI_MetalGrate.json"),
        "name": "MI_MetalGrate",
        "parent": "M_IndustrialMetal_Master",
        "type": "MaterialInstance",
        "blend_mode": "Masked",
        "two_sided": True,
        "description": "Perforated hexagonal catwalk grating allowing atmospheric light and steam shafts to pass through.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 1.0,
                "RoughnessMultiplier": 0.7,
                "NormalStrength": 1.0,
                "OpacityMaskClipValue": 0.33
            },
            "vector": {
                "BaseColorTint": [0.15, 0.17, 0.20, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/BaseColor/T_Cyberpunk_Floor_Grate_BaseColor",
                "NormalMap": "/Game/Assets/Textures/Normal/T_Cyberpunk_Floor_Grate_Normal",
                "MaskMap": "/Game/Assets/Textures/Masks/T_Mask_Hexagon_Grate"
            }
        }
    },
    # 6. M_DarkGlass
    {
        "path": ("Glass", "MI_DarkGlass.json"),
        "name": "MI_DarkGlass",
        "type": "MasterMaterial",
        "shading_model": "DefaultLit",
        "blend_mode": "Translucent",
        "two_sided": True,
        "description": "Heavy tinted bullet-resistant observation window glass overlooking Sector 09 cyberpunk megacity.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 0.3,
                "RoughnessMultiplier": 0.08,
                "Opacity": 0.45,
                "Refraction": 1.33
            },
            "vector": {
                "BaseColorTint": [0.03, 0.08, 0.12, 1.0]
            }
        }
    },
    # 7. M_CyanEmissive
    {
        "path": ("Emissive", "MI_CyanEmissive.json"),
        "name": "MI_CyanEmissive",
        "type": "MasterMaterial",
        "shading_model": "Unlit",
        "blend_mode": "Opaque",
        "two_sided": False,
        "description": "High-intensity cyan tech indicator and conduit glow for active interactive consoles.",
        "parameters": {
            "scalar": {
                "EmissiveIntensity": 15.0
            },
            "vector": {
                "EmissiveColor": [0.0, 0.90, 1.0, 1.0]
            },
            "textures": {
                "EmissiveMap": "/Game/Assets/Textures/Emissive/T_Cyberpunk_Neon_Lights_Emissive"
            }
        }
    },
    # 8. M_PurpleEmissive
    {
        "path": ("Emissive", "MI_PurpleEmissive.json"),
        "name": "MI_PurpleEmissive",
        "type": "MasterMaterial",
        "shading_model": "Unlit",
        "blend_mode": "Opaque",
        "two_sided": False,
        "description": "Atmospheric purple neon bar accent lighting creating high-contrast cyberpunk color temperature.",
        "parameters": {
            "scalar": {
                "EmissiveIntensity": 14.0
            },
            "vector": {
                "EmissiveColor": [0.85, 0.05, 0.95, 1.0]
            },
            "textures": {
                "EmissiveMap": "/Game/Assets/Textures/Emissive/T_Cyberpunk_Neon_Lights_Emissive"
            }
        }
    },
    # 9. M_RedWarningEmissive
    {
        "path": ("Emissive", "MI_RedWarningEmissive.json"),
        "name": "MI_RedWarningEmissive",
        "type": "MasterMaterial",
        "shading_model": "Unlit",
        "blend_mode": "Opaque",
        "two_sided": False,
        "description": "Pulsing red alarm and security lock beacon for the Level 1 exit blast gate.",
        "parameters": {
            "scalar": {
                "EmissiveIntensity": 18.0
            },
            "vector": {
                "EmissiveColor": [1.0, 0.03, 0.03, 1.0]
            },
            "textures": {
                "EmissiveMap": "/Game/Assets/Textures/Emissive/T_Cyberpunk_Neon_Lights_Emissive"
            }
        }
    },
    # 10. M_IndustrialPaint
    {
        "path": ("SpecialEffects", "MI_IndustrialPaint.json"),
        "name": "MI_IndustrialPaint",
        "parent": "M_IndustrialMetal_Master",
        "type": "MaterialInstance",
        "description": "Hazard yellow / caution striped coating applied to floor edges, lift thresholds, and barricades.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 0.15,
                "RoughnessMultiplier": 0.65,
                "NormalStrength": 1.1
            },
            "vector": {
                "BaseColorTint": [0.95, 0.75, 0.05, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/Decals/T_Decal_Hazard_Stripe_BaseColor"
            }
        }
    },
    # 11. M_VentilationMetal
    {
        "path": ("Metal", "MI_VentilationMetal.json"),
        "name": "MI_VentilationMetal",
        "parent": "M_IndustrialMetal_Master",
        "type": "MaterialInstance",
        "description": "Zinc-coated galvanized sheet metal for air ducts, ventilation units, and cooling fans.",
        "parameters": {
            "scalar": {
                "MetallicMultiplier": 0.92,
                "RoughnessMultiplier": 0.45,
                "NormalStrength": 1.0
            },
            "vector": {
                "BaseColorTint": [0.38, 0.42, 0.45, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/BaseColor/T_Cyberpunk_Wall_Panel_BaseColor",
                "NormalMap": "/Game/Assets/Textures/Normal/T_Cyberpunk_Wall_Panel_Normal",
                "RoughnessMap": "/Game/Assets/Textures/Roughness/T_Cyberpunk_Wall_Panel_Roughness",
                "MetallicMap": "/Game/Assets/Textures/Metallic/T_Cyberpunk_Wall_Panel_Metallic"
            }
        }
    },
    # 12. M_ScreenGlass
    {
        "path": ("Glass", "MI_ScreenGlass.json"),
        "name": "MI_ScreenGlass",
        "type": "MasterMaterial",
        "shading_model": "DefaultLit",
        "blend_mode": "Translucent",
        "two_sided": False,
        "description": "Cyberpunk terminal monitor display glass with phosphor scanlines and biometric GUI readouts.",
        "parameters": {
            "scalar": {
                "EmissiveIntensity": 10.0,
                "RoughnessMultiplier": 0.15,
                "Opacity": 0.85
            },
            "vector": {
                "EmissiveColor": [0.05, 0.85, 0.70, 1.0]
            },
            "textures": {
                "BaseColorMap": "/Game/Assets/Textures/BaseColor/T_Cyberpunk_Terminal_Console_BaseColor",
                "EmissiveMap": "/Game/Assets/Textures/Emissive/T_Cyberpunk_Terminal_Console_Emissive"
            }
        }
    }
]

for mat in MATERIALS:
    subfolder, filename = mat["path"]
    target_dir = os.path.join(MAT_ROOT, subfolder)
    os.makedirs(target_dir, exist_ok=True)
    target_file = os.path.join(target_dir, filename)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(mat, f, indent=2)

print(f"Generated all {len(MATERIALS)} material specifications under Assets/Materials/.")
