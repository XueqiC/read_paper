#!/usr/bin/env python3
"""Compact XSTest panel (Figure 4c): best SFT/KD baseline vs ReAD, mean +- std over three seeds (paper numbers)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'xstest_compact.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'xstest_preview.png')
S.apply(7.5)
xs = {'safe': {'base': ((15.1, .77), (13.1, .69)), 'read': ((13.8, .72), (11.8, .58))},
      'unsafe': {'base': ((75.5, 1.09), (79.0, .88)), 'read': ((78.1, .97), (81.6, .83))}}
fig, axes = plt.subplots(2, 1, figsize=(2.2, 1.75), constrained_layout=True)
for ax, met, title, lim in ((axes[0], 'safe', 'Safe-refusal [%] (lower is better)', (10.3, 16.5)),
                            (axes[1], 'unsafe', 'Unsafe-refusal [%] (higher is better)', (73.8, 83.3))):
    for i, B in enumerate((20, 150)):
        yy = 1 - i; col, mk = S.BUDGET[B]
        (bm, bs), (rm, rs) = xs[met]['base'][i], xs[met]['read'][i]
        ax.plot([bm, rm], [yy, yy], color='#d9d8d2', lw=2.0, zorder=1, solid_capstyle='round')
        ax.errorbar(bm, yy, xerr=bs, fmt=mk, ms=4, mfc='white', mec=S.BASE, color=S.BASE, elinewidth=0.8,
                    capsize=1.8, capthick=0.8, zorder=3)
        ax.errorbar(rm, yy, xerr=rs, fmt=mk, ms=4, mfc=col, mec=col, color=col, elinewidth=0.8, capsize=1.8,
                    capthick=0.8, zorder=4)
    ax.set_yticks([1, 0]); ax.set_yticklabels(['20M', '150M'])
    ax.set_ylim(-0.6, 1.6); ax.set_xlim(*lim); ax.set_title(title, fontsize=7, pad=2)
    S.grid(ax); ax.tick_params(axis='x', labelsize=6.5, pad=1)
fig.savefig(OUT); fig.savefig(PNG, dpi=260); print('wrote', OUT)
