# Character templates

The bundled FBX files are release resources and are not committed to the source branch.

From the repository root, run:

```bash
python scripts/fetch_templates.py
```

The script downloads the pinned v3.2.0 release package, verifies its SHA-256 digest, extracts the six templates, and verifies every extracted file before use.
