#!/usr/bin/env python3
"""Appendix figures: ReAD's advantage with unadjusted 95% Welch CIs, split by comparison group.
Writes signif_onehot.pdf, signif_alloc.pdf, signif_xstest.pdf. Numbers: means/stds printed in the paper."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy import stats
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure')
PREV = sys.argv[2] if len(sys.argv) > 2 else HERE
S.apply(6.6)
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
def block(rows_fn, k):   # returns {B: [(d, lo, hi, p_holm), ...]}
    out = {}
    for bi, B in enumerate((20, 150)):
        r = rows_fn(bi, B); a = holm([x[3] for x in r]); out[B] = [x[:3] + (p,) for x, p in zip(r, a)]
    return out
onehot = block(lambda bi, B: [welch(read[B][0][j], read[B][1][j], best[B][0][j], best[B][1][j]) for j in range(8)], 8)
allocb = block(lambda bi, B: [welch(read_alloc[bi][0], read_alloc[bi][1], v[bi][0], v[bi][1]) for v in alloc.values()], 4)
xr = []
for met, sign in (("safe", -1), ("unsafe", 1)):
    for bi in range(2):
        d, lo, hi, p = welch(xs[met]["read"][bi][0], xs[met]["read"][bi][1], xs[met]["best"][bi][0], xs[met]["best"][bi][1])
        if sign < 0: d, lo, hi = -d, -hi, -lo
        xr.append((d, lo, hi, p))
a = holm([x[3] for x in xr])
xst = {20: [xr[0][:3] + (a[0],), xr[2][:3] + (a[2],)], 150: [xr[1][:3] + (a[1],), xr[3][:3] + (a[3],)]}

def panel(fname, labels, res, figsize, legend=False, xlim=(-1.0, 7.8)):
    fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
    y = np.arange(len(labels))[::-1].astype(float)
    for B, off in ((20, 0.16), (150, -0.16)):
        col, mk = S.BUDGET[B]['color'], S.BUDGET[B]['marker']
        for yy, (d, lo, hi, p) in zip(y, res[B]):
            ax.plot([lo, hi], [yy + off] * 2, color=col, lw=1.0, zorder=3)
            ax.plot([d], [yy + off], marker=mk, ms=3.2, mec=col, mew=0.8, mfc=col if p < 0.05 else 'white', zorder=4)
    ax.axvline(0, color=S.INK, lw=0.6, zorder=2)
    ax.set_yticks(y); ax.set_yticklabels(labels, fontweight='normal', fontsize=6.3); ax.set_ylim(-0.55, len(labels) - 0.45)
    ax.set_xlim(*xlim); ax.set_xticks([0, 2, 4, 6]); ax.set_xlabel('Advantage [points]'); S.grid(ax)
    if legend:
        h = [Line2D([], [], color=S.BLUE, marker='o', ms=3.8, lw=1.0, label='20M'),
             Line2D([], [], color=S.ORANGE, marker='s', ms=3.8, lw=1.0, label='150M'),
             Line2D([], [], color='black', marker='o', ms=3.8, lw=0, label='significant'),
             Line2D([], [], color='black', marker='o', ms=3.8, mfc='white', lw=0, label='n.s.')]
        ax.legend(handles=h, loc='center right', fontsize=5.8, handlelength=1.2, labelspacing=0.15, borderaxespad=0.1, ncol=1)
    fig.savefig(os.path.join(OUTDIR, fname + '.pdf')); fig.savefig(os.path.join(PREV, fname + '_preview.png'), dpi=240)
    print('wrote', fname)
panel('signif_onehot', caps, onehot, (2.2, 1.25))
panel('signif_alloc', list(alloc), allocb, (1.95, 1.25), legend=True)
panel('signif_xstest', ['Safe-refusal\n(reduction)', 'Unsafe-refusal'], xst, (1.65, 1.25))
