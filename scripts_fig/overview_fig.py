#!/usr/bin/env python3
"""ReAD method overview, v4: a technical architecture diagram.

Three modules (white boxes with colored header strips) show the actual components and
equations of Section 3; regular-weight STIX (Times-like) text, bold only for titles;
seaborn-deep accents as in the original figures; capability icons from Figure 1.
"""
import sys, os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ICON_DIR = os.path.join(HERE, 'icons')
OUT_PDF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', 'figure', 'overview.pdf')
OUT_PNG = sys.argv[2] if len(sys.argv) > 2 else os.path.join(HERE, 'overview_preview.png')

BLUE, ORANGE, GREEN, RED = '#4C72B0', '#DD8452', '#55A868', '#C44E52'
INK, INK2, MUTED, LINE, OUT = '#1b1b1b', '#3a3a3a', '#7d7d7d', '#b9b9b9', '#2E3440'
HEAD = {1: '#dde5f1', 2: '#f8e4d4', 3: '#dcede1'}
FILL = {1: '#eef2f8', 2: '#fcf1e8', 3: '#edf6ef'}
ACC = {1: BLUE, 2: ORANGE, 3: GREEN}
plt.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix', 'font.size': 5.4, 'pdf.fonttype': 42})

W, H = 140.0, 66.0
FIG_W = 5.5
fig = plt.figure(figsize=(FIG_W, FIG_W * H / W), dpi=100)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis('off')
UNIT_IN = FIG_W / W
REND = fig.canvas.get_renderer()

def rbox(x, y, w, h, fc='white', ec=LINE, lw=0.6, r=1.0, z=2, ls='-', alpha=1.0):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', fc=fc, ec=ec, lw=lw,
                                zorder=z, ls=ls, alpha=alpha))

def T(x, y, s, size=5.4, color=INK, ha='left', va='center', weight='normal', style='normal', z=12, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, fontweight=weight, fontstyle=style,
                   zorder=z, **kw)

def width(t):
    bb = t.get_window_extent(renderer=REND)
    (x0, _), (x1, _) = ax.transData.inverted().transform([[bb.x0, bb.y0], [bb.x1, bb.y1]])
    return x1 - x0

def seq(x, y, pieces, size=5.4, gap=0.25):
    """Lay out text pieces left to right; piece = (text, color, background or None, style)."""
    for s, col, bg, st in pieces:
        kw = {}
        if bg: kw['bbox'] = dict(fc=bg, ec='none', pad=0.35, boxstyle='round,pad=0.25')
        t = T(x, y, s, size=size, color=col, style=st, **kw)
        x += width(t) + gap
    return x

def arrow(p0, p1, color=INK2, lw=0.75, rad=0.0, z=9, head=6, ls='-'):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=head, color=color, lw=lw, zorder=z,
                                 connectionstyle=f'arc3,rad={rad}', shrinkA=0.6, shrinkB=0.6, linestyle=ls))

def path_arrow(pts, color=INK2, lw=0.75, z=9, head=6):
    xs, ys = zip(*pts[:-1])
    ax.plot(xs, ys, color=color, lw=lw, zorder=z, solid_joinstyle='round')
    arrow(pts[-2], pts[-1], color=color, lw=lw, z=z, head=head)

_img = {}
def icon(name, x, y, size, z=10):
    if name not in _img:
        _img[name] = Image.open(os.path.join(ICON_DIR, f'{name}.png')).convert('RGBA')
    im = _img[name]
    ax.add_artist(AnnotationBbox(OffsetImage(im, zoom=(size * UNIT_IN * 72.0) / max(im.size)), (x, y),
                                 frameon=False, box_alignment=(0.5, 0.5), zorder=z, pad=0))

def robot(cx, cy, s, fill, z=10):
    ax.plot([cx, cx], [cy + 0.30 * s, cy + 0.46 * s], color=OUT, lw=0.5, zorder=z)
    ax.add_patch(Circle((cx, cy + 0.50 * s), 0.06 * s, fc=RED, ec=OUT, lw=0.5, zorder=z))
    rbox(cx - 0.40 * s, cy - 0.30 * s, 0.80 * s, 0.62 * s, fc='#e4e7ed', ec=OUT, lw=0.55, r=0.12 * s, z=z)
    for dx in (-0.17, 0.17):
        ax.add_patch(Circle((cx + dx * s, cy + 0.06 * s), 0.10 * s, fc='white', ec=OUT, lw=0.5, zorder=z + 1))
        ax.add_patch(Circle((cx + dx * s, cy + 0.06 * s), 0.045 * s, fc=fill, ec='none', zorder=z + 2))
    rbox(cx - 0.18 * s, cy - 0.20 * s, 0.36 * s, 0.09 * s, fc='white', ec=OUT, lw=0.5, r=0.02 * s, z=z + 1)

