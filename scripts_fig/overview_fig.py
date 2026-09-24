#!/usr/bin/env python3
"""ReAD method overview, v5: icon-driven architecture diagram with minimal text and no equations.

Keeps the three modules and every component of Section 3, but each component is an icon plus a
one-to-three-word label. Style: white modules with colored header strips, seaborn-deep accents,
flat icons with dark outlines (same style as the capability icons of Figure 1), STIX text.
"""
import sys, os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle, Polygon, Wedge
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, 'icons')
OUT_PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'overview.pdf')
OUT_PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'overview_preview.png')

BLUE, ORANGE, GREEN, RED, GOLD, GRAY = '#4C72B0', '#DD8452', '#55A868', '#C44E52', '#CCB974', '#8C8C8C'
INK, INK2, MUTED, LINE, OUT = '#1b1b1b', '#3a3a3a', '#7d7d7d', '#c2c2c2', '#2E3440'
HEAD = {1: '#dde5f1', 2: '#f8e4d4', 3: '#dcede1'}
LIGHT = {1: '#eef2f8', 2: '#fcf1e8', 3: '#edf6ef'}
ACC = {1: BLUE, 2: ORANGE, 3: GREEN}
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix', 'font.size': 6, 'pdf.fonttype': 42})

W, H = 140.0, 60.0
FIG_W = 5.5
fig = plt.figure(figsize=(FIG_W, FIG_W * H / W), dpi=100)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
UNIT_IN = FIG_W / W
LW = 0.6

def rbox(x, y, w, h, fc='white', ec=LINE, lw=0.6, r=1.0, z=2, ls='-', alpha=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc, ec=ec, lw=lw,
                                zorder=z, ls=ls, alpha=alpha))

def T(x, y, s, size=6, color=INK, ha='center', va='center', weight='normal', style='normal', z=14, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, fontstyle=style,
                   zorder=z, **kw)

def arrow(p0, p1, color=INK2, lw=0.8, rad=0.0, z=9, head=6.5):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=head, color=color, lw=lw, zorder=z,
                                 connectionstyle=f'arc3,rad={rad}', shrinkA=0.6, shrinkB=0.6))

def path_arrow(pts, color=INK2, lw=0.8, z=9, head=6.5):
    xs, ys = zip(*pts[:-1])
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, solid_joinstyle='round')
    arrow(pts[-2], pts[-1], color=color, lw=lw, z=z, head=head)

_img = {}
def cap(name, x, y, size, z=11):
    if name not in _img:
        _img[name] = Image.open(os.path.join(ICON_DIR, f'{name}.png')).convert('RGBA')
    im = _img[name]
    ax.add_artist(AnnotationBbox(OffsetImage(im, zoom=(size * UNIT_IN * 72.0) / max(im.size)), (x, y),
                                 frameon=False, box_alignment=(0.5, 0.5), zorder=z, pad=0))

# ------------------------------- icons -------------------------------
def i_doc(cx, cy, s, z=10):
    x0, y0, w, h, f = cx - 0.36 * s, cy - 0.5 * s, 0.72 * s, s, 0.2 * s
    ax.add_patch(Polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h - f), (x0 + w - f, y0 + h), (x0, y0 + h)],
                         closed=True, fc='white', ec=OUT, lw=LW, zorder=z))
    ax.add_patch(Polygon([(x0 + w - f, y0 + h), (x0 + w - f, y0 + h - f), (x0 + w, y0 + h - f)], closed=True,
                         fc=LINE, ec=OUT, lw=LW, zorder=z + 1))
    for k, (c, frac) in enumerate([(BLUE, .45), (LINE, .75), (LINE, .75), (LINE, .55), (GREEN, .4)]):
        yy = y0 + h - 0.28 * s - k * 0.15 * s
        ax.plot([x0 + 0.1 * s, x0 + 0.1 * s + frac * (w - 0.2 * s)], [yy, yy], color=c, lw=1.0, zorder=z + 1,
                solid_capstyle='round')

