# NEEDED_FROM_AUTHOR.md

Everything Claude Code needs from Rachit to finish revision R1, in the order
it is needed. Written 21 Oct 2026 from `REVISION_RUNBOOK.md`, `DECISIONS.md`,
and the current state of both repositories.

**How to answer.** Fastest: reply in chat using the IDs (for example
"N2: main, expires 3 Jan, no names visible"). The answers go into
`DECISIONS.md` with the date. Anything you leave unanswered gets the
runbook's default where one exists; where none exists, the step waits.

Private file: it refers to the reviews by comment ID (H8). Do not copy it
into `Poker_trust`.

---

## 0. Where things stand (21 Oct)

| Step | State |
|---|---|
| A1 Branch, freeze, project memory | Done. R0 rebuilds to the submitted PDFs exactly (10 pages, 34 references) |
| A2 Rescue the raw data | Done. Release `data-r0` holds the n=20 and ablation databases, checked twice |
| A3 Reproduce rule-based baselines | Runs done (17 Oct, another session); **the written report `reports/A3_reproduction.md` is still owed** |
| B1 Win-rate ledger | Done (code + 15 tests; every database reconciles exactly) |
| B2 Net-winnings headlines | Numbers done and match Appendix C.1; **report `reports/B2_metric_change.md` still owed**; the 20 x 25,000 LFS Phase 1 dataset not yet included |
| B0, B3, B4, B5, C0 to F4 | Not started |

Against the calendar in the runbook we are about four days behind: B0 was
due by 18 Oct, and B3 to C1 plus G1 by 25 Oct. Realistic G1 date is now
about 28 Oct if the items in section 1 come back this week.

**One finding you should know about now** (it creates question N8 below).
The published rule-based numbers reproduce only with the code as it was
*before* commit `57cca9a` (22 May 2026), which fixed side-pot accounting
in `engine/game.py` (and changed `agents/mirror.py`). Rerun at `7ab1996`,
all 20 published per-seed r values match to three decimals. Rerun with
today's code, none do:

| Dataset | Published mean r | Today's code, mean r | Largest per-seed gap |
|---|---|---|---|
| Phase 1 | -0.752 | -0.673 | 0.571 |
| Phase 2 bounded | -0.637 | -0.817 | 0.403 |
| Unbounded, aggressive | -0.609 | -0.753 | 0.491 |
| Unbounded, weak | -0.779 | -0.753 | 0.197 |

The same split runs through the LLM data: Phase 3 (`runs_phase3_long`,
run 30 Apr 2026) predates the fix; Phase 3.1 n=20 (3 Aug, code `92e1b64`)
includes it. So the submitted r ladder compares phases run on two
different engines. The 22 May commit message itself says the old
scorecards "no longer reproduce".

---

## 1. Needed this week (blocking or time-sensitive)

### N1. Reviewer 3 attachment (R3-1)

Log in to the portal and check whether Reviewer 3 left an attachment.
If yes: describe each point **in your own words** (one line each) so I can
add rows `R3-1`, `R3-2`, ... to the register. The runbook says this comes
before any other step, so it is already late. If there is no attachment,
just say "none".

### N2. The anonymous code link

The reviewers' link points at the public repository. I need:

* **Which branch it shows.** H11 depends on this: nothing may be merged or
  pushed to that branch until F3. Note that pull request
  `RachitAgrawal146/Poker_trust#9` (review branch into `main`) is still
  open; **do not merge it** until you know the answer.
* **Expiry date**, and whether it can be extended.
* **Whether your name, school, email or GitHub handle appear anywhere** on
  it (a quick look in a private browser window).
* **Which service hosts it** (for example anonymous.4open.science), so I can
  plan the F3 switch to a clean `review-artifact` branch.

### N3. Exact due date and upload slots

The decision of 17 Sep plus 90 days gives **16 Dec 2026**. Confirm the date
the portal shows, and list the upload slots it offers (main PDF,
tracked-changes PDF, supplement, source files, response letter, cover
letter, ...). F2 builds exactly one file per slot.

### N4. The missing databases

Search your own machines and drives for:

* `runs_phase1_long.sqlite`
* `runs_phase2_long.sqlite`
* `runs_phase2_unbounded.sqlite`, `runs_phase2_unbounded_aggressive.sqlite`
* `runs_phase31_long.sqlite` (the five-seed temperature-1.0 Phase 3.1 run
  behind r = -0.094)

The four rule-based ones are now less urgent: the pre-`57cca9a` rerun
reproduces them exactly. **`runs_phase31_long.sqlite` cannot be regenerated**
(temperature 1.0, not deterministic). If you find it, tell me; it goes into
Release `data-r0`. If you don't, R1 stops citing r = -0.094, the
"temperature-matched" comparison and the boxed illustrative hand that come from it.

