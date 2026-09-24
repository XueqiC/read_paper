"""Shared style for the new data figures: matches the paper's original matplotlib figures
(Times bold, seaborn-deep colors, boxed axes, light grid) but with fewer marks."""
import matplotlib.pyplot as plt
BLUE, ORANGE, GREEN, RED, GRAY = '#4C72B0', '#DD8452', '#55A868', '#C44E52', '#8C8C8C'
INK = '#1d1d1b'
BASE = '#8172B3'   # one-hot / SFT-KD baselines (same hue as 'One-hot KD' in Figure 4b)
BUDGET = {20: (BLUE, 'o'), 150: (ORANGE, 's')}      # as in the original ablation figure
def apply(size=7):
    plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'Liberation Serif'],
                         'font.weight': 'bold', 'axes.labelweight': 'bold', 'axes.titleweight': 'bold',
                         'font.size': size, 'pdf.fonttype': 42, 'mathtext.fontset': 'stix',
                         'axes.edgecolor': '#2E3440', 'axes.linewidth': 0.7, 'xtick.major.width': 0.6,
                         'ytick.major.size': 0, 'xtick.major.size': 2.5, 'legend.frameon': False})
def grid(ax, axis='x'):
    ax.grid(True, axis=axis, color=INK, alpha=0.18, lw=0.6, zorder=0); ax.set_axisbelow(True)
