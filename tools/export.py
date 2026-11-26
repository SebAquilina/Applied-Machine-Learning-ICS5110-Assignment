"""Check the integrated checkout against the ICS5110 submission rules, then build the VLE archive."""
from pathlib import Path
import argparse
import json
import re
import sys
from zipfile import ZipFile, ZIP_DEFLATED

# One entry per member, in notebook order: 01_<technique>_<surname>.ipynb, 02_..., and so on.
MEMBERS = ("aquilina", "buttigieg", "muscat")
PAGE_LIMITS = {"Report": 20, "GenAI_Journal": 10}
MAX_FILE_BYTES = 50 * 1024 * 1024
RAW_WVS_NAME = re.compile(r"WVS_Cross-National_Wave_7", re.I)
ABSOLUTE_PATH = re.compile(r"""["'](?:/(?:Users|home|content|mnt|root|tmp)/|[A-Za-z]:[\\/]|~/)""")
SKIPPED = {"__pycache__", "node_modules"}

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("group", help="two-digit group number")
args = parser.parse_args()
if not re.fullmatch(r"[0-9]{2}", args.group):
    parser.error("Supply a two-digit group number.")
group = "Group" + args.group
name = "ICS5110_2026_" + group
errors, warnings = [], []


def hidden(path):
    return any(part.startswith(".") or part in SKIPPED for part in path.relative_to(root).parts)


def read(path):
    return (root / path).read_text(encoding="utf-8", errors="replace") if (root / path).is_file() else ""


def check_notebook(path):
    """Saved outputs from one clean top-to-bottom run, and no machine-specific paths."""
    try:
        cells = json.loads(read(path)).get("cells", [])
    except json.JSONDecodeError:
        return errors.append(f"Not a valid notebook: {path}")
    code = [cell for cell in cells if cell.get("cell_type") == "code" and "".join(cell.get("source", [])).strip()]
    if not code:
        return errors.append(f"No code cells: {path}")
    counts = [cell.get("execution_count") for cell in code]
    if counts != list(range(1, len(code) + 1)):
        errors.append(f"Not a clean top-to-bottom run (restart, run all, save): {path}")
    if any(out.get("output_type") == "error" for cell in code for out in cell.get("outputs", [])):
        errors.append(f"Saved error output: {path}")
    if not any(cell.get("outputs") for cell in code):
        errors.append(f"No saved outputs: {path}")
    if any(ABSOLUTE_PATH.search("".join(cell.get("source", []))) for cell in code):
        errors.append(f"Absolute path in code (use relative paths only): {path}")


def check_pdf(path, limit=None):
    data = (root / path).read_bytes() if (root / path).is_file() else b""
    if not data.startswith(b"%PDF"):
        return errors.append(f"Not a PDF: {path}") if data else None
    if limit is None:
        return
    try:
        from pypdf import PdfReader
    except ImportError:
        return warnings.append(f"Page limit of {limit} not checked for {path} (pip install pypdf)")
    pages = len(PdfReader(root / path).pages)
    if pages > limit:
        errors.append(f"{pages} pages, limit is {limit} (extra pages are not read): {path}")


paths = [
    "submission_README.md", f"01_report/{group}_Report.pdf",
    f"02_genai_journal/{group}_GenAI_Journal.pdf", "03_code/requirements.txt",
    "03_code/00_data_preparation.ipynb", "03_code/09_comparison.ipynb",
    "04_data/README.md", "05_dashboard/dashboard_url.txt",
    "06_admin/contribution_statement.pdf", "06_admin/excerpt_consent.pdf",
]
for prefix, surname in enumerate(MEMBERS, 1):
    matches = sorted((root / "03_code").glob(f"{prefix:02}_*_{surname}.ipynb"))
    if len(matches) != 1:
        errors.append(f"Expected one technique notebook for {surname}, found {len(matches)}")
    paths += [match.relative_to(root).as_posix() for match in matches]
for folder in ("03_code/dashboard", "04_data/processed"):
    paths += [f.relative_to(root).as_posix() for f in sorted((root / folder).rglob("*")) if f.is_file() and not hidden(f)]

for path in paths:
    file = root / path
    if not file.is_file() or not file.stat().st_size:
        errors.append("Missing or empty: " + path)
    elif RAW_WVS_NAME.search(file.name) or file.stat().st_size > MAX_FILE_BYTES:
        errors.append("Looks like the raw WVS file or an oversized file, which must not be submitted: " + path)
# Anything else in 03_code would be left out of the archive and break notebooks that rely on it.
for file in sorted((root / "03_code").iterdir()):
    if file.is_file() and not hidden(file) and file.relative_to(root).as_posix() not in paths:
        errors.append(f"Outside the submission structure, so it would not be shipped: 03_code/{file.name}")

for path in paths:
    if path.endswith(".ipynb") and (root / path).is_file():
        check_notebook(path)
    elif path.endswith(".pdf"):
        check_pdf(path, next((limit for label, limit in PAGE_LIMITS.items() if path.endswith(label + ".pdf")), None))

url = read("05_dashboard/dashboard_url.txt").strip()
if url and not re.fullmatch(r"https?://\S+", url):
    errors.append("05_dashboard/dashboard_url.txt must contain the live URL and nothing else")
pins = [line.strip() for line in read("03_code/requirements.txt").splitlines() if line.strip() and not line.lstrip().startswith("#")]
if not pins:
    errors.append("03_code/requirements.txt lists no packages")
errors += [f"Unpinned requirement (use ==): {pin}" for pin in pins if not re.match(r"[A-Za-z0-9_.\[\],-]+==\S", pin)]
readme = read("submission_README.md").lower()
if readme:
    errors += [f"submission_README.md does not mention {surname}" for surname in MEMBERS if surname not in readme]
    if group.lower() not in readme.replace(" ", ""):
        errors.append(f"submission_README.md does not state the group number ({group})")
    if url and url.lower() not in readme:
        errors.append("submission_README.md does not contain the dashboard URL from 05_dashboard/dashboard_url.txt")
if len(MEMBERS) not in (4, 5):
    warnings.append(f"{len(MEMBERS)} members listed; the brief specifies groups of 4 or 5")
warnings.append("Not checked here: student IDs in the README, signatures, consent choices, and that the dashboard URL is live")

print("\n".join("Warning: " + warning for warning in warnings), file=sys.stderr)
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
