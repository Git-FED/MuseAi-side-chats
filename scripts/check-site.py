#!/usr/bin/env python3
"""Small smoke test for the no-build static site."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

for page in ROOT.rglob("*.html"):
    source = page.read_text(encoding="utf-8")
    for attribute in ("href", "src"):
        for value in re.findall(rf'{attribute}="([^"]+)"', source):
            if value.startswith(("http:", "https:", "#", "mailto:", "data:", "javascript:")):
                continue
            target = (page.parent / value).resolve()
            if not target.exists():
                errors.append(f"{page.relative_to(ROOT)} -> {value}")

required = [
    ROOT / "index.html",
    ROOT / "support.html",
    ROOT / "discord.html",
    ROOT / "private-communities.html",
    ROOT / "assets" / "favicon.svg",
    ROOT / "assets" / "demo" / "demo.gif",
]
for path in required:
    if not path.exists():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")

if errors:
    print("Static-site smoke test failed:")
    print("\n".join(f"- {error}" for error in errors))
    sys.exit(1)

print(f"Static-site smoke test passed: {len(list(ROOT.rglob('*.html')))} HTML pages checked.")
