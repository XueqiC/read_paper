#!/usr/bin/env python3
"""ReAD method overview figure, v3: matches the paper's original figures.

Style: Times bold text, seaborn-deep accents (#4C72B0 blue, #DD8452 orange, #55A868 green,
#C44E52 red) as in the original matplotlib figures, and hand-drawn flat icons with dark outlines
in the same "lineal color" style as the capability icons of Figure 1 (no emoji).
"""
import sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle, Wedge, Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, 'icons')
OUT_PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'overview.pdf')
OUT_PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'overview_preview.png')

BLUE, ORANGE, GREEN, RED, GOLD, GRAY = '#4C72B0', '#DD8452', '#55A868', '#C44E52', '#CCB974', '#8C8C8C'
INK, INK2, MUTED, EDGE, CARD, OUT = '#1d1d1b', '#3f3e3a', '#7a7974', '#cfcdc4', '#ffffff', '#2E3440'
TINT = {'1': '#e9eef6', '2': '#fbefe6', '3': '#e8f2ea'}
ACC = {'1': BLUE, '2': ORANGE, '3': GREEN}
LIGHT_BLUE = '#b3c4e0'
plt.rcParams.update({'font.family': 'Times New Roman', 'font.weight': 'bold', 'font.size': 6,
                     'pdf.fonttype': 42, 'mathtext.fontset': 'custom',
                     'mathtext.rm': 'Times New Roman:bold', 'mathtext.it': 'Times New Roman:bold:italic',
                     'mathtext.bf': 'Times New Roman:bold'})

W, H = 140.0, 60.0
FIG_W = 5.0
fig = plt.figure(figsize=(FIG_W, FIG_W * H / W), dpi=100)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
UNIT_IN = FIG_W / W
LW = 0.7  # icon outline width (pt)

def rbox(x, y, w, h, fc=CARD, ec=EDGE, lw=0.6, r=1.2, z=2, alpha=1.0, ls='-'):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc, ec=ec, lw=lw,
                       zorder=z, alpha=alpha, ls=ls)
    ax.add_patch(p); return p

def text(x, y, s, size=6, color=INK, ha='left', va='center', weight='bold', style='normal', z=12, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, fontstyle=style,
                   zorder=z, **kw)

def arrow(p0, p1, color=INK2, lw=0.85, rad=0.0, z=9, head=7):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=head, color=color, lw=lw, zorder=z,
                                 connectionstyle=f'arc3,rad={rad}', shrinkA=0.8, shrinkB=0.8))

def polyarrow(pts, color=INK2, lw=1.0, z=9, head=8):
    xs, ys = zip(*pts[:-1])
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, solid_joinstyle='round', solid_capstyle='round')
    arrow(pts[-2], pts[-1], color=color, lw=lw, z=z, head=head)

_img = {}
def cap_icon(name, x, y, size, z=10):
    if name not in _img:
        _img[name] = Image.open(os.path.join(ICON_DIR, f'{name}.png')).convert('RGBA')
    im = _img[name]
    zoom = (size * UNIT_IN * 72.0) / max(im.width, im.height)
    ax.add_artist(AnnotationBbox(OffsetImage(im, zoom=zoom), (x, y), frameon=False,
                                 box_alignment=(0.5, 0.5), zorder=z, pad=0))

# ---------------- hand-drawn icons (flat fill + dark outline) ----------------
def icon_robot(cx, cy, s, fill, z=10):
    rbox(cx - 0.5 * s, cy - 0.44 * s, 0.10 * s, 0.26 * s, fc=fill, ec=OUT, lw=LW, r=0.03 * s, z=z)           # ears
    rbox(cx + 0.40 * s, cy - 0.44 * s, 0.10 * s, 0.26 * s, fc=fill, ec=OUT, lw=LW, r=0.03 * s, z=z)
    ax.plot([cx, cx], [cy + 0.02 * s, cy + 0.26 * s], color=OUT, lw=LW, zorder=z)                          # antenna
    ax.add_patch(Circle((cx, cy + 0.31 * s), 0.07 * s, fc=RED, ec=OUT, lw=LW, zorder=z + 1))
    rbox(cx - 0.40 * s, cy - 0.62 * s, 0.80 * s, 0.64 * s, fc='#dfe3ea', ec=OUT, lw=LW, r=0.12 * s, z=z + 1)  # head
    for dx in (-0.18, 0.18):                                                                                # eyes
        ax.add_patch(Circle((cx + dx * s, cy - 0.20 * s), 0.11 * s, fc='white', ec=OUT, lw=LW, zorder=z + 2))
        ax.add_patch(Circle((cx + dx * s, cy - 0.20 * s), 0.05 * s, fc=fill, ec=OUT, lw=0.4, zorder=z + 3))
    rbox(cx - 0.20 * s, cy - 0.50 * s, 0.40 * s, 0.10 * s, fc='white', ec=OUT, lw=LW, r=0.03 * s, z=z + 2)   # mouth
    for dx in (-0.07, 0.0, 0.07):
        ax.plot([cx + dx * s] * 2, [cy - 0.50 * s, cy - 0.40 * s], color=OUT, lw=0.4, zorder=z + 3)

