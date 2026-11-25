# Team agent instructions

## Assignment context — read at the start of every session

**Objective.** For ICS5110 Applied Machine Learning 2026/27, use World Values Survey Wave 7 respondent data to investigate a question across countries. Each member owns one ML technique. The team compares them on the same cleaned data, train-test split and evaluation protocol and presents the findings in one hosted interactive dashboard.

**Team decision.** Our target is Q51: how often the respondent or their family went without enough food in the preceding 12 months (1 often, 2 sometimes, 3 rarely, 4 never). The team has discussed grouping 1–3 versus 4. That is a proposal. Check the latest agreed decisions in issue #3 before treating any recoding, predictors, country exclusions, techniques, metrics or thresholds as final. Preserve the distinction between survey weights and the costs assigned to prediction errors. Dataset access instructions are in 04_data/README.md (see PR #1).

**What good work demonstrates.** Justify the predictors, cleaning, missing codes and survey weights. Explain each model choice and why the mix is informative. Compare models fairly, show how parameter or cost changes affect a demographic or country group, justify the threshold and explain who bears each error. Examine one confident mistake, whether a human could have caught it, and whether weighting errors by their cost changes the ranking. The dashboard must support side-by-side comparison, threshold adjustment, confidence/error inspection and exploration of the data. Interpret country differences as associations.

**Deadlines and delivery.** By 5 December 2026 submit one paragraph naming the topic, target variable and planned data. By 11 January 2027 one nominated member submits the group ZIP to the VLE. It contains the report (20 pages maximum), AI journal (10 pages maximum including references), runnable code and data pipeline, live dashboard URL, signed contribution statement and individual excerpt-consent choices. Keep the dashboard available until marks are published. Follow README.md and the original brief for exact packaging. The brief specifies groups of four or five; three member branches currently appear in the setup. Confirm the roster or an approved exception with the team.

**Assessment priorities.** Judgement 30%; dataset 15%; interactive dashboard 15%; comparison and insights 15%; documentation 15%; AI journal 10%. Implementation carries no separate marks. Record enough evidence for each member to explain their choices in a viva, including citations for third-party and AI-generated material.

Use a separate clone or worktree per agent. Read these rules before editing. Ask the operator for their assigned branch. Check git branch --show-current before editing, committing and pushing. Stop on a mismatch, detached HEAD, unexpected edits or overlapping assignments. Never switch branches on the operator's behalf.

Member branches own only their numbered notebook in 03_code (01_*_aquilina.ipynb, 02_*_buttigieg.ipynb, 03_*_muscat.ipynb respectively), and their own folder under work/ named after their branch suffix. data-prep owns 03_code/00_data_preparation.ipynb and 04_data. dashboard owns 03_code/dashboard. Coordinate shared files through a separately assigned integration branch and human review.

Never write directly to main, push to another branch, force push, delete branches, merge PRs, discard others' edits or change these controls on a member branch. Explicitly push HEAD to the assigned branch. Open a PR for human review. Flag shared-data or dependency changes for integration. Use the agreed dataset, split and evaluation protocol. Record AI use and checks in your own work folder. Keep raw data, IDs, signatures, consent forms and secrets off public GitHub.

## Coordinate every session in [the shared activity log](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/issues/3)

Read the latest comments when starting or resuming. Post the member name, branch and task before starting. For joint tasks agree on owners and inputs/outputs; acknowledge requests and reply when resolved. Post blockers when they arise. Before ending every session, including research-only work, append the outcome, reasons, checks and next owner. Link detailed evidence instead of duplicating it. If GitHub commenting is unavailable, keep the entry in your assigned notes, flag it as pending and post it when access returns. Never claim an update was posted unless confirmed.

Every PR description must link directly to its session handoff comment in issue #3. Reviewers should confirm the entry describes the changes and checks. The coordination workflow verifies the linked comment exists.

## Keep an assignment record as you work

On a member branch, maintain one running Markdown file at `work/<surname>/log.md`. On data-prep or dashboard, record the same details in the relevant PR description or a follow-up PR comment, so working notes stay out of the submission and inside the branch ownership rules. Link related entries across branches. Read the latest entries when resuming. Update the record with each substantive decision, experiment or AI-assisted contribution, including failed attempts that changed the work. At handoff, link the entries and identify outstanding decisions and their owners.

Use a dated entry with the contributor, question, decision status (proposed, agreed or superseded), options considered, rationale, evidence, checks and outcome. Explain what property of the data or assignment made the chosen option preferable and what trade-off it introduces. Cite the relevant source, notebook section, saved output, commit or PR so another member can verify it. When a decision changes, append the new reason and link the earlier entry. Attribute approval and work accurately for the signed contribution statement.

### Evidence for the report

- Save the checkpoint question, target and intended data. Record departures from that plan and why. For Q51, document how the original response codes map to the chosen outcome and why the grouping suits the research question.
- Record the WVS release and citation, country coverage, predictor choices, exclusions, missing codes, recoding, survey weights and their effects on the usable sample. Cite the codebook or observed counts.
- Explain the team's mix of techniques and each model's suitability. Record alternatives, scaling, feature selection or dimensionality reduction, shared split and evaluation protocol, cross-validation choices and leakage checks.
- For each experiment, identify the data/split version, settings, seed where relevant, run instructions and observed metrics. For each technique, record the before-and-after effect of a parameter or cost-function change on a named demographic or country group.
- Justify the metrics and decision threshold. Identify who bears the cost of a miss and a false alarm. Keep survey weighting separate from error-cost weighting. Record whether weighting errors changes the model ranking. Describe a confident error, its potential harm and whether a human reviewer could realistically catch it.
- Link dashboard views and checks to the reported results, including side-by-side comparisons, threshold trade-offs and confidence versus errors. Record country-level limitations, possible bias and why the results support associations. Keep source and code citations as you go.

### Evidence for the generative AI journal

For noteworthy AI uses, record the tool/model (when known), why it was chosen, its place in the workflow, the prompt and relevant response or a redacted excerpt, what was used, revised or rejected, and its effect on the work. Cite AI-generated code and external material. Describe concrete benefits, errors, bias or privacy concerns where they arose.

Record exactly what was checked, how, by whom and what happened. Mark unchecked outputs explicitly. Preserve dated examples showing how checking practices evolved, including actual errors caught or missed. Each member writes their own personal reflection. Never invent retrospective reasoning, checks, results, approval or personal experience. Keep raw records, private information and sensitive screenshots out of public logs.
