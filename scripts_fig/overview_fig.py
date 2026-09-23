#!/usr/bin/env python3
"""ReAD method overview figure, v2 (matplotlib -> vector PDF; icons embedded as PNG).

Design rules: three stages left->right, one pastel tint + matching badge per stage,
short labels only, one accent color for the feedback loop, pictures instead of words
(robots = LLMs, slot machine = contextual bandit, coins = token budget, clipboard = probes).
"""
import sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon, Circle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, 'icons')
OUT_PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'overview.pdf')
OUT_PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'overview_preview.png')

BLUE, ORANGE, GREEN, RED = '#2a78d6', '#eb6834', '#1baf7a', '#e34948'
INK, INK2, MUTED, EDGE, CARD = '#1d1d1b', '#4a4945', '#8a8983', '#d6d5ce', '#ffffff'
TINT = {'1': '#edf3fc', '2': '#fdf2ea', '3': '#eaf6f0'}
ACC = {'1': BLUE, '2': ORANGE, '3': GREEN}
plt.rcParams.update({'font.family': 'Arial', 'font.size': 5, 'pdf.fonttype': 42,
                     'mathtext.fontset': 'custom', 'mathtext.rm': 'Arial',
                     'mathtext.it': 'Arial:italic', 'mathtext.bf': 'Arial:bold'})

W, H = 140.0, 60.0
FIG_W = 5.0
fig = plt.figure(figsize=(FIG_W, FIG_W * H / W), dpi=100)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
UNIT_IN = FIG_W / W

def box(x, y, w, h, fc=CARD, ec=EDGE, lw=0.6, r=1.2, z=2, ls='-'):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}',
                                fc=fc, ec=ec, lw=lw, zorder=z, ls=ls))

def text(x, y, s, size=5, color=INK, ha='left', va='center', weight='normal', style='normal', z=9, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight,
                   fontstyle=style, zorder=z, **kw)

def arrow(p0, p1, color=INK2, lw=0.8, rad=0.0, z=7, head=7):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=head, color=color, lw=lw,
                                 zorder=z, connectionstyle=f'arc3,rad={rad}', shrinkA=0.8, shrinkB=0.8))

def polyarrow(pts, color=INK2, lw=0.9, z=7, head=8):
    xs, ys = zip(*pts[:-1])
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, solid_joinstyle='round', solid_capstyle='round')
    arrow(pts[-2], pts[-1], color=color, lw=lw, z=z, head=head)

_img = {}
def img(name, x, y, size, z=8, alpha=1.0):
    key = (name, alpha)
    if key not in _img:
        im = Image.open(os.path.join(ICON_DIR, f'{name}.png')).convert('RGBA')
        if alpha < 1:
            a = np.array(im); a[..., 3] = (a[..., 3] * alpha).astype(np.uint8); im = Image.fromarray(a)
        _img[key] = im
    im = _img[key]
    zoom = (size * UNIT_IN * 72.0) / max(im.width, im.height)
    ax.add_artist(AnnotationBbox(OffsetImage(im, zoom=zoom), (x, y), frameon=False,
                                 box_alignment=(0.5, 0.5), zorder=z, pad=0))

def hbars(x, y_top, rows, bar_w, row_h, colors, icon_size=3.0):
    vmax = max(v for _, v in rows)
    for i, (name, v) in enumerate(rows):
        yy = y_top - i * row_h
        img(name, x + 1.6, yy, icon_size)
        c = colors[i] if isinstance(colors, list) else colors
        ax.add_patch(FancyBboxPatch((x + 3.8, yy - row_h * 0.28), (v / vmax) * bar_w, row_h * 0.56,
                                    boxstyle='round,pad=0,rounding_size=0.5', fc=c, ec='none', zorder=5))

def panel(x, w, num, title):
    box(x, 1.2, w, H - 2.4, fc=TINT[num], ec='none', r=2.2, z=1)
    ax.add_patch(Circle((x + 3.4, H - 4.4), 2.1, fc=ACC[num], ec='none', zorder=5))
    text(x + 3.4, H - 4.45, num, size=6.0, color='white', ha='center', weight='bold', z=6)
    text(x + 6.6, H - 4.4, title, size=6.2, weight='bold', color=INK)

panel(1.0, 38.0, '1', 'What does the task need?')
panel(41.5, 57.0, '2', 'Spend one slice of the budget')
panel(100.5, 38.5, '3', 'Measure and re-allocate')

