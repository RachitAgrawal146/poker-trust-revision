# STATUS.md

> **Open blocker (A2, deadline 25 Oct 2026):** the R0 language-model
> databases are still only Actions artifacts. Checked 13 Oct 2026: both
> are present, not expired. `all-databases-phase31-n20` (id 8850193603,
> 6.9 MB) expires 2026-11-01T05:49Z; `all-databases-ablation`
> (id 8880345921, 2.7 MB) expires 2026-11-02T03:18Z. The archive
> workflow is drafted but not pushed; it is waiting for the author's
> go-ahead (see A2 below).

## A1. Branch, freeze, correct the project memory (13 Oct 2026)

**Commits.** PUB `869b1f7` on `revision/r1` (CLAUDE.md). PRIV `4372f4f`
plus bot commit with build outputs, on branch
`claude/optimistic-ritchie-0po68b`.

**Produced.**
* PUB: branch `revision/r1` created from
  `origin/claude/repo-papers-review-chz55c` (`3e87700`) and pushed.
  Confirmed `3e87700` is not in `main` and the branch is 6 commits ahead
  of `main` (`9f9a067`), as section 1 says.
* PUB `CLAUDE.md`: new "Revision mode (2026-10)" section (working branch
  `revision/r1` overrides rule 6; rule 7 abstract instruction retired;
  `tog_submission/` and `tog_build/` frozen at the tag; H3 and H10
  restated; run/* branches + Releases). Status header corrected:
  Phase 3.1 entry is now n=20, temperature 0, 150 hands, mean r = +0.062
  (from `r_by_phase.json`); the -0.094 figure marked superseded and
  absent from the repo. No reviews mentioned.
* PRIV: `DECISIONS.md` (A0 checklist and Q/G tables, all pending),
  `reports/`, `briefs/`, `paper/` (empty), `paper_r0/` = `tog_submission/`
  at `3e87700` plus `IEEEtran.cls` and `IEEEtranN.bst` from
  `tog_build/tog_main_source.zip` (the six files the zip shares with
  `tog_submission/` are byte-identical).
* PRIV `.github/workflows/latex.yml` + `scripts/compare_pdf_text.py`:
  Ubuntu 24.04 TeX Live with `texlive-publishers` and `latexdiff`;
  builds `paper_r0/main.tex` and `supplementary.tex`, fetches the
  submitted PDFs from PUB at `3e87700`, writes a comparison into
  `builds/`, and commits it back. Run 38356099335: success.

**R0 build check (builds/r0_main_check.md, r0_supp_check.md).**

| | Built | Submitted |
|---|---|---|
| Main: pages | 10 | 10 |
| Main: references (rebuilt `.bbl`) | 34 | |
| Main: words, pdftotext | 11,275 | 11,275 (0 differing segments) |
| Supplement: pages / words | 5 / 2,082 | 5 / 2,082 (0 differing segments) |

The `.bbl` regenerated from `references.bib` is byte-identical to the
shipped one.

**Not done / deviations (author please look).**
1. **Tag `tog-r0-submitted` does not exist on the remote yet.** Created
   locally, but the session's git proxy drops tag pushes ("remote end hung
   up", 4 tries) and the GitHub API proxy refuses ref creation (403). The
   fix is to create it from a workflow; I folded that into the A2 archive
   workflow, which is on hold. Alternatively the author can run
   `git tag -a tog-r0-submitted 3e87700 -m "R0 as submitted" && git push origin tog-r0-submitted`
   from their own machine, or create it in the GitHub Releases UI.
2. **PRIV branch.** H9 says PRIV work goes on `main`. This session is
   only allowed to push to `claude/optimistic-ritchie-0po68b`, so all PRIV
   commits are there and `latex.yml` triggers on both branches. The author
   should merge it into `main` (or allow pushes to `main` for later
   sessions).
3. A0 is still open: the branch the anonymous link tracks is unknown.
   Nothing was pushed to `main` or to `claude/repo-papers-review-chz55c`,
   so H11 holds whatever the answer is.

**Surprises.** None in the data. `latexmk` logs include first-pass
"citation undefined" warnings; the final pass resolves them (the text
matches exactly).

## A2. Rescue the raw data — ON HOLD (13 Oct 2026)

**State.** Not started on the remote. Blocked on a permission decision,
not on a technical problem.

**What was verified.**
* Both artifacts exist and are unexpired (sizes and expiry above).
* The session container cannot download them: `gh api .../zip` is
  redirected to Azure blob storage, which the proxy blocks. So the
  workflow route of section 0.4 is needed.
* A2.4 done: all three LFS objects in `research_data/`
  (`runs_phase3_long.sqlite` 12.2 MB, `runs_v3.sqlite.part_00` 1.57 GB,
  `part_01` 0.92 GB) resolve: the LFS batch API returns a download action
  for each, checked without downloading.
* Provenance for the manifest: run 30788234686 = "Paper experiments",
  workflow_dispatch on `main` at `92e1b64`, 3 Aug 2026; run 30874382486 =
  "Run ablation", push to `run-ablation` at `28f3fd1`, 4 Aug 2026
  (concluded `failure` because of the no-notes/no-memory jobs). Model
  `claude-haiku-4-5-20251001`, temperature 0 on the Anthropic path of
  `phase3/llm_chat_agent.py`, 150 hands. The no-memory contamination
  details are in PUB commit `0b43ea5`.
* A2.6 cannot be tested yet: PUB has no Releases.

**Drafted, not committed.** `research_data/tools/check_dbs.py` (read-only
integrity + shape check, tested on a 20-hand local database) is in the
PUB working tree. The archive workflow (`.github/workflows/archive-data.yml`
on `run/archive-data`: download both artifacts, integrity-check, require
20 x 150 hands, tar each experiment with a README marking the
no-memory seeds as contaminated, `SHA256SUMS`, create Release `data-r0`
targeting `3e87700`, plus a separate verify job that downloads from the
Release and re-opens every database; also creates the missing tag) was
refused by the session's permission classifier because it publishes a
public Release. Waiting for the author to confirm.