def i_net(cx, cy, s, col, z=10, box=True):
    if box: rbox(cx - 0.55 * s, cy - 0.5 * s, 1.1 * s, s, fc=LIGHT[1] if col == BLUE else '#f3f8f4', ec=col, lw=0.6,
                 r=0.12 * s, z=z)
    layers = [3, 4, 2]
    pts = [[(cx + (i - 1) * 0.36 * s, cy + (j - (n - 1) / 2) * 0.22 * s) for j in range(n)] for i, n in enumerate(layers)]
    for a, b in zip(pts[:-1], pts[1:]):
        for p in a:
            for q in b:
                ax.plot([p[0], q[0]], [p[1], q[1]], color=MUTED, lw=0.35, zorder=z + 1)
    for L in pts:
        for p in L:
            ax.add_patch(Circle(p, 0.075 * s, fc=col, ec=OUT, lw=0.45, zorder=z + 2))

def i_dice(cx, cy, s, z=10):
    for dx, dy, rot in ((-0.18, -0.08, 0), (0.2, 0.12, 0)):
        x0, y0 = cx + dx * s - 0.3 * s, cy + dy * s - 0.3 * s
        rbox(x0, y0, 0.6 * s, 0.6 * s, fc='white', ec=OUT, lw=LW, r=0.1 * s, z=z + (1 if dx > 0 else 0))
        pips = [(0.5, 0.5)] if dx < 0 else [(0.25, 0.25), (0.75, 0.75), (0.25, 0.75), (0.75, 0.25)]
        for px, py in pips:
            ax.add_patch(Circle((x0 + px * 0.6 * s, y0 + py * 0.6 * s), 0.05 * s, fc=RED if dx < 0 else OUT,
                                ec='none', zorder=z + 2 + (1 if dx > 0 else 0)))

def i_robot(cx, cy, s, fill, z=10):
    ax.plot([cx, cx], [cy + 0.30 * s, cy + 0.46 * s], color=OUT, lw=LW, zorder=z)
    ax.add_patch(Circle((cx, cy + 0.50 * s), 0.065 * s, fc=RED, ec=OUT, lw=LW, zorder=z))
    rbox(cx - 0.52 * s, cy - 0.16 * s, 0.1 * s, 0.24 * s, fc=fill, ec=OUT, lw=LW, r=0.03 * s, z=z)
    rbox(cx + 0.42 * s, cy - 0.16 * s, 0.1 * s, 0.24 * s, fc=fill, ec=OUT, lw=LW, r=0.03 * s, z=z)
    rbox(cx - 0.42 * s, cy - 0.32 * s, 0.84 * s, 0.64 * s, fc='#e4e7ed', ec=OUT, lw=0.7, r=0.13 * s, z=z + 1)
    for dx in (-0.18, 0.18):
        ax.add_patch(Circle((cx + dx * s, cy + 0.05 * s), 0.11 * s, fc='white', ec=OUT, lw=LW, zorder=z + 2))
        ax.add_patch(Circle((cx + dx * s, cy + 0.05 * s), 0.05 * s, fc=fill, ec='none', zorder=z + 3))
    rbox(cx - 0.2 * s, cy - 0.22 * s, 0.4 * s, 0.1 * s, fc='white', ec=OUT, lw=0.5, r=0.03 * s, z=z + 2)
    for dx in (-0.07, 0, 0.07):
        ax.plot([cx + dx * s] * 2, [cy - 0.22 * s, cy - 0.12 * s], color=OUT, lw=0.35, zorder=z + 3)

def i_bubble(x, y, w, h, side, icon=None, z=8, fc='white'):
    rbox(x, y, w, h, fc=fc, ec=OUT, lw=LW, r=1.4, z=z)
    if side == 'right':
        tri = [(x + w - 0.05, y + h * 0.62), (x + w + 2.0, y + h * 0.5), (x + w - 0.05, y + h * 0.36)]
    else:
        tri = [(x + 0.05, y + h * 0.62), (x - 2.0, y + h * 0.5), (x + 0.05, y + h * 0.36)]
    ax.add_patch(Polygon(tri, closed=True, fc=fc, ec='none', zorder=z + 1))
    ax.plot([tri[0][0], tri[1][0], tri[2][0]], [tri[0][1], tri[1][1], tri[2][1]], color=OUT, lw=LW, zorder=z + 1)
    x_text = x + (4.4 if icon else 1.4)
    if icon: cap(icon, x + 2.3, y + h * 0.5, 3.0, z=z + 2)
    for k, frac in enumerate((0.9, 0.7, 0.8)):
        yy = y + h - 1.8 - k * 1.6
        ax.plot([x_text, x_text + frac * (x + w - 1.2 - x_text)], [yy, yy], color=LINE, lw=1.0, zorder=z + 2,
                solid_capstyle='round')

