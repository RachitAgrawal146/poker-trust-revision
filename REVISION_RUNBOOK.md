# REVISION_RUNBOOK.md

Journal revision, round R1, of the poker trust paper. Decision received
17 Sep 2026: "Revise and Resubmit". Hard deadline **16 Dec 2026**; internal
target **12 Dec 2026**.

This file is written for Claude Code. It says what to do, in what order, and
how to know a step is finished. The author (Rachit) says "do step B2" and you
do exactly that step.

**This file belongs in the private repository (section 0.2). Do not commit it,
or anything derived from it that mentions reviews, to the public code repo.**

---

## 0. Read this first

### 0.1 How to work

1. Do **one step per session** unless the author asks for more. Before touching
   anything, read `PUB/CLAUDE.md`, this file, and `PRIV/STATUS.md`.
2. Every step has **Do** and **Done when**. A step is not finished until every
   "Done when" line is true. If a check fails twice, stop and write the blocker
   in `PRIV/STATUS.md`. Do not improvise around it.
3. End every step with one entry in `PRIV/STATUS.md`: step ID, date, commit
   hashes, what was produced, what surprised you, what the author must look at.
4. Steps marked **GATE** need the author's answer before you continue. Ask in
   plain words, list the options, stop.
5. This runbook was written from one reading of the repo plus small pilot runs.
   Where a step turns out to rest on a wrong assumption, say so in `STATUS.md`
   and propose the correction; do not silently follow or silently deviate.

### 0.2 Two repositories

| Name here | Repository | Holds |
|---|---|---|
| `PUB` | The existing public repo `Poker_trust` | Code, experiment harness, workflows, machine-readable outputs (JSON, CSV), data Releases. Nothing about the review |
| `PRIV` | A new **private** repo (suggested name `poker-trust-revision`) | This runbook, `STATUS.md`, `DECISIONS.md`, every report written in words, the briefs, the response tracker, and the manuscript (`PRIV/paper/`) with a frozen copy of the submitted sources (`PRIV/paper_r0/`) |

Why: the public repo sits behind the anonymous link the reviewers use. Reviews
are confidential, and an audit of the submitted paper's weaknesses should not
be readable there before the revision is submitted. Start every session with
both repos attached.

### 0.3 Hard rules

| # | Rule | Why |
|---|---|---|
| H1 | **Do not write, rewrite or paraphrase manuscript prose.** That covers the abstract, body text, captions, any sentence in the supplement, the acknowledgment, the cover letter, and the replies in the response letter. You produce code, data, tables, figures, formulas, pseudocode, prompt listings, numeric macros, bibliography entries, LaTeX plumbing, fact sheets, outlines and check reports. | The associate editor's main complaint is AI-written, low-quality text. The author writes; you check. |
| H2 | **Never spend API money** without gate G2 cleared, a per-job cap and a total cap. | The last run died when credit ran out and lost two arms. |
| H3 | **Never edit** `archetype_params.py`, `preflop_lookup.py`, `phase1/test_cases.py`, or the Stage 5 trust flow in `agents/base_agent.py`. New behaviour goes in new modules and subclasses behind flags whose default reproduces the published behaviour bit for bit. | These produced the published data. |
| H4 | The submitted sources are **frozen** at tag `tog-r0-submitted` (commit `3e87700`). The revision is written in `PRIV/paper/`. | The tracked-changes PDF is a diff against R0. |
| H5 | **No result is typed by hand into LaTeX.** Every result number comes from a data file through a generated macro or table. When porting the author's text you may replace a typed number with its macro if the values are identical, and you show that as a diff. | The last two passes shipped tables that contradicted their own captions. |
| H6 | **Report what the data says.** Do not tune a design, a seed list, a threshold or a metric to rescue a claim. The analysis plan (C0) is committed before the full runs. Negative results are results. | The paper's central claim may not survive. That is acceptable; hiding it is not. |
| H7 | **Verify every citation** against the publisher page or DOI before it enters the `.bib`. Never cite from memory. Log the URL checked. | |
| H8 | **Never commit the decision letter or reviewer text anywhere**, and keep anything that paraphrases reviews, lists the paper's weaknesses, or interprets unpublished results in `PRIV`. Refer to comments by the IDs in section 3. | Reviews are confidential. |
| H9 | Git: in `PUB` work on branch `revision/r1`; in `PRIV` on `main`. If a session cannot push to the working branch of either repo, it works on its own branch in that repo and opens a pull request into the working branch for the author to merge before the next step starts. Follow the commit style in `PUB/CLAUDE.md`. Never force-push, never amend. | Amended 13 Oct 2026 after A1, when the session could push only to its own branch. |
| H10 | Code that produced published data is never changed retroactively. If the paper and the code disagree, the paper changes, or a new flagged variant is added and run. | |
| H11 | Do not merge or push anything to the branch the anonymous review link tracks until step F3. Step A0 records which branch that is. | Reviewers may open the link at any time. |

### 0.4 Environment facts

* The cloud container that usually drives these repos **cannot download GitHub
  Actions artifacts** and **cannot call `workflow_dispatch`**. What works is a
  workflow triggered by a **push to a dedicated branch** that commits small
  outputs back to that branch and uploads databases to a **GitHub Release**.
  The model to copy is `.github/workflows/analytics-n20.yml` on branch
  `analytics-n20` (not `run-ablation.yml`, which pushes to `main` and relies on
  artifacts). If `gh workflow run` works in your session, you may use it.
* `PUB` is public, so its Actions minutes are free; a job must end within 350
  minutes; keep at most 20 jobs running, 10 for LLM runs. `PRIV` has a small
  free allowance; use it only for LaTeX builds.
* The rule-based simulator runs at about 6 hands per second per core (two
  independent measurements on 12 Oct 2026). Measure the runner's speed in C2.
* Releases do not expire. Actions artifacts do (step A2).
* `tog_submission/` does not contain `IEEEtran.cls` or `IEEEtranN.bst`; they are
  inside `tog_build/tog_main_source.zip`. Builds need a TeX Live with the
  publishers collection and `latexdiff`; run them in a workflow.

### 0.5 Terms

| Term | Meaning |
|---|---|
| R0, R1 | The submitted version; the revision |
| Published roster | Stage 6 roster, fixed seats (Oracle 0 to Judge 7), 200-chip stacks with rebuys, submitted trust model |
| Net winnings | Chips won minus chips put in. Equals `final_stack - 200 * (1 + rebuys)` in rebuy runs |
| Win rate | Net chips per 100 hands. Compute in chips. The display unit (big blind = 2 chips, or big bet = 4 chips) is fixed in C0 after checking the convention in the limit hold'em literature |
| Showdown and non-showdown winnings | A player's net chips in hands where **that player** did or did not reach showdown. Not a split by whether the hand had a showdown |
| Trust statistic | R0 uses the mean over the seven observers of trust at the **final hand's** snapshot (`analysis/compute_metrics.py`). C0 fixes the R1 statistic |
| Reading | An agent's play depending on what it has observed or been told about a specific opponent |
| `no_read` roster | The published roster with all reading off: Predator always on its baseline table, Mirror always on its default table, Judge's trigger threshold out of reach. Three small subclasses, no change to existing files. First needed in B4 and B5; build it once under `revision_experiments/` and reuse it in C1 |
| Valid seed | All hands played; chips conserved; under the new protocol no rebuy and no all-in; zero API errors; at most 1% of LLM replies unparseable |
| Protocol v2 | The LLM setup defined in step D1 |

---

## 1. Ground truth about the public repository (verified 12 Oct 2026)

