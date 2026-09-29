# Head orientation and final axis nudge.
#
#   orient_down()  rotate a head cutout so its shaft stub points straight DOWN,
#                  before the fine levelling pass. Replaces hand-set coarse
#                  angles, which are the usual cause of a large residual.
#
#   axis_nudge()   after a first render, measure the neck against the shaft on
#                  the SHIPPED png and shift the padded head canvas to close
#                  the gap. Typically takes a build from several px of offset
#                  to under one px on every club slide. Two minutes.
#
# Requires level.py from this same folder (trim, alpha, rot) and scipy.

import numpy as np
from PIL import Image
from scipy.ndimage import binary_erosion
from level import trim, alpha, rot


def shaft_angle(im, er=14):
    """Direction from the head's centre of mass to the shaft tip.

    Erode the alpha mask hard: what survives is the head, because the shaft is
    thin. The farthest non-core pixels from the head centroid are the shaft tip.
    Returns degrees where 0 = pointing right (+x) and +90 = pointing down (+y),
    which is image coordinates, not maths coordinates.
    """
    a = alpha(im)
    core = binary_erosion(a, np.ones((er, er)))
    if core.sum() < 50:                      # head too small for that kernel
        core = binary_erosion(a, np.ones((6, 6)))
    ys, xs = np.where(core)
    cy, cx = ys.mean(), xs.mean()
    ys2, xs2 = np.where(a & ~core)
    if len(ys2) == 0:
        return None
    d = (ys2 - cy) ** 2 + (xs2 - cx) ** 2
    k = max(1, len(d) // 100)                # mean of the farthest 1%, not one pixel
    idx = np.argsort(d)[-k:]
    ty, tx = ys2[idx].mean(), xs2[idx].mean()
    ang = np.degrees(np.arctan2(ty - cy, tx - cx))
    return ang, (cy, cx), (ty, tx)


def orient_down(src, dst, er=14, verbose=True):
    """Rotate a head cutout so the shaft stub points down. Run BEFORE level2()."""
    im = trim(Image.open(src).convert("RGBA"))
    r = shaft_angle(im, er)
    if r is None:
        im.save(dst)
        return im, 0.0
    ang, _, _ = r
    delta = ang - 90.0                       # PIL rotates CCW for positive degrees
    im2 = rot(im, delta)
    if verbose:
        a2 = shaft_angle(im2, er)
        now = a2[0] if a2 else float("nan")
        print(f"  orient {src}: shaft at {ang:+.1f} deg -> rotate {delta:+.1f} -> now {now:+.1f}")
    im2.save(dst)
    return im2, delta


def measure_axis(png, ground_rgb, bands, club_col=(0, 470), thr=60):
    """Measure the club's horizontal centre in each band of a SHIPPED 1080x1350 slide.

    ground_rgb: the theme's paper colour, e.g. (0xD9,0xD9,0xD9) for zone.
    bands: dict of name -> (y0, y1) at 1x. For bandHeights [440,290,330] with the
           140px topbar, the useful ones are
           neck (555,578), shaft (600,850), grip (900,1180).
    Returns {name: centre_x} and prints the offsets that matter.
    """
    im = np.array(Image.open(png).convert("RGB")).astype(int)
    mask = np.abs(im - np.array(ground_rgb)).sum(axis=2) > thr
    mask[:, club_col[1]:] = False
    mask[:, :club_col[0]] = False
    out = {}
    for name, (y0, y1) in bands.items():
        cols = mask[y0:y1].sum(axis=0)
        out[name] = float(np.average(np.arange(len(cols)), weights=cols)) if cols.sum() else None
    if out.get("neck") is not None and out.get("shaft") is not None:
        print(f"  {png}: neck-shaft {out['neck']-out['shaft']:+.1f}px", end="")
        if out.get("grip") is not None:
            print(f"   grip-shaft {out['grip']-out['shaft']:+.1f}px", end="")
        print()
    return out


def axis_nudge(pad_png, offset_render_px, render_scale, min_px=2, verbose=True):
    """Shift a padded head canvas so its neck lands on the shaft axis.

    offset_render_px: (neck - shaft) measured on the shipped slide. Positive means
                      the neck sits to the RIGHT of the shaft.
    render_scale:     min(maxW/canvas_w, (bandH-16)/canvas_h) for that head.

    The art moves by offset/scale canvas pixels. Because the template centres the
    image, moving the art left is done by padding transparent columns on the right.
    Re-render after calling this.
    """
    px = int(round(offset_render_px / render_scale))
    if abs(px) < min_px:
        if verbose:
            print(f"  {pad_png}: no shift needed ({px:+d}px)")
        return None
    im = Image.open(pad_png).convert("RGBA")
    w, h = im.size
    canvas = Image.new("RGBA", (w + 2 * abs(px), h), (0, 0, 0, 0))
    canvas.paste(im, (0 if px > 0 else 2 * abs(px), 0))
    canvas.save(pad_png)
    if verbose:
        print(f"  {pad_png}: shift {px:+d} canvas px -> new canvas {canvas.size}")
    return canvas


def render_scale(pad_png, maxW, bandH):
    """The scale the template will actually apply. Never compute a join from maxW
    alone: a height-limited head silently halves its join width."""
    im = Image.open(pad_png)
    return min(maxW / im.width, (bandH - 16) / im.height)