def i_template(x, y, w, h, z=6):
    for k in (2, 1, 0):
        rbox(x + 0.8 * k, y + 0.8 * k, w, h, fc='white', ec=OUT, lw=LW, r=0.8, z=z - k)
    rows = [[(2.2, LINE), (2.2, BLUE), (3.0, LINE)], [(3.0, LINE), (2.0, ORANGE), (2.4, LINE)], [(1.8, LINE), (2.4, BLUE), (1.6, LINE)]]
    for i, row in enumerate(rows):
        xx, yy = x + 1.0, y + h - 1.8 - i * 2.0
        for L, c in row:
            if c == LINE:
                ax.plot([xx, xx + L], [yy, yy], color=LINE, lw=1.0, zorder=z + 1, solid_capstyle='round')
            else:
                rbox(xx, yy - 0.55, L, 1.1, fc=c, ec='none', r=0.3, z=z + 1, alpha=0.85)
            xx += L + 0.5

def i_meter(x, y, s, z=8):
    for k, c in enumerate(('#f6d9c4', '#eeb48c', ORANGE)):
        hh = (0.35 + 0.3 * k) * s
        rbox(x + k * 0.36 * s, y, 0.28 * s, hh, fc=c, ec=OUT, lw=0.5, r=0.05 * s, z=z)

def i_coin(cx, cy, s, alpha=1.0, z=10):
    ax.add_patch(Circle((cx, cy), 0.5 * s, fc=GOLD, ec=OUT, lw=LW, zorder=z, alpha=alpha))
    ax.add_patch(Circle((cx, cy), 0.33 * s, fc='none', ec='#8f7e3f', lw=0.45, zorder=z + 1, alpha=alpha))

def i_clipboard(cx, cy, s, z=10):
    rbox(cx - 0.36 * s, cy - 0.5 * s, 0.72 * s, 0.94 * s, fc='#b07a4f', ec=OUT, lw=LW, r=0.06 * s, z=z)
    rbox(cx - 0.28 * s, cy - 0.42 * s, 0.56 * s, 0.74 * s, fc='white', ec=OUT, lw=LW, r=0.02 * s, z=z + 1)
    rbox(cx - 0.15 * s, cy + 0.34 * s, 0.30 * s, 0.14 * s, fc=GRAY, ec=OUT, lw=LW, r=0.03 * s, z=z + 2)
    for k, ok in enumerate((True, True, True, False)):
        yy = cy + 0.20 * s - k * 0.17 * s
        ax.add_patch(Rectangle((cx - 0.21 * s, yy - 0.05 * s), 0.10 * s, 0.10 * s, fc='white', ec=OUT, lw=0.4, zorder=z + 2))
        if ok: ax.plot([cx - 0.2 * s, cx - 0.165 * s, cx - 0.10 * s], [yy, yy - 0.04 * s, yy + 0.06 * s],
                       color=GREEN, lw=0.8, zorder=z + 3)
        ax.plot([cx - 0.05 * s, cx + 0.2 * s], [yy, yy], color=LINE, lw=0.8, zorder=z + 2)

def i_scatter(cx, cy, s, z=10):
    x0, y0 = cx - 0.45 * s, cy - 0.4 * s
    rbox(x0 - 0.05 * s, y0 - 0.08 * s, 0.98 * s, 0.9 * s, fc='white', ec=OUT, lw=LW, r=0.08 * s, z=z)
    ax.plot([x0 + 0.08 * s, x0 + 0.08 * s, x0 + 0.85 * s], [y0 + 0.72 * s, y0 + 0.06 * s, y0 + 0.06 * s],
            color=OUT, lw=0.5, zorder=z + 1)
    for px, py in ((.2, .2), (.33, .36), (.45, .3), (.58, .5), (.7, .58), (.78, .66)):
        ax.add_patch(Circle((x0 + px * s, y0 + py * s), 0.035 * s, fc=BLUE, ec='none', zorder=z + 2))
    ax.plot([x0 + 0.14 * s, x0 + 0.84 * s], [y0 + 0.14 * s, y0 + 0.72 * s], color=RED, lw=0.8, zorder=z + 2)

