#!/usr/bin/env python3
"""Forest plot of every reported ReAD comparison + XSTest levels (replaces Tables 3-4 in the main text).
All numbers are the means and standard deviations printed in the paper (three seeds)."""
import os, sys
import numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'signif_xstest.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'signif_preview.png')

C20, C150 = '#4C72B0', '#DD8452'          # budget colors of the original ablation figure (seaborn deep)
GRAY, BLUE, INK, INK2, GRID = '#8C8C8C', '#4C72B0', '#1d1d1b', '#3f3e3a', '#dcdbd5'
MK = {20: 'o', 150: 's'}
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Liberation Serif', 'DejaVu Serif'],
                     'font.weight': 'bold', 'axes.labelweight': 'bold', 'axes.titleweight': 'bold',
                     'font.size': 7, 'pdf.fonttype': 42, 'mathtext.fontset': 'stix',
                     'axes.edgecolor': '#2E3440', 'axes.linewidth': 0.7,
                     'xtick.color': INK, 'ytick.color': INK, 'xtick.major.width': 0.6, 'ytick.major.size': 0})
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
    d = m1 - m2
    return d, d - stats.t.ppf(.975, df) * se, d + stats.t.ppf(.975, df) * se, 2 * stats.t.sf(abs(d / se), df)

def holm(ps):
    ps = np.asarray(ps); order = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for k, i in enumerate(order):
        run = max(run, (len(ps) - k) * ps[i]); adj[i] = min(1, run)
    return adj

# ---- rows: (label, {20: (d, lo, hi, p_holm), 150: ...}) ----
groups = []
rows = []
for B in (20, 150):
    res = [welch(read[B][0][j], read[B][1][j], best[B][0][j], best[B][1][j]) for j in range(8)]
    adj = holm([r[3] for r in res])
    for j, c in enumerate(caps):
        if B == 20: rows.append([c, {}])
        rows[j][1][B] = res[j][:3] + (adj[j],)
groups.append(("vs. strongest one-hot", rows))
rows = []
for bi, B in enumerate((20, 150)):
    res = [welch(read_alloc[bi][0], read_alloc[bi][1], v[bi][0], v[bi][1]) for v in alloc.values()]
    adj = holm([r[3] for r in res])
    for j, k in enumerate(alloc):
        if B == 20: rows.append([k, {}])
        rows[j][1][B] = res[j][:3] + (adj[j],)
groups.append(("vs. allocation schedules", rows))
res, keys = [], []
for met, sign in (("safe", -1), ("unsafe", 1)):
    for bi, B in enumerate((20, 150)):
        r = xs[met]["read"][bi]; b = xs[met]["best"][bi]
        d, lo, hi, p = welch(r[0], r[1], b[0], b[1])
        if sign < 0: d, lo, hi = -d, -hi, -lo          # improvement = reduction of safe refusals
        res.append((d, lo, hi, p)); keys.append((met, B))
adj = holm([r[3] for r in res])
rows = [["Safe-refusal (reduction)", {}], ["Unsafe-refusal", {}]]
for (met, B), r, a in zip(keys, res, adj):
    rows[0 if met == "safe" else 1][1][B] = r[:3] + (a,)
groups.append(("Held-out XSTest", rows))

# ---- figure ----
fig = plt.figure(figsize=(5.5, 2.55))
gs = fig.add_gridspec(2, 2, width_ratios=[2.05, 1.0], height_ratios=[1, 1], wspace=0.08, hspace=0.95,
                      left=0.2, right=0.985, top=0.93, bottom=0.14)
ax = fig.add_subplot(gs[:, 0])
y = 0.0; yt, yl, heads = [], [], []
OFF = 0.19
for gname, grows in groups:
    heads.append((y, gname)); y -= 1.0
    for label, vals in grows:
        for B, col, off in ((20, C20, OFF), (150, C150, -OFF)):
            d, lo, hi, pa = vals[B]
            ax.plot([lo, hi], [y + off] * 2, color=col, lw=1.0, solid_capstyle='butt', zorder=3)
            ax.plot([lo, lo], [y + off - 0.12, y + off + 0.12], color=col, lw=0.9, zorder=3)
            ax.plot([hi, hi], [y + off - 0.12, y + off + 0.12], color=col, lw=0.9, zorder=3)
            ax.plot([d], [y + off], marker=MK[B], ms=3.6, mec=col, mew=1.0,
                    mfc=col if pa < 0.05 else 'white', zorder=4)
        yt.append(y); yl.append(label); y -= 1.0
    y -= 0.25
