#!/usr/bin/env python3
"""Appendix figure: ReAD advantage with unadjusted 95% Welch CIs for every reported comparison,
one panel per budget, filled = significant after Holm correction. Numbers: means/stds printed in the paper."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import stats
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.transforms as mtrans
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'signif_xstest.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'signif_preview.png')
S.apply(7)
n = 3
caps = ["General", "Steerability", "Reasoning", "Math", "Code", "Tool Use", "LCU", "Multilingual"]
read = {20: ([35.02, 58.03, 10.01, 21.06, 77.06, 29.82, 33.58, 73.04], [.41, .61, .12, .68, .97, .64, .49, .84]),
        150: ([41.80, 78.20, 10.40, 35.20, 83.90, 31.30, 35.60, 84.10], [.45, .70, .10, .80, 1.00, .55, .55, .90])}
best = {20: ([34.02, 54.21, 9.62, 19.34, 74.62, 27.41, 31.72, 70.81], [.43, .66, .13, .72, 1.12, .69, .50, .91]),
        150: ([40.18, 72.63, 10.26, 33.02, 80.57, 29.48, 33.73, 79.97], [.51, .79, .11, .92, 1.16, .69, .64, .97])}
alloc = {"Uniform static": ((60.94, .48), (64.73, .36)), "Task-static mix": ((61.71, .43), (65.52, .33)),
         "Greedy one-step": ((62.03, .41), (66.01, .30)), "Grid-searched": ((61.88, .42), (65.81, .31))}
read_alloc = ((63.04, .39), (67.21, .28))
xs = {"safe": {"best": ((15.1, .77), (13.1, .69)), "read": ((13.8, .72), (11.8, .58))},
      "unsafe": {"best": ((75.5, 1.09), (79.0, .88)), "read": ((78.1, .97), (81.6, .83))}}
def welch(m1, s1, m2, s2):
    se = np.sqrt(s1 ** 2 / n + s2 ** 2 / n)
    df = se ** 4 / ((s1 ** 2 / n) ** 2 / (n - 1) + (s2 ** 2 / n) ** 2 / (n - 1))
    d = m1 - m2; q = stats.t.ppf(.975, df) * se
    return d, d - q, d + q, 2 * stats.t.sf(abs(d / se), df)
def holm(ps):
    ps = np.asarray(ps); order = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for k, i in enumerate(order):
        run = max(run, (len(ps) - k) * ps[i]); adj[i] = min(1, run)
    return adj
res = {20: [], 150: []}
labels, heads = [], []
for bi, B in enumerate((20, 150)):
    r = [welch(read[B][0][j], read[B][1][j], best[B][0][j], best[B][1][j]) for j in range(8)]
    a = holm([x[3] for x in r]); res[B] += [x[:3] + (p,) for x, p in zip(r, a)]
    r = [welch(read_alloc[bi][0], read_alloc[bi][1], v[bi][0], v[bi][1]) for v in alloc.values()]
    a = holm([x[3] for x in r]); res[B] += [x[:3] + (p,) for x, p in zip(r, a)]
xr = []
for met, sign in (("safe", -1), ("unsafe", 1)):
    for bi in range(2):
        d, lo, hi, p = welch(xs[met]["read"][bi][0], xs[met]["read"][bi][1], xs[met]["best"][bi][0], xs[met]["best"][bi][1])
        if sign < 0: d, lo, hi = -d, -hi, -lo
        xr.append((d, lo, hi, p))
a = holm([x[3] for x in xr])
res[20] += [xr[0][:3] + (a[0],), xr[2][:3] + (a[2],)]; res[150] += [xr[1][:3] + (a[1],), xr[3][:3] + (a[3],)]
groups = [('vs. strongest one-hot', caps), ('vs. allocation schedules', list(alloc)),
          ('XSTest', ['Safe-refusal (reduction)', 'Unsafe-refusal'])]
ypos, y = [], 0.0
for g, rows in groups:
    heads.append((y, g)); y -= 1
    for rr in rows: ypos.append(y); labels.append(rr); y -= 1
    y -= 0.3
fig, axes = plt.subplots(1, 2, figsize=(5.5, 2.35), sharey=True, gridspec_kw=dict(wspace=0.06))
fig.subplots_adjust(left=0.24, right=0.99, top=0.9, bottom=0.15)
for ax, B in zip(axes, (20, 150)):
    col, mk = S.BUDGET[B]
    for yy, (d, lo, hi, p) in zip(ypos, res[B]):
        ax.plot([lo, hi], [yy, yy], color=col, lw=1.0, zorder=3)
        ax.plot([d], [yy], marker=mk, ms=3.8, mec=col, mew=0.9, mfc=col if p < 0.05 else 'white', zorder=4)
    ax.axvline(0, color=S.INK, lw=0.6, zorder=2)
    ax.set_xlim(-1.0, 7.8); ax.set_title(f'Budget {B}M', fontsize=7.5, color=col, pad=3)
    ax.set_xlabel('ReAD advantage [points]'); S.grid(ax)
axes[0].set_yticks(ypos); axes[0].set_yticklabels(labels, fontsize=6.6, fontweight='normal')
axes[0].set_ylim(y + 0.5, 0.6)
htr = mtrans.blended_transform_factory(fig.transFigure, axes[0].transData)
for yy, g in heads:
    axes[0].text(0.01, yy, g, transform=htr, ha='left', va='center', fontsize=6.9, clip_on=False)
fig.savefig(OUT); fig.savefig(PNG, dpi=240); print('wrote', OUT)
