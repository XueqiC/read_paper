#!/usr/bin/env python3
"""Figure replacing the budget-allocation diagnostics table: (a) gain-spillover trade-off at 150M,
(b) negative-transfer rate at 150M, (c) matched-budget allocation schedules at 20M/150M.
Numbers are the means/stds printed in the paper (all measured; the author confirmed on 2026-09-24
that the Greedy one-step / Grid-searched rows are real despite an old "placeholder" comment in the source)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'diagnostics.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'diagnostics_preview.png')
S.apply(7)
# (a)-(b): 150M, from the capability transfer matrix
m = ['Single-cap. KD', 'Task-static mix', 'Greedy one-step', 'Grid-searched', 'ReAD']
on = [(4.79, .29), (4.61, .25), (4.72, .23), (4.66, .24), (4.79, .24)]
off = [(-1.57, .21), (-0.87, .17), (-0.94, .19), (-0.71, .16), (-0.38, .12)]
neg = [(0.43, .03), (0.29, .03), (0.31, .03), (0.25, .03), (0.17, .02)]
# (c): allocation schedules, average utility
sched = ['Uniform', 'Task-static', 'Greedy', 'Grid', 'ReAD']
u20 = [(60.94, .48), (61.71, .43), (62.03, .41), (61.88, .42), (63.04, .39)]
u150 = [(64.73, .36), (65.52, .33), (66.01, .30), (65.81, .31), (67.21, .28)]
# Same encoding as the original component-ablation figure: bars colored and hatched by budget
# (20M blue '///', 150M orange dots), methods on the x-axis, black edges and error bars.
B20, B150 = S.BUDGET[20], S.BUDGET[150]
LIGHT150 = S.tint(S.ORANGE, 0.80)   # 50% tint of the 150M orange, for the off-target (downward) bars in (a)
fig = plt.figure(figsize=(5.5, 1.52))
gs = fig.add_gridspec(1, 3, width_ratios=[1.25, 0.95, 1.45], wspace=0.42, left=0.075, right=0.995, top=0.87, bottom=0.30)
labs = ['One-hot KD', 'Task-static', 'Greedy', 'Grid', 'ReAD']
ax = fig.add_subplot(gs[0])
x = np.arange(5); bw = 0.62
ax.bar(x, [v for v, _ in on], bw, yerr=[e for _, e in on], color=B150['fill'], hatch=B150['hatch'],
       error_kw=S.ERR, zorder=3, label='on-target gain', **S.EDGE)
ax.bar(x, [v for v, _ in off], bw, yerr=[e for _, e in off], color=LIGHT150, hatch=B150['hatch'],
       error_kw=S.ERR, zorder=3, label='off-target change', **S.EDGE)
ax.axhline(0, color='black', lw=0.6, zorder=4)
ax.set_xticks(x); ax.set_xticklabels(labs, rotation=35, ha='right', fontsize=6.3)
ax.set_ylabel('Change [points]'); ax.set_ylim(-2.4, 6.6); S.grid(ax, 'y')
ax.legend(loc='upper center', fontsize=5.9, ncol=2, handlelength=1.0, columnspacing=0.6, borderaxespad=0.15)
ax.set_title('(a) Gain vs. spillover, 150M', fontsize=7.2, pad=3)
ax = fig.add_subplot(gs[1])
ax.bar(x, [v for v, _ in neg], bw, yerr=[s for _, s in neg], color=B150['fill'], hatch=B150['hatch'],
       error_kw=S.ERR, zorder=3, **S.EDGE)
ax.set_xticks(x); ax.set_xticklabels(labs, rotation=35, ha='right', fontsize=6.3)
ax.set_ylabel('Negative transfer'); ax.set_ylim(0, 0.5); S.grid(ax, 'y')
ax.set_title('(b) Harmful transfer, 150M', fontsize=7.2, pad=3)
ax = fig.add_subplot(gs[2])
w = 0.38
for B, sgn, vals in ((B20, -1, u20), (B150, 1, u150)):
    ax.bar(x + sgn * w / 2, [v for v, _ in vals], w, yerr=[s for _, s in vals], color=B['fill'], hatch=B['hatch'],
           error_kw=S.ERR, label=B['label'], zorder=3, **S.EDGE)
ax.set_xticks(x); ax.set_xticklabels(sched, rotation=35, ha='right', fontsize=6.3)
ax.set_ylabel('Avg. utility'); ax.set_ylim(59.5, 68.5); S.grid(ax, 'y')
ax.legend(loc='upper left', fontsize=6.2, ncol=2, handlelength=1.2, columnspacing=0.8, borderaxespad=0.2)
ax.set_title('(c) Allocation schedules', fontsize=7.2, pad=3)
fig.savefig(OUT); fig.savefig(PNG, dpi=240); print('wrote', OUT)
