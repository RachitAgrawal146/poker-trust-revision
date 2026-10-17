# STATUS.md

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
1. **Tag `tog-r0-submitted`: resolved in A2.** The session's git proxy drops
   tag pushes and the API proxy refuses ref creation, so the tag was created
   by the A2 archive workflow (run 38357267471): annotated tag object
   `04efcb5`, pointing at `3e87700`.
2. **PRIV branch.** This session can push only to
   `claude/optimistic-ritchie-0po68b`, so PRIV commits are there and
   `latex.yml` triggers on both branches. On the author's instruction H9
   was amended (13 Oct): a session that cannot push to a working branch
   works on its own branch and opens a pull request for the author to merge
   before the next step. Pull request opened into `main` at the end of A2.
3. A0 is still open: the branch the anonymous link tracks is unknown.
   Nothing was pushed to `main` or to `claude/repo-papers-review-chz55c`,
   so H11 holds whatever the answer is.

**Surprises.** None in the data. `latexmk` logs include first-pass
"citation undefined" warnings; the final pass resolves them (the text
matches exactly).

## A2. Rescue the raw data (13 Oct 2026)

**Commits.** PUB on `revision/r1`: `3680435` (workflow + check tool),
`e9582ff` and `a8fb324` (bot: source checks, first verification),
`34a72d7` (MANIFEST.md), `e637b39` (bot: second verification). The same
history is on `run/archive-data`. PRIV: this entry, the H9 amendment.

**Produced.**
* `PUB/.github/workflows/archive-data.yml` (push to `run/archive-data`,
  `actions: read`, `contents: write`) and
  `PUB/research_data/tools/check_dbs.py`. Author approved publishing the
  Release on 13 Oct.
* Release `data-r0` (public, tag on `3e87700`):
  `phase31_n20_r0.tar.gz` (6.9 MB), `ablation_r0.tar.gz` (2.7 MB),
  `phase31_n20_source.json`, `ablation_source.json`, `SHA256SUMS`. Each
  archive carries a README with protocol and provenance; the ablation
  README marks the no-memory folders contaminated, "do not analyse".
  README and release notes are factual and do not mention the review.
* Tag `tog-r0-submitted` (see A1, deviation 1).
* `PUB/research_data/MANIFEST.md`: LFS datasets, Release datasets, and
  datasets named in the docs but held nowhere, each with protocol and
  checksum.
* `PUB/research_data/checks/`: source checks, `data-r0.SHA256SUMS`, and
  one verification record per run.

**Checks (Done when).**

| Check | Result |
|---|---|
| Phase 3.1 n=20: 20 databases, 150 hands each, integrity ok | yes; seeds match the 20-seed list; `runs.git_sha` = `92e1b64` in all 20 |
| Ablation: integrity ok | yes, 8 databases: no-cot 42/137/256/512/1024, no-memory 256/512/1024; 150 hands each; `runs.git_sha` = `28f3fd1` |
| Release lists the archives | yes, 5 assets |
| Verification in the first run (separate job, fresh runner) | run 38357267471: SHA256SUMS ok, every file re-opened, per-file SHA-256 identical to source |
| **Second workflow run** downloads and opens them | run 38357503497 (push of `34a72d7`): archive steps skipped because the Release was complete, verify job success |
| A2.4 LFS objects resolve | yes (batch API, no download); 2.5 GB file not copied |
| A2.6 download from the session container | **works with `curl -sSfL` on the `releases/download/...` URL** (redirect to release-assets.githubusercontent.com is allowed). Downloaded both archives, `sha256sum -c` ok, all 28 databases opened with `check_dbs.py`, all_ok. `gh release download` does **not** work (it uses GraphQL, which the proxy blocks); `gh api .../releases/assets/<id>` with `Accept: application/octet-stream` also works. **So A3 may run small analyses in the session.** |

**Surprises.**
* Both artifacts were still present (expiry 1 and 2 Nov), so nothing
  was lost.
* The ablation run (30874382486) concluded `failure` overall because of
  the no-notes / no-memory jobs; its aggregate artifact was still
  uploaded and is complete for what it contains.
* `reports/phase31_long_scorecard.txt` (UTF-16) still describes the
  five-seed temperature-1.0 Phase 3.1 run; `r_by_phase.json` cites it only
  for Phases 1-3 and takes Phase 3.1 from the n=20 run. Worth a line in B3.

**Author, please look at.**
1. Merge the PRIV pull request into `main` before the next step (H9).
2. The A0 items in `DECISIONS.md` are still open, in particular which
   branch the anonymous link tracks (H11) and whether the four missing
   databases exist on your machines. Release `data-r0` is the place to
   attach them.
