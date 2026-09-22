# Thesis template and writing guide

Università degli Studi di Perugia — Dipartimento di Ingegneria

One template for **BSc, MSc and PhD** theses. The structure is identical at every
level; only the entries on the title page change. Nothing else needs editing to
switch between them.

---

## Getting started

**On Overleaf** (easiest) — zip this folder, then *New Project → Upload Project*.
Press *Recompile*. Set the compiler to **pdfLaTeX** under *Menu → Compiler*.

**Locally** — you need a TeX distribution (MiKTeX or TeX Live). Then:

```bash
latexmk -pdf Main.tex
```

That runs pdfLaTeX, biber and pdfLaTeX twice, in the right order. Running
pdfLaTeX once is not enough: references and the table of contents will be wrong.

### What you edit

Open `Main.tex` and find the block marked **THESIS INFORMATION**. It is the only
part of `Main.tex` you should touch:

| Field | What to put |
|---|---|
| `\thesistype` | Uncomment one: Bachelor's / Master's / Doctoral |
| `\thesistitle` | Your title, as it will appear on the cover |
| `\author` | Your name |
| `\degreecourse` | e.g. *Corso di Laurea Magistrale in Ingegneria Meccanica* |
| `\academicyear` | e.g. 2026/2027 |
| `\supervisor` | Your supervisor |
| `\cosupervisorname` | Co-supervisor, or `{}` if there is none |
| `\coordinatorname` | PhD only — the doctoral course coordinator. `{}` otherwise |
| `\group` | Research group, or `{}` |

Empty fields disappear from the title page automatically — no need to delete the
surrounding layout.

**The logo.** Put the departmental logo at `Figures/logo.pdf` or `Figures/logo.png`.
Until you do, a placeholder box of the same size is drawn, so the document always
compiles. Ask your supervisor for the current official file rather than taking one
off a website.

---

## Structure of the thesis

This is the standard structure for an experimental thesis in our group. Follow it
unless your supervisor tells you otherwise — examiners expect it, and deviating
costs you explanation time you would rather spend on your results.

### Abstract — unnumbered

One page, no more. Written **last**, even though it appears first.

It must stand alone: someone who never opens the rest should still learn what you
did and what you found. Five sentences is a reliable recipe:

1. The context, and why it matters
2. The specific gap or open question you addressed
3. What you did — method, rig, sample size
4. What you found — **with numbers**, not adjectives
5. What it means, or what it enables

No citations. No abbreviations you have not spelled out.

### Sommario — unnumbered, Italian

If the thesis is written in **English**, an Italian abstract is expected. It is
effectively **mandatory for work carried out abroad during Erasmus mobility**,
because the examining board reads in Italian.

It is a translation of the English abstract, not a separate text. If you write the
thesis in Italian, delete the file and its `\include` line.

### 1 — Introduction

Convince the reader that your question was worth asking, and that nobody had
answered it. Four sections:

- **Background and motivation** — the engineering context, and why anyone should
  care: what fails, what it costs, who is affected. Start wide, narrow down, and
  end with the reason the work was undertaken. Write for a competent engineer who
  does *not* work in your specific field.
- **State of the art** — what has been done, by whom, and what each approach
  achieved. A **critical review, not a list**. Every paragraph should end with what
  the cited work could *not* do — those limitations are what justify your work.
- **Open research question** — the gap in one or two sentences, then the question.
  Specific enough to be answered yes/no or with a number. Then the objectives that
  follow from it, usually three to five.
- **Structure of the thesis** — one short paragraph per chapter. The map the
  examiner navigates by.

> *Weak:* "This thesis studies thermoelastic measurements."
> *Strong:* "Can stress mode shapes be identified on a rotating component without
> fiducial markers, and up to what rotational speed?"

### 2 — Theoretical background

Every concept the reader needs to follow Chapters 4 and 5, and nothing else.

**One section per area of theory you actually use.** If a piece of theory never
reappears later in the thesis, delete it — it is padding, and an examiner will ask
why it is there.

This chapter is **other people's work**, so it must be fully referenced. Your own
contribution goes in Chapter 3.

### 3 — Methodology *(optional)*

Include this chapter **only if you developed something yourself**: a new algorithm,
a new processing chain, a new identification or calibration procedure.

This is where your **original contribution** lives. Everything here must be yours;
anything taken from the literature belongs in Chapter 2.

Sections: rationale (why existing methods were not enough) → the proposed method →
implementation → validation strategy.

Make it **reproducible**. A competent reader should be able to reimplement your
method from this chapter alone.

If your work is purely experimental — you applied an existing method to a new case —
delete the file and its `\include` line. LaTeX renumbers everything for you.

### 4 — Experimental campaign

Let someone else repeat exactly what you did. Past tense, impersonal, **no results**.

- **Experimental test bench** — what the rig is, with a photograph *and* a schematic.
  List every instrument in a table: manufacturer, model, range, resolution,
  calibration status. In a measurements group that table is the first thing an
  examiner looks at. One subsection per bench if you used more than one.
- **Experimental protocol** — the procedure in the order performed: specimen
  preparation, mounting, environmental conditions, excitation, acquisition settings
  (sampling rate, duration, triggering) and the test matrix. Say how many
  repetitions and why. State what you did *not* control.
