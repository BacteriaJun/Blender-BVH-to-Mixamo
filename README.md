# BVH to Mixamo Converter v3.1

A Blender add-on for converting BVH motion capture data into a Mixamo-compatible rig, with support for binding BVH animation directly to an existing Mixamo armature or to an imported Mixamo FBX character template.

一个用于 Blender 的 BVH 动捕转换与绑定插件。它可以将 BVH 动捕数据转换为 Mixamo 标准骨骼，也可以将 BVH 动画直接绑定到场景中的 Mixamo 骨架，或一键绑定到内置/自定义 Mixamo 人物 FBX 模板。

---

## Overview | 项目简介

**BVH to Mixamo Converter** is designed for practical animation workflows where BVH motion capture files need to be reused on Mixamo-style characters. It handles skeleton renaming, animation F-Curve remapping, hierarchy reconstruction, framerate synchronization, constraint-based retargeting, NLA baking, JSON-based bone mapping, and FBX character template binding.

本插件面向真实动捕工作流，重点解决 BVH 动捕文件与 Mixamo 人物骨骼不兼容的问题。v3.1 在原有 BVH → Mixamo 转换、绑定已有骨骼的基础上，新增了 **JSON 骨骼映射系统** 与 **人物 FBX 模板绑定模式**，可以更方便地适配不同来源的 BVH 文件，并将动画直接生成到人物模型上。

---

## Key Features | 核心特性

- **BVH → Mixamo skeleton conversion**  
  将 BVH 骨骼转换为 Mixamo 标准命名骨骼。

- **Bind to selected Mixamo armature**  
  将 BVH 动画绑定到场景中已有的 Mixamo 骨架，不破坏原模型蒙皮。

- **Bind to Mixamo FBX character template**  
  直接导入内置或自定义 Mixamo 人物 `.fbx`，并将 BVH 动画绑定到该人物上，在场景中生成带动画的人物角色。

- **JSON-based bone mapping**  
  使用内置 `default_mixamo_mapping.json`，也支持用户选择自定义 JSON 映射表。

- **Real custom mapping preset**  
  `custom_mapping_example.json` is not a placeholder. It is a usable Mixamo-prefixed BVH mapping preset for BVH files whose source bones are already named like `mixamorig:Hips`, `mixamorig:LeftArm`, etc.  
  `custom_mapping_example.json` 不是空案例，而是一份真实可用的 Mixamo 前缀骨骼映射表。

- **Automatic BVH framerate detection**  
  自动解析 BVH 文件中的 `Frame Time` 并同步 Blender 场景 FPS。

- **F-Curve animation path remapping**  
  骨骼重命名时同步修复动画数据路径，避免动画丢失。

- **Mixamo-style hierarchy reconstruction**  
  自动按 Mixamo 标准重建骨骼父子关系。

- **Constraint-driven animation transfer + NLA baking**  
  使用 Copy Location / Copy Rotation 约束转移动画，并通过 NLA Bake 烘焙为关键帧。

- **Mapping diagnostics**  
  导入 BVH 后输出映射诊断信息，包括源骨骼数量、映射数量、成功匹配数量、缺失骨骼和未配置骨骼。

- **Template registry for future expansion**  
  v3.1 预留了人物模板注册表结构，未来会继续添加更多一键绑定模板。

---

## Requirements | 环境要求

- Blender 4.5+
- BVH motion capture file
- Mixamo-style armature or Mixamo FBX character template
- For template binding mode: a Mixamo-compatible `.fbx` character file

---

## Installation | 安装方法

1. Download the add-on zip package.
2. Open Blender.
3. Go to **Edit → Preferences → Add-ons → Install...**.
4. Select the zip file, for example:

   ```text
   bvh_to_mixamo_3.1_template_binding.zip
   ```

5. Enable **BVH to Mixamo Converter**.
6. Open the 3D View sidebar with `N`.
7. Find the **Mixamo Tools** panel.

---

## Package Structure | 插件结构

```text
bvh_to_mixamo/
  __init__.py
  presets/
    default_mixamo_mapping.json
    custom_mapping_example.json
  templates/
    mixamo_default_character.fbx
```

### File descriptions | 文件说明

| File | Description |
|---|---|
| `__init__.py` | Main Blender add-on source code |
| `presets/default_mixamo_mapping.json` | Built-in default BVH → Mixamo mapping |
| `presets/custom_mapping_example.json` | Real Mixamo-prefixed BVH mapping preset |
| `templates/mixamo_default_character.fbx` | Built-in Mixamo character template for one-click binding |

---

## Workflow | 使用流程

### Mode 1: Create New Mixamo Armature | 创建新 Mixamo 骨骼

Use this mode when you only want to convert a BVH file into a Mixamo-style animated armature.

适合只想把 BVH 转换成 Mixamo 标准骨骼动画的情况。

1. Select a BVH file.
2. Choose the bone mapping source:
   - Built-in default JSON
   - Custom JSON
