#!/usr/bin/env python3
"""Figure 1 (exploratory study) redrawn as one vector figure at print size.
Data: data/figure1_matrices.json, the exact matrices of the original figure (reproduced from the original
generator; they match the original raster cell by cell). Panels (c) and (d) are computed from them exactly as
in the original notebook: (c) top-5 targets by Small->Large diagonal gain, marginal gains Small->Medium and
Medium->Large; (d) top-5 targets by the increase of average negative change on the other capabilities."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import fig_style as S
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'study.pdf')
PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'study_preview.png')
S.apply(6.8)
D = json.load(open(os.path.join(HERE, 'data', 'figure1_matrices.json')))
caps = D['caps']; T = {k: np.array(v) for k, v in D['T'].items()}
ICON = {c: os.path.join(HERE, 'icons', c.lower().replace(' ', '_') + '.png') for c in caps}
_cache = {}
def icon(c):
    if c not in _cache:
        _cache[c] = np.asarray(Image.open(ICON[c]).convert('RGBA'))   # full 512 px source
    return _cache[c]
def put_icon(ax, c, xy, size_in, coords):
    zoom = size_in * 72 / icon(c).shape[1]
    ab = AnnotationBbox(OffsetImage(icon(c), zoom=zoom), xy, xycoords=coords, frameon=False,
                        box_alignment=(0.5, 0.5), annotation_clip=False, zorder=5)
    ax.add_artist(ab)

W, H = 5.5, 1.62
fig = plt.figure(figsize=(W, H))
def axes_in(x0, y0, w, h, **kw): return fig.add_axes([x0 / W, y0 / H, w / W, h / H], **kw)
cmap = S.diverging(); norm = TwoSlopeNorm(vmin=-20.95, vcenter=0.0, vmax=20.95)   # colour range of the original
IC = 0.105   # icon size (in) on heatmap axes
hm_y, hm_s = 0.36, 0.92
panels = []
for k, (name, x0) in enumerate((('small', 0.17), ('large', 1.37))):
    ax = axes_in(x0, hm_y, hm_s, hm_s)
    im = ax.pcolormesh(np.arange(9), np.arange(9), T[name], cmap=cmap, norm=norm, shading='flat',
                       edgecolors='face', linewidth=0.0)   # vector cells
    ax.set_xlim(0, 8); ax.set_ylim(8, 0); ax.set_aspect('equal')
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_linewidth(0.6)
    for i, c in enumerate(caps):
        put_icon(ax, c, (-0.075, 1 - (i + 0.5) / 8), IC, 'axes fraction')      # rows: distilled target
        put_icon(ax, c, ((i + 0.5) / 8, -0.075), IC, 'axes fraction')          # columns: evaluated capability
    panels.append(ax)
cax = axes_in(2.33, hm_y, 0.055, hm_s)
cb = fig.colorbar(im, cax=cax, ticks=[-20, -10, 0, 10, 20]); cb.outline.set_linewidth(0.5)
cb.solids.set_rasterized(False); cb.solids.set_edgecolor('face')
cb.ax.tick_params(labelsize=6.3, length=2, width=0.5, pad=1)
cb.set_label(r'$\Delta$ score [points]', fontsize=6.4, labelpad=1)
# (c) diminishing returns
gS, gM, gL = np.diag(T['small']), np.diag(T['medium']), np.diag(T['large'])
order = np.argsort(-(gL - gS))[:5]
dSM, dML = (gM - gS)[order], (gL - gM)[order]
ax = axes_in(3.07, hm_y, 1.10, hm_s)
x = np.arange(5); w = 0.38
ax.bar(x - w / 2, dSM, w, color=S.BLUE, label=r'Small$\rightarrow$Medium', zorder=3, **S.EDGE)
ax.bar(x + w / 2, dML, w, color=S.ORANGE, label=r'Medium$\rightarrow$Large', zorder=3, **S.EDGE)
ax.set_xticks([]); ax.set_xlim(-0.6, 4.6); ax.set_ylim(0, 15.5); ax.set_yticks([0, 5, 10, 15])
ax.set_ylabel('Marginal target gain\n[points]', fontsize=6.6, labelpad=4); S.grid(ax, 'y')
ax.tick_params(axis='y', labelsize=6.3, pad=1)
for xi, i in zip(x, order): put_icon(ax, caps[i], (xi, -0.075), 0.13, ('data', 'axes fraction'))
ax.legend(loc='upper right', fontsize=5.6, handlelength=1.0, handletextpad=0.4, labelspacing=0.2, borderaxespad=0.2, frameon=True, framealpha=0.9,
          edgecolor='#cccccc', fancybox=False)
panels.append(ax)
# (d) rising spillover
def harm(M):
    A = M.copy(); np.fill_diagonal(A, 0.0); return np.maximum(-A, 0.0).sum(1) / (A.shape[0] - 1)
Hs = np.vstack([harm(T['small']), harm(T['medium']), harm(T['large'])]).T
o2 = np.argsort(-(Hs[:, 2] - Hs[:, 0]))[:5]
ax = axes_in(4.62, hm_y, 0.80, hm_s)
for i in o2:
    ax.plot([0, 1, 2], Hs[i], marker='o', ms=2.6, lw=1.1, color=S.CAP_LINE[caps[i]], label=caps[i], zorder=3)
ax.set_xticks([0, 1, 2]); ax.set_xticklabels(['20M', '80M', '150M']); ax.set_xlim(-0.15, 2.15)
ax.set_ylim(-0.3, 7.4); ax.set_yticks([0, 2, 4, 6])
ax.set_ylabel('Negative spillover\n[points]', fontsize=6.6, labelpad=4); ax.set_xlabel('Budget [tokens]', fontsize=6.6, labelpad=1)
ax.tick_params(axis='both', labelsize=6.3, pad=1); S.grid(ax, 'both')
ax.legend(loc='upper left', fontsize=5.4, handlelength=1.0, handletextpad=0.4, labelspacing=0.12, borderaxespad=0.2, frameon=True,
          framealpha=0.9, edgecolor='#cccccc', fancybox=False)
panels.append(ax)
# sub-captions (LaTeX footnotesize look) and the icon legend row
for ax, t in zip(panels, ['(a) Small budget', '(b) Large budget', '(c) Diminishing returns', '(d) Rising spillover']):
    bb = ax.get_position(); fig.text((bb.x0 + bb.x1) / 2, 0.02 / H, t, ha='center', va='bottom', fontsize=8,
                                    fontweight='normal')
# icon legend row, laid out from measured label widths and centred on the page
r = fig.canvas.get_renderer(); ICW, GAP, SEP = 0.13, 0.05, 0.11
tw = [fig.text(0, 0, c, fontsize=7.4).get_window_extent(r).width / fig.dpi for c in caps]
for t in fig.texts[-len(caps):]: t.remove()
total = sum(ICW + GAP + w for w in tw) + SEP * (len(caps) - 1); xx = (W - total) / 2; yy = (H - 0.11) / H
for c, w in zip(caps, tw):
    fig.add_artist(AnnotationBbox(OffsetImage(icon(c), zoom=ICW * 72 / icon(c).shape[1]), ((xx + ICW / 2) / W, yy),
                                  xycoords='figure fraction', frameon=False))
    fig.text((xx + ICW + GAP) / W, yy, c, ha='left', va='center', fontsize=7.4)
    xx += ICW + GAP + w + SEP
fig.savefig(OUT, dpi=900); fig.savefig(PNG, dpi=300)   # dpi only sets the icon bitmaps' resolution; print('wrote', OUT)