- **Data processing** — everything done to the raw data before it becomes a result:
  filtering, windowing, synchronisation, outlier rejection, averaging. Give
  **parameters**, not just step names.

> *Not reproducible:* "A low-pass filter was applied."
> *Reproducible:* "A 4th-order zero-phase Butterworth low-pass filter with a 500 Hz
> cut-off was applied."

If you rejected data, say which, how much, and on what criterion — decided **before**
you looked at the results.

### 5 — Results and discussion

The chapter the examiner reads most carefully, and the one that earns the mark.

**Results** are what the data show: neutral, factual, with uncertainty.
**Discussion** is what it means, why it happened, how it compares with the
literature, and where it does not hold.

You may interleave them section by section (recommended) or keep them separate.
Either way the reader must always know which one they are reading.

Close the chapter with an explicit **Limitations** section: the conditions under
which your conclusions do *not* hold. Students are reluctant to write this. Do not
be — stating your own limits shows you understand your work, and stops an examiner
raising them as though you had not noticed.

### 6 — Conclusions

Two to four pages. **No new material, no new figures, no new citations.**

What was done → what was found, with numbers → the answer to the research question
from Chapter 1, stated plainly → what it contributes → future work, as concrete
next steps rather than "more research is needed".

*Test:* if someone read only the Abstract and this chapter, would they have an
accurate picture of the thesis?

### References

Managed by `biblio.bib` and formatted automatically in IEEE style. Cite with
`\cite{key}`. Never type a reference by hand into the text.

### Acknowledgements

Placed at the end here; some students prefer the front, and either is accepted.

Conventionally two parts. **Professional**: supervisor, co-supervisor, laboratory,
technical staff, funding bodies and project names, any host institution during
mobility — if the work was funded by a project, **name it**, because funders require
this. **Personal**: family and friends, in whatever language you like.

---

## Indicative length

Pages of body text, excluding front matter, references and appendices. Your
supervisor's opinion overrides this table.

| | Typical range |
|---|---|
| BSc thesis | 40–60 pages |
| MSc thesis | 70–110 pages |
| PhD thesis | 120+ pages |

Nobody has ever been marked down for a thesis that was too short and complete.
Padding is visible from across the room.

---

## Rules that actually affect your mark

**Units.** Always `\SI{9.81}{\metre\per\second\squared}`, never typed by hand. It
keeps the spacing right and makes the whole thesis consistent.

**Uncertainty.** Every measured quantity carries one. A number without an
uncertainty is an opinion. `\SI{1.23 +- 0.04}{\milli\metre}`.

**Figures.** Every figure is referred to in the text (`Figure~\ref{fig:x}`) and
discussed. A figure nobody mentions should be deleted. Axis labels carry units, and
the font must be readable at print size — check by printing one page.

**Captions.** A caption should be understandable without the body text: what is
plotted, under what conditions, what to notice.

**Tables.** Use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`). No vertical rules.

**Cross-references.** Always `\ref` and `\label`, never "see the figure above" —
the figure will move.

**Tense.** What you did: past. What the literature says: present. What a figure
shows: present.

**Person.** Impersonal throughout. "The specimen was mounted", not "I mounted the
specimen".

---

## Common ways theses lose marks

- The state of the art is a list of summaries with no criticism, so the gap is
  never established and the work appears unmotivated.
- Theory is included that is never used again.
- Results are presented without uncertainty.
- The Discussion repeats the Results instead of explaining them.
- Conclusions introduce new findings that appear nowhere else.
- The Abstract is written first and never updated, so it describes a thesis that
  was not written.
- Figures exported as screenshots — blurry, unreadable axes.
- The Limitations section is missing, so the examiner supplies it for you.

---

## Files in this folder

```
Main.tex                     the only file you configure
MastersDoctoralThesis.cls    document class — do not edit
biblio.bib                   your bibliography database
Figures/                     put logo.pdf and all your figures here
Chapters/
  0a_Abstract.tex            English abstract
  0b_Sommario.tex            Italian abstract
  1_Introduction.tex
  2_Theoretical_background.tex
  3_Methodology.tex          optional — delete if not applicable
  4_Experimental_campaign.tex
  5_Results_and_discussion.tex
  6_Conclusions.tex
  7_Acknowledgements.tex
Appendices/
  AppendixA.tex              optional
```

Each chapter file opens with a comment block explaining what belongs in it. Those
comments are for you — they never appear in the PDF, and you can delete them once
you no longer need them.

---

## A note on appendices

Appendices hold material that supports the thesis but would interrupt it: full
derivations, data sheets, calibration certificates, long tables, code listings.

**Nothing essential to the argument may live only in an appendix.** If the reader
must see it to follow you, it belongs in the body. Every appendix must be referred
to at least once from the main text.

---

## If something breaks

**`Undefined control sequence`** — usually a typo in a command, or a missing
package. The line number in the error is reliable; start there.

**`Citation undefined`** — the key is not in `biblio.bib`, or you have not run
biber. Run `latexmk -pdf Main.tex` again.

**References show as `??`** — compile again. Cross-references need two passes.

**A figure will not appear** — check the path, and that you have not left `draft`
enabled in the class options.

Ask early rather than losing a day. Setup problems are a perfectly good reason to
open an issue on the course repository.