def badge(cx, cy, k, r=0.95):
    ax.add_patch(Circle((cx, cy), r, fc=ACC[k], ec='none', zorder=12))
    T(cx, cy - 0.05, str(k), size=4.4, color='white', ha='center', weight='bold', z=13)

def module(x, w, k, title):
    rbox(x, 1.2, w, H - 2.4, fc='white', ec=ACC[k], lw=0.9, r=1.6, z=1)
    ax.add_patch(FancyBboxPatch((x, H - 7.0), w, 5.8, boxstyle='round,pad=0,rounding_size=1.6', fc=HEAD[k],
                                ec='none', zorder=1.5))
    ax.add_patch(Rectangle((x + 0.45, H - 7.0), w - 0.9, 2.0, fc=HEAD[k], ec='none', zorder=1.6))
    ax.add_patch(Circle((x + 3.2, H - 4.1), 1.9, fc=ACC[k], ec='none', zorder=3))
    T(x + 3.2, H - 4.15, str(k), size=6.4, color='white', ha='center', weight='bold', z=4)
    T(x + 6.0, H - 4.1, title, size=6.6, weight='bold')

def bars(x, y_top, rows, bar_w, row_h, colors, icon_size=2.2, labels=False):
    vmax = max(v for _, v in rows)
    for i, (name, v) in enumerate(rows):
        yy = y_top - i * row_h
        icon(name, x + 1.3, yy, icon_size)
        c = colors[i] if isinstance(colors, list) else colors
        ax.add_patch(Rectangle((x + 3.0, yy - row_h * 0.26), v / vmax * bar_w, row_h * 0.52, fc=c, ec='none', zorder=6))
        if labels:
            T(x + 3.6 + v / vmax * bar_w, yy, f'{v:.2f}', size=4.6, color=MUTED)

module(1.0, 44.0, 1, 'Requirement identification')
module(47.0, 48.0, 2, 'Targeted generation and distillation')
module(97.0, 42.0, 3, 'Uncertainty-aware allocation')

# ================================ module 1 ================================
rbox(3.0, 45.0, 17.5, 11.5, fc=FILL[1])
T(4.2, 54.4, r'Task card $\mathcal{D}^{\mathrm{spec}}_\tau$', size=5.8, weight='bold')
for i, s in enumerate(['task description', 'input/output format', 'evaluation target', 'a few exemplars']):
    T(4.6, 51.6 - 2.0 * i, r'$\bullet$ ' + s, size=4.9, color=INK2)
arrow((20.8, 50.7), (23.6, 50.7))
rbox(23.8, 45.0, 19.4, 11.5, fc=FILL[1])
T(33.5, 54.4, r'Identifier $g_\phi$', size=5.8, weight='bold', ha='center')
for i, s in enumerate(['Transformer encoder', 'two-layer MLP', 'softmax']):
    rbox(25.4, 50.2 - 2.45 * i, 16.2, 1.9, fc='white', ec=BLUE, lw=0.5, r=0.5, z=4)
    T(33.5, 51.15 - 2.45 * i, s, size=4.8, ha='center', color=INK2)
arrow((33.5, 44.8), (33.5, 41.9))
T(3.4, 41.0, r'requirement $\mathbf{r}_\tau\in\Delta^{|\mathcal{C}|}$', size=5.8, weight='bold')
r_rows = [('math', .40), ('reasoning', .22), ('general', .15), ('steerability', .08),
          ('code', .06), ('tool_use', .045), ('lcu', .035), ('multilingual', .025)]
bars(3.4, 37.4, r_rows, bar_w=17.0, row_h=2.55, colors=[BLUE] * 3 + ['#b7c6df'] * 5, labels=True)
ax.add_patch(FancyBboxPatch((3.0, 30.9), 29.0, 7.8, boxstyle='round,pad=0,rounding_size=0.6', fc='none', ec=BLUE,
                            lw=0.6, ls=(0, (2.0, 1.2)), zorder=7))