3. Enable FPS matching if needed.
4. Select **Create New Mixamo Armature**.
5. Click **Convert**.
6. The add-on imports BVH, remaps bones, repairs animation paths, and generates a Mixamo-style animated armature.

---

### Mode 2: Bind to Selected Mixamo Armature | 绑定到已选 Mixamo 骨骼

Use this mode when a Mixamo character already exists in the scene.

适合场景里已经有 Mixamo 人物模型和骨架的情况。

1. Select the target Mixamo armature in the Blender scene.
2. Select the BVH file.
3. Choose the mapping source.
4. Select **Bind to Selected Mixamo Armature**.
5. Click **Bind**.
6. The add-on imports the BVH, converts the temporary BVH armature, transfers the animation to the selected Mixamo armature, bakes the animation, and removes the temporary BVH armature.

---

### Mode 3: Bind to FBX Character Template | 绑定到人物 FBX 模板

Use this mode when you want the add-on to import a Mixamo FBX character automatically and generate the animated character directly in the scene.

适合希望“一键导入人物模型并生成绑定动画”的情况。

1. Select the BVH file.
2. Choose the mapping source.
3. Select **Bind to FBX Character Template**.
4. Choose a template source:
   - Built-in Mixamo default character
   - Custom Mixamo FBX file
5. Click **Bind to FBX Character Template**.
6. The add-on imports the character FBX, finds the armature, clears template animation if needed, imports BVH, converts the BVH skeleton, transfers animation to the FBX character armature, bakes the result, and leaves the animated character in the scene.

---

## JSON Bone Mapping | JSON 骨骼映射系统

v3.1 moves bone mapping out of hard-coded Python dictionaries and into external JSON configuration files. This makes it easier to adapt the add-on to BVH files exported from different motion capture tools.

v3.1 将骨骼映射从代码常量升级为 JSON 配置文件，便于适配不同动捕软件导出的 BVH 命名格式。

### Default JSON format | 默认 JSON 格式

```json
{
  "name": "Default BVH to Mixamo Mapping",
  "description": "Default source BVH bone names mapped to Mixamo bone names.",
  "version": "1.0",
  "target": "mixamo",
  "mapping": {
    "Hips": "mixamorig:Hips",
    "Spine": "mixamorig:Spine",
    "Spine1": "mixamorig:Spine1",
    "Spine2": "mixamorig:Spine2",
    "Neck": "mixamorig:Neck",
    "Head": "mixamorig:Head",
    "LeftArm": "mixamorig:LeftArm",
    "LeftForeArm": "mixamorig:LeftForeArm",
    "LeftHand": "mixamorig:LeftHand",
    "RightArm": "mixamorig:RightArm",
    "RightForeArm": "mixamorig:RightForeArm",
    "RightHand": "mixamorig:RightHand",
    "LeftUpLeg": "mixamorig:LeftUpLeg",
    "LeftLeg": "mixamorig:LeftLeg",
    "LeftFoot": "mixamorig:LeftFoot",
    "RightUpLeg": "mixamorig:RightUpLeg",
    "RightLeg": "mixamorig:RightLeg",
    "RightFoot": "mixamorig:RightFoot"
  }
}
```

### Custom mapping example | 自定义映射示例

If your BVH source bones use Unreal-like names, you can create a JSON file like this:

```json
{
  "name": "Unreal Style BVH to Mixamo Mapping",
  "description": "Example mapping for BVH files using Unreal-style bone names.",
  "version": "1.0",
  "target": "mixamo",
  "mapping": {
    "pelvis": "mixamorig:Hips",
    "spine_01": "mixamorig:Spine",
    "spine_02": "mixamorig:Spine1",
    "spine_03": "mixamorig:Spine2",
    "neck_01": "mixamorig:Neck",
    "head": "mixamorig:Head",
    "upperarm_l": "mixamorig:LeftArm",
    "lowerarm_l": "mixamorig:LeftForeArm",
    "hand_l": "mixamorig:LeftHand",
    "upperarm_r": "mixamorig:RightArm",
    "lowerarm_r": "mixamorig:RightForeArm",
    "hand_r": "mixamorig:RightHand",
    "thigh_l": "mixamorig:LeftUpLeg",
    "calf_l": "mixamorig:LeftLeg",
    "foot_l": "mixamorig:LeftFoot",
    "thigh_r": "mixamorig:RightUpLeg",
    "calf_r": "mixamorig:RightLeg",
    "foot_r": "mixamorig:RightFoot"
  }
}
```

### Notes | 注意事项

- Source bone names must match the BVH file exactly.
- Target bone names should remain Mixamo-style names, such as `mixamorig:Hips`.
- If no bones are matched, conversion is cancelled to prevent invalid processing.
- Different BVH exporters may use different naming conventions, so a custom JSON may be required.

---

## FBX Character Template Binding | 人物 FBX 模板绑定

v3.1 introduces a template-based binding pipeline.