| Fact | Detail |
|---|---|
| The manuscript the reviewers read | Branch `claude/repo-papers-review-chz55c` at `3e87700`, folder `tog_submission/`; 10 pages, 34 references. It is 6 commits ahead of `main` (`9f9a067`) and was never merged. `main` holds the older July text |
| Phase 1 data in the repo | `research_data/runs_v3.sqlite.part_00/01` (Git LFS, about 2.5 GB): 20 seeds x 25,000 hands, **not** the 5 x 10,000 the paper describes, with a different seed list. It is the source of the paper's 87.1% and 38.5% figures |
| Phase 3 data in the repo | `research_data/runs_phase3_long.sqlite` (LFS): 5 seeds x 500 hands, temperature 1.0 |
| Data **not** in the repo | `runs_phase1_long.sqlite` and `runs_phase2_long.sqlite` (the 5 x 10,000 runs behind the published r values), the unbounded runs, and `runs_phase31_long.sqlite` (the five-seed temperature-1.0 Phase 3.1 run behind r = -0.094, the "temperature-matched" comparison and Box S2). `phase3/phase3_report.md` calls the last one LFS-tracked; it is not |
| Canonical Phase 3.1 (n=20, temperature 0) | Only in Actions artifact `all-databases-phase31-n20` of run `30788234686`, 90-day retention from 3 Aug 2026. Aggregates in `paper_resources/data/phase31_n20_stats.json` |
| Ablation | Artifact `all-databases-ablation` of run `30874382486`, 90 days from 4 Aug 2026. no-cot: 5 clean seeds. no-memory: 3 seeds, contaminated by credit exhaustion. no-notes: nothing |
| The database schema | Stores actions, showdown hole cards and per-hand trust snapshots. It does **not** store community cards, hole cards of players who folded, or decision-time hand-strength buckets. Blinds are not rows in `actions` |
| `CLAUDE.md` is stale | Status header says Phase 3.1 r = -0.094; rule 6 says the working branch is `main`; rule 7 says to reuse the "canonical abstract" verbatim |
| Page limit | Full papers: 10 pages, two-column, references included, supplementary material excluded; USD 200 per extra page; more than 12 pages needs justification in the cover letter. Source: https://transactions.games/submit/submission-guidelines (read 12 Oct 2026) |
| AI policy | AI-generated content (text, figures, images, code) must be disclosed in the acknowledgments, naming the system, the sections and the level of use. Source: IEEE Author Center, guidelines for AI-generated content (read 12 Oct 2026) |

---

## 2. What the revision must achieve

The submitted paper claims that reputation punishes honest players (trust and
profit correlate at r = -0.75 under rule-based agents) and that reasoning
scaffolds remove the effect (r near 0 under LLM agents with scaffolds).

Objections from the review, confirmed against the code:

1. **Reputation is never isolated from playing style.** In Phase 1 only
   Predator reads the posterior; Mirror and Judge react to opponents through
   their own counters; the five static agents react to no one. In Phase 2 the
   adaptive agents drop Predator's exploit table and Mirror's copying, so
   nobody reads the posterior at all. A pilot with all reading switched off
   reproduces the published correlation (Appendix C.2).
2. **The outcome metric is wrong.** Final stack ignores rebuys. Under net
   winnings the most-trusted archetype is the biggest loser in the canonical
   Phase 3.1 data, not sixth "above its buy-in" (Appendix C.1).
3. **Samples are far too small**, above all in the LLM phases.
4. **The ablation named in the abstract was not completed.**
5. **Methods are under-specified and partly wrong**, and the writing reads as
   AI-generated and undisclosed.

Problems the reviewers have not raised but could find:

6. The LLM personality prompts **contain Phase 1 outcomes** (one archetype "is
   catastrophic", another "the most economically successful", trust scores,
   who gets identified), and each decision prompt shows the **archetype name**
   of every opponent who has acted in the current betting round. Both have
   been true since the first Phase 3 commit (13 Apr 2026).
7. The trust model's likelihood **treats the three hand-strength buckets as
   equally likely**. Preflop the true shares are 3.3% Strong, 10.9% Medium,
   85.8% Weak, so the model expects Sentinel to fold to a preflop bet 50% of
   the time when its policy implies 83% (Appendix C.4). The paper calls the
   likelihood "well-specified".
8. An **all-in player is folded automatically** if anyone bets later in the
   hand (`engine/game.py`, the `agent.stack <= 0` branch), contrary to the
   side-pot description. It hits the chronic losers when short-stacked.
9. Many paper statements contradict the code or the data (step B3).

**The strategy.** Rebuild the evidence in three layers, each with a standard
metric and adequate samples.

* **Layer 1, style only.** Rule-based agents with all reading off. Any profit
  gap here is playing style.
* **Layer 2, reading switched on in a controlled way.** One explicit, uniform
  mechanism by which agents respond to a bettor's reputation, applied
  (a) to one target archetype at a time and (b) to everyone, using either the
  inferred posterior or the true type. The primary quantity is the **cost of
  being read**: an archetype's win rate when others respond to *its*
  reputation, minus its win rate with all reading off. Controls separate
  reading from mere loosening of the table, from correct attribution, and from
  random noise.
* **Layer 3, language models.** A small, clean, matched experiment (design
  chosen at G2), framed as exploratory.

Whether the "transparency paradox" survives is an empirical outcome of Layer
2. Either answer is publishable. Build nothing that presumes one.

**What the pilot does and does not show.** A crude version of the mechanism
(Appendix B) moved the published correlation from -0.73 to -0.32 and +0.04 as
its strength rose, and cut the maniac's win rate by two-thirds (Appendix C.3).
That is a rule-based mechanism reproducing the "attenuation" the paper
attributes to language-model reasoning. But the crude version also makes the
whole table call more, folds strong hands to "honest" bettors, treats only one
honest archetype as trusted, and acts on a fifth of the decisions. It proves
the layer is worth building. It is not the design.

---

## 3. Reviewer-comment register

Short labels only (H8). The author has the letter for exact wording. Type:
**X** new experiment or analysis, **M** methods or definitions, **W** author's
writing, **T** typesetting, **A** author action.

### Editor

| ID | Comment | Type | Step |
|---|---|---|---|
| ED-1 | Provide a detailed account of all changes | W | F1, F4 |
| ED-2 | Highlight changes in the revised manuscript | T | F2 |
| ED-3 | Resubmit within 90 days, same manuscript type, delete redundant files | A, T | A0, F2, F4 |
| ED-4 | Disclose AI-generated content in the acknowledgments: system, sections, level | W | E8 |
| AE-1 | Borderline; serious work needed to reach the journal's bar | X | B, C, D |
| AE-2 | Strong suspicion of AI writing; must be addressed and mentioned | W | E6, E8 |
| AE-3 | Writing quality is the real problem | W | E5 to E7 |

### Reviewer 1

| ID | Comment | Type | Step |
|---|---|---|---|
| R1-W1 | Key details missing: bluff versus value bet, origin of the "GTO" baseline, the actual strategies | M | B3, E2 |
| R1-W2 | Sample sizes far too low; 150 hands gives a handful of showdowns | X | C3, C4 for rule-based. LLM: longer seeds in D, and the limits stated plainly (E4, E5) |
| R1-W3 | The evaluation does not separate the value of aggression from the effect of reputation; opponents cannot respond | X | C0 to C4 |
| R1-W4 | Parts of the study named in the abstract were not done | X, W | D (Q4), F2 abstract gate |
| R1-M1 | Introduction example switches abruptly to "opponent" | W | E5 |
| R1-M2 | Bluffing is not cheating | W | E5, F2 gate |
| R1-M3 | "Walkover" is not a poker term as used | W, T | B1 mapping, F2 gate |
| R1-M4 | Use standard poker names for the archetypes | W, T | Q2, B1 mapping |
| R1-M5 | Final stack is a poor metric with rebuys; use win rate or regret; why side pots; consider unlimited stacks | X | B1, B2, C1, D1 |
| R1-M6 | Origin of the baseline strategy; equity-driven or rank-driven; a strong draw is not a bluff | M, X | B3, B5, E2 |
| R1-M7 | The "no chance to win" hand has no runout; does the calling station never fold | M | B0, B3, E2 |
| R1-M8 | The Phase 3 softening is sampling noise, not reasoning | X | C1 noise control, D matched temperature |
| R1-M9 | Running out of quota is no reason to leave the study unfinished | X | D |
| R1-M10 | Standard results were pushed to the appendix | W, T | E1, E5 |

