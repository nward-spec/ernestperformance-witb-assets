from PIL import Image
import numpy as np

def trim(im):
    a = np.array(im)[...,3] > 10
    ys, xs = np.where(a)
    return im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))

def rot(im, deg):
    return trim(im.rotate(deg, expand=True, resample=Image.BICUBIC))

def alpha(im, thr=60):
    return np.array(im)[...,3] > thr

def stub_rows(a, band_px):
    """rows of the bottom band that are 'shaft thickness'"""
    h = a.shape[0]
    rows = np.where(a.any(axis=1))[0]
    lo = max(0, rows.max() - band_px)
    return lo, rows.max()

def axis_angle(a, lo, hi):
    """angle in degrees of the centroid line over rows lo..hi (0 = vertical)"""
    ys, cs = [], []
    for y in range(lo, hi+1):
        row = a[y]
        if row.sum() > 0:
            ys.append(y); cs.append(np.average(np.arange(a.shape[1]), weights=row.astype(float)))
    if len(ys) < 5: return 0.0, 0.0
    ys = np.array(ys, float); cs = np.array(cs, float)
    m, c = np.polyfit(ys, cs, 1)
    resid = float(np.sqrt(np.mean((cs - (m*ys+c))**2)))
    return float(np.degrees(np.arctan(m))), resid

def level(src, dst, coarse=0.0, band=150, passes=3, verbose=True):
    im = trim(Image.open(src).convert("RGBA"))
    if coarse: im = rot(im, coarse)
    total = coarse
    for p in range(passes):
        a = alpha(im)
        lo, hi = stub_rows(a, band)
        ang, resid = axis_angle(a, lo, hi)
        if abs(ang) < 0.08: break
        # empirical sign check
        best = None
        for s in (+1, -1):
            cand = rot(im, s*ang)
            ac = alpha(cand); l2, h2 = stub_rows(ac, band)
            a2, r2 = axis_angle(ac, l2, h2)
            if best is None or abs(a2) < abs(best[1]): best = (cand, a2, s*ang)
        im, ang2, applied = best
        total += applied
        if verbose: print(f"  {src} pass{p}: angle {ang:+.2f} -> {ang2:+.2f} (applied {applied:+.2f})")
    a = alpha(im); lo, hi = stub_rows(a, band)
    ang, resid = axis_angle(a, lo, hi)
    if verbose: print(f"  {src}: total rotation {total:+.2f}, residual axis angle {ang:+.3f}, rms {resid:.2f}")
    im.save(dst)
    return im