def icon_slot(cx, cy, s, z=10):
    ax.add_patch(Wedge((cx - 0.04 * s, cy + 0.20 * s), 0.30 * s, 0, 180, fc=ORANGE, ec=OUT, lw=LW, zorder=z))
    rbox(cx - 0.42 * s, cy - 0.50 * s, 0.76 * s, 0.72 * s, fc=RED, ec=OUT, lw=LW, r=0.06 * s, z=z + 1)
    rbox(cx - 0.34 * s, cy - 0.20 * s, 0.60 * s, 0.26 * s, fc='white', ec=OUT, lw=LW, r=0.03 * s, z=z + 2)
    for k in range(3):
        xx = cx - 0.24 * s + k * 0.20 * s
        text(xx, cy - 0.07 * s, '7', size=0.30 * s * 2.2, color=RED, ha='center', z=z + 4)
        if k: ax.plot([xx - 0.10 * s] * 2, [cy - 0.20 * s, cy + 0.06 * s], color=OUT, lw=0.4, zorder=z + 3)
    rbox(cx - 0.34 * s, cy - 0.42 * s, 0.60 * s, 0.12 * s, fc=GOLD, ec=OUT, lw=LW, r=0.02 * s, z=z + 2)
    ax.plot([cx + 0.34 * s, cx + 0.46 * s, cx + 0.46 * s], [cy - 0.18 * s, cy - 0.18 * s, cy + 0.20 * s],
            color=OUT, lw=LW, zorder=z)
    ax.add_patch(Circle((cx + 0.46 * s, cy + 0.26 * s), 0.07 * s, fc=GOLD, ec=OUT, lw=LW, zorder=z + 1))

def icon_coin(cx, cy, s, alpha=1.0, z=10):
    ax.add_patch(Circle((cx, cy), 0.5 * s, fc=GOLD, ec=OUT, lw=LW, zorder=z, alpha=alpha))
    ax.add_patch(Circle((cx, cy), 0.34 * s, fc='none', ec='#9a8747', lw=0.5, zorder=z + 1, alpha=alpha))
    text(cx, cy - 0.02 * s, '$', size=0.5 * s * 2.2, color='#6f6232', ha='center', z=z + 2, alpha=alpha)

def icon_clipboard(cx, cy, s, z=10):
    rbox(cx - 0.36 * s, cy - 0.5 * s, 0.72 * s, 0.94 * s, fc='#b07a4f', ec=OUT, lw=LW, r=0.06 * s, z=z)
    rbox(cx - 0.28 * s, cy - 0.42 * s, 0.56 * s, 0.74 * s, fc='white', ec=OUT, lw=LW, r=0.02 * s, z=z + 1)
    rbox(cx - 0.15 * s, cy + 0.34 * s, 0.30 * s, 0.14 * s, fc=GRAY, ec=OUT, lw=LW, r=0.03 * s, z=z + 2)
    for k, ok in enumerate((True, True, True, False)):
        yy = cy + 0.20 * s - k * 0.17 * s
        ax.add_patch(Rectangle((cx - 0.21 * s, yy - 0.05 * s), 0.10 * s, 0.10 * s, fc='white', ec=OUT, lw=0.45,
                               zorder=z + 2))
        if ok: ax.plot([cx - 0.20 * s, cx - 0.165 * s, cx - 0.10 * s], [yy, yy - 0.04 * s, yy + 0.06 * s],
                       color=GREEN, lw=0.8, zorder=z + 3)
        ax.plot([cx - 0.05 * s, cx + 0.20 * s], [yy, yy], color=EDGE, lw=0.7, zorder=z + 2)

