# ReAD: Reinforcement-Guided Capability Distillation for Large Language Models

LaTeX source of the ICLR 2027 submission (anonymous, double-blind).

## Build

```bash
latexmk -pdf main.tex
```

(or `pdflatex main && bibtex main && pdflatex main && pdflatex main`). The output is `main.pdf`.

## Layout

| File | Content |
|---|---|
| `main.tex` | preamble, title, abstract, section inputs |
| `intro.tex`, `prelim.tex`, `method_revised.tex`, `theortical_revised.tex`, `experiment_revised.tex`, `conclusion.tex` | main text |
| `statements.tex` | AI use statement (required), Ethics statement, Reproducibility statement — placed after the main text, before the references, per the ICLR 2027 Author Guidelines |
| `appendix.tex` | appendices |
| `ref.bib` | bibliography (`iclr2027_conference.bst`, natbib author–year) |
| `figure/` | figures |
| `iclr2027_conference.sty`, `iclr2027_conference.bst`, `fancyhdr.sty`, `natbib.sty`, `math_commands.tex` | official ICLR 2027 style files (unmodified) |

## Camera-ready

Fill in `\author{...}` in `main.tex`, uncomment `\iclrfinalcopy`, and replace the anonymized code link in the abstract and the Reproducibility statement.
