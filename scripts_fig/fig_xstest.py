#!/usr/bin/env python3
"""Compact XSTest panel (Figure 5c): best SFT/KD baseline vs ReAD, mean +- std over three seeds (paper numbers).
Drawn exactly like the original component-ablation panel next to it: methods on the x-axis, bars colored and
hatched by budget (20M blue '///', 150M orange dots), black edges and error bars."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'xstest_compact.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'xstest_preview.png')
S.apply(7)
SCALE = 0.73   # shown at height 92pt in Figure 5
xs = {'safe': {'base': ((15.1, .77), (13.1, .69)), 'read': ((13.8, .72), (11.8, .58))},
      'unsafe': {'base': ((75.5, 1.09), (79.0, .88)), 'read': ((78.1, .97), (81.6, .83))}}
fig, axes = plt.subplots(1, 2, figsize=(2.2, 1.75))
fig.subplots_adjust(left=0.13, right=0.99, top=0.80, bottom=0.17, wspace=0.42)
x = np.arange(2); w = 0.38
for ax, met, title, lim in ((axes[0], 'safe', r'Safe-refusal [%] $\downarrow$', (10, 16.5)),
                            (axes[1], 'unsafe', r'Unsafe-refusal [%] $\uparrow$', (73, 83.5))):
    for i, (B, sgn) in enumerate(((20, -1), (150, 1))):
        vals = [xs[met]['base'][i], xs[met]['read'][i]]
        ax.bar(x + sgn * w / 2, [v for v, _ in vals], w, yerr=[s for _, s in vals], color=S.BUDGET[B]['color'],
               hatch=S.hatch(B, SCALE), error_kw=S.ERR, label=S.BUDGET[B]['label'], zorder=3, **S.EDGE)
    ax.set_xticks(x); ax.set_xticklabels(['Best\nbaseline', 'ReAD'], fontsize=6.5)
    ax.set_ylim(*lim); ax.set_title(title, fontsize=6.8, pad=2); S.grid(ax, 'y')
    ax.tick_params(axis='y', labelsize=6.2, pad=1)
h, l = axes[0].get_legend_handles_labels()
fig.legend(h, l, loc='upper center', ncol=2, fontsize=6.5, handlelength=1.3, columnspacing=1.0,
           borderaxespad=0.1, bbox_to_anchor=(0.56, 1.0))
fig.savefig(OUT); fig.savefig(PNG, dpi=260); print('wrote', OUT)
