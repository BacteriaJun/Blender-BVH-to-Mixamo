#!/usr/bin/env python3
"""Fetch and verify the FBX templates bundled with the v3.2.0 release."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "bvh_to_mixamo" / "templates"
RELEASE_URL = (
    "https://github.com/BacteriaJun/BVH-Motion-Retargeter/releases/download/"
    "V3.2.0/bvh_motion_retargeter_v3.2.0_release.zip"
)
ARCHIVE_SHA256 = "8c137abbef58f59f70c7b3c7900d368c68b252d1284512310c57f5d1e93aacbb"
TEMPLATE_SHA256 = {
    "mixamo_default_black.fbx": "dab537495fa0319d5726ccc8e7ea5b19202aee77cdf604b1d635e5d6404f8dc3",
    "mixamo_default_character.fbx": "f462c82fc2b114948170930d453696813fa9475d892b1fa75b773bec32f9656f",
    "mixamo_default_green.fbx": "24d848a9ae7e439a7bfff56bfe0c9e9a4f80816df804455381cb72183a48e6b4",
    "mixamo_default_pink.fbx": "f0f34dc825dfd8b6cd3549afc9c8e83e9c7148c36501cb57484141d0d7250ed7",
    "mixamo_default_purple.fbx": "7f8627706a1446eb16e9e08868be144d3f9a0dd484930908f4311f63f850a2aa",
    "mixamo_default_white.fbx": "ae11767e5b5940ae6e7a900667cc1148e44c7cfce3bccdcdf993a6a82efa9ad2",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path, expected: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise RuntimeError(f"Checksum mismatch for {path.name}: expected {expected}, got {actual}")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="bvh-retargeter-") as temporary_dir:
        archive_path = Path(temporary_dir) / "release.zip"
        print(f"Downloading {RELEASE_URL}")
        with urllib.request.urlopen(RELEASE_URL) as response, archive_path.open("wb") as output:
            shutil.copyfileobj(response, output)
        verify(archive_path, ARCHIVE_SHA256)

        with zipfile.ZipFile(archive_path) as archive:
            for filename, expected in TEMPLATE_SHA256.items():
                member = f"bvh_to_mixamo/templates/{filename}"
                target = OUTPUT_DIR / filename
                with archive.open(member) as source, target.open("wb") as output:
                    shutil.copyfileobj(source, output)
                verify(target, expected)
                print(f"Verified {target.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
