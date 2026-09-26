"""Shared style for all data figures. One palette for the whole paper: the muted seaborn-"deep" tones of
the original Figure 1, applied with the same hue identities the original figures used:
- one method, one color (hue order of the original budget-scaling curves; ReAD pink);
- one budget, one color + hatch + marker (component-ablation convention: 20M blue with '///',
  150M orange with dots), black bar edges and black hatching."""
import matplotlib.pyplot as plt
# tab10 hue -> seaborn-deep tone (same hue identity)
TAB2DEEP = {'#1f77b4': '#4C72B0', '#ff7f0e': '#DD8452', '#2ca02c': '#55A868', '#d62728': '#C44E52',
            '#9467bd': '#8172B3', '#8c564b': '#937860', '#e377c2': '#DA8BC3', '#7f7f7f': '#8C8C8C',
            '#bcbd22': '#CCB974', '#17becf': '#64B5CD'}
# ReAD takes the deep red (it sits better next to the blue/orange budget colours); Resp-KD, which only
# appears in the budget curves, takes the pink.
METHOD = {'Resp-SFT': '#4C72B0', 'CoT-SFT': '#DD8452', 'Logit-SFT': '#55A868', 'Resp-KD': '#DA8BC3',
          'CoT-KD': '#8172B3', 'Logit-KD': '#937860', 'ReAD': '#C44E52',
          # the three capability-specific methods only appear in the radar: three shades of the palette blue
          'Step-by-Step': '#27406B', 'EoTD': '#6F93CE', 'CodePLAN': '#A9BFE3'}
BUDGET = {20: dict(color='#4C72B0', hatch='//////', marker='o', label='20M'),
          150: dict(color='#DD8452', hatch='......', marker='s', label='150M')}
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

# capability colors of the original Figure 1(d) (seaborn-deep, indexed by capability)
CAP_LINE = {'General': '#4C72B0', 'Reasoning': '#55A868', 'Math': '#C44E52', 'Code': '#8172B3', 'Tool Use': '#64B5CD'}
def diverging():
    """Blue-white-red map in the same deep tones, for signed score changes."""
    from matplotlib.colors import LinearSegmentedColormap
    return LinearSegmentedColormap.from_list('deep_div', ['#1F3A66', '#4C72B0', '#A8BCDC', '#F7F7F7',
                                                          '#E4A9AB', '#C44E52', '#7A1F24'])
