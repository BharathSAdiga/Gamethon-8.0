"""
Generates complete technical Blueprint architecture definitions for all 7 actors under Assets/Blueprints/.
"""

import os
import json

REPO_ROOT = r"d:\unreal engine"
BP_ROOT = os.path.join(REPO_ROOT, "Assets", "Blueprints")

BLUEPRINTS = [
    {
        "category": "Doors",
        "name": "BP_IndustrialDoor",
        "parent_class": "Actor",
        "implemented_interfaces": ["BPI_Interactable"],
        "description": "Modular industrial sliding door actor with smooth vertical travel and status lighting.",
        "components": [
            {"name": "DefaultSceneRoot", "type": "USceneComponent", "parent": None},
            {"name": "DoorFrame", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mesh": "SM_Door_Frame", "mobility": "Static"},
            {"name": "DoorPanel", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mesh": "SM_Industrial_Door", "mobility": "Movable"},
            {"name": "IndicatorLight", "type": "UPointLightComponent", "parent": "DoorFrame", "color": [255, 30, 30], "intensity": 1500.0},
            {"name": "InteractionBox", "type": "UBoxComponent", "parent": "DefaultSceneRoot", "extent": [120, 180, 220], "collision_profile": "Trigger"},
            {"name": "DoorAudioComp", "type": "UAudioComponent", "parent": "DoorPanel"},
            {"name": "DoorTimeline", "type": "UTimelineComponent", "parent": None, "length": 1.2, "curve": "EaseInOut"}
        ],
        "variables": [
            {"name": "IsOpen", "type": "bool", "default": False, "replicated": True},
            {"name": "CanInteract", "type": "bool", "default": True, "replicated": False},
            {"name": "OpenDuration", "type": "float", "default": 1.2, "editable": True},
            {"name": "ClosedTransform", "type": "FTransform", "default": "Identity", "editable": False},
            {"name": "OpenHeightOffset", "type": "float", "default": 240.0, "editable": True},
            {"name": "AutoCloseDelay", "type": "float", "default": 5.0, "editable": True}
        ],
        "events": [
            "OnInteract(AActor* Caller)",
            "OnDoorOpened(AActor* DoorRef)",
            "OnDoorClosed(AActor* DoorRef)"
        ]
    },
    {
        "category": "Doors",
        "name": "BP_LockedGate",
        "parent_class": "Actor",
        "description": "Massive armored mechanical blast gate sealing Level 1 exit, responsive to BP_ControlTerminal.",
        "components": [
            {"name": "DefaultSceneRoot", "type": "USceneComponent", "parent": None},
            {"name": "GateFrame", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mesh": "SM_Large_Gate", "mobility": "Static"},
            {"name": "GatePanelLeft", "type": "UStaticMeshComponent", "parent": "GateFrame", "mobility": "Movable"},
            {"name": "GatePanelRight", "type": "UStaticMeshComponent", "parent": "GateFrame", "mobility": "Movable"},
            {"name": "RedWarningLight", "type": "UPointLightComponent", "parent": "GateFrame", "color": [255, 20, 20], "intensity": 3500.0},
            {"name": "AlarmAudioComp", "type": "UAudioComponent", "parent": "GateFrame"},
            {"name": "GateOpenTimeline", "type": "UTimelineComponent", "parent": None, "length": 3.5, "curve": "MechanicalCubic"}
        ],
        "variables": [
            {"name": "IsLocked", "type": "bool", "default": True, "replicated": True},
            {"name": "IsOpening", "type": "bool", "default": False, "replicated": True},
            {"name": "OpenDuration", "type": "float", "default": 3.5, "editable": True},
            {"name": "GateRetractionDistance", "type": "float", "default": 260.0, "editable": True},
            {"name": "WarningStrobeRate", "type": "float", "default": 1.5, "editable": True}
        ],
        "events": [
            "UnlockAndOpenGate()",
            "OnGateFullyOpened()"
        ]
    },
    {
        "category": "Interactive",
        "name": "BP_ControlTerminal",
        "parent_class": "Actor",
        "implemented_interfaces": ["BPI_Interactable"],
        "description": "Interactive cyberpunk hacking and security clearance console linked to BP_LockedGate.",
        "components": [
            {"name": "DefaultSceneRoot", "type": "USceneComponent", "parent": None},
            {"name": "TerminalBody", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mesh": "SM_ControlTerminal", "mobility": "Static"},
            {"name": "ScreenMesh", "type": "UStaticMeshComponent", "parent": "TerminalBody", "mesh": "SM_Monitor_Screen", "mobility": "Static"},
            {"name": "StatusLight", "type": "UPointLightComponent", "parent": "ScreenMesh", "color": [0, 220, 255], "intensity": 1800.0},
            {"name": "InteractionCollision", "type": "USphereComponent", "parent": "TerminalBody", "radius": 120.0, "collision_profile": "Trigger"},
            {"name": "TerminalWidget", "type": "UWidgetComponent", "parent": "ScreenMesh"},
            {"name": "KeypadAudio", "type": "UAudioComponent", "parent": "TerminalBody"}
        ],
        "variables": [
            {"name": "IsActive", "type": "bool", "default": True, "editable": True},
            {"name": "IsGateUnlocked", "type": "bool", "default": False, "replicated": True},
            {"name": "TargetGateRef", "type": "TSoftObjectPtr<ABP_LockedGate>", "default": None, "editable": True},
            {"name": "TerminalID", "type": "FName", "default": "TERM_GATE_09", "editable": True}
        ],
        "events": [
            "OnInteract(AActor* Caller)",
            "OnSecurityOverrideComplete()"
        ]
    },
    {
        "category": "Interactive",
        "name": "BP_InteractablePanel",
        "parent_class": "Actor",
        "implemented_interfaces": ["BPI_Interactable"],
        "description": "Wall-mounted flush console for breaker resets, vent overrides, and auxiliary power.",
        "components": [
            {"name": "DefaultSceneRoot", "type": "USceneComponent", "parent": None},
            {"name": "PanelMesh", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mesh": "SM_Access_Panel", "mobility": "Static"},
            {"name": "IndicatorLight", "type": "UPointLightComponent", "parent": "PanelMesh", "color": [255, 30, 30], "intensity": 800.0},
            {"name": "InteractionBox", "type": "UBoxComponent", "parent": "DefaultSceneRoot", "extent": [80, 80, 120], "collision_profile": "Trigger"},
            {"name": "ClickAudio", "type": "UAudioComponent", "parent": "PanelMesh"}
        ],
        "variables": [
            {"name": "IsActivated", "type": "bool", "default": False, "replicated": True},
            {"name": "InteractionEnabled", "type": "bool", "default": True, "editable": True},
            {"name": "PanelEventTag", "type": "FName", "default": "Panel_Power_Aux", "editable": True}
        ],
        "events": [
            "OnInteract(AActor* Caller)",
            "OnPanelTriggered(FName Tag)"
        ]
    },
    {
        "category": "Lift",
        "name": "BP_LiftPlatform",
        "parent_class": "Actor",
        "description": "Elevator platform inside Sector 09 vertical shaft with safety railings and audio cues.",
        "components": [
            {"name": "DefaultSceneRoot", "type": "USceneComponent", "parent": None},
            {"name": "TopPositionScene", "type": "USceneComponent", "parent": "DefaultSceneRoot"},
            {"name": "PlatformMesh", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mesh": "SM_LiftPlatform", "mobility": "Movable"},
            {"name": "Railings", "type": "UStaticMeshComponent", "parent": "PlatformMesh", "mesh": "SM_Railing_Straight", "mobility": "Movable"},
            {"name": "UnderglowLight", "type": "UPointLightComponent", "parent": "PlatformMesh", "color": [0, 220, 255], "intensity": 2500.0},
            {"name": "LiftAudio", "type": "UAudioComponent", "parent": "PlatformMesh"},
            {"name": "LiftMovementTimeline", "type": "UTimelineComponent", "parent": None, "length": 5.0, "curve": "HermiteSmooth"}
        ],
        "variables": [
            {"name": "IsAtBottom", "type": "bool", "default": True, "replicated": True},
            {"name": "IsMoving", "type": "bool", "default": False, "replicated": True},
            {"name": "TravelDistance", "type": "float", "default": 1200.0, "editable": True},
            {"name": "TravelDuration", "type": "float", "default": 5.0, "editable": True}
        ],
        "events": [
            "CallLift()",
            "OnLiftDeparted(bool bWasAtBottom)",
            "OnLiftArrived(bool bIsAtBottom)"
        ]
    },
    {
        "category": "Lighting",
        "name": "BP_NeonLight",
        "parent_class": "Actor",
        "description": "Atmospheric cyberpunk neon bar casting rich colored bounce illumination with dynamic color switching.",
        "components": [
            {"name": "DefaultSceneRoot", "type": "USceneComponent", "parent": None},
            {"name": "NeonStripMesh", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mesh": "SM_Neon_Light_Cyan", "mobility": "Static"},
            {"name": "PointLight", "type": "UPointLightComponent", "parent": "NeonStripMesh", "color": [0, 230, 255], "intensity": 3500.0, "attenuation": 600.0}
        ],
        "variables": [
            {"name": "NeonColour", "type": "FLinearColor", "default": [0.0, 0.90, 1.0, 1.0], "editable": True},
            {"name": "EmissiveIntensity", "type": "float", "default": 15.0, "editable": True},
            {"name": "LightIntensity", "type": "float", "default": 3500.0, "editable": True},
            {"name": "IsEnabled", "type": "bool", "default": True, "editable": True}
        ],
        "events": [
            "UserConstructionScript()",
            "ToggleLight(bool bEnable)"
        ]
    },
    {
        "category": "Environmental",
        "name": "BP_SurveillanceCamera",
        "parent_class": "Actor",
        "description": "Environmental security camera prop with sweeping volumetric light cone and alert state.",
        "components": [
            {"name": "DefaultSceneRoot", "type": "USceneComponent", "parent": None},
            {"name": "CameraMount", "type": "UStaticMeshComponent", "parent": "DefaultSceneRoot", "mobility": "Static"},
            {"name": "SwivelRoot", "type": "USceneComponent", "parent": "CameraMount", "mobility": "Movable"},
            {"name": "CameraHousingMesh", "type": "UStaticMeshComponent", "parent": "SwivelRoot", "mesh": "SM_SurveillanceCamera", "mobility": "Movable"},
            {"name": "VisionSpotLight", "type": "USpotLightComponent", "parent": "SwivelRoot", "color": [0, 215, 255], "intensity": 2500.0, "inner_cone": 25.0, "outer_cone": 45.0},
            {"name": "CameraAudio", "type": "UAudioComponent", "parent": "CameraHousingMesh"},
            {"name": "SweepTimeline", "type": "UTimelineComponent", "parent": None, "length": 4.0, "curve": "PingPong"}
        ],
        "variables": [
            {"name": "RotationSpeed", "type": "float", "default": 25.0, "editable": True},
            {"name": "SweepAngleMax", "type": "float", "default": 60.0, "editable": True},
            {"name": "IsActive", "type": "bool", "default": True, "editable": True}
        ],
        "events": [
            "EventBeginPlay()",
            "DisableCamera()",
            "TriggerAlert(bool bAlert)"
        ]
    }
]

for bp in BLUEPRINTS:
    cat_dir = os.path.join(BP_ROOT, bp["category"])
    os.makedirs(cat_dir, exist_ok=True)
    target_file = os.path.join(cat_dir, f"{bp['name']}.json")
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(bp, f, indent=2)

print(f"Generated all {len(BLUEPRINTS)} Blueprint architecture specifications under Assets/Blueprints/.")
