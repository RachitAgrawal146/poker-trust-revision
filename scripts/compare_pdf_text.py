#!/usr/bin/env python3
"""Compare the text of a freshly built PDF with a reference PDF.

Writes a short Markdown report: page counts, reference count (from a
.bbl, if given), and a word-level diff of the pdftotext output with
whitespace normalised. Exit status is always 0; the report is the result.
"""
import argparse
import difflib
import re
import subprocess


def pdf_pages(path):
    out = subprocess.run(["pdfinfo", path], capture_output=True, text=True).stdout
    m = re.search(r"^Pages:\s+(\d+)", out, re.M)
    return int(m.group(1)) if m else None


def pdf_words(path):
    text = subprocess.run(["pdftotext", "-enc", "UTF-8", path, "-"],
                          capture_output=True, text=True).stdout
    # Rejoin words hyphenated across line breaks, then split on whitespace.
    text = re.sub(r"-\n(?=[a-z])", "", text)
    return text.split()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--built", required=True)
    ap.add_argument("--submitted", required=True)
    ap.add_argument("--bbl")
    ap.add_argument("--label", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    built, sub = pdf_words(a.built), pdf_words(a.submitted)
    sm = difflib.SequenceMatcher(None, sub, built, autojunk=False)
    ops = [op for op in sm.get_opcodes() if op[0] != "equal"]

    lines = [f"## {a.label}", "",
             "| Check | Built | Submitted |", "|---|---|---|",
             f"| Pages | {pdf_pages(a.built)} | {pdf_pages(a.submitted)} |",
             f"| Words (pdftotext) | {len(built)} | {len(sub)} |"]
    if a.bbl:
        with open(a.bbl, encoding="utf-8", errors="replace") as fh:
            n_refs = len(re.findall(r"\\bibitem", fh.read()))
        lines.append(f"| References (\\bibitem in rebuilt .bbl) | {n_refs} | |")
    lines += ["", f"Word-sequence similarity: {sm.ratio():.6f}; "
              f"differing segments: {len(ops)}", ""]
    for tag, i1, i2, j1, j2 in ops[:200]:
        lines.append(f"* `{tag}` submitted[{i1}:{i2}] = "
                     f"`{' '.join(sub[i1:i2])[:200]}` -> built[{j1}:{j2}] = "
                     f"`{' '.join(built[j1:j2])[:200]}`")
    if len(ops) > 200:
        lines.append(f"* ... {len(ops) - 200} more")
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n\n")


if __name__ == "__main__":
    main()
