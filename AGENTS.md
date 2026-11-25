# Team agent instructions

Use a separate clone or worktree per agent. Read these rules before editing. Ask the operator for their assigned branch. Check git branch --show-current before editing, committing and pushing. Stop on a mismatch, detached HEAD, unexpected edits or overlapping assignments. Never switch branches on the operator's behalf.

Member branches own only their numbered notebook in 03_code (01_*_aquilina.ipynb, 02_*_buttigieg.ipynb, 03_*_muscat.ipynb respectively), and their own folder under work/ named after their branch suffix. data-prep owns 03_code/00_data_preparation.ipynb and 04_data. dashboard owns 03_code/dashboard. Coordinate shared files through a separately assigned integration branch and human review.

Never write directly to main, push to another branch, force push, delete branches, merge PRs, discard others' edits or change these controls on a member branch. Explicitly push HEAD to the assigned branch. Open a PR for human review. Flag shared-data or dependency changes for integration. Use the agreed dataset, split and evaluation protocol. Record AI use and checks in your own work folder. Keep raw data, IDs, signatures, consent forms and secrets off public GitHub.