### Reviewer 2

| ID | Comment | Type | Step |
|---|---|---|---|
| R2-A1 | Abstract too detailed | W | E5 |
| R2-A2 | Tie the end of the abstract to the opening motivation | W | E5 |
| R2-I1 | State AI use; one intro sentence reads as machine-written | W | E6, E8 |
| R2-I2 | Define the transparency paradox in the introduction | W | E5 |
| R2-I3 | "This question" before any question is asked | W | E5 |
| R2-I4 | Introduction must say what was found | W | E5 |
| R2-I5 | Delete the last sentence of the introduction | W | E5 |
| R2-B1 | Research question belongs in the introduction, unmissable | W | E5 |
| R2-B2 | The bullet list in Background adds nothing | W | E5 |
| R2-BA1 | Engage the Prisoner's Dilemma literature; say why poker adds to it | W | E3, E5 |
| R2-BA2 | Break subsection A into paragraphs | W | E5 |
| R2-BB1 | "its" should be "their" for a player | W | E7 |
| R2-BB2 | The Fudenberg and Levine sentence is unexplained | W | E3, E5 |
| R2-BB3 | The Mailath and Samuelson sentence is unexplained | W | E3, E5 |
| R2-BB4 | Paragraph break needed at "Our setup" | W | E5 |
| R2-BB5 | Phases referenced before they are defined | W | E5 |
| R2-BC1 | Ordinal words with no first or second | W | E7 |
| R2-BC2 | Cite the Prisoner's Dilemma | W | E3 |
| R2-BC3 | Open with the dilemma as the framing device | W | E5 |
| R2-BC4 | Break subsection C into paragraphs | W | E5 |
| R2-BC5 | Slow-play is listed as an action | W | E5 |
| R2-BD1 | Put the opponent-modelling citation where the topic is first mentioned (the citations exist) | W | E5 |
| R2-BD2 | Some author names render in red | T | E1 |
| R2-BE1 | Cut the "both are standard" sentence | W | E5 |
| R2-M1 | Define the phases before Background uses them | W | E5 |
| R2-M2 | Why "Phase 3.1" and not Phase 4 | W, T | Q2, B1 mapping |
| R2-MC1 | Why a length-8 posterior; cite if borrowed | M | E2, E3 |
| R2-MC2 | Cite the equations unless original | M | E3 |
| R2-MD1 | "2\*" is an odd phase name | W, T | Q2, B1 mapping |
| R2-MF1 | Cite the Monte Carlo evaluator and the library | M | E3 |
| R2-RB1 | Interpretation has leaked into Results | W | E5, E7 |
| R2-RC1 | Replace paragraphs about rebuys and chips with a plot | X | C4 (a plot, not a table) |
| R2-RF1 | The ablation subsection adds little as it stands | X | D (Q4) |
| R2-D1 | The "unsettling title" sentence is stale | W | E5, F2 gate |
| R2-D2 | "No numerical optimisation can resolve it" needs proof or softer wording | W | E5, F2 gate |
| R2-DA1 | The one-sentence definition of trust belongs much earlier | W | E5 |
| R2-DB1 | Cite CMA-ES and REINFORCE or drop them; move the point to limitations | W | E3, E5 |
| R2-DC1 | Are the three implications new; what was unexpected | W | E4, E5 |
| R2-C1 | The URL renders in red | T | E1 |
| R2-C2 | The code looks LLM-generated; disclose | W | E8 |
| R2-C3 | The closing question is the best line; move it up front | W | E5 |
| R2-CIT1 | References 17 and 24 show a dash instead of authors | T | E1 |

### Reviewer 3

| ID | Comment | Type | Step |
|---|---|---|---|
| R3-1 | No comments in the letter; they may be attached in the portal | A | A0. If there is an attachment, the author describes each point in his own words and you add rows `R3-n` here before any other step |

---

## 4. Author questions and gates

Record every answer in `PRIV/DECISIONS.md` with the date. Until a question is
answered, build so that either answer works.

| ID | Question | Default if no answer |
|---|---|---|
| Q1 | Adopt the three-layer framing in section 2 as the paper's spine | Adopt |
| Q2 | Display names: standard poker terms for archetypes, descriptive phase names instead of "2\*" and "3.1" | Standard terms in the paper; code names unchanged |
| Q3 | Replace "honesty" with a neutral term that matches its definition, one minus the bluff frequency (for example "non-bluff rate") | Replace |
| Q4 | LLM experiment: which design (Appendix D: reputation shown or hidden, or the scaffold factorial) and which budget | No LLM runs until answered |
| Q5 | Hill-climbing phases in the main text or the supplement | Supplement |
| Q6 | Stay within 10 pages or pay for extra pages | 10 pages |
| Q7 | Primary trust model for new runs: the submitted one or the corrected one (step B5) | Decide at G1 with the B5 report. If still unanswered: submitted one primary, corrected one as sensitivity |

| Gate | When | The author must |
|---|---|---|
| G1 | After C0 | Approve the analysis plan, including the reading mechanism; answer Q1, Q7 |
| G2 | After D1 | Answer Q4; approve the prompts; top up API credit; confirm the caps |
| G3 | After E4 | Read the results summary; fix the paper's main claim and title; answer Q2, Q3, Q5, Q6 |
| G4 | After F3 | Final read; cover letter; response letter; upload |

---

## 5. Steps

### Phase A. Safeguard and set up

#### A0. Author-only checks

* Log in to the journal's portal. Check whether Reviewer 3 left an attachment
  (R3-1). Open the revision link: note the exact due date and the upload slots.
* Open the anonymous code link in a private browser window. Note whether it
  loads, **which branch it shows**, when it expires, and whether your name,
  school or email appear anywhere.
* Create the private repository and put this file in it.
* Look on your own machines and drives for `runs_phase31_long.sqlite`,
  `runs_phase1_long.sqlite`, `runs_phase2_long.sqlite` and the unbounded
  runs. Tell Claude Code which exist; attach any you find to Release `data-r0`
  after step A2.

**Done when** the answers are in `PRIV/DECISIONS.md`.

#### A1. Branch, freeze, correct the project memory

**Do**

1. `PUB`: create branch `revision/r1` from
   `origin/claude/repo-papers-review-chz55c`. Not from `main`. Tag `3e87700` as
   `tog-r0-submitted`.
2. `PRIV`: create `STATUS.md`, `DECISIONS.md`, `reports/`, `briefs/`,
   `paper_r0/` (copy of `tog_submission/` plus the class and style files from
   `tog_build/tog_main_source.zip`) and `paper/` (empty).
3. `PRIV`: add a build workflow with TeX Live (publishers collection) and
   `latexdiff`. Build `paper_r0/` and compare `pdftotext` output with
   `PUB/tog_build/tog_anonymous_FINAL.pdf`.
4. `PUB/CLAUDE.md`: add a short "Revision mode" section. State that the
   working branch for the revision is `revision/r1` (overriding rule 6), that
   rule 7's "canonical abstract verbatim" instruction is retired, that
   `tog_submission/` and `tog_build/` are frozen at the tag, and repeat H3 and
   H10. Correct the stale status header. Mention no reviews.
5. Do not open or merge a pull request into `main`, and do not touch the
   branch the anonymous link tracks (H11).

**Done when** the R0 build is 10 pages with 34 references and its text matches
the submitted PDF; the tag exists; both repos carry the items above.

#### A2. Rescue the raw data. Do this before 25 Oct 2026

The n=20 Phase 3.1 databases and the ablation databases exist only as Actions
artifacts that expire about 1 and 2 Nov 2026.

**Do**