# ============================== stage 1 ==============================
box(3.5, 39.0, 33.5, 11.0, z=3)
img('emoji_memo', 6.9, 46.6, 4.4)
text(10.2, 46.8, 'Task card', size=5.6, weight='bold')
text(5.0, 42.9, 'Q: 3 pens cost \\$4.50.', size=4.8, color=INK2, style='italic')
text(5.0, 40.6, '    How much are 7 pens?', size=4.8, color=INK2, style='italic')
arrow((20.2, 38.7), (20.2, 34.7))
text(21.6, 36.7, 'identifier $g_\\phi$', size=4.8, color=INK2)
text(3.8, 32.4, 'requirement $\\mathbf{r}_\\tau$', size=5.6, weight='bold')
r_rows = [('math', .40), ('reasoning', .22), ('general', .15), ('steerability', .08),
          ('code', .06), ('tool_use', .045), ('lcu', .035), ('multilingual', .025)]
LIGHT_BLUE = '#b9d0f0'
hbars(4.2, 28.6, r_rows, bar_w=24, row_h=3.3, colors=[BLUE] * 3 + [LIGHT_BLUE] * 5)
ax.add_patch(FancyBboxPatch((3.3, 20.5), 33.9, 9.9, boxstyle='round,pad=0,rounding_size=0.8',
                            fc='none', ec=BLUE, lw=0.7, ls=(0, (2.2, 1.4)), zorder=6))
text(36.4, 21.9, 'essential', size=4.6, color=BLUE, ha='right', weight='bold')

# ============================== stage 2 ==============================
text(44.2, 50.2, 'allocation $\\mathbf{w}_t$', size=5.6, weight='bold')
hbars(44.4, 46.6, [('math', .55), ('reasoning', .30), ('general', .15)], bar_w=10.5, row_h=3.4, colors=BLUE)
arrow((37.6, 25.5), (44.3, 42.0), rad=-0.32)
text(40.9, 32.0, 'prior', size=4.4, color=INK2, ha='center', rotation=66)
# templates
for k in range(3):
    box(64.0 + 0.9 * k, 38.2 + 0.9 * k, 10.0, 9.2, z=3 - k)
img('emoji_puzzle', 69.0, 44.2, 5.2)
text(69.0, 39.8, 'templates', size=4.6, color=INK2, ha='center', weight='bold')
arrow((58.4, 43.2), (63.8, 43.2))
text(61.1, 45.0, 'sample', size=4.4, color=INK2, ha='center')
# prompts
def prompt(x, y, name, l1, l2):
    box(x, y, 20.2, 7.4, z=3)
    img(name, x + 2.2, y + 3.7, 3.3)
    text(x + 4.3, y + 5.0, l1, size=4.5, color=INK2, style='italic')
    text(x + 4.3, y + 2.5, l2, size=4.5, color=INK2, style='italic')
prompt(77.0, 42.2, 'math', '3 pens cost \\$4.50;', 'how much are 7?')
prompt(77.0, 33.6, 'reasoning', 'All A are B, some B', 'are C. Some A are C?')
arrow((75.3, 43.0), (76.8, 43.0))
# teacher
box(77.0, 17.0, 20.2, 12.8, fc='#fde6d9', ec=ORANGE, lw=0.9, r=1.6, z=3)
img('emoji_robot', 81.8, 23.4, 7.6)
text(86.8, 25.9, 'Teacher', size=5.6, weight='bold', color=ORANGE)
text(86.8, 22.6, '70B', size=4.8, color=INK2)
text(86.8, 20.2, 'frozen', size=4.8, color=INK2)
arrow((87.1, 33.4), (87.1, 30.0))
text(88.3, 31.7, '$x$', size=5.0, color=INK2)
# answer bubble
box(51.0, 19.5, 23.0, 8.2, r=2.0, z=3)
ax.add_patch(Polygon([(73.9, 24.8), (76.8, 23.4), (73.9, 22.2)], closed=True, fc=CARD, ec='none', zorder=4))
ax.plot([73.95, 76.8, 73.95], [24.8, 23.4, 22.2], color=EDGE, lw=0.6, zorder=4)
text(62.5, 25.3, '$y$: "Each pen is \\$1.50,', size=4.6, color=INK2, ha='center', style='italic')
text(62.5, 22.3, 'so 7 pens cost \\$10.50."', size=4.6, color=INK2, ha='center', style='italic')
# student
box(60.0, 4.0, 19.0, 11.4, fc='#dde9f9', ec=BLUE, lw=0.9, r=1.6, z=3)
img('emoji_robot', 64.0, 9.7, 6.0)
text(68.3, 11.6, 'Student', size=5.6, weight='bold', color=BLUE)
text(68.3, 8.2, '8B, trained', size=4.8, color=INK2)
arrow((62.5, 19.3), (66.0, 15.6))
text(58.8, 17.3, 'distill on $(x, y)$', size=4.4, color=INK2, ha='right')
# budget coins
text(44.2, 13.3, 'budget $B$', size=5.2, weight='bold')
for k in range(5):
    img('emoji_coin', 45.8 + k * 3.1, 9.2, 2.8, alpha=1.0 if k == 0 else 0.35, z=8 + k)