### N5. Session setup

* **Attach both repositories to every session.** The 17 Oct session worked
  only on `Poker_trust`, so the A3 and B2 reports and its `STATUS.md`
  entries never reached this repository.
* **Merge my pull requests before the next step** (H9). A pull request
  will follow this file.
* Expect to be asked to approve: pushes to branches other than the
  session's own, and anything that publishes (Releases `data-r1`, the F3
  branch). If the prompts get in the way, you can add a permission rule;
  otherwise answer them as they come.

### N6. Earlier public versions and the anonymity gate

F2 and F3 search every file, PDF and PDF metadata for identifying strings.
Send me the exact list:

* your name as it appears anywhere (all variants), school, city, email
  addresses, GitHub handle;
* the mentoring programme (Polygence appears in the repo) and your
  mentor's name;
* every earlier venue or posting: was the paper **posted on arXiv** (the
  `arxiv_build/` bundle and its TODO suggest an arXiv submission was
  prepared)? Submitted to TMLR or JEI? If it is publicly posted under your
  name, tell me the identifier; check whether IEEE ToG's double-anonymous
  policy requires anything (for example not citing it, or noting it to the
  editor).

### N7. AI use outside these repositories (for E8 and ED-4, AE-2, R2-I1, R2-C2)

I can list everything in the two git histories. I cannot see what happened
elsewhere. List every AI tool you used outside these repos for this paper,
what for, and roughly when: chat assistants for drafting or paraphrasing
(the arXiv TODO speaks of a "final paraphrased manuscript"), grammar tools,
translation, figure tools. A short list is enough; the acknowledgment must
name the system, the sections and the level of use.

---

## 2. Decisions (record in `DECISIONS.md`)

Each row: what the question changes, the runbook default, my
recommendation, and when it is needed.

| ID | Question | Default | My recommendation | Needed by |
|---|---|---|---|---|
| Q1 | Use the three-layer design (style only; reading switched on in a controlled way; language models) as the paper's spine | Adopt | Adopt. It answers R1-W3 directly and works whichever way the results go | G1, ~28 Oct |
| Q7 | Trust model for the new runs: the submitted one, or the corrected one from B5 | Decide at G1 with the B5 report | Wait for the B5 report; I will bring a recommendation to G1 | G1 |
| **N8 (new)** | **Which engine the R1 runs use**, given the 57cca9a finding in section 0 | none | **Today's (fixed) engine for every new run**, and run the continuity condition `published` on both engines so the size of the change is reported. Do not run new experiments on a version with a known side-pot bug. The paper must say which engine produced which dataset | G1 |
| Q4 | Language-model experiment: which design and budget (Appendix D) | No LLM runs | See section 3 | G2, ~1 Nov |
| Q2 | Display names: standard poker terms for archetypes; descriptive phase names instead of "2\*" and "3.1" | Standard terms in the paper; code names unchanged | Default. The mapping already exists in `analysis/display_names.json`; you only approve the names | G3, ~8 Nov |
| Q3 | Replace "honesty" with a neutral term (for example "non-bluff rate") | Replace | Replace. It is what the number measures | G3 |
| Q5 | Hill-climbing phases in the main text or the supplement | Supplement | Supplement. They lean on the engine question above and on B3 row 23 | G3 |
| Q6 | Stay within 10 pages, or pay USD 200 per extra page (more than 12 needs justification) | 10 pages | Decide at G3 when the exhibit count is known | G3 |
| N9 | Where you write the text: `paper/sections/` in this repository, or Overleaf (I port it word for word, H1, E6) | none | Either works; tell me before 9 Nov | E1, ~8 Nov |

---

## 3. Money and accounts

### Language-model runs (Q4, gate G2)

Rates from the R0 runs; add about 10% for smoke tests and reruns. No LLM
design meets a poker standard of evidence, which is why this layer is
framed as exploratory.

| Option | What it tests | Hands | Approximate cost incl. 10% |
|---|---|---|---|
| None | Nothing new. R0 LLM data re-analysed; scaffold and ablation claims leave the abstract and conclusions (R1-W4) | 0 | USD 0 |
| R-small | Reasoning off/on x reputation hidden/shown, 4 arms x 5 seeds x 500 hands. The paper's own question in LLM agents | 10,000 | ~USD 200 |
| R-large | Same, 10 seeds | 20,000 | ~USD 400 |
| F-small | All 8 combinations of reasoning, memory, notes; 5 seeds x 300 hands. Completes the ablation the abstract names | 12,000 | ~USD 235 |
| F-large | Same, 500 hands | 20,000 | ~USD 400 |

