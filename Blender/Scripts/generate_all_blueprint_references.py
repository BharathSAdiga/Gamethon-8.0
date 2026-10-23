"""
Master generator for all 7 technical Blueprint reference images for Level 1 Sector 09.
All images are rendered at 2560x1440 resolution and saved in Assets/Reference/Blueprints/:
1. BP_IndustrialDoor_Reference.png
2. BP_LockedGate_Reference.png
3. BP_ControlTerminal_Reference.png
4. BP_LiftPlatform_Reference.png
5. BP_SurveillanceCamera_Reference.png
6. BP_InteractablePanel_Reference.png
7. BP_NeonLight_Reference.png
"""

import os
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = r"d:\unreal engine"
OUT_DIR = os.path.join(REPO_ROOT, "Assets", "Reference", "Blueprints")
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 2560, 1440

# Fonts
font_title = ImageFont.truetype("bahnschrift.ttf", 46)
font_subtitle = ImageFont.truetype("bahnschrift.ttf", 24)
font_sec_hdr = ImageFont.truetype("bahnschrift.ttf", 26)
font_body_bold = ImageFont.truetype("segoeui.ttf", 20)
font_body = ImageFont.truetype("segoeui.ttf", 18)
font_code = ImageFont.truetype("consola.ttf", 17)
font_node_title = ImageFont.truetype("segoeui.ttf", 18)
font_node_pin = ImageFont.truetype("segoeui.ttf", 15)

# Color Palette
BG_DARK = (11, 14, 20, 255)
BG_PANEL = (17, 23, 34, 255)
BG_PANEL_HDR = (23, 32, 48, 255)
BORDER_CYAN = (0, 210, 255, 180)
BORDER_PURPLE = (170, 45, 230, 180)
BORDER_MUTED = (40, 52, 72, 255)
TEXT_WHITE = (240, 245, 255, 255)
TEXT_MUTED = (140, 158, 180, 255)
CYAN_ACCENT = (0, 230, 255, 255)
PURPLE_ACCENT = (195, 75, 255, 255)
RED_ACCENT = (255, 60, 60, 255)
GREEN_ACCENT = (50, 230, 110, 255)
ORANGE_ACCENT = (255, 160, 20, 255)

PIN_EXEC = (255, 255, 255, 255)
PIN_BOOL = (220, 40, 40, 255)
PIN_FLOAT = (120, 230, 70, 255)
PIN_VECTOR = (240, 210, 40, 255)
PIN_OBJECT = (50, 160, 240, 255)

def draw_header(draw, title, category, actor_class):
    draw.rectangle([0, 0, W, 100], fill=(14, 18, 28, 255))
    draw.line([0, 99, W, 99], fill=BORDER_CYAN, width=2)
    draw.line([0, 102, W, 102], fill=(0, 210, 255, 60), width=3)
    draw.text((50, 22), title, fill=CYAN_ACCENT, font=font_title)
    draw.text((50 + draw.textlength(title, font=font_title) + 30, 36),
              f"|  {category}  |  Unreal Engine 5.6 Native Blueprint  |  Class: {actor_class}",
              fill=TEXT_MUTED, font=font_subtitle)
    draw.text((W - 550, 32), "LAST SECOND — SECTOR 09", fill=PURPLE_ACCENT, font=font_sec_hdr)
    draw.text((W - 550, 62), "LEVEL 1 TECHNICAL ARCHITECTURE SPEC", fill=TEXT_MUTED, font=font_body)

def draw_panel(draw, x, y, w, h, title, border_col=BORDER_MUTED):
    draw.rectangle([x, y, x+w, y+h], fill=BG_PANEL, outline=border_col, width=2)
    draw.rectangle([x, y, x+w, y+42], fill=BG_PANEL_HDR)
    draw.line([x, y+42, x+w, y+42], fill=border_col, width=1)
    draw.line([x, y, x+15, y], fill=CYAN_ACCENT, width=3)
    draw.line([x, y, x, y+15], fill=CYAN_ACCENT, width=3)
    draw.line([x+w-15, y+h, x+w, y+h], fill=PURPLE_ACCENT, width=3)
    draw.line([x+w, y+h-15, x+w, y+h], fill=PURPLE_ACCENT, width=3)
    draw.text((x + 18, y + 8), title, fill=CYAN_ACCENT, font=font_sec_hdr)

def draw_ue_node(draw, x, y, w, h, title, header_col, inputs, outputs):
    draw.rectangle([x, y, x+w, y+h], fill=(22, 26, 35, 255), outline=(50, 60, 80, 255), width=2)
    draw.rectangle([x, y, x+w, y+28], fill=header_col)
    draw.text((x+12, y+5), title, fill=TEXT_WHITE, font=font_node_title)
    curr_y = y + 36
    for pin_name, pin_type in inputs:
        draw.ellipse([x+8, curr_y+3, x+18, curr_y+13], fill=pin_type, outline=(255, 255, 255, 200))
        draw.text((x+24, curr_y), pin_name, fill=TEXT_WHITE, font=font_node_pin)
        curr_y += 24
    curr_y = y + 36
    for pin_name, pin_type in outputs:
        draw.ellipse([x+w-18, curr_y+3, x+w-8, curr_y+13], fill=pin_type, outline=(255, 255, 255, 200))
        txt_len = draw.textlength(pin_name, font=font_node_pin)
        draw.text((x+w-24-txt_len, curr_y), pin_name, fill=TEXT_WHITE, font=font_node_pin)
        curr_y += 24

def draw_wire(draw, start, end, col=TEXT_WHITE, width=2):
    x1, y1 = start
    x2, y2 = end
    mid_x = (x1 + x2) // 2
    draw.line([x1, y1, mid_x, y1], fill=col, width=width)
    draw.line([mid_x, y1, mid_x, y2], fill=col, width=width)
    draw.line([mid_x, y2, x2, y2], fill=col, width=width)