text(44.2, 5.3, 'one slice per step', size=4.2, color=MUTED)

# ============================== stage 3 ==============================
arrow((79.3, 9.7), (103.0, 9.7))
text(91.2, 11.3, 'test', size=4.4, color=INK2, ha='center')
img('emoji_clipboard', 106.5, 11.2, 7.2)
text(106.5, 5.2, 'probes', size=4.6, color=INK2, ha='center', weight='bold')
text(112.2, 17.9, 'change $\\Delta\\mathbf{s}_t$', size=5.4, weight='bold')
ds = [('math', 1.8), ('reasoning', 0.6), ('general', 0.2), ('steerability', -0.4)]
x0 = 121.4
ax.plot([x0, x0], [3.8, 16.2], color=MUTED, lw=0.5, zorder=4)
for i, (nm, v) in enumerate(ds):
    yy = 14.6 - i * 3.2
    img(nm, 113.6, yy, 2.9)
    L = v / 1.8 * 9.0; c = GREEN if v >= 0 else RED
    ax.add_patch(FancyBboxPatch((x0 if v >= 0 else x0 + L, yy - 0.95), abs(L), 1.9,
                                boxstyle='round,pad=0,rounding_size=0.4', fc=c, ec='none', zorder=5))
    text(x0 + L + (0.6 if v >= 0 else -0.6), yy, f'{v:+.1f}', size=4.2, color=c,
         ha='left' if v >= 0 else 'right', weight='bold')
arrow((126.0, 19.4), (126.0, 22.4))
# reward
box(103.0, 22.6, 34.0, 9.4, z=3)
text(120.0, 29.8, 'reward $\\widehat{R}_t$', size=5.4, weight='bold', ha='center')
for (cx, w, lab, fc, col) in [(108.3, 7.2, 'gain', '#d5f1e5', GREEN), (119.6, 10.4, 'spillover', '#fadada', RED),
                              (131.1, 7.0, 'cost', '#e9e8e4', INK2)]:
    ax.add_patch(FancyBboxPatch((cx - w / 2, 24.2), w, 3.2, boxstyle='round,pad=0,rounding_size=0.8',
                                fc=fc, ec='none', zorder=4))
    text(cx, 25.8, lab, size=4.9, color=col, ha='center', weight='bold')
text(113.1, 25.8, '$-$', size=5.4, ha='center'); text(126.1, 25.8, '$-$', size=5.4, ha='center')
arrow((120.0, 32.3), (120.0, 35.0))
# bandit
box(103.0, 35.2, 34.0, 15.3, z=3)
img('emoji_slot', 107.2, 45.4, 7.0)
text(111.6, 47.6, 'bandit picks $\\mathbf{w}_{t+1}$', size=5.4, weight='bold')
text(111.6, 44.8, 'UCB: $\\mu + \\kappa\\,\\sigma$', size=4.6, color=MUTED)
for k, (lab, m, s) in enumerate([('keep', .60, .05), ('+math', .56, .13), ('+reason', .72, .09)]):
    cx = 115.0 + k * 7.6
    ax.add_patch(FancyBboxPatch((cx - 1.8, 38.2), 3.6, m * 6.5, boxstyle='round,pad=0,rounding_size=0.4',
                                fc=BLUE if k == 2 else '#c7d8f0', ec='none', zorder=4))
    ax.plot([cx, cx], [38.2 + (m - s) * 6.5, 38.2 + (m + s) * 6.5], color=INK, lw=0.6, zorder=5)
    text(cx, 36.9, lab, size=4.1, color=INK2, ha='center')
text(132.9, 40.6, 'chosen', size=4.4, color=BLUE, weight='bold', ha='left')
# feedback loop
polyarrow([(120.0, 50.7), (120.0, 53.0), (60.5, 53.0), (60.5, 50.1)], color=BLUE, lw=1.1)
text(80.0, 51.6, 'next step $t\\!+\\!1$, until $B$ is spent', size=4.8, color=BLUE, ha='center', weight='bold')

fig.savefig(OUT_PDF)
fig.savefig(OUT_PNG, dpi=220)
print('wrote', OUT_PDF, OUT_PNG)
