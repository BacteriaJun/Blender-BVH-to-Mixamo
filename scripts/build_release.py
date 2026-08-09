#!/usr/bin/env python3
"""Build a deterministic Blender install ZIP from the tracked add-on source."""

from __future__ import annotations

import argparse
import ast
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = ROOT / "bvh_to_mixamo"
MANIFEST = PACKAGE / "blender_manifest.toml"
ADDON_INFO = PACKAGE / "addon_info.py"
EXCLUDED_PARTS = {"__pycache__", "docs", "tests"}
EXCLUDED_SUFFIXES = {".pyc", ".pyo"}
REQUIRED_TEMPLATES = {
    "mixamo_default_black.fbx",
    "mixamo_default_character.fbx",
    "mixamo_default_green.fbx",
    "mixamo_default_pink.fbx",
    "mixamo_default_purple.fbx",
    "mixamo_default_white.fbx",
}


def manifest_version() -> str:
    text = MANIFEST.read_text(encoding="utf-8")
    match = re.search(r'^version\s*=\s*"([^"]+)"\s*$', text, flags=re.MULTILINE)
    if not match:
        raise RuntimeError("version was not found in blender_manifest.toml")
    return match.group(1)


def addon_version() -> str:
    tree = ast.parse(ADDON_INFO.read_text(encoding="utf-8"), filename=str(ADDON_INFO))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "ADDON_VERSION" for target in node.targets
        ):
            value = ast.literal_eval(node.value)
            return ".".join(str(part) for part in value)
    raise RuntimeError("ADDON_VERSION was not found in addon_info.py")


def package_files() -> list[Path]:
    return [
        path
        for path in sorted(PACKAGE.rglob("*"))
        if path.is_file()
        and not EXCLUDED_PARTS.intersection(path.relative_to(PACKAGE).parts)
        and path.suffix not in EXCLUDED_SUFFIXES
    ]


def build(output: Path) -> Path:
    version = manifest_version()
    code_version = addon_version()
    if version != code_version:
        raise RuntimeError(f"Version mismatch: manifest={version}, addon_info={code_version}")

    missing_templates = sorted(
        name for name in REQUIRED_TEMPLATES if not (PACKAGE / "templates" / name).is_file()
    )
    if missing_templates:
        raise RuntimeError(
            "Missing bundled templates. Run `python scripts/fetch_templates.py` first: "
            + ", ".join(missing_templates)
        )

    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in package_files():
            relative = source.relative_to(ROOT).as_posix()
            info = zipfile.ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, source.read_bytes())
    return output


def main() -> None:
    version = manifest_version()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "dist" / f"bvh_motion_retargeter_v{version}_release.zip",
        help="Output ZIP path",
    )
    args = parser.parse_args()
    output = build(args.output.resolve())
    print(f"Built {output.relative_to(ROOT)} ({output.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