def icon_card(cx, cy, s, z=10):
    x0, y0, w, h, f = cx - 0.34 * s, cy - 0.46 * s, 0.62 * s, 0.86 * s, 0.16 * s
    ax.add_patch(Polygon([(x0, y0), (x0 + w, y0), (x0 + w, y0 + h - f), (x0 + w - f, y0 + h), (x0, y0 + h)],
                         closed=True, fc='white', ec=OUT, lw=LW, zorder=z))
    ax.add_patch(Polygon([(x0 + w - f, y0 + h), (x0 + w - f, y0 + h - f), (x0 + w, y0 + h - f)], closed=True,
                         fc=EDGE, ec=OUT, lw=LW, zorder=z + 1))
    for k in range(4):
        yy = y0 + h - 0.24 * s - k * 0.15 * s
        ax.plot([x0 + 0.09 * s, x0 + w - (0.24 if k == 0 else 0.10) * s], [yy, yy], color=BLUE if k == 0 else EDGE,
                lw=0.8, zorder=z + 1)
    # pencil
    px, py = cx + 0.30 * s, cy - 0.30 * s
    ax.add_patch(Polygon([(px - 0.05 * s, py + 0.02 * s), (px + 0.20 * s, py + 0.50 * s),
                          (px + 0.29 * s, py + 0.45 * s), (px + 0.04 * s, py - 0.03 * s)],
                         closed=True, fc=GOLD, ec=OUT, lw=LW, zorder=z + 2))
    ax.add_patch(Polygon([(px - 0.05 * s, py + 0.02 * s), (px + 0.04 * s, py - 0.03 * s), (px - 0.06 * s, py - 0.10 * s)],
                         closed=True, fc='#f1d9b5', ec=OUT, lw=LW, zorder=z + 2))

def hbars(x, y_top, rows, bar_w, row_h, colors, icon_size=3.2):
    vmax = max(v for _, v in rows)
    for i, (name, v) in enumerate(rows):
        yy = y_top - i * row_h
        cap_icon(name, x + 1.7, yy, icon_size)
        c = colors[i] if isinstance(colors, list) else colors
        ax.add_patch(Rectangle((x + 4.0, yy - row_h * 0.27), (v / vmax) * bar_w, row_h * 0.54, fc=c, ec=OUT,
                               lw=0.45, zorder=6))

def panel(x, w, num, title):
    rbox(x, 1.2, w, H - 2.4, fc=TINT[num], ec='none', r=2.2, z=1)
    ax.add_patch(Circle((x + 3.4, H - 4.4), 2.15, fc=ACC[num], ec=OUT, lw=0.5, zorder=5))
    text(x + 3.4, H - 4.5, num, size=6.8, color='white', ha='center', z=6)
    text(x + 6.7, H - 4.4, title, size=7.2, color=INK)

panel(1.0, 38.0, '1', 'What does the task need?')
panel(41.5, 57.0, '2', 'Spend one slice of the budget')
panel(100.5, 38.5, '3', 'Measure and re-allocate')

# ============================== stage 1 ==============================
rbox(3.5, 39.0, 33.5, 11.0, z=3, ec=OUT, lw=0.5)
icon_card(7.0, 47.0, 5.0)
text(11.0, 46.9, 'Task card', size=6.6)
text(5.0, 42.5, 'Q: 3 pens cost \\$4.50.', size=5.6, color=INK2, weight='normal', style='italic')
text(5.0, 40.3, '    How much are 7 pens?', size=5.6, color=INK2, weight='normal', style='italic')
arrow((20.2, 38.7), (20.2, 34.7))
text(21.6, 36.7, 'identifier $g_\\phi$', size=5.8, color=INK2)
text(3.8, 32.4, 'requirement $\\mathbf{r}_\\tau$', size=6.6)
r_rows = [('math', .40), ('reasoning', .22), ('general', .15), ('steerability', .08),
          ('code', .06), ('tool_use', .045), ('lcu', .035), ('multilingual', .025)]
hbars(4.2, 28.6, r_rows, bar_w=24, row_h=3.3, colors=[BLUE] * 3 + [LIGHT_BLUE] * 5)
ax.add_patch(FancyBboxPatch((3.3, 20.5), 33.9, 9.9, boxstyle='round,pad=0,rounding_size=0.8', fc='none', ec=BLUE,
                            lw=0.8, ls=(0, (2.2, 1.4)), zorder=7))