ax.axvline(0, color=INK2, lw=0.7, zorder=2)
ax.set_yticks(yt); ax.set_yticklabels(yl, fontsize=6.8)
import matplotlib.transforms as mtrans
htr = mtrans.blended_transform_factory(fig.transFigure, ax.transData)
for yy, g in heads:
    ax.text(0.012, yy, g, transform=htr, ha='left', va='center', fontsize=6.9, fontweight='bold', color=INK,
            bbox=dict(fc='white', ec='none', pad=0.6), zorder=6, clip_on=False)
ax.set_ylim(y + 0.6, 0.6)
ax.set_xlim(-1.6, 9.2)
ax.set_xlabel('ReAD Advantage [Points]', fontsize=7.2)
ax.grid(axis='x', color=INK, alpha=0.25, lw=0.6, zorder=0)
ax.tick_params(axis='x', labelsize=6.5, length=2)
leg = [Line2D([], [], color=C20, marker='o', ms=3.6, mfc=C20, lw=1.0, label='Budget 20M'),
       Line2D([], [], color=C150, marker='s', ms=3.6, mfc=C150, lw=1.0, label='Budget 150M'),
       Line2D([], [], color=INK2, marker='o', ms=3.6, mfc=INK2, lw=0, label='significant (Holm)'),
       Line2D([], [], color=INK2, marker='o', ms=3.6, mfc='white', lw=0, label='not significant')]
y_alloc = np.mean([t for t, l in zip(yt, yl) if l in alloc])
ax.legend(handles=leg, loc='center right', bbox_to_anchor=(9.2, y_alloc), bbox_transform=ax.transData,
          fontsize=6.2, frameon=True, framealpha=0.9, ncol=1,
          handlelength=1.5, borderpad=0.4, labelspacing=0.25)
ax.set_title('(a) All reported comparisons', fontsize=7.2, loc='left', color=INK, pad=4)

def levels(axx, met, title, xlim, better):
    for i, B in enumerate((20, 150)):
        yy = 1 - i
        (bm, bs), (rm, rs) = xs[met]["best"][i], xs[met]["read"][i]
        col = C20 if B == 20 else C150
        axx.plot([bm, rm], [yy, yy], color=GRID, lw=2.2, zorder=2, solid_capstyle='round')
        axx.errorbar(bm, yy, xerr=bs, fmt=MK[B], ms=3.8, color=GRAY, mfc='white', mec=GRAY, mew=1.0,
                     elinewidth=0.9, capsize=1.8, capthick=0.9, zorder=3)
        axx.errorbar(rm, yy, xerr=rs, fmt=MK[B], ms=3.8, color=col, mfc=col, mec=col, elinewidth=0.9,
                     capsize=1.8, capthick=0.9, zorder=4)
        if i == 0:
            lo_first = rm < bm
            axx.text(rm, yy + 0.38, 'ReAD', ha='center', fontsize=6.2, color=INK)
            axx.text(bm, yy - 0.42, 'baseline', ha='center', fontsize=6.2, color=GRAY)
    axx.set_yticks([1, 0]); axx.set_yticklabels(['20M', '150M'], fontsize=6.8)
    axx.set_ylim(-0.6, 1.75); axx.set_xlim(*xlim)
    axx.set_title(title, fontsize=7.2, loc='left', color=INK, pad=4)
    axx.set_xlabel(f'Score [%] ({better} is better)', fontsize=6.8)
    axx.grid(axis='x', color=INK, alpha=0.25, lw=0.6, zorder=0)
    axx.tick_params(axis='x', labelsize=6.3, length=2); axx.yaxis.set_tick_params(pad=1)

levels(fig.add_subplot(gs[0, 1]), 'safe', '(b) XSTest safe-refusal', (10.5, 17.0), 'lower')
levels(fig.add_subplot(gs[1, 1]), 'unsafe', '(c) XSTest unsafe-refusal', (73.3, 84.0), 'higher')
fig.savefig(OUT); fig.savefig(PNG, dpi=240)
for g, rs in groups:
    for label, v in rs:
        print(f"{g[:22]:22s} {label:26s} " + "  ".join(f"{B}M d={v[B][0]:+.2f} [{v[B][1]:+.2f},{v[B][2]:+.2f}] pH={v[B][3]:.3f}" for B in (20, 150)))
print('wrote', OUT)
