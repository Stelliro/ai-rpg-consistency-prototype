from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "Mørkyn"


def fix_text(text: str) -> str:
    text = text.replace("M├╕rkyn", NAME)
    text = text.replace("MÃ¸rkyn", NAME)
    text = text.replace("M\u00c3\u00b8rkyn", NAME)
    # Mojibake variants sometimes seen when UTF-8 was decoded as cp1252
    text = text.replace("MÃ¸rkyn", NAME)
    text = re.sub(r"(?<![A-Za-z])Morkyn(?![A-Za-z])", NAME, text)
    text = text.replace("AI RPG Consistency Prototype", NAME)
    return text


def main() -> None:
    targets = [
        "README.md",
        "CHANGELOG.md",
        "CODEBASE_INDEX.md",
        "static/index.html",
        "app/main.py",
        "start_ai_rpg.ps1",
        "start_ai_rpg.bat",
        "static/app.js",
    ]
    for rel in targets:
        path = ROOT / rel
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = fix_text(original)
        if rel == "static/index.html":
            updated = updated.replace("<title>AI RPG</title>", f"<title>{NAME}</title>")
            updated = updated.replace("<h1>AI RPG</h1>", f"<h1>{NAME}</h1>")
        if rel == "app/main.py":
            updated = updated.replace('FastAPI(title="AI RPG Consistency Prototype")', f'FastAPI(title="{NAME}")')
            updated = updated.replace('"app": "AI RPG Consistency Prototype"', f'"app": "{NAME}"')
        if rel == "start_ai_rpg.ps1":
            updated = updated.replace("Starting AI RPG...", f"Starting {NAME}...")
        if rel == "start_ai_rpg.bat":
            updated = updated.replace("AI RPG launch mode:", "Morkyn launch mode:")
            updated = updated.replace("Morkyn launch mode:", "Morkyn launch mode:")
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            print(f"updated {rel}")
        else:
            print(f"unchanged {rel}")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "Mørkyn" in readme, "README missing proper Mørkyn"
    assert "M├" not in readme
    assert "## Media" not in readme
    assert "ui-play.png" in readme
    assert "| Logo | Key art |" not in readme
    print("README checks OK")


if __name__ == "__main__":
    main()