text(36.4, 21.9, 'essential', size=5.6, color=BLUE, ha='right')

# ============================== stage 2 ==============================
text(44.2, 50.2, 'allocation $\\mathbf{w}_t$', size=6.6)
hbars(44.4, 46.6, [('math', .55), ('reasoning', .30), ('general', .15)], bar_w=10.5, row_h=3.4, colors=BLUE)
arrow((37.6, 25.5), (44.3, 42.0), rad=-0.32)
text(40.9, 32.0, 'prior', size=5.4, color=INK2, ha='center', rotation=66)
# template library: stacked cards with typed slots
for k in range(3):
    rbox(64.0 + 0.9 * k, 38.2 + 0.9 * k, 10.0, 9.2, z=3 - k, ec=OUT, lw=0.5)
for i, (yy, wslot, cslot) in enumerate([(44.6, 3.2, BLUE), (42.6, 2.4, ORANGE)]):
    ax.plot([65.2, 67.4], [yy, yy], color=MUTED, lw=0.8, zorder=5)
    rbox(67.8, yy - 0.7, wslot, 1.4, fc=cslot, ec=OUT, lw=0.4, r=0.4, z=5, alpha=0.85)
    ax.plot([67.8 + wslot + 0.4, 72.6], [yy, yy], color=MUTED, lw=0.8, zorder=5)
text(69.0, 39.9, 'templates', size=5.6, color=INK2, ha='center')
arrow((58.4, 43.2), (63.8, 43.2))
text(60.8, 45.0, 'sample', size=5.2, color=INK2, ha='center')
def prompt(x, y, name, l1, l2):
    rbox(x, y, 20.2, 7.4, z=3, ec=OUT, lw=0.5)
    cap_icon(name, x + 2.3, y + 3.7, 3.4)
    text(x + 4.5, y + 5.0, l1, size=5.3, color=INK2, weight='normal', style='italic')
    text(x + 4.5, y + 2.5, l2, size=5.3, color=INK2, weight='normal', style='italic')
prompt(77.0, 42.2, 'math', '3 pens cost \\$4.50;', 'how much are 7?')
prompt(77.0, 33.6, 'reasoning', 'All A are B, some B', 'are C. Some A are C?')
arrow((75.3, 43.0), (76.8, 43.0))
# teacher
rbox(77.0, 17.0, 20.2, 12.8, fc='#f8e1d0', ec=ORANGE, lw=1.0, r=1.6, z=3)
icon_robot(82.3, 25.4, 7.6, ORANGE)
text(87.3, 25.9, 'Teacher', size=6.8, color=ORANGE)
text(87.3, 22.6, '70B', size=5.8, color=INK2, weight='normal')
text(87.3, 20.2, 'frozen', size=5.8, color=INK2, weight='normal')
arrow((87.1, 33.4), (87.1, 30.0))
text(88.3, 31.7, '$x$', size=6.0, color=INK2)
# answer bubble
rbox(51.0, 19.5, 23.0, 8.2, r=2.0, z=3, ec=OUT, lw=0.5)
ax.add_patch(Polygon([(73.9, 24.8), (76.8, 23.4), (73.9, 22.2)], closed=True, fc=CARD, ec='none', zorder=4))
ax.plot([73.95, 76.8, 73.95], [24.8, 23.4, 22.2], color=OUT, lw=0.5, zorder=4)
text(62.5, 25.3, '$y$: "Each pen is \\$1.50,', size=5.5, color=INK2, ha='center', weight='normal', style='italic')
text(62.5, 22.3, 'so 7 pens cost \\$10.50."', size=5.5, color=INK2, ha='center', weight='normal', style='italic')
# student
rbox(60.0, 4.0, 19.0, 11.4, fc='#dbe3f0', ec=BLUE, lw=1.0, r=1.6, z=3)
icon_robot(64.2, 11.3, 6.0, BLUE)
text(68.6, 11.6, 'Student', size=6.8, color=BLUE)
text(68.6, 8.2, '8B, trained', size=5.8, color=INK2, weight='normal')
arrow((62.5, 19.3), (66.0, 15.6))
text(58.8, 17.3, 'distill on $(x, y)$', size=5.4, color=INK2, ha='right')
# budget coins
text(44.2, 13.3, 'budget $B$', size=6.2)
for k in range(5):
    icon_coin(45.9 + k * 3.1, 9.2, 2.7, alpha=1.0 if k == 0 else 0.35, z=10 + 3 * k)