T(31.6, 29.9, r'task-essential $\mathcal{C}_{\mathrm{ess}}$ (top-$k$)', size=4.8, color=BLUE, ha='right', va='top')
# offline pretraining inset
rbox(3.0, 3.0, 40.2, 14.0, fc='#f6f8fb', ec=BLUE, lw=0.55, ls=(0, (2.4, 1.4)), r=1.0)
T(4.2, 15.1, r'Offline pretraining of $g_\phi$ (once, shared by all tasks)', size=5.0, weight='bold', color=INK2)
chips = [r'$\mathbf{w}^{(m)}\!\sim\!\mathrm{Dir}$', 'probe distill', r'$(\Delta\mathbf{s}^{(m)},\,\Delta U^{(m)})$']
xx = 4.0
for i, c in enumerate(chips):
    t = T(xx + 0.8, 11.25, c, size=4.8)
    w0 = width(t) + 1.6
    rbox(xx, 9.6, w0, 3.3, fc='white', ec=LINE, lw=0.5, r=0.6, z=4)
    if i < len(chips) - 1: arrow((xx + w0 + 0.1, 11.25), (xx + w0 + 2.1, 11.25), head=4.0, lw=0.55)
    xx += w0 + 2.2
T(23.1, 6.2, r'$\min_\phi \sum_{\tau,m}\left(\Delta U^{(m)}_\tau - g_\phi(\mathcal{D}^{\mathrm{spec}}_\tau)^{\!\top}\Delta\mathbf{s}^{(m)}_\tau\right)^2+\lambda_{\mathrm{ent}}\,\mathcal{H}(g_\phi)$',
  size=5.3, ha='center')
path_arrow([(43.3, 10.0), (44.1, 10.0), (44.1, 47.5), (43.4, 47.5)], color=BLUE, lw=0.6, head=4.5)
T(42.9, 24.0, 'trains', size=4.6, color=BLUE, rotation=90, ha='center')

# ================================ module 2 ================================
T(48.6, 55.4, r'allocation $\mathbf{w}_t$', size=5.8, weight='bold')
bars(48.6, 52.4, [('math', .55), ('reasoning', .30), ('general', .15)], bar_w=8.5, row_h=2.6, colors=ORANGE)
T(48.6, 44.9, r'prior: $\mathbf{r}_\tau$ from', size=4.6, color=MUTED)
badge(59.6, 44.95, 1)
arrow((62.2, 50.0), (65.0, 50.0))
T(63.6, 51.8, r'$c\!\sim\!\mathbf{w}_t$', size=4.9, ha='center', color=INK2)
rbox(65.2, 41.4, 28.6, 15.1, fc=FILL[2])
T(66.3, 54.6, r'Template library $\mathcal{P}_c$', size=5.8, weight='bold')
seq(66.3, 51.9, [('"', INK2, None, 'italic'), ('[N]', BLUE, '#dbe3f0', 'normal'), ('pens cost', INK2, None, 'italic'),
                 ('[P]', ORANGE, '#f8e1cf', 'normal'), ('; cost of', INK2, None, 'italic'),
                 ('[M]', BLUE, '#dbe3f0', 'normal'), ('?"', INK2, None, 'italic')], size=5.0, gap=0.35)
T(66.3, 49.6, r'typed slots $\cdot$ fixed seeds $\cdot$ format rules', size=4.7, color=MUTED)
T(66.3, 47.3, r'difficulty $d_c(x)$', size=4.9, color=INK2)
for i, (lab, col) in enumerate([('easy', '#f6d9c4'), ('medium', '#eeb48c'), ('hard', ORANGE)]):
    ax.add_patch(Rectangle((75.6 + i * 5.7, 46.6), 5.7, 1.5, fc=col, ec='white', lw=0.5, zorder=5))
    T(75.6 + i * 5.7 + 2.85, 45.3, lab, size=4.4, color=INK2, ha='center')