v3.1 新增人物模板绑定流程。

### Built-in template | 内置模板

The add-on includes:

```text
templates/mixamo_default_character.fbx
```

When using the built-in template mode, the add-on imports this FBX automatically and transfers the BVH animation to its armature.

### Custom FBX template | 自定义人物模板

You can also select your own Mixamo-compatible `.fbx` character.

Recommended requirements:

- The FBX should contain one humanoid armature.
- The armature should use Mixamo-compatible bone names.
- The mesh should already be skinned to the armature.
- Avoid using a non-humanoid or heavily customized rig unless you also provide a compatible mapping and retargeting setup.

---

## Future Template Expansion | 未来模板扩展

v3.1 keeps a template registry in the source code. Future one-click binding templates can be added by:

1. Placing a new `.fbx` file into the `templates/` directory.
2. Registering it in `TEMPLATE_REGISTRY`.
3. Adding it to the template selection UI.

This structure allows the add-on to evolve from a single-template tool into a multi-character binding workflow.

---

## Technical Details | 技术实现细节

### 1. BVH import and framerate parsing

The add-on reads the BVH `Frame Time` value, computes FPS, and optionally synchronizes the Blender scene framerate.

### 2. JSON mapping loading

The add-on loads the active mapping table from either:

- `presets/default_mixamo_mapping.json`
- a user-selected custom JSON file

If the built-in JSON cannot be loaded, the add-on falls back to the internal default mapping table.

### 3. Mapping diagnostics

Before conversion, the add-on compares source BVH bones against the active mapping table and prints diagnostic information.

### 4. F-Curve path remapping

When source bones are renamed, the add-on updates animation F-Curve `data_path` values so the existing BVH animation remains connected after renaming.

### 5. Hierarchy reconstruction

The converted armature is rebuilt according to a Mixamo-style hierarchy while preserving bone transforms as much as possible.

### 6. Animation transfer

For binding modes, animation is transferred from the processed BVH armature to the target Mixamo armature using Copy Location and Copy Rotation constraints.

### 7. NLA baking

The constraint-driven animation is baked into real keyframes using Blender's NLA bake operation.

### 8. Temporary armature cleanup

In binding modes, the temporary BVH armature is removed after animation transfer, leaving the target animated character in the scene.

---

## Version History | 版本历史

### v1.0

- Initial BVH to Mixamo skeleton hierarchy conversion.
- 初步实现 BVH → Mixamo 骨骼层级转换。

### v2.0

- Fixed scale and size issues in bone mapping.
- 修复骨骼比例与大小问题。

### v2.1

- Improved UI layout and usability.
- 优化插件 UI。

### v2.2

- Fixed hip joint connection issues.
- 修复胯部骨骼粘连问题。

### v2.3

- Added automatic BVH framerate detection and optional scene FPS synchronization.
- 新增 BVH 帧率自动识别与场景同步。

### v2.4

- Added binding to existing Mixamo rigs.
- Added constraint-based animation transfer and NLA baking.
- 新增绑定到已有 Mixamo 骨骼功能，包括动画迁移与烘焙。

### v3.0

- Added built-in JSON bone mapping.
- Added custom JSON mapping support.
- Added mapping diagnostics.
- 新增内置 JSON 骨骼映射、自定义 JSON 映射与映射诊断。

### v3.1

- Added built-in Mixamo FBX character template binding.
- Added custom FBX template binding support.
- Added template registry structure for future one-click binding expansion.
- Improved compatibility for production-style BVH → animated FBX character workflows.
- 新增内置 Mixamo 人物 FBX 模板绑定、自定义人物模板绑定，并保留扩展多模板一键绑定。

---

## Known Limitations | 已知限制

- This is a lightweight retargeting workflow, not a full professional retargeting solver.
- BVH files with very different rest poses, bone rolls, or coordinate systems may require manual adjustment.
- Foot locking, root motion control, loop correction, and IK-based cleanup are not yet included.
- Custom FBX templates should use Mixamo-compatible humanoid armatures.
- Some complex rigs may require additional retargeting calibration.

---

## Troubleshooting | 常见问题

### The conversion reports zero matched bones.

Your BVH bone names do not match the selected mapping table. Use a custom JSON mapping file that matches your BVH source bone names.

### The character imports but does not move correctly.

Check whether the target FBX armature uses Mixamo-compatible bone names. Also check whether the BVH source has a different rest pose or axis orientation.

### The animation speed is wrong.

Enable FPS matching so the add-on reads the BVH `Frame Time` and synchronizes the Blender scene framerate.

### The mesh breaks after binding.

Use template binding or selected-rig binding only with a properly skinned Mixamo-compatible FBX character.

### Some fingers or toes do not animate.

The source BVH may not contain finger or toe bones, or the active JSON mapping may not include them.

---

## Author | 作者

Junius Tang / BacteriaJun

GitHub: `BacteriaJun/Blender-BVH-to-Mixamo`

---

## License | 许可证

MIT License