def i_slot(cx, cy, s, z=10):
    ax.add_patch(Wedge((cx - 0.04 * s, cy + 0.2 * s), 0.30 * s, 0, 180, fc=ORANGE, ec=OUT, lw=LW, zorder=z))
    rbox(cx - 0.42 * s, cy - 0.5 * s, 0.76 * s, 0.72 * s, fc=RED, ec=OUT, lw=LW, r=0.06 * s, z=z + 1)
    rbox(cx - 0.34 * s, cy - 0.2 * s, 0.6 * s, 0.26 * s, fc='white', ec=OUT, lw=LW, r=0.03 * s, z=z + 2)
    for k in range(3):
        xx = cx - 0.24 * s + k * 0.2 * s
        T(xx, cy - 0.07 * s, '7', size=s * 0.62, color=RED, weight='bold', z=z + 4)
    rbox(cx - 0.34 * s, cy - 0.42 * s, 0.6 * s, 0.12 * s, fc=GOLD, ec=OUT, lw=LW, r=0.02 * s, z=z + 2)
    ax.plot([cx + 0.34 * s, cx + 0.46 * s, cx + 0.46 * s], [cy - 0.18 * s, cy - 0.18 * s, cy + 0.2 * s], color=OUT,
            lw=LW, zorder=z)
    ax.add_patch(Circle((cx + 0.46 * s, cy + 0.26 * s), 0.07 * s, fc=GOLD, ec=OUT, lw=LW, zorder=z + 1))

def bars(x, y_top, rows, bar_w, row_h, colors, icon_size=2.4):
    vmax = max(v for _, v in rows)
    for i, (name, v) in enumerate(rows):
        yy = y_top - i * row_h
        cap(name, x + 1.3, yy, icon_size)
        c = colors[i] if isinstance(colors, list) else colors
        ax.add_patch(Rectangle((x + 3.0, yy - row_h * 0.27), v / vmax * bar_w, row_h * 0.54, fc=c, ec=OUT, lw=0.35, zorder=6))

def badge(cx, cy, k, r=1.0):
    ax.add_patch(Circle((cx, cy), r, fc=ACC[k], ec='none', zorder=15))
    T(cx, cy - 0.05, str(k), size=4.6, color='white', weight='bold', z=16)

def module(x, w, k, title):
    rbox(x, 1.0, w, H - 2.0, fc='white', ec=ACC[k], lw=0.9, r=1.6, z=1)
    ax.add_patch(FancyBboxPatch((x, H - 6.6), w, 5.6, boxstyle='round,pad=0,rounding_size=1.6', fc=HEAD[k],
                                ec='none', zorder=1.5))
    ax.add_patch(Rectangle((x + 0.45, H - 6.6), w - 0.9, 2.0, fc=HEAD[k], ec='none', zorder=1.6))
    ax.add_patch(Circle((x + 3.2, H - 3.8), 1.9, fc=ACC[k], ec='none', zorder=3))
    T(x + 3.2, H - 3.85, str(k), size=6.6, color='white', weight='bold', z=4)
    T(x + 6.0, H - 3.8, title, size=7.0, weight='bold', ha='left')

module(1.0, 42.0, 1, 'Set capability priorities')
module(45.0, 50.0, 2, 'Generate and distill one step')
module(97.0, 42.0, 3, 'Measure and re-allocate')

# =============================== module 1 ===============================
i_doc(7.0, 44.6, 8.0); T(7.0, 38.6, 'task card', size=5.8, color=INK2)
arrow((11.3, 44.6), (15.3, 44.6))
i_net(21.5, 44.6, 8.4, BLUE); T(21.5, 38.6, r'identifier $g_\phi$', size=5.8, color=INK2)
arrow((26.4, 44.6), (29.6, 44.6))
T(35.6, 47.6, r'$\mathbf{r}_\tau$', size=7.0, weight='bold')
T(35.6, 45.2, 'capability', size=5.2, color=MUTED); T(35.6, 43.3, 'priorities', size=5.2, color=MUTED)
r_rows = [('math', .40), ('reasoning', .22), ('general', .15), ('steerability', .08),
          ('code', .06), ('tool_use', .045), ('lcu', .035), ('multilingual', .025)]