def pad_stub(src, dst, band=60, trim_shaft_to=None):
    im = trim(Image.open(src).convert("RGBA"))
    a = alpha(im)
    if trim_shaft_to:
        widths = a.sum(axis=1)
        nz = widths[widths>0]
        shaft_t = np.median(nz[-40:])
        head_rows = np.where(widths > 3*shaft_t)[0]
        keep = min(im.height, head_rows.max() + trim_shaft_to)
        im = im.crop((0,0,im.width, keep)); a = alpha(im)
    pts = trace_stub(a)
    if len(pts) >= 8:
        k = max(8, len(pts)//3)
        sx = int(np.median([p[1] for p in pts[:k]]))
        stubw = float(np.median([p[2] for p in pts[:k]]))
    else:
        rows = np.where(a.any(axis=1))[0]
        band_rows = rows[-max(3, band):]
        sx = int(np.concatenate([np.where(a[r])[0] for r in band_rows]).mean())
        stubw = float(np.median([a[r].sum() for r in band_rows]))
    new_w = 2*max(sx, im.width - sx)
    canvas = Image.new("RGBA", (new_w, im.height), (0,0,0,0))
    canvas.paste(im, (new_w//2 - sx, 0))
    canvas.save(dst)
    # report stub width (median alpha row width over bottom 3%)
    print(f"  pad {dst}: canvas {canvas.size}, traced stub width {stubw:.1f}px")
    return canvas, stubw

def runs(row):
    idx = np.where(row)[0]
    if len(idx)==0: return []
    splits = np.where(np.diff(idx) > 1)[0]
    groups = np.split(idx, splits+1)
    return [(g[0], g[-1]) for g in groups]

def trace_stub(a, max_rows=600, grow=2.4, seed_min=8):
    """Follow the shaft up from near the bottom; stop when it widens into the head."""
    rows = np.where(a.any(axis=1))[0]
    if len(rows) == 0: return []
    y0, y1 = rows.min(), rows.max()
    # seed: scan up from the bottom for the first row with a run of >= seed_min px
    y = None
    for yy in range(y1, max(y0, y1 - int(0.15*(y1-y0)) - 5) - 1, -1):
        rr = [r for r in runs(a[yy]) if r[1]-r[0]+1 >= seed_min]
        if rr:
            y = yy; cur = max(rr, key=lambda r: r[1]-r[0]); break
    if y is None: return []
    pts = [(y, (cur[0]+cur[1])/2.0, cur[1]-cur[0]+1)]
    widths = [cur[1]-cur[0]+1]
    for yy in range(y-1, max(y0, y-max_rows)-1, -1):
        rr = [r for r in runs(a[yy]) if r[1]-r[0]+1 >= 3]
        if not rr: break
        c0 = pts[-1][1]
        cand = min(rr, key=lambda r: abs((r[0]+r[1])/2.0 - c0))
        w = cand[1]-cand[0]+1
        med = np.median(widths[:8]) if len(widths) >= 8 else np.median(widths)
        if w > grow*max(med, 6): break
        if abs((cand[0]+cand[1])/2.0 - c0) > 25: break
        pts.append((yy, (cand[0]+cand[1])/2.0, w)); widths.append(w)
    return pts

def stub_angle(a, keep=None):
    pts = trace_stub(a)
    if len(pts) < 8: return 0.0, 0.0, len(pts)
    if keep: pts = pts[:keep]
    ys = np.array([p[0] for p in pts], float); cs = np.array([p[1] for p in pts], float)
    m, c = np.polyfit(ys, cs, 1)
    resid = float(np.sqrt(np.mean((cs-(m*ys+c))**2)))
    return float(np.degrees(np.arctan(m))), resid, len(pts)

def level2(src, dst, coarse=0.0, passes=4, keep=None, verbose=True):
    im = trim(Image.open(src).convert("RGBA"))
    if coarse: im = rot(im, coarse)
    total = coarse
    for p in range(passes):
        a = alpha(im)
        ang, resid, n = stub_angle(a, keep)
        if verbose: print(f"  pass{p}: stub pts {n}, angle {ang:+.2f}, rms {resid:.2f}")
        if abs(ang) < 0.08: break
        best = None
        for s in (+1,-1):
            cand = rot(im, s*ang)
            a2, r2, n2 = stub_angle(alpha(cand), keep)
            if best is None or abs(a2) < abs(best[1]): best = (cand, a2, s*ang)
        im, a2, applied = best
        total += applied
    ang, resid, n = stub_angle(alpha(im), keep)
    if verbose: print(f"  {src}: total {total:+.2f}, residual {ang:+.3f} deg over {n} rows, rms {resid:.2f}")
    im.save(dst)
    return im

def crop_to_hosel(src, dst, margin=6):
    """Crop the shaft off just below where it widens into the hosel/ferrule, so the
    strip joins the head at the widest part of the stub rather than at the thin tip."""
    im = trim(Image.open(src).convert("RGBA"))
    a = alpha(im)
    pts = trace_stub(a)          # bottom -> up
    if len(pts) < 6:
        im.save(dst); return im, None
    y_top = int(pts[-1][0]) + margin
    im = trim(im.crop((0, 0, im.width, min(im.height, y_top))))
    im.save(dst)
    a2 = alpha(im); rows = np.where(a2.any(axis=1))[0]
    w = float(np.median([a2[r].sum() for r in rows[-4:]]))
    print(f"  crop_to_hosel {dst}: {im.size}, join width {w:.0f}px")
    return im, w

def crop_to_target(src, dst, maxW, target_disp, iters=4, margin=4):
    """Crop the shaft so that, once padded and rendered at maxW, the join with the
    strip lands as close as possible to target_disp px at 1x layout scale."""
    im0 = trim(Image.open(src).convert("RGBA"))
    best = None
    for _ in range(iters):
        a = alpha(im0); pts = trace_stub(a)
        if len(pts) < 6: break
        # estimate the padded canvas width for a candidate crop
        cand = []
        for (y, cx, w) in pts:          # bottom -> up, widths increase toward the head
            im = trim(im0.crop((0, 0, im0.width, min(im0.height, int(y)+margin))))
            aa = alpha(im); rows = np.where(aa.any(axis=1))[0]
            jw = float(np.median([aa[r].sum() for r in rows[-4:]]))
            cs = np.average(np.arange(im.width), weights=aa[rows[-1]].astype(float))
            sx = int(cs); new_w = 2*max(sx, im.width-sx)
            cand.append((abs(jw*maxW/new_w - target_disp), y, jw*maxW/new_w, im))
        cand.sort(key=lambda t: t[0])
        best = cand[0]
        break
    if best is None:
        im0.save(dst); return im0, None
    _, y, disp, im = best
    im.save(dst)
    print(f"  crop_to_target {dst}: cut at y={int(y)}, join renders {disp:.1f}px at maxW {maxW}")
    return im, disp
