#!/usr/bin/env python3
"""Swap two fill/stroke colours in matplotlib PDFs (all content/pattern streams); geometry untouched."""
import sys, re, os, pymupdf
def rgb(h): return [int(h[i:i + 2], 16) / 255 for i in (1, 3, 5)]
def fmt(v): return ('%.10f' % v).rstrip('0').rstrip('.') if v not in (0, 1) else str(int(v))
def pat(h): return r'\s+'.join(re.escape(fmt(v)) for v in rgb(h))
def swap(path, a, b):
    rx = re.compile(r'(?<![\d.])(' + pat(a) + r'|' + pat(b) + r')\s+(rg|RG|sc|SC|scn|SCN)\b')
    A, B = ' '.join(fmt(v) for v in rgb(a)), ' '.join(fmt(v) for v in rgb(b))
    na = re.compile(pat(a))
    d = pymupdf.open(path); n = 0
    for x in range(1, d.xref_length()):
        try:
            if not d.xref_is_stream(x): continue
            s = d.xref_stream(x).decode('latin1')
        except Exception: continue
        t = rx.sub(lambda m: (B if na.fullmatch(m.group(1)) else A) + ' ' + m.group(2), s)
        if t != s: d.update_stream(x, t.encode('latin1')); n += 1
    d.save(path + '.tmp', garbage=3, deflate=True); d.close(); os.replace(path + '.tmp', path); return n
a, b = sys.argv[1], sys.argv[2]
for p in sys.argv[3:]: print(p, 'streams changed:', swap(p, a, b))