bars(3.2, 34.2, r_rows, bar_w=24.0, row_h=2.45, colors=[BLUE] * 3 + ['#b7c6df'] * 5)
ax.add_patch(FancyBboxPatch((2.8, 28.1), 37.6, 7.4, boxstyle='round,pad=0,rounding_size=0.6', fc='none', ec=BLUE,
                            lw=0.7, ls=(0, (2.2, 1.3)), zorder=7))
T(39.6, 32.6, 'prioritized', size=5.6, color=BLUE, ha='right', weight='bold')
# offline pretraining (icons only)
rbox(2.8, 2.4, 37.6, 12.2, fc='#f6f8fb', ec=BLUE, lw=0.55, ls=(0, (2.4, 1.4)), r=1.0)
T(4.0, 12.9, 'offline, once', size=5.4, color=BLUE, ha='left', weight='bold')
i_dice(9.2, 7.6, 5.4); T(9.2, 3.6, 'random mixes', size=5.0, color=INK2)
arrow((13.0, 7.6), (16.6, 7.6), head=5)
i_robot(21.2, 7.6, 4.6, BLUE); T(21.2, 3.6, 'short distill', size=5.0, color=INK2)
arrow((25.0, 7.6), (28.6, 7.6), head=5)
i_scatter(33.4, 7.9, 6.0); T(33.4, 3.6, r'fit $g_\phi$', size=5.0, color=INK2)
path_arrow([(40.6, 8.5), (41.8, 8.5), (41.8, 41.0), (26.4, 41.0)], color=BLUE, lw=0.6, head=4.8)

# =============================== module 2 ===============================
T(47.0, 50.2, r'allocation $\mathbf{w}_t$', size=6.0, weight='bold', ha='left')
bars(47.0, 46.6, [('math', .55), ('reasoning', .30), ('general', .15)], bar_w=9.0, row_h=2.8, colors=ORANGE)
T(47.0, 38.6, r'prior $\mathbf{r}_\tau$', size=5.2, color=MUTED, ha='left'); badge(55.6, 38.65, 1, r=0.9)
arrow((60.6, 44.6), (64.4, 44.6))
T(62.5, 46.4, 'sample', size=5.0, color=INK2)
i_template(65.2, 40.4, 11.2, 7.6); T(71.2, 38.4, 'templates', size=5.8, color=INK2)
i_meter(82.2, 42.6, 7.0); T(85.4, 38.4, 'curriculum', size=5.8, color=INK2)
arrow((81.8, 41.4), (90.4, 41.4), color=ORANGE, lw=0.6, head=4.2); T(86.1, 40.2, 'easy → hard', size=4.6, color=ORANGE)
# prompt -> teacher -> answer
arrow((70.0, 37.0), (61.0, 32.6), rad=0.12)
i_bubble(47.0, 23.5, 15.0, 8.6, 'right', icon='math'); T(54.5, 34.0, r'prompt $x$', size=5.6, color=INK2)
rbox(65.4, 21.4, 13.2, 13.0, fc='#fbe7d8', ec=ORANGE, lw=0.9, r=1.4, z=3)
i_robot(72.0, 29.2, 7.8, ORANGE); T(72.0, 23.4, 'teacher', size=5.8, color=ORANGE, weight='bold')
i_bubble(81.4, 23.5, 12.2, 8.6, 'left'); T(87.5, 34.0, r'answer $y$', size=5.6, color=INK2)
# distill -> student
path_arrow([(87.5, 23.2), (87.5, 13.4), (79.8, 10.2)], lw=0.8)
T(89.2, 17.6, 'distill', size=5.4, color=INK2, ha='left')
rbox(65.4, 3.0, 13.2, 13.0, fc='#dfe6f1', ec=BLUE, lw=0.9, r=1.4, z=3)
i_robot(72.0, 10.6, 6.4, BLUE); T(72.0, 5.0, r'student $S_t$', size=5.8, color=BLUE, weight='bold')
# budget
T(47.0, 16.6, r'budget $B$', size=6.0, weight='bold', ha='left')
for k in range(5):
    i_coin(48.8 + k * 3.0, 11.6, 2.7, alpha=1.0 if k == 0 else 0.35, z=10 + 3 * k)
