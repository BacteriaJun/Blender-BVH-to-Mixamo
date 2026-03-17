# BVH to Mixamo Converter
A Blender addon to convert BVH motion capture data to Mixamo standard rig, with fixed frame rate synchronization.

## 简体中文 | English

## 功能介绍 (Feature Overview)
BVH to Mixamo Converter 是一款专为 Blender 设计的插件，能够一键将 BVH 动捕骨骼数据转换为 Mixamo 标准骨骼格式，完美解决动捕数据与 Mixamo 骨骼不兼容的问题。V2.3.1 版本重点修复了帧率同步问题，确保动画速度精准还原。

BVH to Mixamo Converter is a Blender addon designed to convert BVH motion capture data to Mixamo standard rig format with one click, solving the incompatibility issue between motion capture data and Mixamo rigs. Version 2.3.1 focuses on fixing frame rate synchronization issues to ensure accurate animation speed reproduction.

### 核心特性 (Key Features)
- ✨ **一键转换**: 简单直观的操作界面，一键完成BVH到Mixamo骨骼的转换
- 🎞️ **帧率同步**: 自动读取BVH文件原始帧率并同步到Blender场景，修复动画速度不一致问题
- 🦴 **完整骨骼映射**: 支持完整的人体骨骼映射（躯干、四肢、手部精细骨骼）
- 🔧 **骨骼层级修复**: 自动修复Mixamo标准骨骼层级结构，修正腿部分叉问题
- ✅ **动画验证**: 自动验证动画数据完整性，提供详细的转换日志
- 📐 **保持原始比例**: 保留原始动画和骨骼尺寸，不强制缩放
- 🔄 **撤销支持**: 完整的Undo/Redo支持，操作更安全

## 安装方法 (Installation)
1. 下载插件文件（`bvh_to_mixamo.py`）
2. 打开 Blender，进入 `编辑 > 偏好设置 > 插件 > 安装`
3. 选择下载的插件文件并安装
4. 启用插件 "BVH to Mixamo Converter"

## 使用指南 (Usage Guide)
1. 在 3D 视图中打开侧边栏（快捷键 `N`）
2. 找到 "Mixamo Tools" 标签页
3. 点击 "选择BVH文件" 按钮，选择你的BVH动捕文件
4. 建议勾选 "自动匹配BVH帧率" 选项
5. 点击 "生成Mixamo骨骼" 按钮，等待转换完成
6. 转换完成后，Mixamo标准骨骼会自动添加到场景中

### 注意事项 (Notes)
- 📝 文件路径请使用英文，避免中文、空格或特殊字符
- ⚙️ 推荐使用 Blender 4.0.0 及以上版本
- 🔍 转换过程会在控制台输出详细日志，可用于调试
- 🎨 转换后的骨骼可直接用于 Mixamo 动画重定向或 ARP/Rigify 重映射

## 技术细节 (Technical Details)
- **Blender 版本要求**: 4.0.0+
- **插件位置**: 3D View > Sidebar > Mixamo Tools
- **骨骼映射**: 完整支持Mixamo标准骨骼命名规范
- **帧率处理**: 自动解析BVH文件的Frame Time参数，计算精确帧率

## 更新日志 (Changelog)
Version History
中文
v1.0

实现了 BVH → Mixamo 骨骼层级转换 的基础功能，完成了项目最核心的初始流程搭建。

v2.0

修复并优化了 骨骼映射过程中的尺寸/比例问题，提升了转换后骨架结构与目标骨骼的匹配准确性。

v2.1

优化了插件的 UI 界面显示，使操作流程更加直观，使用体验更友好。

v2.2

修复了 胯部骨骼粘连问题，改进了 Hips 与腿部骨骼的层级和连接关系，提升了骨架结构的正确性。

v2.3

修复了 BVH 导入后的帧率同步问题。
实现了从原始 BVH 文件中自动读取帧率，并在转换后 自动切换 Blender 场景帧率 的功能，同时支持用户按需开启或关闭该选项。

v2.4