text(44.2, 5.3, 'one slice per step', size=5.2, color=MUTED, weight='normal')

# ============================== stage 3 ==============================
arrow((79.3, 9.7), (103.0, 9.7))
text(91.2, 11.3, 'test', size=5.4, color=INK2, ha='center')
icon_clipboard(106.6, 11.6, 7.0)
text(106.6, 5.0, 'probes', size=5.6, color=INK2, ha='center')
text(112.2, 17.9, 'change $\\Delta\\mathbf{s}_t$', size=6.4)
ds = [('math', 1.8), ('reasoning', 0.6), ('general', 0.2), ('steerability', -0.4)]
x0 = 121.4
ax.plot([x0, x0], [3.8, 16.2], color=MUTED, lw=0.5, zorder=4)
for i, (nm, v) in enumerate(ds):
    yy = 14.6 - i * 3.2
    cap_icon(nm, 113.6, yy, 3.0)
    L = v / 1.8 * 9.0; c = GREEN if v >= 0 else RED
    ax.add_patch(Rectangle((x0 if v >= 0 else x0 + L, yy - 0.95), abs(L), 1.9, fc=c, ec=OUT, lw=0.45, zorder=6))
    text(x0 + L + (0.6 if v >= 0 else -0.6), yy, f'{v:+.1f}', size=5.2, color=c, ha='left' if v >= 0 else 'right')
arrow((126.0, 19.4), (126.0, 22.4))
# reward
rbox(103.0, 22.6, 34.0, 9.4, z=3, ec=OUT, lw=0.5)
text(120.0, 29.8, 'reward $\\widehat{R}_t$', size=6.4, ha='center')
for (cx, w, lab, fc, col) in [(108.3, 7.4, 'gain', '#d7ebdc', GREEN), (119.6, 10.8, 'spillover', '#f3d6d7', RED),
                              (131.2, 7.2, 'cost', '#e7e6e1', INK2)]:
    rbox(cx - w / 2, 24.2, w, 3.2, fc=fc, ec=col, lw=0.6, r=0.8, z=4)
    text(cx, 25.8, lab, size=5.8, color=col, ha='center')
text(113.1, 25.8, '$-$', size=6.2, ha='center'); text(126.1, 25.8, '$-$', size=6.2, ha='center')
arrow((120.0, 32.3), (120.0, 35.0))
# bandit
rbox(103.0, 35.2, 34.0, 15.3, z=3, ec=OUT, lw=0.5)
icon_slot(107.4, 45.4, 7.0)
text(112.0, 47.6, 'bandit picks $\\mathbf{w}_{t+1}$', size=6.4)
text(112.0, 44.8, 'UCB: $\\mu + \\kappa\\,\\sigma$', size=5.6, color=MUTED, weight='normal')
for k, (lab, m, s) in enumerate([('keep', .60, .05), ('+math', .56, .13), ('+reason', .72, .09)]):
    cx = 115.0 + k * 7.6
    ax.add_patch(Rectangle((cx - 1.8, 38.2), 3.6, m * 6.5, fc=BLUE if k == 2 else LIGHT_BLUE, ec=OUT, lw=0.45,
                           zorder=4, hatch='///' if k == 2 else None))
    ax.plot([cx, cx], [38.2 + (m - s) * 6.5, 38.2 + (m + s) * 6.5], color=INK, lw=0.6, zorder=5)
    for yy in (38.2 + (m - s) * 6.5, 38.2 + (m + s) * 6.5):
        ax.plot([cx - 0.6, cx + 0.6], [yy, yy], color=INK, lw=0.6, zorder=5)
    text(cx, 36.9, lab, size=5.0, color=INK2, ha='center', weight='normal')
text(130.2, 45.0, 'chosen', size=5.4, color=BLUE, ha='center')
# feedback loop
polyarrow([(120.0, 50.7), (120.0, 53.0), (60.5, 53.0), (60.5, 50.1)], color=BLUE, lw=1.2)
text(80.0, 51.6, 'next step $t\\!+\\!1$, until $B$ is spent', size=5.8, color=BLUE, ha='center')

fig.savefig(OUT_PDF)
fig.savefig(OUT_PNG, dpi=220)
print('wrote', OUT_PDF, OUT_PNG)
