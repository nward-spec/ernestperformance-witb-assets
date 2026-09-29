# Hosel verticality for the WITB club renders.
#
# WHY THIS EXISTS. Levelling a club head by its shaft stub is easy to get
# wrong in a way that passes review: a head can be dead centre on the club
# axis and still be tipped twenty degrees. Position and angle are different
# measurements and you must report both.
#
# Two traps when measuring the angle:
#   1. Walking up the shaft and stopping where it widens into the hosel gives
#      only 12 to 18 rows on a photo with a short stub in frame. Far too short
#      a baseline: the iteration wanders.
#   2. Rotating with expand+trim leaves an anti-aliased taper at the very
#      bottom (e.g. 85px narrowing to 9px over ~40 rows). Fitting through that
#      tail drags the angle badly.
#
# The fix: anchor on the shaft PLATEAU width, search several band depths and
# take the NARROWEST sustained feature (the shaft is the thinnest thing in
# frame), and reject any fit whose residual is too large to be a straight
# shaft.
#
# Usage, per head, after orient.orient_down has the shaft pointing roughly down:
#     from hosel import make_vertical, angle
#     make_vertical('cutouts/or-driver.png', 'cutouts/v-driver.png')
# then crop the shaft, pad on the stub, render, and verify with angle() on the
# levelled cutout plus a neck/shaft position check on the shipped PNG.
#
# If a head has no usable hosel in frame at all, do not fight it: swap in a
# retail sole shot whose loft stamp matches the spec. A 36-row fit is not
# worth shipping.

import numpy as np
from PIL import Image
from level import trim, alpha, rot


def _runs(row):
    idx = np.where(row)[0]
    if len(idx) == 0:
        return []
    sp = np.where(np.diff(idx) > 1)[0]
    return [(g[0], g[-1]) for g in np.split(idx, sp + 1)]


def shaft_rows(im, bottom_frac=None, lo=0.55, hi=1.7, min_rows=25):
    """Rows that are genuinely shaft: width within [lo,hi] x the plateau width.

    With bottom_frac None, searches several band depths and returns the one with
    the SMALLEST plateau that still yields min_rows and fits straight. Anchoring
    on a single deep band measured the driver's HEAD (332px) as its "shaft".
    """
    if bottom_frac is None:
        best = None
        for bf in (0.06, 0.09, 0.12, 0.18, 0.25, 0.35):
            r = shaft_rows(im, bottom_frac=bf, lo=lo, hi=hi, min_rows=min_rows)
            if r is None:
                continue
            ys, cs, plateau = r
            m, c = np.polyfit(ys, cs, 1)
            rms = float(np.sqrt(np.mean((cs - (m * ys + c)) ** 2)))
            # A real shaft is straight: rms is well under a pixel to about 1px.
            # Fitting the HEAD gives rms in the tens. Without this gate the iron
            # locks onto a 202px "shaft" at rms 26 and rotates 40 degrees.
            if rms > max(2.5, 0.06 * plateau):
                continue
            if best is None or plateau < best[2]:
                best = r
        return best
    a = alpha(im)
    rows = np.where(a.any(axis=1))[0]
    if len(rows) < min_rows:
        return None
    w = np.array([a[r].sum() for r in rows], float)
    nb = max(min_rows, int(bottom_frac * len(rows)))
    band = w[-nb:]
    if (band > 2).sum() < 5:
        return None
    plateau = np.percentile(band[band > 2], 75)      # shaft width, taper excluded
    ok = []
    for i in range(len(rows) - 1, -1, -1):
        width = w[i]
        if width < lo * plateau or width > hi * plateau:
            if ok:
                break                                 # left the shaft, stop
            continue                                  # still in the taper, keep looking
        rr = _runs(a[rows[i]])
        if not rr:
            continue
        seg = max(rr, key=lambda r: r[1] - r[0])
        ok.append((rows[i], (seg[0] + seg[1]) / 2.0, width))
    if len(ok) < min_rows:
        return None
    return (np.array([o[0] for o in ok], float),
            np.array([o[1] for o in ok], float),
            plateau)


def angle(im, trim_frac=0.2):
    """(degrees, rows, rms, shaft_width). 0 degrees = hosel vertical."""
    r = shaft_rows(im)
    if r is None:
        return None
    ys, cs, plateau = r
    m, c = np.polyfit(ys, cs, 1)
    res = np.abs(cs - (m * ys + c))
    k = max(20, int(len(ys) * (1 - trim_frac)))
    keep = np.argsort(res)[:k]
    m, c = np.polyfit(ys[keep], cs[keep], 1)
    rms = float(np.sqrt(np.mean((cs[keep] - (m * ys[keep] + c)) ** 2)))
    return float(np.degrees(np.arctan(m))), len(keep), rms, float(plateau)


def make_vertical(src, dst, tol=0.3, passes=14, verbose=True):
    """Rotate until the hosel is vertical to within tol degrees."""
    im = trim(Image.open(src).convert("RGBA"))
    a0 = angle(im)
    if a0 is None:
        if verbose:
            print(f"  {src}: NO SHAFT LINE FOUND, use a retail head with a hosel")
        im.save(dst)
        return im, None
    total, ang = 0.0, a0[0]
    for _ in range(passes):
        if abs(ang) < tol:
            break
        best = None
        for s in (+1, -1):                      # empirical sign check every pass
            cand = rot(im, s * ang)
            r = angle(cand)
            if r is None:
                continue
            if best is None or abs(r[0]) < abs(best[1]):
                best = (cand, r[0], s * ang)
        if best is None or abs(best[1]) >= abs(ang) - 1e-3:
            break                               # no improvement, stop rather than spin
        im, ang, applied = best
        total += applied
    r = angle(im)
    if verbose:
        print(f"  {src}: {a0[0]:+.2f} -> {r[0]:+.2f} deg over {r[1]} rows "
              f"(rms {r[2]:.1f}, shaft {r[3]:.0f}px), rotation {total:+.2f}")
    im.save(dst)
    return im, r[0]