My recommendation: **R-small**. It tests the question the paper asks,
with prompts cleaned of the problems in section 2 of the runbook (Phase 1
outcomes and opponents' archetype names in the prompts). Choose F only if
you want to keep the scaffold claims; choose None if the budget is not
there, and the scaffold claims go.

At G2 I also need:

* **API credit topped up** to the chosen amount. The last run died when the
  credit ran out.
* **Confirm the GitHub secret `ANTHROPIC_API_KEY`** is still set in
  `Poker_trust` (Settings, Secrets and variables, Actions). I cannot read
  repository secrets from here.
* **Two caps**: a per-job cap and a total cap, in dollars.
* **Your approval of the v2 prompts** (I show them at G2; about 20 minutes).

### Other costs

* **Page charges** if Q6 goes over 10 pages: USD 200 per page.
* **Anonymous data host** for F3: the reviewers' copy cannot point at
  Releases under your GitHub handle. I will propose options at F3; you will
  need to create the account.
* GitHub Actions minutes: free (public repository). Nothing to do.

---

## 4. Your time, gate by gate

| Gate or task | When (adjusted) | What I bring | What you do | Time |
|---|---|---|---|---|
| G1 | ~28 Oct | `ANALYSIS_PLAN.md` (reading mechanism compared on a pilot, the one reputation variable, primary quantity, controls, seeds and sample sizes, what each outcome would mean), the B5 trust-instrument report, N8 | Approve or change the plan; answer Q1, Q7, N8. Nothing in the plan changes after the full runs start (H6) | ~30 min |
| G2 | by ~1 Nov | Protocol v2 prompts, dry-run results, cost table | Answer Q4; approve the prompts; top up credit; confirm the caps and the secret | ~20 min |
| G3 | ~8 Nov | One-page results summary: what each layer found, what in R0 is confirmed, weakened or overturned, what was unexpected | **Fix the paper's main claim and its title**; answer Q2, Q3, Q5, Q6 | 1 to 2 h |
| E6 Writing | 9 to 29 Nov | One outline per section (facts, macros, exhibits, comment IDs, word budget, "do not" list), then a check report after each section | **Write every section**, the supplement text and all captions. Suggested order: Methods, Results, Introduction, Background, Discussion and Limitations, Conclusion, Abstract | most of 3 weeks |
| Mentor read | 30 Nov to 6 Dec | Full draft built, check pass done | **Book your mentor now** for that week | |
| Acknowledgment | 30 Nov to 6 Dec | AI-use inventory (E8), using your N7 list | Write the acknowledgment and AI disclosure | ~30 min |
| Response letter | 30 Nov to 6 Dec | Response tracker: every comment ID, what changed, where (page, line), which exhibit | Write the replies and the cover letter | 2 to 3 h |
| G4 | 7 to 12 Dec | Clean PDF, tracked-changes PDF, supplement, source zip, portal abstract, all F2 gates passed | Final read; point the anonymous link at `review-artifact` and check its expiry; upload; delete redundant files in the portal (ED-3) | 1 to 2 h |

H1 in plain words: I do not write or rewrite any sentence of the paper,
the supplement, captions, acknowledgment, cover letter or response
letter. I produce the numbers, tables, figures, formulas, outlines and
checks, and I port your text into LaTeX without changing a word.

**Extension trigger.** If the full rule-based runs (C3) are not finished by
8 Nov, or the draft is under half written by 20 Nov, write to the
editor-in-chief about an extension before 25 Nov. I will tell you on
those dates.

---

## 5. Also new title page (only if G3 changes the title)

Your name, affiliation as you want it to appear, and contact details for
a new title page. The arXiv TODO noted a mismatch between "Independent
research" on the title page and the school on the form; decide which one
you use and use it everywhere.

---

## 6. Things I will check myself (no action from you)

So you are not surprised later:

* In both the published data and the rerun, **Phase 2 bounded and the weak
  unbounded run give identical results for seed 512** (same final stacks,
  same trust, r = -0.717 in both). Either the weak hill-climber never left
  the bounds in that seed, or a dataset was mislabelled. B3 will settle it.
* `reports/phase31_long_scorecard.txt` still describes the five-seed
  temperature-1.0 Phase 3.1 run. B3 row.
* The A3 and B2 written reports and their `STATUS.md` entries, owed by
  the 17 Oct session; the next session writes them first.

---

## Reply template

```
N1 R3 attachment: none / yes, points: ...
N2 anon link: branch ..., expires ..., host ..., identifying info visible: yes/no
N3 due date: ...; upload slots: ...
N4 databases found: ...
N5 noted
N6 identifying strings: ...; arXiv: posted yes/no (id ...); other venues: ...
N7 AI tools used outside the repos: ...
N8 engine: fixed engine for new runs (recommended) / other: ...
N9 writing in: paper/sections / Overleaf
Q1 ... Q7 at G1; Q4 at G2; Q2 Q3 Q5 Q6 at G3 (or now if you already know)
```
