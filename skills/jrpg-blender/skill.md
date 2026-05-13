---
name: jrpg-blender
description: Boys Quest JRPG — Blender asset pipeline for retargeting animations and baking textures for RPG Developer Bakin.
---

# Boys Quest JRPG — Blender Asset Pipeline

## Project
**Boys Quest** — Steam JRPG built in **RPG Developer Bakin** (pivoted from Godot 2026-04-29).
Design sensibility: Persona 5 — black/red/gold, aggressive geometry, fast motion.

## Paths
- **Project root:** `C:\Users\Pinko\claudesandbox\jrpg\`
- **Godot project (paused):** `jrpg\boys-quest\`
- **Tools / Blender scripts:** `jrpg\tools\`

## Blender Installs
- **System (5.1):** `C:\Program Files\Blender Foundation\Blender 5.1\blender.exe`
- **Portable (5.1.1):** `C:\Users\Pinko\AppData\Local\blender-portable\blender-5.1.1-windows-x64\blender.exe`

Run headlessly (no GUI):
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background --python script.py
```

**CRITICAL: Never recursively list the Blender install directory — it has 7,000+ files and will exhaust context before any work starts.**

## Key Asset Files
| File | Description |
|---|---|
| `new joker model\joker_persona_5_strikets.glb` | Active Joker model (P5 Strikers, suffixed bone names `bone_N_0M`) |
| `Models\source\H0000_Joker.fbx` | Original Persona FBX (253 bones, DDS textures) |
| `Models\source\*.dds` | 18 DDS texture files (numbered: 0,2,3,7,11,12,16,19,21,22,25,27,28,30,33,35,38,40,42,44) |
| `Models\textures\*.png` | 12 converted PNGs (partial — bake pass still needed) |
| `Models\Run.fbx` | Mixamo run animation source |
| `Models\joker_rigged.glb` | Output: Joker + retargeted run + idle anims |
| `assets\models\characters\joker_rigged.glb` | Copy used by Godot project |

## Retarget Pipeline (COMPLETE — v17 is latest)

Script: `tools\retarget_joker_v17.py`

What it does:
1. Imports `joker_persona_5_strikets.glb` (new model, `bone_N_0M` naming)
2. Imports `Models\Run.fbx` (Mixamo run animation)
3. Retargets via LOCAL rotation + rest-pose correction (eliminates bone-axis mismatch)
4. Generates 60-frame procedural idle sway
5. Exports → `Models\joker_rigged.glb`

Key explicit bone mappings:
```
bone_8_09   → mixamorig:LeftUpLeg
bone_9_010  → mixamorig:RightUpLeg
bone_10_011 → mixamorig:LeftLeg
bone_11_012 → mixamorig:RightLeg
bone_3_04   → mixamorig:Hips
bone_4_05   → mixamorig:Spine
```
Log: `tools\fresh_retarget_log.txt`

Run it:
```powershell
& "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe" --background --python "C:\Users\Pinko\claudesandbox\jrpg\tools\retarget_joker_v17.py"
```

## Texture Baking (TODO)

Goal: Convert all DDS textures → baked PNG maps for RPG Developer Bakin character import.

Partial work done: `Models\textures\` has 12 PNGs. Need a full bake pass for all 18+ DDS files.

Bake script pattern:
```python
import bpy

# Import the GLB
bpy.ops.import_scene.gltf(filepath=r"C:\...\joker_persona_5_strikets.glb")

# For each mesh object:
for obj in bpy.context.scene.objects:
    if obj.type != 'MESH': continue
    bpy.context.view_layer.objects.active = obj
    
    # Add Image Texture node to each material for bake target
    img = bpy.data.images.new(f"bake_{obj.name}", width=2048, height=2048)
    for mat in obj.data.materials:
        if not mat or not mat.use_nodes: continue
        nodes = mat.node_tree.nodes
        bake_node = nodes.new('ShaderNodeTexImage')
        bake_node.image = img
        nodes.active = bake_node
    
    # Bake diffuse color
    bpy.context.scene.cycles.bake_type = 'DIFFUSE'
    bpy.ops.object.bake(type='DIFFUSE', pass_filter={'COLOR'})
    img.save_render(filepath=rf"C:\...\Models\baked\{obj.name}.png")
```

Output to: `Models\baked\`

## Bakin Import Notes
- Bakin accepts GLB for character models
- Animations must be embedded in the GLB
- Export: `bpy.ops.export_scene.gltf(filepath=..., export_animations=True, export_skins=True)`
- Bakin animation names Bakin expects: `idle`, `walk`, `run`
- Characters go in Bakin's character database → assigned to map events

## Script Version History
`tools\retarget_joker_v1.py` through `v17.py` — each version addressed a specific retarget issue. v17 is definitive. Don't re-open old versions without reading what changed.
