# upload_service/upload_api.py
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import shutil, uuid, subprocess, re
from typing import Optional

BASE = Path(__file__).resolve().parent.parent
DOCS_BASE = BASE / "docs" / "modules"   # docs/modules/moduleX/teamY/weekN.md
TOOLS = BASE / "tools"
TMP = BASE / "tmp_uploads"
TRASH = BASE / "deleted_docs"
BACKUP = BASE / "backups"

TMP.mkdir(parents=True, exist_ok=True)
TRASH.mkdir(parents=True, exist_ok=True)
BACKUP.mkdir(parents=True, exist_ok=True)

ALLOWED = {".docx", ".pdf"}
VALID_MODULES = {"module1", "module2", "module3", "module4"}

app = FastAPI(title="Docs Upload API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def slug(s: str) -> str:
    return re.sub(r"[^a-z0-9\-]", "-", s.lower())


def module_for_week(week_num: int) -> str:
    if 1 <= week_num <= 4:
        return "module1"
    if 5 <= week_num <= 8:
        return "module2"
    if 9 <= week_num <= 12:
        return "module3"
    if 13 <= week_num <= 16:
        return "module4"
    raise HTTPException(400, "week must be 1..16")


def run_converter(in_path: Path, out_path: Path):
    """DOCX/PDF -> markdown (no front-matter)."""
    if in_path.suffix.lower() == ".docx":
        subprocess.run(
            ["python", str(TOOLS / "convert_docx_to_md.py"), str(in_path), str(out_path)],
            check=True,
        )
    elif in_path.suffix.lower() == ".pdf":
        subprocess.run(
            ["python", str(TOOLS / "convert_pdf_to_md.py"), str(in_path), str(out_path)],
            check=True,
        )
    else:
        raise HTTPException(400, "Unsupported file type (only .docx/.pdf)")


def run_sanitizer(md_path: Path, title_prefix: str):
    """Auto-wrap code into ```python fences (snippet style)."""
    sanitizer = TOOLS / "sanitize_and_wrap.py"
    if not sanitizer.exists():
        print("Sanitizer missing:", sanitizer)
        return
    subprocess.run(
        ["python", str(sanitizer), str(md_path), title_prefix],
        check=True,
    )


@app.get("/form", response_class=HTMLResponse)
def html_form():
    return """
    <html><body>
    <h3>Upload doc</h3>
    <form action="/upload/" enctype="multipart/form-data" method="post">
      <label>team: <input name="team" value="teamA"/></label><br/>
      <label>week: <input name="week" value="week1"/></label><br/>
      <input name="file" type="file" />
      <button type="submit">Upload</button>
    </form>
    </body></html>
    """


@app.post("/upload/")
async def upload(
    team: str = Form(...),
    week: str = Form(...),
    file: UploadFile = File(...),
):
    """
    Upload a .docx or .pdf, convert to markdown for module/team/week,
    wrap code as snippets, add front-matter, and return saved path.

    week can be "week1", "week-01", "1", etc.
    """
    team_slug = slug(team)
    week_clean = week.lower().replace("week", "").replace("-", "").strip()
    if not week_clean.isdigit():
        raise HTTPException(400, "week must be like 'week5', '5', or 'week-05'")
    w = int(week_clean)
    module = module_for_week(w)
    week_id = f"week{w}"

    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED:
        raise HTTPException(400, "Only .docx or .pdf allowed")

    dest_dir = DOCS_BASE / module / team_slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    out_md = dest_dir / f"{week_id}.md"

    # backup existing md (simple .bak copy) before overwrite
    if out_md.exists():
        bak_name = f"{week_id}__{uuid.uuid4().hex}.md.bak"
        bak_path = BACKUP / bak_name
        shutil.copy2(str(out_md), str(bak_path))
        print("Backed up existing md ->", bak_path)

    # save tmp upload
    tmp_name = TMP / f"{uuid.uuid4().hex}{ext}"
    with tmp_name.open("wb") as f_tmp:
        shutil.copyfileobj(file.file, f_tmp)

    # call converter -> markdown
    try:
        run_converter(tmp_name, out_md)
    except subprocess.CalledProcessError as e:
        try:
            tmp_name.unlink()
        except:
            pass
        raise HTTPException(500, f"Conversion failed: {e}")

    # ✅ MDX-safe pass on the generated markdown
    try:
        subprocess.run(
            ["python", str(TOOLS / "mdx_safe.py"), str(out_md)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print("mdx_safe failed (keeping raw markdown anyway):", e)

    # remove tmp
    try:
        tmp_name.unlink()
    except Exception:
        pass
    # auto-snippet (wrap code) on raw markdown (no front-matter yet)
    try:
        title_prefix = f"{team_slug} {week_id}"
        run_sanitizer(out_md, title_prefix)
    except subprocess.CalledProcessError as e:
        print("Sanitizer failed:", e)

    # delete tmp
    try:
        tmp_name.unlink()
    except Exception:
        pass

    # now add front-matter if missing
    text = out_md.read_text(encoding="utf-8") if out_md.exists() else ""
    if not text.lstrip().startswith("---"):
        nice_week = f"Week {w:02d}"
        nice_team = team_slug.replace("-", " ").title()
        fm = f"""---
id: {week_id}
title: {nice_week} — {nice_team}
sidebar_label: {nice_week}
---

"""
        out_md.write_text(fm + text, encoding="utf-8")

    rel = str(out_md.relative_to(BASE))
    print("Saved converted markdown:", rel)
    return JSONResponse({"ok": True, "saved": rel})


@app.post("/delete/")
async def delete_doc(
    module: str = Form(...),
    team: str = Form(...),
    week: str = Form(...),
):
    """
    Move existing markdown to deleted_docs/ and create a stub "No document" md.

    module: module1..module4
    team:   teamA/teamB/teamC (any string, will be slugged)
    week:   'week4' or '4' etc. (we map to weekN filename)
    """
    mod = module.lower()
    if mod not in VALID_MODULES:
        raise HTTPException(400, f"module must be one of {sorted(VALID_MODULES)}")

    team_slug = slug(team)
    week_clean = week.lower().replace("week", "").replace("-", "").strip()
    if not week_clean.isdigit():
        raise HTTPException(400, "week must be like 'week5', '5', or 'week-05'")
    w = int(week_clean)
    week_id = f"week{w}"

    md_path = DOCS_BASE / mod / team_slug / f"{week_id}.md"
    if not md_path.exists():
        raise HTTPException(404, f"No markdown found to delete at {md_path}")

    trash_name = f"{mod}_{team_slug}_{week_id}_{uuid.uuid4().hex}.md"
    trash_path = TRASH / trash_name
    shutil.move(str(md_path), str(trash_path))
    print(f"Moved {md_path} -> {trash_path}")

    nice_week = week_id.replace("-", " ").title()
    nice_team = team_slug.replace("-", " ").title()
    stub = f"""---
id: {week_id}
title: {nice_week} — {nice_team}
sidebar_label: {nice_week}
---

_No document uploaded yet. Previous upload was deleted._

[Upload documentation for this week](/upload?module={mod}&team={team_slug}&week={week_id})
"""
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text(stub, encoding="utf-8")
    print("Wrote stub at", md_path)

    return JSONResponse({"ok": True, "moved_to": str(trash_path.relative_to(BASE))})