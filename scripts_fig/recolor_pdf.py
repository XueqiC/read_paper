#!/usr/bin/env python3
"""Recolor matplotlib PDFs from tab10 to the paper's seaborn-deep tones (same hue identity), touching only the
colour operators in every content / pattern / XObject stream, so the geometry is unchanged."""
import sys, re, pymupdf
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from fig_style import TAB2DEEP
def rgb(h): return [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
def fmt(v): return ('%.10f' % v).rstrip('0').rstrip('.') if v not in (0, 1) else str(int(v))
def recolor(path):
    d = pymupdf.open(path); n = 0
    pats = []
    for old, new in TAB2DEEP.items():
        a = [fmt(v) for v in rgb(old)]
        pat = re.compile(r'(?<![\d.])' + r'\s+'.join(re.escape(x) for x in a) + r'\s+(rg|RG|sc|SC|scn|SCN)\b')
        pats.append((pat, ' '.join(fmt(v) for v in rgb(new))))
    for x in range(1, d.xref_length()):
        try:
            if not d.xref_is_stream(x): continue
            s = d.xref_stream(x).decode('latin1')
        except Exception: continue
        t = s
        for pat, rep in pats: t = pat.sub(lambda m: rep + ' ' + m.group(1), t)
        if t != s: d.update_stream(x, t.encode('latin1')); n += 1
    d.save(path + '.tmp', garbage=3, deflate=True); d.close()
    import os; os.replace(path + '.tmp', path); return n
for p in sys.argv[1:]: print(p, 'streams changed:', recolor(p))
