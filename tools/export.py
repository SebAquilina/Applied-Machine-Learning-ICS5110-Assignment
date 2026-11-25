"""Build the ICS5110 VLE archive from the integrated checkout."""
from pathlib import Path
import argparse
import re
from zipfile import ZipFile, ZIP_DEFLATED

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument("group", help="two-digit group number")
args = parser.parse_args()
if not re.fullmatch(r"[0-9]{2}", args.group):
    parser.error("Supply a two-digit group number.")
group = "Group" + args.group
name = "ICS5110_2026_" + group
paths = [
    "submission_README.md", f"01_report/{group}_Report.pdf",
    f"02_genai_journal/{group}_GenAI_Journal.pdf", "03_code/requirements.txt",
    "03_code/00_data_preparation.ipynb", "03_code/09_comparison.ipynb",
    "04_data/README.md", "05_dashboard/dashboard_url.txt",
    "06_admin/contribution_statement.pdf", "06_admin/excerpt_consent.pdf",
]
errors = []
for prefix, surname in enumerate(("aquilina", "buttigieg", "muscat"), 1):
    matches = list((root / "03_code").glob(f"{prefix:02}_*_{surname}.ipynb"))
    if len(matches) != 1:
        errors.append(f"Expected one technique notebook for {surname}")
for file in sorted((root / "03_code").glob("*.ipynb")):
    if re.fullmatch(r"0[1-5]_.+_.+\.ipynb", file.name):
        paths.append(file.relative_to(root).as_posix())
for folder in ("03_code/dashboard", "04_data/processed"):
    for file in sorted((root / folder).rglob("*")):
        if file.is_file() and not any(p.startswith(".") or p in {"__pycache__", "node_modules"} for p in file.relative_to(root).parts):
            paths.append(file.relative_to(root).as_posix())
for path in paths:
    if not (root / path).is_file() or not (root / path).stat().st_size:
        errors.append("Missing or empty: " + path)
if errors:
    parser.exit(1, "\n".join(errors) + "\n")
out = root / "dist"
out.mkdir(exist_ok=True)
target = out / (name + ".zip")
with ZipFile(target.with_suffix(".tmp"), "w", ZIP_DEFLATED) as archive:
    archive.writestr(name + "/04_data/processed/", "")
    for path in paths:
        dest = "README.md" if path == "submission_README.md" else path
        archive.write(root / path, name + "/" + dest)
target.with_suffix(".tmp").replace(target)
print(target)