# -------------------------------------------------------------
# 1. BP_IndustrialDoor
# -------------------------------------------------------------
def make_bp_industrial_door():
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "BP_IndustrialDoor", "Interactive Architecture", "AActor")
    
    # 1. Purpose
    draw_panel(draw, 50, 120, 750, 240, "1. ACTOR PURPOSE & PERFORMANCE SPEC")
    cy = 175
    for lbl, val in [
        ("Summary:", "Reusable industrial sliding door with smooth vertical travel."),
        ("Level 1 Context:", "Used at Sector 09 corridors, airlocks, and security checkpoints."),
        ("Gameplay Role:", "Standard interactive doorway triggered via interact key or proximity sensor."),
        ("Tick Policy:", "Tick Disabled (bCanEverTick = false). Movement driven via Timeline curve."),
        ("Collision:", "Frame has BlockAll; Door Panel uses BlockAllDynamic. Simple box collision bounds."),
        ("Replication:", "Server-authoritative state replicated with OnRep_IsOpen client interpolation.")
    ]:
        draw.text((70, cy), lbl, fill=CYAN_ACCENT, font=font_body_bold)
        draw.text((220, cy), val, fill=TEXT_WHITE, font=font_body)
        cy += 27

    # 2. Components
    draw_panel(draw, 50, 380, 750, 300, "2. COMPONENT HIERARCHY")
    cy = 435
    for c_type, c_desc in [
        ("[Root]", "DefaultSceneRoot (USceneComponent) — Absolute World Placement"),
        ("├── [Mesh]", "DoorFrame (UStaticMeshComponent: SM_Door_Frame) — Static Collision Anchor"),
        ("├── [Mesh]", "DoorPanel (UStaticMeshComponent: SM_Industrial_Door) — Movable Shutter"),
        ("├── [Light]", "IndicatorLight (UPointLightComponent) — Red (Closed) / Cyan (Open) Status"),
        ("├── [Collision]", "InteractionBox (UBoxComponent) — Size: (120, 180, 220), QueryOnly Collision"),
        ("├── [Audio]", "DoorAudioComp (UAudioComponent) — Hydraulic hiss & heavy clamp sfx"),
        ("└── [Timeline]", "DoorTimeline (UTimelineComponent) — 1.2s Float Curve (EaseInOut)")
    ]:
        draw.text((70, cy), c_type, fill=PURPLE_ACCENT, font=font_code)
        draw.text((200, cy), c_desc, fill=TEXT_WHITE, font=font_body)
        cy += 34

    # 3. Variables
    draw_panel(draw, 50, 700, 750, 400, "3. IMPORTANT VARIABLES & DEFAULTS")
    for h_txt, h_x in [("Variable Name", 70), ("Type", 320), ("Default Value", 470), ("Category / Description", 600)]:
        draw.text((h_x, 750), h_txt, fill=CYAN_ACCENT, font=font_body_bold)
    draw.line([70, 778, 770, 778], fill=BORDER_MUTED, width=1)
    cy = 790
    for v_name, v_type, v_def, v_desc in [
        ("IsOpen", "Boolean", "False", "State / Replicated"),
        ("CanInteract", "Boolean", "True", "State / Lockout guard"),
        ("OpenDuration", "Float", "1.2", "Config / Timeline length"),
        ("ClosedTransform", "Transform", "[Relative Zero]", "Internal / Cached origin"),
        ("OpenHeightOffset", "Float", "240.0", "Config / Vertical slide (cm)"),
        ("DoorCloseDelay", "Float", "5.0", "Config / Auto-close timer"),
        ("AutoCloseEnabled", "Boolean", "False", "Config / Keep open or timer"),
        ("DynamicMatInstance", "UMaterialInstanceDynamic*", "None", "Visuals / Dynamic emissive")
    ]:
        draw.text((70, cy), v_name, fill=TEXT_WHITE, font=font_code)
        draw.text((320, cy), v_type, fill=ORANGE_ACCENT, font=font_code)
        draw.text((470, cy), v_def, fill=GREEN_ACCENT, font=font_code)
        draw.text((600, cy), v_desc, fill=TEXT_MUTED, font=font_body)
        cy += 32

    # 4. Logic Graph
    draw_panel(draw, 830, 120, 1680, 680, "4. BLUEPRINT EVENT FLOW & LOGIC GRAPH")
    draw_ue_node(draw, 870, 180, 240, 120, "BPI_Interact (Event)", (180, 40, 40, 255), [], [("Exec", PIN_EXEC), ("Instigator", PIN_OBJECT)])
    draw_ue_node(draw, 1160, 180, 200, 120, "Branch", (90, 90, 90, 255), [("Exec", PIN_EXEC), ("Condition", PIN_BOOL)], [("True", PIN_EXEC), ("False", PIN_EXEC)])
    draw_ue_node(draw, 1420, 180, 220, 110, "Set CanInteract", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("Value (False)", PIN_BOOL)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1690, 180, 240, 110, "Play Sound at Loc", (40, 100, 120, 255), [("Exec", PIN_EXEC), ("Sound", PIN_OBJECT)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1980, 180, 240, 150, "Timeline (OpenDoor)", (160, 120, 30, 255), [("Play / Reverse", PIN_EXEC)], [("Update", PIN_EXEC), ("Finished", PIN_EXEC), ("Alpha", PIN_FLOAT)])
    draw_ue_node(draw, 1880, 380, 220, 130, "Lerp (Vector)", (40, 120, 60, 255), [("A (Closed)", PIN_VECTOR), ("B (Open)", PIN_VECTOR), ("Alpha", PIN_FLOAT)], [("Return Value", PIN_VECTOR)])
    draw_ue_node(draw, 2150, 380, 280, 130, "SetRelativeLocation", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("Target (Panel)", PIN_OBJECT), ("NewLoc", PIN_VECTOR)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1520, 520, 260, 120, "Toggle IsOpen State", (120, 40, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC), ("IsOpen", PIN_BOOL)])
    draw_ue_node(draw, 1830, 520, 250, 120, "Set CanInteract = True", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("Value (True)", PIN_BOOL)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2130, 520, 280, 120, "Update Status Light", (0, 120, 140, 255), [("Exec", PIN_EXEC), ("LightColor", PIN_VECTOR)], [("Exec", PIN_EXEC)])

    draw_wire(draw, (1110, 216), (1160, 216), PIN_EXEC)
    draw_wire(draw, (1360, 216), (1420, 216), PIN_EXEC)
    draw_wire(draw, (1640, 216), (1690, 216), PIN_EXEC)
    draw_wire(draw, (1930, 216), (1980, 216), PIN_EXEC)
    draw_wire(draw, (2220, 216), (2250, 320), PIN_EXEC)
    draw_wire(draw, (2250, 320), (2150, 416), PIN_EXEC)
    draw_wire(draw, (2220, 264), (1880, 464), PIN_FLOAT)
    draw_wire(draw, (2100, 416), (2150, 464), PIN_VECTOR)
    draw_wire(draw, (2220, 240), (2260, 360), PIN_EXEC)
    draw_wire(draw, (2260, 360), (1520, 556), PIN_EXEC)
    draw_wire(draw, (1780, 556), (1830, 556), PIN_EXEC)
    draw_wire(draw, (2080, 556), (2130, 556), PIN_EXEC)

    # 5. Inputs / Outputs
    draw_panel(draw, 830, 820, 800, 570, "5. INPUTS, OUTPUTS & INTERFACES")
    draw.text((860, 875), "IMPLEMENTED INTERFACE: BPI_Interactable", fill=CYAN_ACCENT, font=font_body_bold)
    cy = 920
    for n_title, n_desc in [
        ("Input Function:", "OnInteract(AActor* Caller) — Triggers open/close cycle if unlocked."),
        ("Input Function:", "ForceLockDoor(bool bLock) — Locks door and forces warning state."),
        ("Input Function:", "TriggerProximityOpen() — Automated opening for AI / patrol drones."),
        ("Output Event:", "OnDoorOpened(AActor* DoorRef) — Dispatched upon reaching max travel."),
        ("Output Event:", "OnDoorClosed(AActor* DoorRef) — Dispatched upon complete seal."),
        ("Audio FX:", "SFX_Pneumatic_Release (Start) | SFX_Heavy_Hydraulic_Loop (Moving) | SFX_Clamp_Latch (End)"),
        ("Dynamic Material:", "Scalar Param 'StatusGlow' set to 0.0 (Closed Red) or 1.0 (Open Cyan).")
    ]:
        draw.text((860, cy), n_title, fill=PURPLE_ACCENT, font=font_body_bold)
        draw.text((1020, cy), n_desc, fill=TEXT_WHITE, font=font_body)
        cy += 44

    # 6. Expected Result Visual
    draw_panel(draw, 1660, 820, 850, 570, "6. EXPECTED IN-GAME RESULT & VISUAL STATE")
    draw.rectangle([1700, 880, 2460, 1340], fill=(14, 18, 25, 255), outline=BORDER_CYAN, width=1)
    # Closed Door
    draw.rectangle([1740, 930, 2040, 1290], fill=(24, 30, 42, 255), outline=CYAN_ACCENT, width=3)
    draw.rectangle([1770, 960, 2010, 1260], fill=(40, 46, 58, 255), outline=(60, 70, 85, 255), width=2)
    draw.ellipse([1870, 940, 1910, 955], fill=RED_ACCENT)
    draw.text((1760, 1300), "STATE: CLOSED (Locked/Sealed)", fill=RED_ACCENT, font=font_body_bold)
    # Open Door
    draw.rectangle([2120, 930, 2420, 1290], fill=(24, 30, 42, 255), outline=CYAN_ACCENT, width=3)
    draw.rectangle([2150, 940, 2390, 1030], fill=(40, 46, 58, 255), outline=(60, 70, 85, 255), width=2)
    draw.rectangle([2150, 1030, 2390, 1260], fill=(10, 12, 16, 255))
    draw.ellipse([2250, 940, 2290, 955], fill=CYAN_ACCENT)
    draw.text((2140, 1300), "STATE: OPEN (Cleared Passage)", fill=CYAN_ACCENT, font=font_body_bold)

    img.save(os.path.join(OUT_DIR, "BP_IndustrialDoor_Reference.png"))
    print("Exported: BP_IndustrialDoor_Reference.png")


