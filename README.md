# ICS5110 Applied Machine Learning
Team workspace for the World Values Survey Wave 7 assignment. Read AGENTS.md before editing. Use member/aquilina, member/buttigieg or member/muscat for individual work. Use data-prep for shared data preparation and dashboard for the web app. Agree on a single evaluation protocol and split before training. Submit the topic, target and data paragraph by 5 December 2026.

## Run the dashboard
From the repository root run `python -m http.server 8000 --directory 03_code/dashboard` and visit http://localhost:8000. The same directory can be deployed to a static web host. Record the final public URL in 05_dashboard/dashboard_url.txt. Keep it live until marks are published.

## Package the submission
Work from an integrated checkout. Place final PDFs, the signed forms and a completed submission README locally. Keep student IDs and signatures out of this public repository. Run `python tools/export.py 07`, replacing 07 with the assigned group number. The script reports missing files and writes the ZIP in dist/. Back up the ZIP privately. One member uploads it to the VLE by 11 January 2027.

Local submission_README.md must include group number, member names, IDs, techniques, live URL and run instructions. Put pinned Python dependencies in 03_code/requirements.txt. Execute notebooks top to bottom using relative paths and save outputs. Record the WVS release, filename and download URL in 04_data/README.md. Keep raw WVS downloads outside the repo. Put cleaned data in processed/ or rebuild it in the preparation notebook. Review page limits (20 report, 10 journal), consent choices, signatures, hosted URL and reproducibility before upload.