T(47.0, 7.2, 'one slice', size=5.2, color=MUTED, ha='left'); T(47.0, 5.2, 'per step', size=5.2, color=MUTED, ha='left')

# =============================== module 3 ===============================
arrow((78.8, 9.4), (99.4, 9.4)); T(89.4, 10.9, r'$S_{t+1}$', size=5.8, color=INK2)
i_clipboard(104.0, 10.0, 8.0); T(104.0, 3.4, 'probes', size=5.8, color=INK2)
arrow((108.6, 9.4), (110.6, 9.4), head=5)
T(124.0, 16.6, r'change $\Delta\mathbf{s}_t$', size=5.8, weight='bold')
x0 = 125.4
ax.plot([x0, x0], [2.6, 14.6], color=MUTED, lw=0.5, zorder=4)
for i, (nm, v) in enumerate([('math', 1.8), ('reasoning', 0.6), ('general', 0.2), ('steerability', -0.4)]):
    yy = 13.2 - i * 3.0
    cap(nm, 114.2, yy, 2.4)
    L = v / 1.8 * 10.5; c = GREEN if v >= 0 else RED
    ax.add_patch(Rectangle((x0 if v >= 0 else x0 + L, yy - 0.8), abs(L), 1.6, fc=c, ec=OUT, lw=0.35, zorder=6))
arrow((118.0, 18.4), (118.0, 20.6), head=5)
# reward chips
T(99.4, 28.0, r'reward $\widehat{R}_t$', size=6.0, weight='bold', ha='left')
xx = 99.6
for lab, fc, col, w in (('gain', '#d5ead9', GREEN, 8.0), ('spill', '#f2d3d4', RED, 8.0), ('cost', '#e6e5e0', INK2, 8.0)):
    rbox(xx, 21.8, w, 3.6, fc=fc, ec=col, lw=0.6, r=0.8, z=5); T(xx + w / 2, 23.6, lab, size=5.8, color=col, weight='bold')
    if lab != 'cost': T(xx + w + 1.35, 23.6, '−', size=7, color=INK)
    xx += w + 2.7
badge(103.6, 26.4, 1, r=0.9)
arrow((118.0, 30.2), (118.0, 32.4), head=5)
# bandit
i_slot(103.4, 44.2, 7.6); T(103.4, 37.8, 'bandit', size=5.8, color=INK2)
for j in range(3):
    i_net(113.4 + 0.9 * j, 45.4 - 0.9 * j, 5.6, GREEN, z=10 + 4 * j)
T(114.3, 38.2, 'reward models', size=5.4, color=INK2)
arrow((119.6, 44.2), (121.6, 44.2), head=5)
for k, (m, s_) in enumerate([(.58, .05), (.52, .14), (.72, .09)]):
    cx = 124.4 + k * 4.4
    ax.add_patch(Rectangle((cx - 1.4, 40.2), 2.8, m * 8.0, fc=GREEN if k == 2 else '#b9dbc2', ec=OUT, lw=0.35,
                           zorder=5, hatch='////' if k == 2 else None))
    lo, hi = 40.2 + (m - s_) * 8.0, 40.2 + (m + s_) * 8.0
    ax.plot([cx, cx], [lo, hi], color=INK, lw=0.55, zorder=6)
    for yy in (lo, hi): ax.plot([cx - 0.5, cx + 0.5], [yy, yy], color=INK, lw=0.55, zorder=6)
T(128.8, 38.2, r'UCB: $\mu+\kappa\sigma$', size=5.4, color=INK2)
T(133.2, 49.6, r'$\mathbf{w}_{t+1}$', size=5.8, color=GREEN, weight='bold')
# loop
path_arrow([(118.0, 50.8), (118.0, 52.3), (60.0, 52.3), (60.0, 50.6)], color=GREEN, lw=1.0, head=6)
T(89.0, 52.3, r'  next step with $\mathbf{w}_{t+1}$  ', size=5.6, color=GREEN, weight='bold',
  bbox=dict(fc='white', ec='none', pad=0.2))

fig.savefig(OUT_PDF); fig.savefig(OUT_PNG, dpi=240)
print('wrote', OUT_PDF, OUT_PNG)
