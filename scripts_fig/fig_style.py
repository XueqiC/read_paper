"""Shared style for the new data figures. Colors and shapes follow the paper's ORIGINAL figures:
- one method, one color: the matplotlib tab10 colors of the original budget-scaling curves
  (Resp-SFT ... Logit-KD, ReAD pink); methods that never appear there take the remaining tab10 colors;
- one budget, one color + hatch + marker: the original component-ablation bars
  (20M blue with '///', 150M orange with dots), black bar edges and black hatching."""
import matplotlib.pyplot as plt
METHOD = {'Resp-SFT': '#1f77b4', 'CoT-SFT': '#ff7f0e', 'Logit-SFT': '#2ca02c', 'Resp-KD': '#d62728',
          'CoT-KD': '#9467bd', 'Logit-KD': '#8c564b', 'ReAD': '#e377c2',
          'Step-by-Step': '#bcbd22', 'EoTD': '#17becf', 'CodePLAN': '#7f7f7f'}
BUDGET = {20: dict(color='#1f77b4', hatch='//////', marker='o', label='20M'),
          150: dict(color='#ff7f0e', hatch='......', marker='s', label='150M')}
# The original ablation PDF is drawn with '//' and '..' and shrunk to about one third in the paper;
# the new figures are placed near 1:1, so their hatches are three times denser to look the same.
BLUE, ORANGE = BUDGET[20]['color'], BUDGET[150]['color']
READ = METHOD['ReAD']
INK = '#1d1d1b'
EDGE = dict(edgecolor='black', linewidth=0.6)
ERR = dict(elinewidth=0.7, capsize=1.6, capthick=0.7, ecolor='black')
def apply(size=7):
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Liberation Serif'],
                         'font.weight': 'bold', 'axes.labelweight': 'bold', 'axes.titleweight': 'bold',
                         'font.size': size, 'pdf.fonttype': 42, 'mathtext.fontset': 'stix',
                         'axes.edgecolor': '#2E3440', 'axes.linewidth': 0.7, 'xtick.major.width': 0.6,
                         'ytick.major.size': 0, 'xtick.major.size': 2.5, 'legend.frameon': False,
                         'hatch.color': 'black', 'hatch.linewidth': 0.35})
def grid(ax, axis='x'):
    ax.grid(True, axis=axis, color=INK, alpha=0.18, lw=0.6, zorder=0); ax.set_axisbelow(True)
def hatch(B, scale=1.0):
    """Hatch for budget B in a figure shown at `scale` x its native size in the paper."""
    return ('/' if B == 20 else '.') * max(2, round(2 * scale / 0.335))