新增 绑定到现有 Mixamo 骨骼 功能。
支持将 BVH 动画直接转移到场景中已存在的 Mixamo 骨骼上，并通过约束与烘焙完成动画绑定，从而保留原有角色网格与绑定关系。

### 早期版本
- 🚀 初始版本发布，实现基础BVH到Mixamo骨骼转换
- 📌 完善骨骼映射表，支持完整手部骨骼
- 🎨 优化UI界面，添加使用说明

## 作者 (Author)
👨‍💻 Junius

## 许可证 (License)
本插件采用 MIT 许可证开源，你可以自由使用、修改和分发。

---

## 免责声明 (Disclaimer)
本插件仅用于学习和研究目的，使用时请确保你拥有BVH动捕数据的使用权限。作者不对因使用本插件造成的任何损失承担责任。

---

# BVH to Mixamo Converter
Blender插件 - 一键将BVH骨骼转化为Mixamo标准骨骼（修复帧率同步问题）

## English | 简体中文

## Feature Overview
BVH to Mixamo Converter is a Blender addon that converts BVH motion capture data to Mixamo standard rig format with one click, perfectly solving the incompatibility between motion capture data and Mixamo rigs. Version 2.3.1 focuses on fixing frame rate synchronization issues to ensure accurate animation speed reproduction.

### Key Features
- ✨ **One-click conversion**: Intuitive interface, complete BVH to Mixamo rig conversion with one click
- 🎞️ **Frame rate synchronization**: Automatically read the original frame rate of BVH files and sync to Blender scene, fixing animation speed inconsistency
- 🦴 **Complete bone mapping**: Support full human skeleton mapping (torso, limbs, detailed hand bones)
- 🔧 **Bone hierarchy repair**: Automatically fix Mixamo standard bone hierarchy and correct leg bifurcation issues
- ✅ **Animation validation**: Automatically verify animation data integrity and provide detailed conversion logs
- 📐 **Preserve original scale**: Keep original animation and bone dimensions without forced scaling
- 🔄 **Undo support**: Complete Undo/Redo support for safer operation

## Installation
1. Download the addon file (`bvh_to_mixamo.py`)
2. Open Blender, go to `Edit > Preferences > Add-ons > Install`
3. Select the downloaded addon file and install
4. Enable the addon "BVH to Mixamo Converter"

## Usage Guide
1. Open the sidebar in 3D View (shortcut `N`)
2. Find the "Mixamo Tools" tab
3. Click the "Select BVH File" button to choose your BVH motion capture file
4. It is recommended to check the "Auto match BVH frame rate" option
5. Click the "Generate Mixamo Rig" button and wait for conversion to complete
6. After conversion, the Mixamo standard rig will be automatically added to the scene

### Notes
- 📝 Use English for file paths, avoid Chinese, spaces or special characters
- ⚙️ Recommended to use Blender 4.0.0 or above
- 🔍 The conversion process outputs detailed logs in the console for debugging
- 🎨 Converted rigs can be directly used for Mixamo animation retargeting or ARP/Rigify remapping

## Technical Details
- **Blender Version Requirement**: 4.0.0+
- **Addon Location**: 3D View > Sidebar > Mixamo Tools
- **Bone Mapping**: Fully supports Mixamo standard bone naming conventions
- **Frame Rate Processing**: Automatically parses BVH file Frame Time parameter to calculate accurate frame rate

## Changelog
### v2.3.1
- 🐛 Fixed frame rate synchronization issue, resolved animation speed inconsistency
- 🎯 Optimized BVH frame rate reading logic for improved accuracy
- 🔧 Improved bone hierarchy repair algorithm, optimized leg bifurcation
- ✅ Added animation data validation feature for enhanced stability

### Earlier Versions
- 🚀 Initial release, implemented basic BVH to Mixamo rig conversion
- 📌 Improved bone mapping table to support complete hand bones
- 🎨 Optimized UI interface and added usage instructions

## Author
👨‍💻 Junius

## License
This addon is open source under the MIT License, you can use, modify and distribute it freely.

---

## Disclaimer
This addon is for learning and research purposes only. When using, please ensure you have the right to use the BVH motion capture data. The author is not responsible for any losses caused by the use of this addon.