tc = T(66.3, 43.6, r'curriculum over $t$', size=4.5, color=ORANGE)
arrow((66.3 + width(tc) + 0.8, 43.6), (92.4, 43.6), color=ORANGE, lw=0.55, head=4)
# prompt -> teacher -> answer
arrow((79.0, 41.2), (57.5, 37.6), rad=0.1)
rbox(48.4, 28.2, 15.6, 9.2, fc='white')
T(49.3, 35.5, r'prompt $x$', size=5.2, weight='bold')
T(49.3, 32.8, '"3 pens cost \\$4.50;', size=4.8, color=INK2, style='italic')
T(49.3, 30.5, ' how much are 7?"', size=4.8, color=INK2, style='italic')
arrow((64.2, 32.8), (66.0, 32.8))
rbox(66.2, 27.8, 15.2, 10.0, fc='#fbe7d8', ec=ORANGE, lw=0.8, r=1.2)
robot(69.4, 32.6, 4.4, ORANGE)
T(72.3, 34.4, r'Teacher $T$', size=5.2, weight='bold', color=ORANGE)
T(72.3, 31.4, '70B, frozen', size=4.7, color=INK2)
arrow((81.6, 32.8), (83.2, 32.8))
rbox(83.4, 28.2, 10.4, 9.2, fc='white')
T(84.2, 35.5, r'answer $y$', size=5.2, weight='bold')
T(84.2, 32.8, '"\\$1.50 each,', size=4.8, color=INK2, style='italic')
T(84.2, 30.5, ' so \\$10.50"', size=4.8, color=INK2, style='italic')
# distill -> student
path_arrow([(88.6, 28.0), (88.6, 22.2), (81.2, 14.8)], lw=0.75)
T(67.0, 22.3, r'$\mathcal{L}_{\mathrm{distill}}=-\sum_{j}\log p_{\theta_t}(y_j\,|\,x,y_{<j})$', size=5.3, ha='center')
T(67.0, 19.6, 'token-level distillation on $(x,y)$', size=4.6, color=MUTED, ha='center')
rbox(64.4, 4.0, 16.6, 10.6, fc='#dfe6f1', ec=BLUE, lw=0.8, r=1.2)
robot(67.6, 9.0, 4.2, BLUE)
T(70.4, 11.2, r'Student $S_t$', size=5.2, weight='bold', color=BLUE)
T(70.4, 8.6, r'8B, updated', size=4.7, color=INK2)
T(70.4, 6.3, r'$\rightarrow S_{t+1}$', size=4.8, color=INK2)
# budget gauge
T(48.6, 14.6, r'token budget $B$', size=5.2, weight='bold')
for k in range(10):
    ax.add_patch(Rectangle((48.6 + k * 1.45, 10.6), 1.2, 2.2, fc=ORANGE if k < 4 else '#f3dccb', ec='none', zorder=5))
T(48.6, 8.2, r'$T=20$ steps', size=4.7, color=INK2)
T(48.6, 5.9, r'$b_{t+1}=b_t-\mathrm{cost}_t$', size=4.9, color=INK2)

# ================================ module 3 ================================
arrow((81.2, 9.3), (99.6, 9.3))
T(90.4, 10.6, r'$S_{t+1}$', size=5.0, ha='center', color=INK2)
rbox(99.8, 3.4, 11.2, 13.0, fc=FILL[3])
T(105.4, 14.4, 'probe suite', size=5.0, weight='bold', ha='center')
for k in range(4):
    yy = 11.8 - k * 2.0
    ax.add_patch(Rectangle((101.2, yy - 0.5), 1.0, 1.0, fc='white', ec=OUT, lw=0.4, zorder=5))
    if k < 3: ax.plot([101.3, 101.65, 102.1], [yy, yy - 0.35, yy + 0.4], color=GREEN, lw=0.7, zorder=6)
    ax.plot([102.8, 109.6], [yy, yy], color=LINE, lw=0.7, zorder=5)
T(105.4, 4.5, 'small, fixed', size=4.4, color=MUTED, ha='center')
arrow((111.2, 9.3), (112.9, 9.3), head=4.5)
T(113.2, 15.6, r'$\Delta\mathbf{s}_t=\mathbf{s}^{\mathrm{probe}}(S_{t+1})-\mathbf{s}^{\mathrm{probe}}(S_t)$', size=4.9)
x0 = 124.2
ax.plot([x0, x0], [3.4, 13.4], color=MUTED, lw=0.5, zorder=4)
for i, (nm, v) in enumerate([('math', 1.8), ('reasoning', 0.6), ('general', 0.2), ('steerability', -0.4)]):
    yy = 12.2 - i * 2.4
    icon(nm, 115.6, yy, 2.1)
    L = v / 1.8 * 8.0; c = GREEN if v >= 0 else RED
    ax.add_patch(Rectangle((x0 if v >= 0 else x0 + L, yy - 0.7), abs(L), 1.4, fc=c, ec='none', zorder=6))
    T(x0 + L + (0.5 if v >= 0 else -0.5), yy, f'{v:+.1f}', size=4.5, color=c, ha='left' if v >= 0 else 'right')
