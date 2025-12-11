from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
DOCS_BASE = BASE / "docs" / "modules"

teams = ["teamA", "teamB", "teamC"]
weeks_per_module = {
    "module1": range(1, 5),
    "module2": range(5, 9),
    "module3": range(9, 13),
    "module4": range(13, 17),
}

template = """---
id: week{WEEK}
title: Week {WEEK:02d} — {TEAM}
sidebar_label: Week {WEEK:02d}
---

_No document uploaded yet._

[📤 Upload documentation for this week](/upload?team={TEAM_ID}&week=week{WEEK})
"""

for module, week_range in weeks_per_module.items():
    for team in teams:
        team_dir = DOCS_BASE / module / team
        team_dir.mkdir(parents=True, exist_ok=True)
        for w in week_range:
            md_path = team_dir / f"week{w}.md"
            if not md_path.exists():
                content = template.format(WEEK=w, TEAM=team.title(), TEAM_ID=team)
                md_path.write_text(content, encoding="utf-8")
                print("✅ Created:", md_path)
            else:
                print("⏩ Skipped (exists):", md_path)
