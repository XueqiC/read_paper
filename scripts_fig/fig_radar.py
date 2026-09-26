#!/usr/bin/env python3
"""Figure 5b redrawn: ReAD vs capability-specific distillation methods at 150M.
The values are the polygon radii of the ORIGINAL radar PDF (radar_values_from_pdf.json), recovered from its
vector geometry and normalized by the outer circle, so the shapes are identical to the original figure.
Only the typography (larger, bold, black labels) and the unified method colors change."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'rqX_radar_sota_vs_read_150m.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'radar_preview.png')
S.apply(6.5)
vals = json.load(open(os.path.join(HERE, 'radar_values_from_pdf.json')))
caps = ['General', 'Steerability', 'Reasoning', 'Math', 'Code', 'Tool Use', 'LCU', 'Multilingual']   # 0, 45, ..., 315 deg
ang = np.deg2rad(np.arange(0, 360, 45))
order = ['ReAD', 'Step-by-Step', 'EoTD', 'CodePLAN']
fig = plt.figure(figsize=(1.72, 1.60))
ax = fig.add_axes([0.235, 0.085, 0.53, 0.57], projection='polar')
ax.set_theta_zero_location('E'); ax.set_theta_direction(1)
MK = {'ReAD': 'o', 'Step-by-Step': 's', 'EoTD': '^', 'CodePLAN': 'D'}
for name in order[::-1]:
    r = np.array([vals[name][c] for c in caps]); c = S.METHOD[name]
    a2, r2 = np.r_[ang, ang[:1]], np.r_[r, r[:1]]
    main = name == 'ReAD'
    ax.fill(a2, r2, color=c, alpha=0.22 if main else 0.06, zorder=2)
    ax.plot(a2, r2, color=c, lw=1.7 if main else 1.25, zorder=4 if main else 3)
    ax.plot(ang, r, ls='none', marker=MK[name], ms=2.6 if main else 2.1, color=c, mec='white', mew=0.3,
            zorder=5 if main else 3)
ax.set_ylim(0, 1); ax.set_yticks([0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels([])
ax.set_xticks(ang); ax.set_xticklabels([])
ax.grid(color='#b0b0b0', lw=0.4); ax.spines['polar'].set_linewidth(0.7); ax.spines['polar'].set_color('black')
for a, c in zip(ang, caps):
    ha = 'left' if np.cos(a) > 0.3 else ('right' if np.cos(a) < -0.3 else 'center')
    va = 'bottom' if np.sin(a) > 0.3 else ('top' if np.sin(a) < -0.3 else 'center')
    ax.text(a, 1.12, c, ha=ha, va=va, fontsize=6.3, fontweight='bold', color='black')
h = [Line2D([], [], color=S.METHOD[n], lw=1.6, marker=MK[n], ms=3.2, mec='white', mew=0.3, label=n) for n in order]
fig.legend(handles=h, loc='upper center', ncol=2, fontsize=6.2, handlelength=1.2, columnspacing=0.8,
           labelspacing=0.25, borderaxespad=0.1, bbox_to_anchor=(0.5, 0.995), prop={'weight': 'bold', 'size': 6.2})
fig.savefig(OUT); fig.savefig(PNG, dpi=300); print('wrote', OUT)