arrow((134.5, 16.6), (134.5, 18.6), head=4.5)
# reward
rbox(99.8, 18.8, 38.0, 11.2, fc=FILL[3])
T(100.8, 28.1, 'proxy reward', size=5.4, weight='bold')
badge(136.3, 28.1, 1)
seq(100.8, 24.9, [(r'$\widehat{R}_t=$', INK, None, 'normal'), (r'$\mathbf{r}_\tau^{\!\top}\Delta\mathbf{s}_t$', INK, '#d5ead9', 'normal'),
                  (r'$-\,\beta$', INK, None, 'normal'), (r'$\mathrm{Spill}_t$', INK, '#f2d3d4', 'normal'),
                  (r'$-\,\lambda$', INK, None, 'normal'), (r'$\mathrm{cost}_t$', INK, '#e6e5e0', 'normal')], size=5.6, gap=0.5)
T(100.8, 21.0, r'$\mathrm{Spill}_t=\sum_{c\in\mathcal{C}_{\mathrm{ess}}} r_{\tau,c}\,[-\Delta s_{t,c}]_+$', size=5.2, color=INK2)
arrow((118.8, 30.2), (118.8, 32.6), head=4.5)
T(119.6, 31.4, r'append $(\mathbf{x}_t,\mathbf{w}_t,\widehat{R}_t)$', size=4.5, color=MUTED)
# bandit
rbox(99.8, 32.8, 38.0, 23.7, fc=FILL[3])
T(100.8, 54.5, 'contextual bandit', size=5.8, weight='bold')
badge(136.3, 54.5, 1)
T(100.8, 51.7, r'context $\mathbf{x}_t=[\mathbf{r}_\tau;\,\mathbf{s}^{\mathrm{probe}}(S_t);\,b_t;\,\rho_t]$', size=5.0)
for j in range(3):
    rbox(101.0 + 0.7 * j, 45.6 - 0.7 * j, 10.6, 4.0, fc='white', ec=GREEN, lw=0.5, r=0.6, z=4 + j)
T(107.1, 46.2, r'$h_{\eta_1},\ldots,h_{\eta_J}$', size=5.0, ha='center', z=12)
T(107.1, 42.5, 'bootstrap MLP ensemble', size=4.4, color=MUTED, ha='center')
arrow((113.5, 46.2), (116.0, 46.2), head=4.5)
T(116.3, 47.6, r'$\mu(\mathbf{x}_t,\mathbf{w})$', size=5.0)
T(116.3, 44.9, r'$\sigma(\mathbf{x}_t,\mathbf{w})$', size=5.0)
T(130.4, 49.4, r'candidates $\mathcal{A}(\tau)$', size=4.6, color=INK2, ha='center')
for k, (m, s_) in enumerate([(.60, .05), (.56, .13), (.70, .09)]):
    cx = 126.6 + k * 3.9
    ax.add_patch(Rectangle((cx - 1.1, 40.8), 2.2, m * 6.0, fc=GREEN if k == 2 else '#b9dbc2', ec='none', zorder=5))
    lo, hi = 40.8 + (m - s_) * 6.0, 40.8 + (m + s_) * 6.0
    ax.plot([cx, cx], [lo, hi], color=INK, lw=0.5, zorder=6)
    for yy in (lo, hi): ax.plot([cx - 0.45, cx + 0.45], [yy, yy], color=INK, lw=0.5, zorder=6)
T(134.4, 39.8, r'$\mathbf{w}_{t+1}$', size=4.8, color=GREEN, ha='center', weight='bold')
T(118.8, 35.6, r'$\mathbf{w}_{t+1}=\mathrm{argmax}_{\mathbf{w}\in\mathcal{A}(\tau)}\;\mu(\mathbf{x}_{t+1},\mathbf{w})+\kappa\,\sigma(\mathbf{x}_{t+1},\mathbf{w})$',
  size=5.2, ha='center')
# loop back to allocation
path_arrow([(118.8, 56.8), (118.8, 58.2), (55.0, 58.2), (55.0, 57.0)], color=GREEN, lw=1.0, head=6)
T(76.0, 58.2, r'  next step: $\mathbf{w}_{t+1}$, $b_{t+1}$  ', size=5.2, color=GREEN, ha='center', weight='bold',
  bbox=dict(fc='white', ec='none', pad=0.2))

fig.savefig(OUT_PDF); fig.savefig(OUT_PNG, dpi=240)
print('wrote', OUT_PDF, OUT_PNG)
