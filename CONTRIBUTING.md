# Contributing

Thanks for helping improve BVH Motion Retargeter.

## Development setup

1. Use Python 3.11, matching Blender 4.2's Python baseline.
2. Install Ruff: `python -m pip install ruff`.
3. Run the local checks:

   ```bash
   python scripts/fetch_templates.py
   ruff check .
   python -m compileall -q bvh_to_mixamo scripts tests
   python -m unittest discover -s tests -v
   python scripts/build_release.py
   ```

4. Install the generated ZIP from `dist/` in Blender for an integration test.

## Project conventions

- Keep Blender runtime code in `bvh_to_mixamo/`.
- Keep tests, documentation, and release tooling outside the installable add-on.
- Store reusable bone mappings as JSON files in `bvh_to_mixamo/presets/`.
- Fetch bundled FBX resources with `scripts/fetch_templates.py`; do not commit generated copies.
- Do not commit generated ZIP packages; publish them as GitHub Release assets.
- Update `ADDON_VERSION` and `blender_manifest.toml` together for each release.
- Add user-visible changes to `CHANGELOG.md`.

## Pull requests

Keep changes focused, explain how they were tested, and include Blender version details for behavior changes.

---

# 贡献指南

- Blender 运行时代码放在 `bvh_to_mixamo/`。
- 测试、文档和发布脚本放在插件包之外。
- 生成的 ZIP 不提交到主分支，应作为 GitHub Release 附件发布。
- 发布时同步更新 `ADDON_VERSION` 与 `blender_manifest.toml`。
- 功能改动请注明测试所用的 Blender 版本。