1. `PUB`: add `.github/workflows/archive-data.yml`, triggered by a push to
   `run/archive-data`, with `actions: read` and `contents: write`.
2. Download `all-databases-phase31-n20` (run `30788234686`) and
   `all-databases-ablation` (run `30874382486`). Run `PRAGMA integrity_check`
   on each file. Confirm 20 databases of 150 hands for the replication.
3. Create Release `data-r0`; upload one compressed archive per experiment and
   `SHA256SUMS`. Keep the three contaminated no-memory seeds, marked in a
   README inside the archive. Do not analyse them.
4. Check that the LFS objects in `research_data/` resolve. Do not copy the
   2.5 GB Phase 1 file into the release.
5. Commit `research_data/MANIFEST.md`: each dataset, where it lives, protocol
   (model id, temperature, hands, seeds, prompt version), checksum.
6. From the session container, try to download one Release asset directly.
   Record whether it works; step A3 depends on the answer.

**Done when** the release lists the archives and a second workflow run can
download and open them.

**If the artifacts are already gone**, say so at the top of `STATUS.md` and
tell the author at once. Only the aggregate JSON would remain.

#### A3. Analysis venue, then reproduce the rule-based baselines

**Do**

1. `PUB`: add `.github/workflows/analysis.yml`, triggered by a push to
   `run/analysis`. It downloads named Release assets (and LFS objects), runs
   one named analysis script, and commits only JSON and CSV outputs to the run
   branch. Written reports go to `PRIV`. If A2.6 showed the container can fetch
   Release assets, small analyses may run in the session instead.
2. `PUB`: add `.github/workflows/rule-based.yml`, triggered by a push to
   `run/rule-based`, with a matrix over (condition, seed chunk) and four
   processes per job. Step C1 will reuse it.
3. Run the four test suites and record the results:
   `python3 phase1/run_tests.py --stage all`, `python3 tests/test_trust_model.py`,
   `python3 tests/test_engine_sidepot.py`, `python3 phase3/validate_phase31.py`.
   Stage 5.3 and 6.1 are expected to fail (see `CLAUDE.md`).
4. Regenerate with full logging: Phase 1 (`phase1/run_sim.py --stage 6`, seeds
   42,137,256,512,1024, 10,000 hands), Phase 2
   (`phase2/adaptive/run_adaptive.py`, same seeds and hands) and both unbounded
   variants (settings in `paper_resources/notes/phase2_unbounded_writeup*.md`).