# -------------------------------------------------------------
# 2. BP_LockedGate
# -------------------------------------------------------------
def make_bp_locked_gate():
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "BP_LockedGate", "Level Transition Architecture", "AActor")
    
    # 1. Purpose
    draw_panel(draw, 50, 120, 750, 240, "1. ACTOR PURPOSE & PERFORMANCE SPEC")
    cy = 175
    for lbl, val in [
        ("Summary:", "Heavy armored mechanical gate sealing the Sector 09 Level 1 exit."),
        ("Level 1 Context:", "Blocks progression until the adjacent control terminal is hacked/activated."),
        ("Gameplay Role:", "End-of-level climax gate; unlocks with siren, strobe lights, and hydraulic recoil."),
        ("Tick Policy:", "Tick Disabled. Uses Timer for warning strobe, Timeline for mechanical slide."),
        ("Collision:", "GateFrame uses BlockAll; Shutter panels use BlockAllDynamic. Prevents skip."),
        ("Replication:", "Server-replicated bIsLocked flag with client FX multicasts.")
    ]:
        draw.text((70, cy), lbl, fill=CYAN_ACCENT, font=font_body_bold)
        draw.text((220, cy), val, fill=TEXT_WHITE, font=font_body)
        cy += 27

    # 2. Components
    draw_panel(draw, 50, 380, 750, 300, "2. COMPONENT HIERARCHY")
    cy = 435
    for c_type, c_desc in [
        ("[Root]", "DefaultSceneRoot (USceneComponent) — Root Transform Anchor"),
        ("├── [Mesh]", "GateFrame (UStaticMeshComponent: SM_Large_Gate) — Massive Structural Support"),
        ("├── [Mesh]", "GateShutterLeft (UStaticMeshComponent) — Horizontal Sliding Leaf Left"),
        ("├── [Mesh]", "GateShutterRight (UStaticMeshComponent) — Horizontal Sliding Leaf Right"),
        ("├── [Light]", "WarningStrobeLight (UPointLightComponent) — Pulsing Red Warning Beacon"),
        ("├── [Audio]", "AlarmSirenAudio (UAudioComponent) — Heavy mechanical klaxon & air-release"),
        ("└── [Timeline]", "GateOpenTimeline (UTimelineComponent) — 3.5s Mechanical Travel Curve")
    ]:
        draw.text((70, cy), c_type, fill=PURPLE_ACCENT, font=font_code)
        draw.text((200, cy), c_desc, fill=TEXT_WHITE, font=font_body)
        cy += 34

    # 3. Variables
    draw_panel(draw, 50, 700, 750, 400, "3. IMPORTANT VARIABLES & DEFAULTS")
    for h_txt, h_x in [("Variable Name", 70), ("Type", 320), ("Default Value", 470), ("Category / Description", 600)]:
        draw.text((h_x, 750), h_txt, fill=CYAN_ACCENT, font=font_body_bold)
    draw.line([70, 778, 770, 778], fill=BORDER_MUTED, width=1)
    cy = 790
    for v_name, v_type, v_def, v_desc in [
        ("IsLocked", "Boolean", "True", "State / Replicated"),
        ("IsOpening", "Boolean", "False", "State / Lockout guard"),
        ("OpenDuration", "Float", "3.5", "Config / Heavy gate travel (s)"),
        ("GateTravelDistance", "Float", "260.0", "Config / Horizontal retraction (cm)"),
        ("WarningStrobeRate", "Float", "1.5", "Config / Strobe flash rate (Hz)"),
        ("LinkedTerminal", "ABP_ControlTerminal*", "None", "Reference / Associated console"),
        ("EndLevelTriggerVolume", "ABoxTrigger*", "None", "Level Design / Sector 02 transition")
    ]:
        draw.text((70, cy), v_name, fill=TEXT_WHITE, font=font_code)
        draw.text((320, cy), v_type, fill=ORANGE_ACCENT, font=font_code)
        draw.text((470, cy), v_def, fill=GREEN_ACCENT, font=font_code)
        draw.text((600, cy), v_desc, fill=TEXT_MUTED, font=font_body)
        cy += 32

    # 4. Logic Graph
    draw_panel(draw, 830, 120, 1680, 680, "4. BLUEPRINT EVENT FLOW & LOGIC GRAPH")
    draw_ue_node(draw, 870, 180, 260, 120, "CustomEvent: UnlockGate", (180, 40, 40, 255), [], [("Exec", PIN_EXEC), ("UnlockCaller", PIN_OBJECT)])
    draw_ue_node(draw, 1180, 180, 200, 120, "Branch", (90, 90, 90, 255), [("Exec", PIN_EXEC), ("Condition", PIN_BOOL)], [("True", PIN_EXEC), ("False", PIN_EXEC)])
    draw_ue_node(draw, 1440, 180, 230, 110, "Set IsOpening = True", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("Value (True)", PIN_BOOL)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1720, 180, 250, 110, "Clear Warning Timer", (140, 80, 40, 255), [("Exec", PIN_EXEC), ("TimerHandle", PIN_OBJECT)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2020, 180, 240, 150, "Timeline (GateTravel)", (160, 120, 30, 255), [("PlayFromStart", PIN_EXEC)], [("Update", PIN_EXEC), ("Finished", PIN_EXEC), ("Alpha", PIN_FLOAT)])
    draw_ue_node(draw, 1820, 380, 240, 130, "Lerp Dual Panels", (40, 120, 60, 255), [("Alpha", PIN_FLOAT)], [("LeftLoc", PIN_VECTOR), ("RightLoc", PIN_VECTOR)])
    draw_ue_node(draw, 2120, 380, 310, 130, "Set Panel Rel Locations", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("LeftLoc", PIN_VECTOR), ("RightLoc", PIN_VECTOR)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1500, 530, 280, 120, "Set Strobe Light to Cyan", (0, 120, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1830, 530, 290, 120, "Enable Level Transition", (120, 40, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])

    draw_wire(draw, (1130, 216), (1180, 216), PIN_EXEC)
    draw_wire(draw, (1380, 216), (1440, 216), PIN_EXEC)
    draw_wire(draw, (1670, 216), (1720, 216), PIN_EXEC)
    draw_wire(draw, (1970, 216), (2020, 216), PIN_EXEC)
    draw_wire(draw, (2260, 216), (2280, 320), PIN_EXEC)
    draw_wire(draw, (2280, 320), (2120, 416), PIN_EXEC)
    draw_wire(draw, (2260, 264), (1820, 416), PIN_FLOAT)
    draw_wire(draw, (2060, 416), (2120, 440), PIN_VECTOR)
    draw_wire(draw, (2260, 240), (2290, 360), PIN_EXEC)
    draw_wire(draw, (2290, 360), (1500, 566), PIN_EXEC)
    draw_wire(draw, (1780, 566), (1830, 566), PIN_EXEC)

    # 5. Inputs / Outputs
    draw_panel(draw, 830, 820, 800, 570, "5. INPUTS, OUTPUTS & INTERFACES")
    draw.text((860, 875), "GATE SECURITY LOGIC INTERFACE", fill=CYAN_ACCENT, font=font_body_bold)
    cy = 920
    for n_title, n_desc in [
        ("Public Event:", "UnlockGate() — Callable by BP_ControlTerminal upon successful hack."),
        ("Public Event:", "LockGate() — Resets gate to locked condition with sirens."),
        ("Internal Strobe:", "Timer-driven function cycling WarningStrobeLight at 1.5Hz."),
        ("Output Dispatcher:", "OnGateFullyOpened — Triggers music cue, opens path to Sector 02."),
        ("Sound Effects:", "SFX_Gate_HeavyMotors, SFX_Hydraulic_Decompression, SFX_MetalClash_End."),
        ("Light Color:", "Locked: Glowing Red (255, 20, 20) | Unlocked: High-tech Cyan (0, 220, 255).")
    ]:
        draw.text((860, cy), n_title, fill=PURPLE_ACCENT, font=font_body_bold)
        draw.text((1020, cy), n_desc, fill=TEXT_WHITE, font=font_body)
        cy += 44

    # 6. Expected Result Visual
    draw_panel(draw, 1660, 820, 850, 570, "6. EXPECTED IN-GAME RESULT & VISUAL STATE")
    draw.rectangle([1700, 880, 2460, 1340], fill=(14, 18, 25, 255), outline=BORDER_CYAN, width=1)
    # Locked
    draw.rectangle([1730, 930, 2050, 1290], fill=(24, 30, 42, 255), outline=RED_ACCENT, width=3)
    draw.rectangle([1760, 960, 2020, 1260], fill=(45, 20, 20, 255), outline=RED_ACCENT, width=2)
    draw.text((1770, 1070), "LOCKED / RESTRICTED", fill=RED_ACCENT, font=font_body_bold)
    draw.text((1740, 1300), "STATUS: LOCKED (Siren Active)", fill=RED_ACCENT, font=font_body_bold)
    # Unlocked
    draw.rectangle([2110, 930, 2430, 1290], fill=(24, 30, 42, 255), outline=CYAN_ACCENT, width=3)
    draw.rectangle([2130, 960, 2230, 1260], fill=(30, 45, 55, 255), outline=CYAN_ACCENT, width=2)
    draw.rectangle([2310, 960, 2410, 1260], fill=(30, 45, 55, 255), outline=CYAN_ACCENT, width=2)
    draw.rectangle([2230, 960, 2310, 1260], fill=(10, 14, 20, 255))
    draw.text((2120, 1300), "STATUS: UNLOCKED (Passage Open)", fill=CYAN_ACCENT, font=font_body_bold)

    img.save(os.path.join(OUT_DIR, "BP_LockedGate_Reference.png"))
    print("Exported: BP_LockedGate_Reference.png")


# -------------------------------------------------------------
# 3. BP_ControlTerminal
# -------------------------------------------------------------
def make_bp_control_terminal():
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "BP_ControlTerminal", "Interactive Tech / Gameplay", "AActor")
    
    # 1. Purpose
    draw_panel(draw, 50, 120, 750, 240, "1. ACTOR PURPOSE & PERFORMANCE SPEC")
    cy = 175
    for lbl, val in [
        ("Summary:", "Cyberpunk computer console standing adjacent to the locked mechanical gate."),
        ("Level 1 Context:", "Allows player to initiate security override to unlock the blast doors."),
        ("Gameplay Role:", "Interactive focal objective; emits cyan cybernetic glow and keypad audio."),
        ("Tick Policy:", "Tick Disabled. Event-driven interaction via player trace/overlap."),
        ("Collision:", "Pillar base has BlockAll; Interaction Sphere has QueryOnly (Pawn overlap)."),
        ("Replication:", "Server-validated interaction state; propagates screen state to all clients.")
    ]:
        draw.text((70, cy), lbl, fill=CYAN_ACCENT, font=font_body_bold)
        draw.text((220, cy), val, fill=TEXT_WHITE, font=font_body)
        cy += 27

    # 2. Components
    draw_panel(draw, 50, 380, 750, 300, "2. COMPONENT HIERARCHY")
    cy = 435
    for c_type, c_desc in [
        ("[Root]", "DefaultSceneRoot (USceneComponent) — Base Anchor Point"),
        ("├── [Mesh]", "TerminalPedestal (UStaticMeshComponent: SM_ControlTerminal) — Metal Base"),
        ("├── [Mesh]", "AngledMonitor (UStaticMeshComponent: SM_Monitor_Screen) — Display Mesh"),
        ("├── [Collision]", "InteractionRadius (USphereComponent) — Radius: 120cm Interaction Zone"),
        ("├── [Light]", "ConsoleLight (UPointLightComponent) — Ambient Cyan Keyboard Wash"),
        ("├── [Widget]", "ScreenWidgetComp (UWidgetComponent) — Cyberpunk Terminal GUI Display"),
        ("└── [Audio]", "KeypadAudioComp (UAudioComponent) — Cyberpunk chirps & override sfx")
    ]:
        draw.text((70, cy), c_type, fill=PURPLE_ACCENT, font=font_code)
        draw.text((200, cy), c_desc, fill=TEXT_WHITE, font=font_body)
        cy += 34

    # 3. Variables
    draw_panel(draw, 50, 700, 750, 400, "3. IMPORTANT VARIABLES & DEFAULTS")
    for h_txt, h_x in [("Variable Name", 70), ("Type", 320), ("Default Value", 470), ("Category / Description", 600)]:
        draw.text((h_x, 750), h_txt, fill=CYAN_ACCENT, font=font_body_bold)
    draw.line([70, 778, 770, 778], fill=BORDER_MUTED, width=1)
    cy = 790
    for v_name, v_type, v_def, v_desc in [
        ("IsActive", "Boolean", "True", "Config / Terminal operational flag"),
        ("IsGateUnlocked", "Boolean", "False", "State / Gate clearance status"),
        ("TargetGate", "ABP_LockedGate*", "None", "Instance Editable / Target gate reference"),
        ("TerminalID", "FName", "'TERM_09_EXIT'", "Config / Diagnostic tracking tag"),
        ("HackDuration", "Float", "1.5", "Config / Interaction hold length (s)"),
        ("ScreenMaterialInstance", "UMaterialInstanceDynamic*", "None", "Visuals / Screen emissive switcher")
    ]:
        draw.text((70, cy), v_name, fill=TEXT_WHITE, font=font_code)
        draw.text((320, cy), v_type, fill=ORANGE_ACCENT, font=font_code)
        draw.text((470, cy), v_def, fill=GREEN_ACCENT, font=font_code)
        draw.text((600, cy), v_desc, fill=TEXT_MUTED, font=font_body)
        cy += 32

    # 4. Logic Graph
    draw_panel(draw, 830, 120, 1680, 680, "4. BLUEPRINT EVENT FLOW & LOGIC GRAPH")
    draw_ue_node(draw, 870, 180, 240, 120, "BPI_Interact (Event)", (180, 40, 40, 255), [], [("Exec", PIN_EXEC), ("Instigator", PIN_OBJECT)])
    draw_ue_node(draw, 1160, 180, 210, 120, "Branch (CanHack)", (90, 90, 90, 255), [("Exec", PIN_EXEC), ("Condition", PIN_BOOL)], [("True", PIN_EXEC), ("False", PIN_EXEC)])
    draw_ue_node(draw, 1430, 180, 230, 110, "Play Terminal SFX", (40, 100, 120, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1710, 180, 260, 110, "Update Dynamic Mat", (0, 120, 140, 255), [("Exec", PIN_EXEC), ("Param: State", PIN_FLOAT)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2020, 180, 270, 130, "Call TargetGate.Unlock", (120, 40, 140, 255), [("Exec", PIN_EXEC), ("Target (Gate)", PIN_OBJECT)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1600, 380, 260, 120, "Set IsGateUnlocked", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("Value (True)", PIN_BOOL)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1920, 380, 280, 120, "Trigger Clearance Widget", (40, 120, 60, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])

    draw_wire(draw, (1110, 216), (1160, 216), PIN_EXEC)
    draw_wire(draw, (1370, 216), (1430, 216), PIN_EXEC)
    draw_wire(draw, (1660, 216), (1710, 216), PIN_EXEC)
    draw_wire(draw, (1970, 216), (2020, 216), PIN_EXEC)
    draw_wire(draw, (2290, 216), (2320, 320), PIN_EXEC)
    draw_wire(draw, (2320, 320), (1600, 416), PIN_EXEC)
    draw_wire(draw, (1860, 416), (1920, 416), PIN_EXEC)

    # 5. Inputs / Outputs
    draw_panel(draw, 830, 820, 800, 570, "5. INPUTS, OUTPUTS & INTERFACES")
    draw.text((860, 875), "TERMINAL INTERACTION SPECIFICATION", fill=CYAN_ACCENT, font=font_body_bold)
    cy = 920
    for n_title, n_desc in [
        ("Interact Event:", "Triggered when player presses [E] / Action Key within 120cm sphere."),
        ("Target Reference:", "Exposes 'TargetGate' variable (Instance Editable) to wire directly in level."),
        ("Visual Feedback:", "Console screen switches from 'SYSTEM LOCKED' (Red) to 'ACCESS GRANTED' (Cyan)."),
        ("Security Sound:", "Plays chirp sequence, followed by heavy gate release thud."),
        ("Lockout Guard:", "Once unlocked, terminal ignores subsequent interactions to prevent re-trigger.")
    ]:
        draw.text((860, cy), n_title, fill=PURPLE_ACCENT, font=font_body_bold)
        draw.text((1020, cy), n_desc, fill=TEXT_WHITE, font=font_body)
        cy += 44

    # 6. Expected Result Visual
    draw_panel(draw, 1660, 820, 850, 570, "6. EXPECTED IN-GAME RESULT & VISUAL STATE")
    draw.rectangle([1700, 880, 2460, 1340], fill=(14, 18, 25, 255), outline=BORDER_CYAN, width=1)
    # Terminal Stand
    draw.rectangle([1980, 1100, 2180, 1310], fill=(30, 36, 48, 255), outline=CYAN_ACCENT, width=2)
    # Angled screen
    draw.polygon([(1940, 1100), (2220, 1100), (2260, 940), (1900, 940)], fill=(18, 24, 32, 255), outline=CYAN_ACCENT)
    draw.text((1950, 980), "SECTOR 09 SEC-OVERRIDE", fill=CYAN_ACCENT, font=font_body_bold)
    draw.text((1960, 1030), "STATUS: ONLINE / READY", fill=GREEN_ACCENT, font=font_code)
    draw.ellipse([2060, 1230, 2100, 1270], fill=CYAN_ACCENT)
    draw.text((1880, 1315), "INTERACTION: [E] HACK / OVERRIDE GATE", fill=TEXT_WHITE, font=font_body_bold)

    img.save(os.path.join(OUT_DIR, "BP_ControlTerminal_Reference.png"))
    print("Exported: BP_ControlTerminal_Reference.png")


# -------------------------------------------------------------
# 4. BP_LiftPlatform
# -------------------------------------------------------------
def make_bp_lift_platform():
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "BP_LiftPlatform", "Vertical Transport System", "AActor")
    
    # 1. Purpose
    draw_panel(draw, 50, 120, 750, 240, "1. ACTOR PURPOSE & PERFORMANCE SPEC")
    cy = 175
    for lbl, val in [
        ("Summary:", "Modular industrial elevator platform moving between Sector 09 shaft elevations."),
        ("Level 1 Context:", "Connects ground maintenance zone to upper catwalks and control overlook."),
        ("Gameplay Role:", "Player stands on platform and presses call button; deterministic smooth vertical travel."),
        ("Tick Policy:", "Tick Disabled. Movement handled via Timeline component with ease-in/out curve."),
        ("Collision:", "Platform floor uses BlockAll; Railings use BlockAll to prevent player falling off."),
        ("Attachment:", "Player automatically attaches as dynamic base during movement to avoid jitter.")
    ]:
        draw.text((70, cy), lbl, fill=CYAN_ACCENT, font=font_body_bold)
        draw.text((220, cy), val, fill=TEXT_WHITE, font=font_body)
        cy += 27

    # 2. Components
    draw_panel(draw, 50, 380, 750, 300, "2. COMPONENT HIERARCHY")
    cy = 435
    for c_type, c_desc in [
        ("[Root]", "DefaultSceneRoot (USceneComponent) — Bottom Reference Point"),
        ("├── [Scene]", "TopPositionScene (USceneComponent) — Upper Travel Waypoint Target"),
        ("├── [Mesh]", "PlatformMesh (UStaticMeshComponent: SM_LiftPlatform) — Heavy Grated Floor"),
        ("├── [Mesh]", "Railings (UStaticMeshComponent: SM_Railing_Straight) — Safety Perimeter"),
        ("├── [Light]", "UnderglowLight (UPointLightComponent) — Rich Cyan/Purple Shaft Illumination"),
        ("├── [Audio]", "LiftMotorAudio (UAudioComponent) — Looping industrial winch/motor sound"),
        ("└── [Timeline]", "LiftMovementTimeline (UTimelineComponent) — 5.0s Hermite Curve Travel")
    ]:
        draw.text((70, cy), c_type, fill=PURPLE_ACCENT, font=font_code)
        draw.text((200, cy), c_desc, fill=TEXT_WHITE, font=font_body)
        cy += 34

    # 3. Variables
    draw_panel(draw, 50, 700, 750, 400, "3. IMPORTANT VARIABLES & DEFAULTS")
    for h_txt, h_x in [("Variable Name", 70), ("Type", 320), ("Default Value", 470), ("Category / Description", 600)]:
        draw.text((h_x, 750), h_txt, fill=CYAN_ACCENT, font=font_body_bold)
    draw.line([70, 778, 770, 778], fill=BORDER_MUTED, width=1)
    cy = 790
    for v_name, v_type, v_def, v_desc in [
        ("IsAtBottom", "Boolean", "True", "State / Replicated current floor"),
        ("IsMoving", "Boolean", "False", "State / Lockout guard"),
        ("TravelDistance", "Float", "1200.0", "Config / Vertical height delta (cm)"),
        ("TravelDuration", "Float", "5.0", "Config / Timeline length (s)"),
        ("BottomZ", "Float", "0.0", "Internal / Cached bottom coordinate"),
        ("TopZ", "Float", "1200.0", "Internal / Cached top coordinate"),
        ("AutoReturnTime", "Float", "0.0", "Config / 0 = stays at arrival floor")
    ]:
        draw.text((70, cy), v_name, fill=TEXT_WHITE, font=font_code)
        draw.text((320, cy), v_type, fill=ORANGE_ACCENT, font=font_code)
        draw.text((470, cy), v_def, fill=GREEN_ACCENT, font=font_code)
        draw.text((600, cy), v_desc, fill=TEXT_MUTED, font=font_body)
        cy += 32

    # 4. Logic Graph
    draw_panel(draw, 830, 120, 1680, 680, "4. BLUEPRINT EVENT FLOW & LOGIC GRAPH")
    draw_ue_node(draw, 870, 180, 250, 120, "CallLift / Trigger (Event)", (180, 40, 40, 255), [], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1170, 180, 200, 120, "Branch (!IsMoving)", (90, 90, 90, 255), [("Exec", PIN_EXEC), ("Condition", PIN_BOOL)], [("True", PIN_EXEC), ("False", PIN_EXEC)])
    draw_ue_node(draw, 1430, 180, 230, 110, "Set IsMoving = True", (40, 80, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1710, 180, 240, 110, "Play Motor Audio", (40, 100, 120, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2000, 180, 250, 150, "Timeline (LiftTravel)", (160, 120, 30, 255), [("Play / Reverse", PIN_EXEC)], [("Update", PIN_EXEC), ("Finished", PIN_EXEC), ("Alpha", PIN_FLOAT)])
    draw_ue_node(draw, 1860, 380, 230, 130, "Lerp Relative Z", (40, 120, 60, 255), [("BottomZ", PIN_FLOAT), ("TopZ", PIN_FLOAT), ("Alpha", PIN_FLOAT)], [("NewZ", PIN_FLOAT)])
    draw_ue_node(draw, 2140, 380, 300, 130, "Set Platform Location", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("NewZ", PIN_FLOAT)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1520, 530, 270, 120, "Toggle IsAtBottom State", (120, 40, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1840, 530, 260, 120, "Set IsMoving = False", (40, 80, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2150, 530, 280, 120, "Play Clamp Arrival SFX", (40, 100, 120, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])

    draw_wire(draw, (1120, 216), (1170, 216), PIN_EXEC)
    draw_wire(draw, (1370, 216), (1430, 216), PIN_EXEC)
    draw_wire(draw, (1660, 216), (1710, 216), PIN_EXEC)
    draw_wire(draw, (1950, 216), (2000, 216), PIN_EXEC)
    draw_wire(draw, (2250, 216), (2280, 320), PIN_EXEC)
    draw_wire(draw, (2280, 320), (2140, 416), PIN_EXEC)
    draw_wire(draw, (2250, 264), (1860, 464), PIN_FLOAT)
    draw_wire(draw, (2090, 416), (2140, 464), PIN_FLOAT)
    draw_wire(draw, (2250, 240), (2290, 360), PIN_EXEC)
    draw_wire(draw, (2290, 360), (1520, 566), PIN_EXEC)
    draw_wire(draw, (1790, 566), (1840, 566), PIN_EXEC)
    draw_wire(draw, (2100, 566), (2150, 566), PIN_EXEC)

    # 5. Inputs / Outputs
    draw_panel(draw, 830, 820, 800, 570, "5. INPUTS, OUTPUTS & INTERFACES")
    draw.text((860, 875), "LIFT CONTROL INTERFACE SPECIFICATION", fill=CYAN_ACCENT, font=font_body_bold)
    cy = 920
    for n_title, n_desc in [
        ("Input Function:", "ToggleLiftDirection() — Initiates travel to opposite floor."),
        ("Input Function:", "CallToFloor(int FloorIndex) — Sends lift to specified waypoint."),
        ("Output Event:", "OnLiftDeparted(int FromFloor) — Dispatched when movement starts."),
        ("Output Event:", "OnLiftArrived(int ToFloor) — Dispatched when platform locks into landing teeth."),
        ("Audio Profile:", "SFX_Lift_Start_Clank, SFX_Cable_Whine_Loop, SFX_Hydro_Clamp_Arrival."),
        ("Safety Interlock:", "Rejects activation commands while bIsMoving is True.")
    ]:
        draw.text((860, cy), n_title, fill=PURPLE_ACCENT, font=font_body_bold)
        draw.text((1020, cy), n_desc, fill=TEXT_WHITE, font=font_body)
        cy += 44

    # 6. Expected Result Visual
    draw_panel(draw, 1660, 820, 850, 570, "6. EXPECTED IN-GAME RESULT & VISUAL STATE")
    draw.rectangle([1700, 880, 2460, 1340], fill=(14, 18, 25, 255), outline=BORDER_CYAN, width=1)
    # Shaft guides
    draw.line([1820, 910, 1820, 1310], fill=(60, 75, 100, 255), width=8)
    draw.line([2340, 910, 2340, 1310], fill=(60, 75, 100, 255), width=8)
    # Top landing
    draw.rectangle([1820, 920, 2340, 950], fill=(30, 36, 48, 255), outline=CYAN_ACCENT, width=2)
    # Bottom landing
    draw.rectangle([1820, 1270, 2340, 1300], fill=(30, 36, 48, 255), outline=CYAN_ACCENT, width=2)
    # Moving platform in mid shaft
    draw.rectangle([1860, 1060, 2300, 1110], fill=(45, 55, 75, 255), outline=CYAN_ACCENT, width=3)
    # Platform safety railings
    draw.line([1880, 1060, 1880, 1010], fill=CYAN_ACCENT, width=4)
    draw.line([2280, 1060, 2280, 1010], fill=CYAN_ACCENT, width=4)
    draw.line([1880, 1010, 2280, 1010], fill=CYAN_ACCENT, width=4)
    draw.text((1960, 1125), "ELEVATION: TRAVELING (+Z)", fill=CYAN_ACCENT, font=font_body_bold)
    draw.text((1940, 1155), "VERTICAL DISPLACEMENT: 12.0m", fill=TEXT_MUTED, font=font_code)

    img.save(os.path.join(OUT_DIR, "BP_LiftPlatform_Reference.png"))
    print("Exported: BP_LiftPlatform_Reference.png")


# -------------------------------------------------------------
# 5. BP_SurveillanceCamera
# -------------------------------------------------------------
def make_bp_surveillance_camera():
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "BP_SurveillanceCamera", "Environmental Security Prop", "AActor")
    
    # 1. Purpose
    draw_panel(draw, 50, 120, 750, 240, "1. ACTOR PURPOSE & PERFORMANCE SPEC")
    cy = 175
    for lbl, val in [
        ("Summary:", "Wall/ceiling mounted cyberpunk surveillance camera with sweeping visual cone."),
        ("Level 1 Context:", "Monitors Sector 09 transit corridors and restricted observation bays."),
        ("Gameplay Role:", "Environmental atmosphere and visual stealth hazard; can be powered off/hacked."),
        ("Tick Policy:", "Optional Timeline or low-frequency Timer. Avoids per-frame expensive Tick."),
        ("Collision:", "Camera housing uses NoCollision or QueryOnly simple sphere for projectile hit."),
        ("Volumetric:", "Uses SpotLight with Volumetric Scattering Intensity for dramatic cyan light cone.")
    ]:
        draw.text((70, cy), lbl, fill=CYAN_ACCENT, font=font_body_bold)
        draw.text((220, cy), val, fill=TEXT_WHITE, font=font_body)
        cy += 27

    # 2. Components
    draw_panel(draw, 50, 380, 750, 300, "2. COMPONENT HIERARCHY")
    cy = 435
    for c_type, c_desc in [
        ("[Root]", "DefaultSceneRoot (USceneComponent) — Wall Mount Plate Anchor"),
        ("├── [Mesh]", "BaseMountMesh (UStaticMeshComponent) — Static Wall Bracket"),
        ("├── [Scene]", "SwivelYawRoot (USceneComponent) — Yaw Rotation Joint Component"),
        ("│   └── [Mesh]", "CameraLensMesh (UStaticMeshComponent: SM_SurveillanceCamera) — Lens Housing"),
        ("│   └── [Light]", "VisionConeLight (USpotLightComponent) — Outer Cone 45°, Volumetric Cyan Beam"),
        ("└── [Audio]", "ServoMotorAudio (UAudioComponent) — Subtle high-tech robotic servo whir")
    ]:
        draw.text((70, cy), c_type, fill=PURPLE_ACCENT, font=font_code)
        draw.text((200, cy), c_desc, fill=TEXT_WHITE, font=font_body)
        cy += 34

    # 3. Variables
    draw_panel(draw, 50, 700, 750, 400, "3. IMPORTANT VARIABLES & DEFAULTS")
    for h_txt, h_x in [("Variable Name", 70), ("Type", 320), ("Default Value", 470), ("Category / Description", 600)]:
        draw.text((h_x, 750), h_txt, fill=CYAN_ACCENT, font=font_body_bold)
    draw.line([70, 778, 770, 778], fill=BORDER_MUTED, width=1)
    cy = 790
    for v_name, v_type, v_def, v_desc in [
        ("IsActive", "Boolean", "True", "State / Camera powered state"),
        ("RotationSpeed", "Float", "25.0", "Config / Degrees per second sweep"),
        ("SweepAngleMax", "Float", "60.0", "Config / Maximum yaw displacement"),
        ("DetectionRadius", "Float", "800.0", "Config / Spotlight attenuation (cm)"),
        ("AlertColor", "LinearColor", "(1.0, 0.05, 0.05)", "Config / Color when alerted"),
        ("NormalColor", "LinearColor", "(0.0, 0.85, 1.0)", "Config / Idle sweep color")
    ]:
        draw.text((70, cy), v_name, fill=TEXT_WHITE, font=font_code)
        draw.text((320, cy), v_type, fill=ORANGE_ACCENT, font=font_code)
        draw.text((470, cy), v_def, fill=GREEN_ACCENT, font=font_code)
        draw.text((600, cy), v_desc, fill=TEXT_MUTED, font=font_body)
        cy += 32

    # 4. Logic Graph
    draw_panel(draw, 830, 120, 1680, 680, "4. BLUEPRINT EVENT FLOW & LOGIC GRAPH")
    draw_ue_node(draw, 870, 180, 240, 120, "Event BeginPlay", (120, 40, 140, 255), [], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1160, 180, 250, 150, "Timeline: SweepPingPong", (160, 120, 30, 255), [("Play", PIN_EXEC)], [("Update", PIN_EXEC), ("Alpha", PIN_FLOAT)])
    draw_ue_node(draw, 1460, 180, 240, 130, "Lerp (Rotator)", (40, 120, 60, 255), [("A (-Yaw)", PIN_VECTOR), ("B (+Yaw)", PIN_VECTOR), ("Alpha", PIN_FLOAT)], [("Rotator", PIN_VECTOR)])
    draw_ue_node(draw, 1750, 180, 290, 130, "Set Relative Rotation", (40, 80, 140, 255), [("Exec", PIN_EXEC), ("Target (Swivel)", PIN_OBJECT), ("NewRot", PIN_VECTOR)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2090, 180, 260, 120, "Play Subtle Servo SFX", (40, 100, 120, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1400, 420, 260, 120, "CustomEvent: DisableCamera", (180, 40, 40, 255), [], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1710, 420, 240, 120, "Stop Timeline", (160, 120, 30, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2000, 420, 270, 120, "Set Light Visibility (Off)", (0, 120, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])

    draw_wire(draw, (1110, 216), (1160, 216), PIN_EXEC)
    draw_wire(draw, (1410, 216), (1750, 216), PIN_EXEC)
    draw_wire(draw, (1410, 264), (1460, 264), PIN_FLOAT)
    draw_wire(draw, (1700, 264), (1750, 264), PIN_VECTOR)
    draw_wire(draw, (2040, 216), (2090, 216), PIN_EXEC)
    draw_wire(draw, (1660, 456), (1710, 456), PIN_EXEC)
    draw_wire(draw, (1950, 456), (2000, 456), PIN_EXEC)

    # 5. Inputs / Outputs
    draw_panel(draw, 830, 820, 800, 570, "5. INPUTS, OUTPUTS & INTERFACES")
    draw.text((860, 875), "SURVEILLANCE BEHAVIOR SPECIFICATION", fill=CYAN_ACCENT, font=font_body_bold)
    cy = 920
    for n_title, n_desc in [
        ("Input Function:", "DisableCamera() — Powers down camera swivel and douses light cone."),
        ("Input Function:", "TriggerAlert(bool bAlert) — Changes beam from soothing cyan to emergency red."),
        ("Sweep Mechanics:", "Smooth ping-pong Timeline between -60° and +60° yaw with 0.8s turnaround pause."),
        ("Performance:", "No Tick overhead; simple rotators and single optimized spot light."),
        ("Lighting Profile:", "SpotLight with InnerCone 25°, OuterCone 45°, 2500 Lumens.")
    ]:
        draw.text((860, cy), n_title, fill=PURPLE_ACCENT, font=font_body_bold)
        draw.text((1020, cy), n_desc, fill=TEXT_WHITE, font=font_body)
        cy += 44

    # 6. Expected Result Visual
    draw_panel(draw, 1660, 820, 850, 570, "6. EXPECTED IN-GAME RESULT & VISUAL STATE")
    draw.rectangle([1700, 880, 2460, 1340], fill=(14, 18, 25, 255), outline=BORDER_CYAN, width=1)
    # Camera Mount
    draw.rectangle([2040, 910, 2120, 950], fill=(45, 55, 75, 255), outline=CYAN_ACCENT, width=2)
    # Swivel ball
    draw.ellipse([2050, 940, 2110, 1000], fill=(30, 38, 52, 255), outline=CYAN_ACCENT, width=2)
    # Lens body angled
    draw.polygon([(2060, 990), (2100, 990), (2120, 1040), (2040, 1040)], fill=(60, 70, 90, 255), outline=CYAN_ACCENT)
    # Light beam cone
    draw.polygon([(2040, 1040), (2120, 1040), (2360, 1290), (1800, 1290)], fill=(0, 210, 255, 45), outline=(0, 210, 255, 120))
    draw.text((1950, 1305), "VOLUMETRIC SURVEILLANCE BEAM", fill=CYAN_ACCENT, font=font_body_bold)

    img.save(os.path.join(OUT_DIR, "BP_SurveillanceCamera_Reference.png"))
    print("Exported: BP_SurveillanceCamera_Reference.png")


# -------------------------------------------------------------
# 6. BP_InteractablePanel
# -------------------------------------------------------------
def make_bp_interactable_panel():
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "BP_InteractablePanel", "Modular Interactive Electronics", "AActor")
    
    # 1. Purpose
    draw_panel(draw, 50, 120, 750, 240, "1. ACTOR PURPOSE & PERFORMANCE SPEC")
    cy = 175
    for lbl, val in [
        ("Summary:", "Universal wall-mounted interactive cyberpunk breaker box and small panel."),
        ("Level 1 Context:", "Used for auxiliary power resets, vent override switches, and elevator calls."),
        ("Gameplay Role:", "Reusable interaction actor implementing BPI_Interactable interface."),
        ("Tick Policy:", "Tick Disabled. Fully event-driven."),
        ("Collision:", "Panel has BlockAll; Interaction Box has QueryOnly (Pawn overlap)."),
        ("Visual Response:", "Dynamic Material switches status light & emissive stripes upon activation.")
    ]:
        draw.text((70, cy), lbl, fill=CYAN_ACCENT, font=font_body_bold)
        draw.text((220, cy), val, fill=TEXT_WHITE, font=font_body)
        cy += 27

    # 2. Components
    draw_panel(draw, 50, 380, 750, 300, "2. COMPONENT HIERARCHY")
    cy = 435
    for c_type, c_desc in [
        ("[Root]", "DefaultSceneRoot (USceneComponent) — Wall Surface Anchor"),
        ("├── [Mesh]", "PanelMesh (UStaticMeshComponent: SM_Access_Panel) — Flush Wall Console"),
        ("├── [Light]", "StatusLight (UPointLightComponent) — Red (Standby) / Cyan (Active) Indicator"),
        ("├── [Collision]", "InteractionCollision (UBoxComponent) — Size: (80, 80, 120) cm"),
        ("└── [Audio]", "SwitchClickAudio (UAudioComponent) — Heavy mechanical toggle click sfx")
    ]:
        draw.text((70, cy), c_type, fill=PURPLE_ACCENT, font=font_code)
        draw.text((200, cy), c_desc, fill=TEXT_WHITE, font=font_body)
        cy += 34

    # 3. Variables
    draw_panel(draw, 50, 700, 750, 400, "3. IMPORTANT VARIABLES & DEFAULTS")
    for h_txt, h_x in [("Variable Name", 70), ("Type", 320), ("Default Value", 470), ("Category / Description", 600)]:
        draw.text((h_x, 750), h_txt, fill=CYAN_ACCENT, font=font_body_bold)
    draw.line([70, 778, 770, 778], fill=BORDER_MUTED, width=1)
    cy = 790
    for v_name, v_type, v_def, v_desc in [
        ("IsActivated", "Boolean", "False", "State / Activated flag"),
        ("InteractionEnabled", "Boolean", "True", "Config / Input enabled"),
        ("PanelEventTag", "FName", "'Panel_Aux_Power'", "Config / Gameplay dispatcher tag"),
        ("AllowToggle", "Boolean", "False", "Config / Can toggle back to false"),
        ("DynamicMaterial", "UMaterialInstanceDynamic*", "None", "Visuals / Dynamic emissive switcher")
    ]:
        draw.text((70, cy), v_name, fill=TEXT_WHITE, font=font_code)
        draw.text((320, cy), v_type, fill=ORANGE_ACCENT, font=font_code)
        draw.text((470, cy), v_def, fill=GREEN_ACCENT, font=font_code)
        draw.text((600, cy), v_desc, fill=TEXT_MUTED, font=font_body)
        cy += 32

    # 4. Logic Graph
    draw_panel(draw, 830, 120, 1680, 680, "4. BLUEPRINT EVENT FLOW & LOGIC GRAPH")
    draw_ue_node(draw, 870, 180, 240, 120, "BPI_Interact (Event)", (180, 40, 40, 255), [], [("Exec", PIN_EXEC), ("Caller", PIN_OBJECT)])
    draw_ue_node(draw, 1160, 180, 220, 120, "Branch (CanInteract)", (90, 90, 90, 255), [("Exec", PIN_EXEC), ("Condition", PIN_BOOL)], [("True", PIN_EXEC), ("False", PIN_EXEC)])
    draw_ue_node(draw, 1430, 180, 220, 110, "Play Switch SFX", (40, 100, 120, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1700, 180, 250, 110, "Set IsActivated = True", (40, 80, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2000, 180, 270, 130, "Set Emissive Vector Param", (0, 120, 140, 255), [("Exec", PIN_EXEC), ("Param", PIN_VECTOR)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1700, 380, 270, 120, "Set Light Color (Cyan)", (0, 120, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2020, 380, 290, 120, "Call OnPanelTriggered", (120, 40, 140, 255), [("Exec", PIN_EXEC), ("Tag", PIN_OBJECT)], [("Exec", PIN_EXEC)])

    draw_wire(draw, (1110, 216), (1160, 216), PIN_EXEC)
    draw_wire(draw, (1380, 216), (1430, 216), PIN_EXEC)
    draw_wire(draw, (1650, 216), (1700, 216), PIN_EXEC)
    draw_wire(draw, (1950, 216), (2000, 216), PIN_EXEC)
    draw_wire(draw, (2270, 216), (2300, 320), PIN_EXEC)
    draw_wire(draw, (2300, 320), (1700, 416), PIN_EXEC)
    draw_wire(draw, (1970, 416), (2020, 416), PIN_EXEC)

    # 5. Inputs / Outputs
    draw_panel(draw, 830, 820, 800, 570, "5. INPUTS, OUTPUTS & INTERFACES")
    draw.text((860, 875), "PANEL INTERFACE SPECIFICATION", fill=CYAN_ACCENT, font=font_body_bold)
    cy = 920
    for n_title, n_desc in [
        ("Event Dispatcher:", "OnPanelTriggered(FName Tag, AActor* PanelRef) — Broadcasts activation."),
        ("Dynamic Material:", "Updates 'EmissiveColor' vector and 'GlowIntensity' scalar parameter."),
        ("Sound Effect:", "SFX_Mechanical_Breaker_Snap with subtle electric spark."),
        ("Level Script Binding:", "Level designers can bind directly to OnPanelTriggered in Level Blueprint."),
        ("Status Light:", "Off: Deep Red (200, 10, 10) | On: High-intensity Cyan (0, 240, 255).")
    ]:
        draw.text((860, cy), n_title, fill=PURPLE_ACCENT, font=font_body_bold)
        draw.text((1020, cy), n_desc, fill=TEXT_WHITE, font=font_body)
        cy += 44

    # 6. Expected Result Visual
    draw_panel(draw, 1660, 820, 850, 570, "6. EXPECTED IN-GAME RESULT & VISUAL STATE")
    draw.rectangle([1700, 880, 2460, 1340], fill=(14, 18, 25, 255), outline=BORDER_CYAN, width=1)
    # Panel box
    draw.rectangle([1940, 930, 2220, 1290], fill=(26, 32, 44, 255), outline=CYAN_ACCENT, width=3)
    # Inner faceplate
    draw.rectangle([1970, 960, 2190, 1260], fill=(36, 44, 60, 255), outline=(55, 68, 90, 255), width=2)
    # Indicator diode
    draw.ellipse([2060, 990, 2100, 1030], fill=CYAN_ACCENT)
    # Toggle switch
    draw.rectangle([2055, 1100, 2105, 1180], fill=(15, 18, 24, 255), outline=(80, 95, 120, 255), width=2)
    draw.rectangle([2065, 1105, 2095, 1140], fill=CYAN_ACCENT)
    draw.text((1960, 1210), "CIRCUIT: ACTIVE / ENERGIZED", fill=CYAN_ACCENT, font=font_body_bold)

    img.save(os.path.join(OUT_DIR, "BP_InteractablePanel_Reference.png"))
    print("Exported: BP_InteractablePanel_Reference.png")


# -------------------------------------------------------------
# 7. BP_NeonLight
# -------------------------------------------------------------
def make_bp_neon_light():
    img = Image.new("RGBA", (W, H), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header(draw, "BP_NeonLight", "Atmospheric Cyberpunk Lighting", "AActor")
    
    # 1. Purpose
    draw_panel(draw, 50, 120, 750, 240, "1. ACTOR PURPOSE & PERFORMANCE SPEC")
    cy = 175
    for lbl, val in [
        ("Summary:", "Configurable neon strip lighting actor casting vibrant cyberpunk bounce light."),
        ("Level 1 Context:", "Used extensively along Sector 09 catwalks, doorways, and signage."),
        ("Color Variants:", "Supports Cyan (tech/clear), Purple (atmosphere/cyber), Red (danger/locked)."),
        ("Tick Policy:", "Tick Disabled. Dynamic parameters updated in Construction Script."),
        ("Performance:", "Uses Point/Rect light with controlled attenuation radius; no expensive shadow casting."),
        ("Flicker FX:", "Optional subtle high-frequency glitch flicker curve driven by lightweight timer.")
    ]:
        draw.text((70, cy), lbl, fill=CYAN_ACCENT, font=font_body_bold)
        draw.text((220, cy), val, fill=TEXT_WHITE, font=font_body)
        cy += 27

    # 2. Components
    draw_panel(draw, 50, 380, 750, 300, "2. COMPONENT HIERARCHY")
    cy = 435
    for c_type, c_desc in [
        ("[Root]", "DefaultSceneRoot (USceneComponent) — Mounting Anchor Point"),
        ("├── [Mesh]", "NeonHousingMesh (UStaticMeshComponent) — Black Metal Channel Bracket"),
        ("├── [Mesh]", "NeonTubeMesh (UStaticMeshComponent) — High-Translucency Glowing Tube"),
        ("├── [Light]", "GlowLight (UPointLightComponent / URectLightComponent) — Diffuse Color Wash"),
        ("└── [Audio]", "NeonHumAudio (UAudioComponent) — Subtle 50Hz electrical filament buzz")
    ]:
        draw.text((70, cy), c_type, fill=PURPLE_ACCENT, font=font_code)
        draw.text((200, cy), c_desc, fill=TEXT_WHITE, font=font_body)
        cy += 34

    # 3. Variables
    draw_panel(draw, 50, 700, 750, 400, "3. IMPORTANT VARIABLES & DEFAULTS")
    for h_txt, h_x in [("Variable Name", 70), ("Type", 320), ("Default Value", 470), ("Category / Description", 600)]:
        draw.text((h_x, 750), h_txt, fill=CYAN_ACCENT, font=font_body_bold)
    draw.line([70, 778, 770, 778], fill=BORDER_MUTED, width=1)
    cy = 790
    for v_name, v_type, v_def, v_desc in [
        ("NeonColour", "LinearColor", "(0.0, 0.9, 1.0)", "Config / Light tint color"),
        ("EmissiveIntensity", "Float", "15.0", "Config / Mesh glow intensity"),
        ("LightIntensity", "Float", "3500.0", "Config / Point light lumens"),
        ("AttenuationRadius", "Float", "600.0", "Config / Light falloff distance (cm)"),
        ("IsEnabled", "Boolean", "True", "Config / Master power switch"),
        ("FlickerGlitchRate", "Float", "0.0", "Config / 0 = steady, >0 = cyber glitch rate")
    ]:
        draw.text((70, cy), v_name, fill=TEXT_WHITE, font=font_code)
        draw.text((320, cy), v_type, fill=ORANGE_ACCENT, font=font_code)
        draw.text((470, cy), v_def, fill=GREEN_ACCENT, font=font_code)
        draw.text((600, cy), v_desc, fill=TEXT_MUTED, font=font_body)
        cy += 32

    # 4. Logic Graph
    draw_panel(draw, 830, 120, 1680, 680, "4. BLUEPRINT EVENT FLOW & LOGIC GRAPH")
    draw_ue_node(draw, 870, 180, 260, 120, "UserConstructionScript", (40, 120, 60, 255), [], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1180, 180, 290, 130, "Create Dynamic Material", (0, 120, 140, 255), [("Exec", PIN_EXEC), ("SourceMat", PIN_OBJECT)], [("Exec", PIN_EXEC), ("Return Value", PIN_OBJECT)])
    draw_ue_node(draw, 1520, 180, 310, 130, "Set Vector Parameter (Color)", (0, 120, 140, 255), [("Exec", PIN_EXEC), ("ColorVal", PIN_VECTOR)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1880, 180, 300, 130, "Set Scalar Param (Intensity)", (0, 120, 140, 255), [("Exec", PIN_EXEC), ("Intensity", PIN_FLOAT)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2230, 180, 240, 130, "Set Light Properties", (160, 120, 30, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 1420, 420, 260, 120, "CustomEvent: ToggleLight", (180, 40, 40, 255), [], [("Exec", PIN_EXEC), ("bEnable", PIN_BOOL)])
    draw_ue_node(draw, 1730, 420, 260, 120, "Set Light Visibility", (160, 120, 30, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])
    draw_ue_node(draw, 2040, 420, 280, 120, "Set Mesh Emissive Multiplier", (0, 120, 140, 255), [("Exec", PIN_EXEC)], [("Exec", PIN_EXEC)])

    draw_wire(draw, (1130, 216), (1180, 216), PIN_EXEC)
    draw_wire(draw, (1470, 216), (1520, 216), PIN_EXEC)
    draw_wire(draw, (1830, 216), (1880, 216), PIN_EXEC)
    draw_wire(draw, (2180, 216), (2230, 216), PIN_EXEC)
    draw_wire(draw, (1680, 456), (1730, 456), PIN_EXEC)
    draw_wire(draw, (1990, 456), (2040, 456), PIN_EXEC)

    # 5. Inputs / Outputs
    draw_panel(draw, 830, 820, 800, 570, "5. INPUTS, OUTPUTS & INTERFACES")
    draw.text((860, 875), "NEON LIGHTING SPECIFICATION", fill=CYAN_ACCENT, font=font_body_bold)
    cy = 920
    for n_title, n_desc in [
        ("Construction Hook:", "Instantly updates in Unreal Editor viewport as artist edits color/intensity."),
        ("Custom Function:", "SetNeonColor(FLinearColor NewColor) — Dynamically transitions tube hue."),
        ("Custom Function:", "TogglePower(bool bPowerOn) — Turns neon bar on/off with realistic buzz drop."),
        ("Lighting Optimization:", "Cast Shadows disabled by default on repeated corridor lights for maximum FPS."),
        ("Emissive Shading:", "Uses Unlit or Subsurface profile for soft fluorescent falloff.")
    ]:
        draw.text((860, cy), n_title, fill=PURPLE_ACCENT, font=font_body_bold)
        draw.text((1020, cy), n_desc, fill=TEXT_WHITE, font=font_body)
        cy += 44

    # 6. Expected Result Visual
    draw_panel(draw, 1660, 820, 850, 570, "6. EXPECTED IN-GAME RESULT & VISUAL STATE")
    draw.rectangle([1700, 880, 2460, 1340], fill=(14, 18, 25, 255), outline=BORDER_CYAN, width=1)
    # Wall surface
    draw.rectangle([1740, 930, 2420, 1290], fill=(20, 24, 32, 255))
    # Cyan neon bar
    draw.rectangle([1780, 980, 2380, 1020], fill=(0, 235, 255, 255), outline=(150, 245, 255, 255), width=2)
    # Glow wash cyan
    draw.ellipse([1750, 950, 2410, 1050], fill=(0, 210, 255, 45))
    draw.text((1800, 1040), "CYAN TECH VARIANT: (0.0, 0.9, 1.0) | 15.0 EMISSIVE", fill=CYAN_ACCENT, font=font_body_bold)
    # Purple neon bar
    draw.rectangle([1780, 1140, 2380, 1180], fill=(210, 50, 255, 255), outline=(240, 150, 255, 255), width=2)
    # Glow wash purple
    draw.ellipse([1750, 1110, 2410, 1210], fill=(195, 75, 255, 45))
    draw.text((1800, 1200), "PURPLE ATMOSPHERE VARIANT: (0.85, 0.05, 0.95) | 15.0 EMISSIVE", fill=PURPLE_ACCENT, font=font_body_bold)

    img.save(os.path.join(OUT_DIR, "BP_NeonLight_Reference.png"))
    print("Exported: BP_NeonLight_Reference.png")


if __name__ == "__main__":
    make_bp_industrial_door()
    make_bp_locked_gate()
    make_bp_control_terminal()
    make_bp_lift_platform()
    make_bp_surveillance_camera()
    make_bp_interactable_panel()
    make_bp_neon_light()
    print("ALL 7 Blueprint reference images generated successfully in Assets/Reference/Blueprints/.")
