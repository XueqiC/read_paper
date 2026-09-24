#!/usr/bin/env python3
"""Appendix figure: points gained over the initial student, ReAD vs strongest one-hot baseline (Table 1 numbers).
Style matches the paper's original figures (Times bold, seaborn deep colors, black-edged hatched bars)."""
import os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'gain_over_student.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'gain_preview.png')
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Liberation Serif'], 'font.weight': 'bold',
                     'axes.labelweight': 'bold', 'axes.titleweight': 'bold', 'font.size': 7.5, 'pdf.fonttype': 42,
                     'axes.edgecolor': '#2E3440', 'axes.linewidth': 0.7})
caps = ["General", "Steerability", "Reasoning", "Math", "Code", "Tool Use", "LCU", "Multilingual"]
student = np.array([31.09, 49.22, 8.72, 15.56, 72.60, 25.83, 30.40, 68.90])
read = {20: (np.array([35.02, 58.03, 10.01, 21.06, 77.06, 29.82, 33.58, 73.04]), np.array([.41, .61, .12, .68, .97, .64, .49, .84])),
        150: (np.array([41.80, 78.20, 10.40, 35.20, 83.90, 31.30, 35.60, 84.10]), np.array([.45, .70, .10, .80, 1.00, .55, .55, .90]))}
best = {20: (np.array([34.02, 54.21, 9.62, 19.34, 74.62, 27.41, 31.72, 70.81]), np.array([.43, .66, .13, .72, 1.12, .69, .50, .91])),
        150: (np.array([40.18, 72.63, 10.26, 33.02, 80.57, 29.48, 33.73, 79.97]), np.array([.51, .79, .11, .92, 1.16, .69, .64, .97]))}
BLUE, GRAY = '#4C72B0', '#8C8C8C'
ek = dict(elinewidth=0.8, capsize=1.8, capthick=0.8, ecolor='black')
fig, axes = plt.subplots(1, 2, figsize=(5.5, 2.7), sharey=True, constrained_layout=True)
y = np.arange(len(caps))[::-1]; h = 0.38
for ax, B in zip(axes, [20, 150]):
    rm, rs = read[B]; bm, bs = best[B]; gr, gb = rm - student, bm - student
    ax.barh(y + h / 2, gr, height=h, color=BLUE, edgecolor='black', linewidth=0.6, hatch='///', alpha=0.92,
            xerr=rs, error_kw=ek, label='ReAD', zorder=3)
    ax.barh(y - h / 2, gb, height=h, color=GRAY, edgecolor='black', linewidth=0.6, hatch='..', alpha=0.75,
            xerr=bs, error_kw=ek, label='Best one-hot baseline', zorder=3)
    xmax = (gr + rs).max()
    for yi, v, s in zip(y, gr, rs):
        ax.text(v + s + 0.02 * xmax, yi + h / 2, f'{v:+.1f}', va='center', ha='left', fontsize=6.3)
    ax.set_xlim(0, xmax * 1.22); ax.set_yticks(y); ax.set_yticklabels(caps)
    ax.set_xlabel('Gain over Student [Points]')
    ax.set_title(f'Budget {B}M', fontsize=8)
    ax.grid(True, axis='x', alpha=0.3, linewidth=0.6, zorder=0); ax.set_axisbelow(True)
    ax.tick_params(axis='y', length=0)
fig.legend(*axes[0].get_legend_handles_labels(), loc='outside upper center', ncol=2, frameon=True, fontsize=7)
fig.savefig(OUT); fig.savefig(PNG, dpi=220); print('wrote', OUT)
