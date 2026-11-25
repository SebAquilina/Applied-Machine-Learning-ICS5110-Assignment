# Matthias Muscat’s assignment log

## 25 November 2026 · Q51 and branch responsibilities

**Contributor and scope.** Matthias Muscat’s branch, with Codex assisting on the repository review. The task was to establish what the team had agreed and whether Matthias owed anyone an input before starting model work. [Session start in #3](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/issues/3#issuecomment-7171475802)

**Agreed target.** Use World Values Survey Wave 7 question Q51. It asks how often the respondent or their family went without enough food in the preceding 12 months. The response codes are 1 often, 2 sometimes, 3 rarely and 4 never. [Team decision](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/issues/3#issuecomment-7170761977)

**Proposed grouping.** Combining 1–3 would count even a rare shortage as a positive outcome. The earlier exploratory grouping, 1–2 versus 3–4, would count “rarely” as negative and answer a different question about recurring shortages. Neither grouping has team approval in #3. Coding labels now could leave members comparing models that predict different outcomes. The group owns this choice and the shared split and evaluation protocol. [Assignment instructions in PR #2](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/blob/876b32b0cf50f7a23361a5fdbf72fbecb5c9cbc3/AGENTS.md)

**Checks and outcome.** Codex checked the current branch, local status including untracked files, and the remote branch tip. The checkout was clean and matched `member/muscat` at `6d71652`. Codex read the branch and main instructions and README, the full instructions at the head of open PR #2, and all three existing team comments in #3. Matthias owns `03_code/03_*_muscat.ipynb` and `work/muscat/`. The thread contained no request waiting on Matthias. The maintainer owns review of #2 and branch synchronisation after merge. This session produced the member log only. [Maintainer handoff](https://github.com/SebAquilina/Applied-Machine-Learning-ICS5110-Assignment/issues/3#issuecomment-7170733684)

**AI-use record.** Matthias asked Codex to “check PR #2” and “read the latest comments in team log #3”. Codex used the PR text and the dated handoff to check the summary against the team's words. The result retained Q51 as agreed and its recoding as proposed. No survey data were inspected and no model was trained in this session.
