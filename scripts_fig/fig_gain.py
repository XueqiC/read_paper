#!/usr/bin/env python3
"""Appendix figure: points gained over the initial student, ReAD vs strongest one-hot baseline (Table 1)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'gain_over_student.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'gain_preview.png')
S.apply(7)
caps = ["General", "Steerability", "Reasoning", "Math", "Code", "Tool Use", "LCU", "Multilingual"]
student = np.array([31.09, 49.22, 8.72, 15.56, 72.60, 25.83, 30.40, 68.90])
read = {20: (np.array([35.02, 58.03, 10.01, 21.06, 77.06, 29.82, 33.58, 73.04]), np.array([.41, .61, .12, .68, .97, .64, .49, .84])),
        150: (np.array([41.80, 78.20, 10.40, 35.20, 83.90, 31.30, 35.60, 84.10]), np.array([.45, .70, .10, .80, 1.00, .55, .55, .90]))}
best = {20: (np.array([34.02, 54.21, 9.62, 19.34, 74.62, 27.41, 31.72, 70.81]), np.array([.43, .66, .13, .72, 1.12, .69, .50, .91])),
        150: (np.array([40.18, 72.63, 10.26, 33.02, 80.57, 29.48, 33.73, 79.97]), np.array([.51, .79, .11, .92, 1.16, .69, .64, .97]))}
# strongest one-hot baseline per capability (underlined in Table 1; identical at both budgets)
base_name = ['Logit-KD', 'Logit-KD', 'CoT-KD', 'CoT-KD', 'Logit-KD', 'Logit-KD', 'Logit-KD', 'Logit-KD']
base_col = [S.METHOD[n] for n in base_name]
fig, axes = plt.subplots(1, 2, figsize=(5.5, 1.95), sharey=True, gridspec_kw=dict(wspace=0.06))
fig.subplots_adjust(left=0.13, right=0.99, top=0.82, bottom=0.19)
y = np.arange(8)[::-1]
for ax, B in zip(axes, (20, 150)):
    mk = S.BUDGET[B]['marker']   # circle = 20M, square = 150M, as in Figures 3 and 5
    gr, gb = read[B][0] - student, best[B][0] - student
    for yy, a, b in zip(y, gb, gr):
        ax.plot([a, b], [yy, yy], color='#d9d8d2', lw=2.0, zorder=1, solid_capstyle='round')
    for yy, g, e, c in zip(y, gb, best[B][1], base_col):
        ax.errorbar(g, yy, xerr=e, fmt=mk, ms=3.8, mfc=c, mec=c, color=c, elinewidth=0.7, capsize=1.5,
                    capthick=0.7, zorder=3)
    ax.errorbar(gr, y, xerr=read[B][1], fmt=mk, ms=3.8, mfc=S.READ, mec=S.READ, color=S.READ, elinewidth=0.7,
                capsize=1.5, capthick=0.7, zorder=4)
    ax.set_title(f'Budget {B}M', fontsize=7.5, pad=3)
    ax.set_xlabel('Gain over student [points]'); S.grid(ax); ax.set_xlim(left=0)
axes[0].set_yticks(y); axes[0].set_yticklabels(caps, fontweight='normal')
from matplotlib.lines import Line2D
h = [Line2D([], [], color=S.METHOD[n], marker='o', ms=3.8, lw=0, label=n) for n in ('ReAD', 'Logit-KD', 'CoT-KD')]
h += [Line2D([], [], color='black', marker='o', mfc='white', ms=3.8, lw=0, label='20M'),
      Line2D([], [], color='black', marker='s', mfc='white', ms=3.8, lw=0, label='150M')]
fig.legend(handles=h, loc='upper center', ncol=5, fontsize=6.5, handlelength=1.0, columnspacing=1.2,
           borderaxespad=0.1, bbox_to_anchor=(0.56, 1.0))
fig.savefig(OUT); fig.savefig(PNG, dpi=240); print('wrote', OUT)