5. Recompute per-seed r by calling `compute_trust_profit_correlation` for each
   `run_id` (the script's command line reads only the last run) and compare
   with `paper_resources/data/r_by_phase.json` to three decimals. Upload the
   databases to `data-r0`.

**Done when** `PRIV/reports/A3_reproduction.md` holds the comparison. If
values differ, record the numpy and treys versions and move on.

### Phase B. Fix the measurement

#### B0. Deterministic replay: recover what the databases do not store

**Do** Add `analysis/replay.py`. Given a database, re-run each seed with the
code at `runs.git_sha`, feeding the **recorded actions** back instead of
sampling or calling a model, so that the random stream deals the same cards.
Recover and store for every hand: the five community cards, every player's
hole cards, and each decision's hand-strength bucket.

**Done when** for every run the replay reproduces the logged showdown hole
cards, hand ranks and per-hand trust snapshots exactly, and the augmented
databases are in Release `data-r0`. For any run where replay cannot be made
exact (most likely the LLM runs), list which later analyses become impossible
for that run (the runout asked for in R1-M7, equity per street, B5 replays).

#### B1. Win-rate ledger and display names

**Do** Add `analysis/winrate.py` with tests.

* Per hand and seat: net chips = pots won minus chips put in. Blinds are not
  rows in `actions`: charge 1 chip to `hands.sb_seat`; charge the big blind
  `final_pot - sum(action amounts) - 1`, which is 2 except when a short stack
  posts 1. Reference code: Appendix A.
* Reconcile exactly: per run, column sums equal `final_stack - 200*(1+rebuys)`
  for every seat and every hand sums to zero.
* Outputs per archetype: net chips, win rate (chips per 100 hands plus the
  display unit), showdown and non-showdown winnings by the player-level
  definition in 0.5, per-hand standard deviation, and intervals. With fewer
  than 10 seeds use a block bootstrap over hands within seeds; otherwise
  resample seeds.
* Add `analysis/display_names.json`: one mapping from code names of archetypes,
  phases, conditions and metrics to display names. Every table and figure
  reads it. Include "pot won without showdown" for the engine's `walkover`.

**Done when** tests pass on the A3 databases with reconciliation error 0.

#### B2. Recompute every published headline under net winnings

**Do** For Phase 1 (both the 5 x 10,000 regeneration and the 20 x 25,000 LFS
dataset), Phase 2, 2\*, 3, 3.1 (n=20) and the no-cot arm: per-seed r with final
stack and with net winnings; Spearman as well as Pearson; per-archetype win
rate with intervals; showdown and non-showdown winnings. Write
`PRIV/reports/B2_metric_change.md`.

**Done when** the Phase 3.1 numbers match Appendix C.1.

#### B3. Paper-versus-code audit

**Do** Go through every equation, definition, metric, table, figure caption
and factual sentence in the R0 main text and supplement. Take equation and
table numbers from the R0 PDF. For each, find the code or data that backs it.
Write `PRIV/reports/B3_audit.md`: claim, location, what the code or data says,
verdict, proposed fix (paper, or flagged code variant per H10).

Confirm or refute these. Rows 1 to 18 come from the first reading of the code;
rows 19 to 30 from an independent second check.

| # | Paper says | Code or data says |
|---|---|---|
| 1 | Eq. 1 (posterior update): noise term is epsilon divided by the number of types (8) | `trust/bayesian_model.py`: epsilon times one over the number of legal actions (2 or 3) |
| 2 | The likelihood is "well-specified" | Unknown buckets are averaged with equal weights; see Appendix C.4 |
| 3 | Third-party evidence weight not stated | `config.TRUST["third_party_weight"] = 0.8`, a likelihood exponent |
| 4 | Decisions use Monte Carlo equity buckets | Postflop only: equity against one random hand, thresholds 0.66 and 0.33, 1,000 samples (50 for the LLM prompt hint). Preflop uses a hand-set lookup table. Showdown refinement and the Judge's grievance count use `_fast_bucket`, a made-hand class, so a strong draw is a value bet to the agent and a bluff to the observer |
| 5 | SU is entropy of the agent's action distribution | `compute_unpredictability` returns observers' mean posterior entropy about the agent |
| 6 | NS "collapses to 0" in the LLM phases | `window_size = 500`: a run of 500 hands or fewer has one window and scores 0 by construction |
| 7 | OA is a variance | It is a standard deviation |
| 8 | TEI is non-showdown winnings per hand | It starts from `final_stack - 200`, ignoring rebuys, and looks for blind actions that are never logged |
| 9 | Wall "never folds" | `weak_call` is 0.55, 0.50, 0.42, 0.35 by street: it folds a weak hand to a bet 45 to 65% of the time. The "never folds" hand in Box S1 is the LLM Wall of Phase 3; check what that agent's prompt says |
| 10 | Table S2 "policy bounds" | Wall's row (bets strong 95 to 100%, folds weak 0 to 5%) matches neither `archetype_params` (`vbr` 0.55 to 0.40) nor `phase2/adaptive/bounds.py` (preflop `vbr` 0.40 to 0.75, `weak_call` 0.30 to 0.70). Mirror's blend is 0.6/0.4 in `agents/mirror.py`, not 0.5/0.5. The Predator row matches no table. Check every row |
| 11 | Wall has about 9.4 rebuys per seed in Phase 1 | `reports/phase2_scorecard_long.txt`: 29 +/- 5; 9.4 is the Phase 3 value |
| 12 | Oracle plays an approximately game-theoretically optimal mix | Its table is hand-set (bluff rate 0.33 on every street) |
| 13 | Honesty scores | `archetype_params.HONESTY_SCORES` is what the trust score uses. `analysis/compute_metrics.HONESTY` and the README table carry different values for Oracle, Mirror and Judge; that dict is never read, so no published number depends on it. Remove the confusion |
| 14 | "Walkover" as a poker term | It is the engine's label |
| 15 | LLM agents receive a personality description | It includes Phase 1 outcome statistics, trust scores and identifiability results |
| 16 | LLM agents infer opponents from play | Prompt lines read `Seat N (archetype): action` for opponents who have acted in the current round, and the reasoning-format example names an archetype |
| 17 | The trust model is the same instrument in every phase | True, but its likelihood tables describe the rule-based policies; in LLM phases it measures resemblance to those policies |
| 18 | The Judge is one of eight types | The type list has only the cooperative Judge |
| 19 | Phase 1 fold-equity and showdown figures (87.1%, 38.5%) come from the described 5 x 10,000 runs | They come from the 20 x 25,000 dataset |
| 20 | Supplementary Table S4, Phase 1 columns | Hand-typed in `analysis/make_paper_figures.py`; several rows match no dataset (for example Sentinel's aggression factor) |
| 21 | Mirror finishes sixth of eight in Phase 1 | The scorecard ranks it fourth |
| 22 | Side pots protect an all-in player | An all-in seat is auto-folded when anyone bets later (`engine/game.py`) |
| 23 | Only the agent's mind changes between phases | Phase 2 also removes Predator's exploit table and Mirror's copying (`phase2/adaptive/adaptive_agent.py`) |
| 24 | Phase 3 agents have no memory across hands | The LLM Judge keeps a persistent grievance ledger and gets a retaliation instruction |
| 25 | The hill-climber searches 36 dimensions | The four `strong_fold` entries are read by no code |
| 26 | The no-CoT arm "retains notes" | Its notes call runs under the one-word-answer system prompt; check whether any note was ever parsed |
| 27 | All databases are available at the anonymous link | See section 1: several are not in the repo |
| 28 | Posterior updated once per observed action | At showdown each action of a revealed player is applied a second time with the known bucket, on top of the live update. The paper does not mention refinement |
| 29 | Preflop "bets" | The engine logs a big-blind option bet as a raise; no preflop bet row exists |
| 30 | The scaffold called chain-of-thought | It bundles a larger token budget, an instruction to weigh opponent reads, a statement that notes will be supplied, and a worked example that names an archetype |

**Done when** every row has a verdict and a fix, and rows are added for
anything else found.

#### B4. Does anyone actually use reputation? (existing data)

**Do** From the action logs (with B0's buckets) of Phase 1, Phase 3 and
Phase 3.1 n=20: for each observer, the rates of fold, call and raise when
facing a bet, split by who bet. A raw split is biased: fixed seating and hand
selection make even static agents look as if they discriminate. Stratify by
street, by the responder's own bucket and by whether the responder had already
checked, and use a run with all reading off as the null distribution.

**Done when** `PRIV/reports/B4_reputation_use.md` says, per phase, which
agents treat bettors differently beyond the null, and by how much.

#### B5. Audit and correct the trust instrument

**Do**

1. Needs one new instrumented run with all reading off. Measure, per
   archetype, street and situation (bet pending or not), the actual action
   frequencies, and compare with the model's marginal likelihoods.
2. Add a flagged likelihood variant built from those measured frequencies
   (`--trust-model empirical`). Bucket priors pooled by street are not enough:
   who reaches a street with what depends on the archetype.
3. Add a flagged variant in which showdown refinement and the Judge use the
   revealed player's **decision-time bucket** (logged, or from B0) instead of
   `_fast_bucket`, and in which refinement replaces the live update for those
   actions instead of adding to it. Do not call `get_hand_strength` in the
   refinement path (`CLAUDE.md`).
4. Add `analysis/replay_trust.py`: recompute trust offline from an augmented
   database under any variant. In LLM runs trust never feeds back into play,
   so this needs no API calls.
5. Report classification accuracy and trust per archetype under each variant.

**Done when** `PRIV/reports/B5_trust_instrument.md` exists, the default
configuration is bit-identical to today's behaviour, and `replay_trust.py`
reproduces the logged snapshots under the submitted model.

### Phase C. New rule-based experiments (free)

#### C0. Analysis plan. GATE G1

**Do** Write `PRIV/ANALYSIS_PLAN.md` before any full run. It must fix:

1. **The reading mechanism.** Compare at least these on a 2-seed, 3,000-hand
   pilot and recommend one as primary:
   * M1, the pilot version (Appendix B), with its known flaws;
   * M2, the same scaling applied only to Medium and Weak hands, with the
     factor bounded;
   * M3, a pot-odds rule: with a bluff-catching hand, continue when the
     believed probability that the bet is a bluff exceeds
     `cost / (pot + cost)`, mixed with the table policy by one strength
     parameter.
   Criteria: never makes a Strong hand fold more; one parameter leads back to
   "all reading off"; the share of decisions it touches is reported; it can be
   stated in two sentences.
2. **One reputation variable**, used both inside the mechanism and in the
   trust-profit association. Candidates: the believed probability that a bet
   is a bluff, or the R0 trust score. Report the other as secondary.
3. **Primary quantity:** the cost of being read, per archetype (section 2).
   Secondary: win rates when everyone reads everyone; the bluff-rate sweep;
   the association per condition as a slope with an interval, with Pearson and
   Spearman r for continuity. State that a correlation over eight designed
   archetypes describes that design and nothing wider.
4. **Controls and what each rules out** (the table in C1).
5. **Seating:** seats permuted per seed, derived from the seed, in every new
   condition.
6. **Sample sizes** from a power calculation on pilot variance, a fixed list
   of conditions and seeds (prefixes of the frozen 20 in
   `phase3/run_phase31_replication.py`), no peeking, and how the eight
   archetype-level comparisons are handled for multiplicity.
7. The win-rate display unit (do the convention check in E3 first), the trust
   statistic, and which legacy metrics survive (recommendation: showdown and
   non-showdown winnings replace TEI, the B4 measure replaces OA, and CS, NS,
   SU, TMA leave the main text).
8. What each possible outcome would mean for the paper's claim.

**Done when** the plan is committed and the author has approved it (G1).

#### C1. One harness for all rule-based conditions

**Do** Add `revision_experiments/run_rule_based.py` and one small config file
per condition. Options: `--condition`, `--seeds`, `--hands`,
`--starting-stack`, `--seat-order fixed|permuted`, `--trust-model`,
`--log-mode full|lean`, `--out`.

| Condition | Definition | What it is for |
|---|---|---|
| `published` | Published roster, legacy settings | Continuity with R0 |
| `no_read` | Predator always plays its baseline table, Mirror its default table, Judge never triggers | Layer 1 |
| `published_predator_off` | Published roster with only Predator's exploit switch off | Size of the one posterior-reading channel that R0 contains |
| `read_target_X_inferred` | `no_read` plus the mechanism, applied only when the bettor is archetype X, using each observer's posterior. One condition per X | Cost of being read, as inferred |
| `read_target_X_true` | Same, with responders knowing X's true type | Cost of being perfectly legible |
| `read_all_inferred` at three strengths, `read_all_true` | Mechanism applied to every bettor | The table when everyone reads everyone |
| `loose_matched` | No reading; every call probability scaled by the realised mean factor of the matching `read_all` condition | Rules out "the table simply calls more" |
| `shuffled` | The mechanism reads the reputation of a random other seat, redrawn each hand from a separate random stream | Rules out effects that need no correct attribution |
| `noise_005`, `noise_010` | `no_read`, with each decision replaced by a random legal action with probability 0.05 or 0.10 | Tests R1-M8: does noise alone weaken the correlation |
| `potodds_no_read` | No reading; bluff-catching hands call by pot odds against the population-average bluff frequency | Separates "opponents fold too much" from "opponents ignore reputation" |
| `sweep_no_read_brXX`, `sweep_read_brXX` | One focal seat plays the Oracle table with bluff rate XX on every street (0.00, 0.10, 0.20, 0.33, 0.50, 0.65, 0.80). Others either do not read, or read the focal seat only. The focal seat itself never reads | Profit against own bluff rate, with and without being read |
| `legacy_stack` | `no_read` with 200 chips and rebuys | Size of the stack and all-in effects |
| `hill_bounded`, `hill_unbounded` | The bounded and the "aggressive" unbounded hill-climbers under the new protocol | Compare with `no_read`, which is their true baseline (B3 row 23) |

Defaults for new conditions: starting stack 100,000 chips, so no seat can go
broke, no all-in and no side pot occurs (R1-M5, B3 row 22); permuted seats;
the trust model from Q7.

Logging for big runs (lean): one row per hand and seat (net chips, reached
showdown, bucket per street), fold/call/raise counts by observer, bettor,
street and responder bucket, trust snapshots every 100 hands, board and hole
cards, and full action logs for the first 1,000 hands of each seed.

**Done when**

* `published` reproduces `phase1/run_sim.py` exactly for seed 42 over 300 hands;
* every mechanism at strength zero is bit-identical to `no_read`;
* chips are conserved everywhere, and with 100,000 chips there are no rebuys
  and no all-ins;
* every condition completes a 2-seed, 200-hand smoke run.

#### C2. Pilot on Actions

**Do** Run 2 seeds x 3,000 hands for every condition. Measure hands per second
on the runner. Reproduce Appendix C.2 with its exact settings (seeds
42,137,256; 200-chip stacks; fixed seats; submitted trust model).

**Done when** the pilot report is in `PRIV/reports/`, C.2 is reproduced, and
job chunks are sized to end within 300 minutes.

#### C3. Full runs

**Do** After G1, run exactly the conditions, seeds and hand counts in the
analysis plan. Upload databases to Release `data-r1`; commit per-condition
summary JSON to the run branch.

**Done when** every planned run is present and valid, and no run was repeated
or dropped after its results were seen. A run that fails for a technical
reason is rerun and logged.

#### C4. Rule-based results

**Do** Generate from data only:

* Figure: win rate per archetype under `published` and `no_read`.
* Figure: cost of being read per archetype, inferred and true, with intervals
  and the controls alongside.
* Figure: win rate against own bluff rate, read and not read.
* Figure: showdown and non-showdown winnings per archetype and condition
  (this is the plot R2-RC1 asks for, in the reviewers' own terms).
* Figure: running win-rate estimate and interval against hands played (R1-W2).
* Table: the association per condition.
* `PRIV/reports/C4_results.md`: what each planned contrast shows, in the order
  of the plan, including every result that goes against R0.

**Done when** all exhibits build from one command and the report covers every
contrast in the plan.

### Phase D. Language-model experiment (costs money)

#### D1. Protocol v2 and the design. GATE G2

**Do**

1. **Prompts.** Create `phase3/prompts_v2/`: one prompt-only file per
   archetype, all in the same fixed template (style in one line; tendencies
   before the flop; tendencies after; response to bets), filled from
   `archetype_params.py`. No outcomes, no trust scores, no mention of the
   simulation, of phases or of other archetypes. Do not reuse the old loader's
   "everything before the Quantitative Targets heading" rule. Add a test that
   every rendered system and user prompt contains no banned term and no
   archetype name other than the agent's own.
2. **Opponents by seat number only** in every prompt line and in the format
   example.
3. **Reasoning as one thing.** If reasoning is a factor, the two levels must
   differ only in being asked to reason before answering. Same instructions
   otherwise, a neutral example, and report the token budgets.
4. **Stack:** 100,000 chips, as in the rule-based runs. The R0 decision
   prompt prints the player's running stack (`Your stack:`), which carries the
   result of earlier hands into every arm, with or without memory. Under
   protocol v2 remove that line, or keep it in every arm and list it in the
   fact sheet. Say which in the G2 summary.
5. **Logging:** board, hole cards, the hand-strength hint, the full prompt and
   full reply of every call, token counts.
6. **Failures:** abort a seed on the first API error that survives the SDK's
   retries (it is resumable). Retry an unparseable reply once. A seed with
   more than 1% unparseable replies is invalid and rerun.
7. **Caps:** a cap per job and a total cap, both checked before each seed
   starts. Order the matrix by seed block (seed 1 of every arm, then seed 2),
   so that running out of money leaves whole blocks, never whole arms missing.
8. **Designs** (the author chooses at G2; details and costs in Appendix D):
   * Design R: reasoning off or on, crossed with reputation hidden or shown
     (a per-opponent reputation line from the same trust instrument). Four
     arms. Tests the paper's own question in language-model agents. Memory and
     notes leave the paper's claims.
   * Design F: all eight on-off combinations of reasoning, memory and notes.
     Tests which scaffold matters. The notes call must see the last 25 hands
     and real showdown results, and must work without reasoning.
9. Dry-run every arm with the mock client.

**Done when** the dry run and prompt tests pass, and the author has answered
Q4, approved the prompts, topped up credit and confirmed the caps (G2).

#### D2. Run

**Do** First a 30-hand live run per arm (a few dollars in total): confirm from
the logged prompts that each factor is really on or off. Then push the full
matrix. Seeds of 500 hands. At most 10 jobs at once. Rerun invalid seeds.
Upload databases and call logs to `data-r1`. Record actual spend from tokens.

**Done when** every arm has its planned number of valid seeds.

#### D3. Outcomes

**Do** Run `winrate.py` and `replay_trust.py` on every arm and on the R0 LLM
datasets (Phase 3, Phase 3.1 n=20, no-cot, and the five-seed run if found).

**Done when** per-arm outcome files exist and reconcile.

#### D4. LLM results

**Do** Generate: a figure of win rate per archetype by arm; a table of each
factor's main effect and interaction with intervals; the B4 measure per arm;
from the logged reasoning, the share of decisions that refer to a specific
opponent's past behaviour, by a keyword rule fixed before looking at outcomes,
with 20 random examples; R0 data beside R1 data as a comparison across
protocols, labelled as such. Write `PRIV/reports/D4_results.md`, including the
minimum effect this sample could have detected.

**Done when** all exhibits build from one command and the report states what
the sample can and cannot show.

### Phase E. Manuscript support (the author writes)

#### E1. Build system

**Do** In `PRIV/paper/`, IEEEtran:

* `numbers.tex`, generated: one macro per result (H5).
* Tables and figures generated into `generated/`, using
  `display_names.json`.
* Typesetting: IEEEtran BST control entry with repeated-name dashes off
  (R2-CIT1); link, citation and URL colours black (R2-BD2, R2-C1).
* `make paper` builds main and supplement and prints the page count.
  `make diff` builds a tracked-changes PDF against `paper_r0/`; if latexdiff
  cannot cope with the restructuring, build a version with all new text
  coloured.

**Done when** a skeleton with every generated exhibit and no prose compiles
with zero undefined references.

#### E2. Methods fact sheet and supplement exhibits

**Do** Write `PRIV/briefs/methods_facts.md`: facts with file and line
references, as bullets, not paragraphs. Generate for the supplement, as
tables, formulas, pseudocode and listings (no sentences, H1): the per-street
parameter table of every archetype from `archetype_params.py`; the Predator
exploit table; the decision rule; the bucket definition; the formulas that
define a bluff, a value bet and the reputation variable; the trust update with
every constant; the reading mechanism; the exact prompts of protocol v1 and
v2; a run table (phase, model id, temperature, seeds, hands, calls, cost); two
illustrative hands chosen by a stated rule, with full board and equity on
every street.

**Done when** each of R1-W1, R1-M6, R1-M7, R2-MC1 has fact-sheet entries with
file and line references.

#### E3. Bibliography

**Do** Verify all 34 existing entries. Find and verify candidates for: the
origin of the Prisoner's Dilemma and the iterated tournaments; what the
Fudenberg-Levine and Mailath-Samuelson works actually show, in one line each;
the provenance of the noise floor and of the tempering step in the trust
update; the hand-evaluator library and Monte Carlo equity estimation; the
win-rate convention in the limit hold'em literature (needed by C0, so do this
part early); CMA-ES and REINFORCE in case that sentence stays.

**Done when** `PRIV/reports/E3_citation_log.md` lists every entry with the URL
checked, and the author has a one-line-per-paper list to choose from.

#### E4. Results summary. GATE G3

**Do** Write `PRIV/briefs/results_summary.md`: one page, plain language, what
each layer found, what in R0 is confirmed, weakened or overturned, and what
was unexpected (R2-DC1). Facts and numbers, no draft sentences for the paper.

**Done when** the author has fixed the main claim and the title and answered
Q2, Q3, Q5, Q6 (G3).

#### E5. Outlines

**Do** One outline per section, supplement included, in `PRIV/briefs/`:
purpose in one line; the points to make, as bullets of facts; the macros,
figures and tables to cite; the comment IDs to satisfy; a word budget that
fits Q6; a "do not" list from the register. No sentences meant for the paper.

**Done when** every section has an outline and every W-type comment ID appears
in exactly one outline.

#### E6. The author writes

The author writes every section, including the supplement's text, in
`PRIV/paper/sections/` or anywhere he prefers. Suggested order: Methods,
Results, Introduction, Background, Discussion and Limitations, Conclusion,
Abstract. You answer factual questions about the data and the code. If the
text is written elsewhere, port it into LaTeX without changing a word (macro
substitution per H5 excepted) and show a diff of the port.

**Done when** every section of the main text and the supplement is in
`PRIV/paper/sections/`, each port diff shows no changed word, and the author
has said the draft is ready for the full check pass.

#### E7. Check pass, after each section

**Do** Report, do not rewrite: results typed instead of macros; claims with no
supporting exhibit; terms used before they are defined; names that bypass the
mapping file; ordinal words without antecedents; interpretation inside
Results; open comment IDs for the section; word count against budget; every
sentence that survives unchanged from R0. If asked "how should I say this",
say what is unclear and why, not a replacement sentence.

**Done when** `PRIV/reports/E7_<section>.md` is a numbered issue list with
line references and the author has replied to each item.

#### E8. AI-use inventory

**Do** From both repos' histories and `STATUS.md`, list every part of the work
an AI system produced, drafted or proposed: code; experiment runs; figures and
tables; prompts; earlier manuscript drafts and reworded passages (the commit
log of May to August 2026 records these); and, for this revision, the
experimental design in section 2, the analysis plan, the outlines and the
checks. Give dates and commit ranges.

**Done when** the inventory is in `PRIV/reports/`, the author has written the
acknowledgment from it, and you have listed anything his statement omits.

### Phase F. Response and submission

#### F1. Response tracker

**Do** `PRIV/response_tracker.md`: one row per comment ID with status, what
changed, where in R1 (section, page, line), and the supporting exhibit or
report. No reviewer text, no reply prose.

**Done when** every ID in section 3 has a row.

#### F2. Build and gate the package

**Do** Build the clean PDF, the tracked-changes PDF, the supplement, a source
zip with only what the main document needs, a plain-text abstract for the
portal, and a new title page if the title changed. Compile the source zip in
an empty directory using only its own files. Strip author and time-zone
metadata from the PDFs. Then run every gate.

| Gate | Pass condition |
|---|---|
| Build | Zero errors and zero undefined references, main and supplement |
| Pages | Main within the Q6 limit, references included |
| Numbers | No result in the prose that does not come from a macro |
| Anonymity | Zero hits in sources, PDFs and PDF metadata for the author's name, school, city, email, GitHub handle, mentoring programme and earlier venues |
| Stale strings (whitespace-insensitive) | Zero hits for `walkover`, `cheat`, `never folds`, `game-theoretic optimal`, `intentionally unsettling`, `Here is the breaking point`, `Both are standard`, `could not have been possible`, `no chance to win`, `cannot resolve it`, `quota` |
| Abstract | Every experiment or scaffold named in the abstract has a completed result in the paper (R1-W4) |
| Pointers | Every supplementary reference resolves to the right float |
| Register | Every comment ID is closed or has a stated reason in the tracker |

**Done when** all gates pass on the exact files to be uploaded.

#### F3. Clean code copy for reviewers

**Do** Build branch `review-artifact` in `PUB` with only what a reviewer needs
to rerun the work: engine, agents, trust model, harness, analysis, prompts, and
a data manifest that points to an anonymous host, not to Releases under the
author's handle. Exclude manuscript folders, notes, title-page files,
`CLAUDE.md` and earlier-venue folders. Propose an anonymous data host to the
author. Run the anonymity gate on the branch.

**Done when** the gate passes and the author has pointed the anonymous link at
the branch and checked its expiry.

#### F4. GATE G4

The author reads the package, writes the cover letter and the response letter
from the tracker, and uploads. Your last act is to rerun all F2 gates on the
uploaded files.

**Done when** every F2 gate passes on the uploaded files and the result is the
last entry in `PRIV/STATUS.md`.

---

## 6. Calendar

| Dates | Claude Code | Author |
|---|---|---|
| 12 to 18 Oct | A1, A2, A3, B0, B1 | A0 |
| 19 to 25 Oct | B2, B3, B4, B5, C0, C1 | G1 (about 30 minutes) |
| 26 Oct to 1 Nov | C2, C3, D1, E3 | Applications. G2 when free (about 20 minutes) |
| 2 to 8 Nov | C4, D2, D3, D4, E1, E2, E4 | G3 (one to two hours) |
| 9 to 29 Nov | E5 in the first two days, then E7 after each section | E6: write the paper |
| 30 Nov to 6 Dec | E7 on the full draft, E8, F1 | Mentor read; acknowledgment; response letter draft |
| 7 to 12 Dec | F2, F3 | G4; upload by 12 Dec |

If C3 is not finished by 8 Nov, or the draft is under half written by 20 Nov,
tell the author to write to the editor-in-chief about an extension before
25 Nov.

---

## Appendix A. Reference code: the ledger

Checked on pilot data: every hand sums to zero and totals match the stack
ledger, except hands where the big blind had a single chip, which the
big-blind rule below handles.

```python
def per_hand_net(conn, run_id, n_seats=8):
    cur = conn.cursor()
    hands = cur.execute(
        "SELECT hand_id, final_pot, had_showdown, walkover_winner, sb_seat, bb_seat "
        "FROM hands WHERE run_id=? ORDER BY hand_id", (run_id,)).fetchall()
    idx = {h[0]: i for i, h in enumerate(hands)}
    net = np.zeros((len(hands), n_seats))
    put_in = np.zeros(len(hands))
    for hid, seat, amt in cur.execute(
            "SELECT hand_id, seat, SUM(amount) FROM actions WHERE run_id=? "
            "AND action_type IN ('call','bet','raise') GROUP BY hand_id, seat", (run_id,)):
        net[idx[hid], seat] -= amt
        put_in[idx[hid]] += amt
    for hid, pot, had_sd, winner, sb, bb in hands:
        net[idx[hid], sb] -= 1                           # blinds are not in the actions table
        net[idx[hid], bb] -= pot - put_in[idx[hid]] - 1  # 2, or 1 for a one-chip stack
        if not had_sd and winner is not None:
            net[idx[hid], winner] += pot
    for hid, seat, won in cur.execute(
            "SELECT hand_id, seat, pot_won FROM showdowns WHERE run_id=?", (run_id,)):
        net[idx[hid], seat] += won
    return net
# A player "reached showdown" in a hand if it has a row in `showdowns` for that hand.
```

## Appendix B. The pilot reading mechanism (M1). A proof of concept, not the design

```python
from trust import bayesian_model as bm
K = bm._KNOWN_L                              # [street, bucket, action, type]
P_WEAK = K[:, 2, :, :] / K.sum(axis=1)       # P(Weak | action, street, type), equal bucket weights
Q_BAR = P_WEAK @ np.full(K.shape[-1], 1.0 / K.shape[-1])

def faced_opening_bet(game_state, me):
    for rec in reversed(game_state.actions_this_round or []):
        if rec.seat == me:
            continue
        if rec.action_type == ActionType.RAISE:
            return None
        if rec.action_type == ActionType.BET:
            return rec
    return None

# inside decide_action, facing a bet, after raise_p and call_p are read from the table:
rec = faced_opening_bet(game_state, self.seat)
post = self.posteriors.get(rec.seat) if rec is not None else None
if beta and post is not None:
    r = bm._ROUND_IDX[rec.betting_round]; a = bm._ACTION_IDX[rec.action_type.value]
    q, qbar = float(P_WEAK[r, a] @ post), float(Q_BAR[r, a])
    call_p = min(max(call_p * (1.0 + beta * (q - qbar) / qbar), 0.0), 1.0 - raise_p)
# then the existing single roll: raise if roll < raise_p, call if roll < raise_p + call_p, else fold
```

It can be added as a subclass without touching `base_agent.py`, draws no extra
random numbers, and at strength 0 reproduces the base roster bit for bit.

Measured behaviour (seed 137, 2,000 hands, on the published roster), which is
why C0 must choose something better:

| Property | Strength 1 | Strength 2 |
|---|---|---|
| Share of facing-a-bet decisions it touches | 22%, none preflop | 22% |
| Mean factor on call probability | 1.34 | 1.71 |
| Mean factor by bettor | Firestorm 1.78, Phantom 1.63, Oracle 1.24, Predator 1.03, Judge 0.98, Mirror 0.95, Sentinel 0.94, Wall 0.38 | Firestorm 2.55, Wall below zero (clamped) |
| Strong hands folded when the factor is 0.6 or less | 37% | 50% |
| Fold rate against Wall's bets, against Firestorm's | 71%, 23% | 87%, 15% |

## Appendix C. Numbers to cross-check against

**C.1 Canonical Phase 3.1, n=20, recomputed from
`paper_resources/data/phase31_n20_stats.json`** (net = final stack minus
200 x (1 + rebuys); 150 hands per seed; win rate shown in big blinds of 2
chips per 100 hands).

| Statistic | Value |
|---|---|
| Mean per-seed r, trust versus final stack | +0.062, population SD 0.378, 95% t-interval -0.119 to +0.244 (as in R0) |
| Mean per-seed r, trust versus net winnings | +0.037, population SD 0.401, 95% t-interval -0.156 to +0.229 |
| Seeds with positive r | 10 of 20 with final stack, 9 of 20 with net winnings |

| Archetype | Mean trust | Net chips per seed | Win rate (SE across seeds) | Showdowns per seed |
|---|---|---|---|---|
| mirror | 0.748 | +80.4 | +26.8 (6.2) | 8.2 |
| sentinel | 0.759 | +34.1 | +11.4 (7.3) | 6.1 |
| oracle | 0.618 | +28.4 | +9.4 (9.6) | 17.8 |
| predator | 0.770 | +24.8 | +8.3 (9.3) | 8.2 |
| phantom | 0.631 | +16.2 | +5.4 (7.6) | 12.3 |
| judge | 0.760 | +3.2 | +1.1 (6.1) | 7.0 |
| firestorm | 0.449 | -83.9 | -28.0 (9.9) | 27.4 |
| wall | 0.937 | -103.1 | -34.4 (11.0) | 43.4 |

These standard errors imply a per-hand spread of 3.4 to 6.0 big blinds in
language-model play.

**C.2 Pilot, published roster against all reading off.** Seeds 42, 137, 256;
3,000 hands each; 200-chip stacks with rebuys; fixed seats; submitted trust
model. Small sample: a sanity check only.

| Condition | r, trust versus final stack, per seed | Mean | r, trust versus net winnings, per seed | Mean |
|---|---|---|---|---|
| published | -0.61, -0.90, -0.68 | -0.73 | -0.39, -0.89, -0.72 | -0.67 |
| all reading off | -0.66, -0.84, -0.78 | -0.76 | -0.29, -0.85, -0.57 | -0.57 |

Win rate in big blinds per 100 hands, published then reading off: firestorm
+39.3, +28.6; sentinel +7.3, +1.0; judge +5.8, +4.2; oracle +5.2, +9.1; mirror
+2.5, +3.6; predator -2.4, +4.8; phantom -23.8, -23.8; wall -33.9, -27.5.
Published roster, chips per 3,000 hands, player-level split: Firestorm
showdown -58, non-showdown +2,417; Wall showdown +950, non-showdown -2,985.
Wall averaged 10 rebuys per 3,000 hands. Per-hand standard deviation of net
chips: 5.7 to 10.3.

**C.3 Pilot of mechanism M1 on the published roster**, same seeds and
settings. Read with Appendix B's caveats.

| Strength | r, trust versus final stack, per seed | Mean | Firestorm win rate | Firestorm showdown, non-showdown chips | Wall win rate |
|---|---|---|---|---|---|
| 0 | -0.61, -0.90, -0.68 | -0.73 | +39.3 | -58, +2,417 | -33.9 |
| 1 | -0.82, -0.42, +0.29 | -0.32 | +12.7 | +603, +156 | -19.2 |
| 2 | -0.44, +0.31, +0.24 | +0.04 | +9.2 | +1,263, -713 | -28.7 |

**C.4 Trust-model check: probability of folding to a preflop bet.** Model
(equal bucket weights) then policy-implied (true preflop bucket shares 3.3%,
10.9%, 85.8%): sentinel 0.50, 0.83; wall 0.23, 0.41; firestorm 0.22, 0.52.

## Appendix D. The LLM experiment: designs, cost, precision

Rates measured in the published runs and encoded in
`.github/workflows/experiments.yml`: about USD 0.0226 per hand in arms with
reasoning (15.9 calls at 0.001422) and USD 0.0133 per hand without (17.6 calls
at 0.000753). In both designs half the arms use reasoning, so a hand costs
about USD 0.018 on average. Add about 10% for smoke tests and reruns. These are
estimates from past runs; the first seed's token log gives the real rate.

| Option | Design | Hands in total | Estimated cost | SE of one factor's effect on an archetype's win rate | Smallest effect detectable (80% power) |
|---|---|---|---|---|---|
| None | No new LLM runs. R0 data re-analysed, confounds stated, scaffold claims removed from abstract and conclusions | 0 | 0 | n/a | n/a |
| R-small | Design R: 4 arms x 5 seeds x 500 hands | 10,000 | about USD 180 | 7 to 12 | 19 to 34 |
| R-large | Design R: 4 arms x 10 seeds x 500 hands | 20,000 | about USD 360 | 5 to 8.5 | 13 to 24 |
| F-small | Design F: 8 arms x 5 seeds x 300 hands | 12,000 | about USD 215 | 6 to 11 | 17 to 31 |
| F-large | Design F: 8 arms x 5 seeds x 500 hands | 20,000 | about USD 360 | 5 to 8.5 | 13 to 24 |

Effects are in big blinds per 100 hands. Precision compares the half of the
arms with a factor against the half without, using the per-hand spread of 3.4
to 6.0 big blinds seen in R0 language-model play (Appendix C.1). For scale:
the largest gaps between archetypes in R0 Phase 3.1 are about 60. A 500-hand
seed with reasoning takes about 4.6 hours, inside the job limit.

No affordable LLM sample meets a poker standard of evidence. That is why
Layers 1 and 2 carry the paper and Layer 3 is framed as exploratory.
