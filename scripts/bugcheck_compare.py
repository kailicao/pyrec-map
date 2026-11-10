"""bugcheck_compare.py BASE FIX: compare a run with a fix (or a null change) against the same case unfixed:
YREC's harness test (2% fractional, integers exact) on each .track, .short and .store, and the track
compared on common ages (models, end age, largest differences in log L, log Teff, log Tc, central X and Y)."""
import sys, re, glob, os, math
TOL = 0.02
def toks(line):
    out = []
    for t in re.split(r"\s+|(?<![Ee])-(?=\d)", line.strip()):
        try: out.append(float(t.replace('D', 'E')) if re.match(r'^[-+]?[\d.]', t) else t)
        except ValueError: out.append(t)
    return out
def lines(p):
    return [l for l in open(p, errors='replace') if not re.search(r'YREC v\S* \(', l)]
def cmp(a, b):
    la, lb = lines(a), lines(b)
    fail, mx, where, first = len(la) != len(lb), 0.0, None, None
    for i, (x, y) in enumerate(zip(la, lb)):
        tx, ty = toks(x), toks(y)
        if len(tx) != len(ty):
            fail = True; first = first or i + 1; continue
        for u, v in zip(tx, ty):
            if isinstance(u, float) and isinstance(v, float):
                if not (math.isfinite(u) and math.isfinite(v)):
                    if not (u != u and v != v): fail = True; first = first or i + 1
                    continue
                d = abs(u - v) / abs(u) if u else (0.0 if v == 0 else 1.0)
                if d > mx: mx, where = d, i + 1
                if d > TOL: fail = True; first = first or i + 1
            elif u != v and not (isinstance(u, float) or isinstance(v, float)):
                pass  # text tokens: ignore (labels)
            elif u != v:
                fail = True; first = first or i + 1
    return fail, mx, where, first, len(la), len(lb)
def track(p):
    cols = None; rows = []
    for l in open(p):
        if 'Age_gyr' in l: cols = l.lstrip('#').split(); continue
        if l.startswith('#') or not l.strip() or not cols: continue
        try: rows.append([float(x.replace('D', 'E')) for x in l.split()[:len(cols)]])
        except ValueError: pass
    return cols, rows
Q = ['LogL_lsun', 'log_Teff', 'LogT_cen', 'X_cen', 'Y_cen']
def trackcmp(a, b):
    import bisect
    ca, ra = track(a); cb, rb = track(b)
    if not ra or not rb: return 'track: no models'
    ia = ca.index('Age_gyr')
    s = [f"models {len(ra)} vs {len(rb)}; end age {ra[-1][ia]:.6g} vs {rb[-1][ia]:.6g} Gyr"]
    # compare on the base's ages, within the common age range, by linear interpolation in the fix's track
    ages_b = [r[ia] for r in rb]
    if any(ages_b[i] > ages_b[i+1] for i in range(len(ages_b)-1)): s.append('(ages not monotonic: compared by model order)')
    lo, hi = max(ra[0][ia], rb[0][ia]), min(ra[-1][ia], rb[-1][ia])
    for q in Q:
        if q not in ca: continue
        k = ca.index(q); kb = cb.index(q); mx = 0.0; at = None
        seen = {}
        for r in ra:
            t = r[ia]
            if t < lo or t > hi: continue
            occ = seen.get(t, 0); seen[t] = occ + 1
            j = bisect.bisect_left(ages_b, t)
            if j < len(rb) and ages_b[j] == t:
                # several models at the same age (a rescaling, a run's start): pair the k-th with the k-th
                k2 = j + occ
                v = rb[k2][kb] if k2 < len(rb) and ages_b[k2] == t else None
                if v is None: continue
            elif j == 0: v = rb[0][kb]
            elif j >= len(rb): v = rb[-1][kb]
            else:
                t0, t1 = rb[j-1][ia], rb[j][ia]
                w = 0 if t1 == t0 else (t - t0) / (t1 - t0); v = rb[j-1][kb]*(1-w) + rb[j][kb]*w
            d = abs(v - r[k])
            if d > mx: mx, at = d, t
        s.append(f"max |d {q}| {mx:.3g}" + (f" (at {at:.4g} Gyr)" if at is not None else ''))
    return '; '.join(s)
base, fix = sys.argv[1], sys.argv[2]
for ext in ('track', 'short', 'store'):
    for a in sorted(glob.glob(f'{base}/**/*.{ext}', recursive=True)):
        b = os.path.join(fix, os.path.relpath(a, base))
        if not os.path.exists(b): print(f'{ext}: missing in fix run'); continue
        if lines(a) == lines(b): print(f'{os.path.basename(a)}: identical'); continue
        fail, mx, where, first, na, nb = cmp(a, b)
        print(f"{os.path.basename(a)}: {'DIFFERS beyond 2%' if fail else 'within 2%'}; largest rel. change {mx:.3g} (line {where}); first failing line {first}; lines {na} vs {nb}")
for a in sorted(glob.glob(f'{base}/**/*.track', recursive=True)):
    b = os.path.join(fix, os.path.relpath(a, base))
    print('track:', trackcmp(a, b) if os.path.exists(b) else 'no track in fix run')
