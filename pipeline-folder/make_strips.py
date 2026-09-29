import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image
import numpy as np

def auto_vertical(im):
    """Rotate so the object's long axis is vertical (PCA on the alpha mask)."""
    a = np.array(im)[...,3] > 40
    ys, xs = np.where(a)
    ys = ys - ys.mean(); xs = xs - xs.mean()
    cov = np.cov(np.vstack([xs, ys]))
    w, v = np.linalg.eigh(cov)
    major = v[:, np.argmax(w)]          # (dx, dy)
    ang = np.degrees(np.arctan2(major[1], major[0]))   # angle of major axis from +x
    rot = -(90 - ang)                    # PIL rotates CCW; bring major axis to vertical
    im2 = im.rotate(rot, expand=True, resample=Image.BICUBIC)
    print(f"    auto_vertical: major axis {ang:+.1f} deg -> rotate {rot:+.1f}")
    return im2

def trim(im):
    a = np.array(im)[...,3]; ys, xs = np.where(a > 10)
    return im.crop((xs.min(), ys.min(), xs.max()+1, ys.max()+1))

def butt_down(im):
    a = np.array(im)[...,3] > 40
    rows = np.where(a.any(axis=1))[0]; n = max(4, len(rows)//6)
    top = np.median([a[r].sum() for r in rows[:n]]); bot = np.median([a[r].sum() for r in rows[-n:]])
    if top > bot: im = im.transpose(Image.ROTATE_180)
    return im

def strip(src, dst, out_w=360, out_h=1260, target=60, auto=True, angle=0,
          make_butt_down=False, flip180=False, anchor="center", y_bias=0.5):
    im = Image.open(src).convert("RGBA")
    if auto: im = auto_vertical(im)
    elif angle: im = im.rotate(angle, expand=True, resample=Image.BICUBIC)
    im = trim(im)
    if make_butt_down: im = butt_down(im)
    if flip180: im = im.transpose(Image.ROTATE_180)
    # straighten: per-row alpha centroid
    arr = np.array(im); al = arr[...,3]; h, w = al.shape; cx = w//2
    out = np.zeros_like(arr)
    for y in range(h):
        row = al[y]
        if row.max() > 10:
            c = int(np.average(np.arange(w), weights=row.astype(float)))
            out[y] = np.roll(arr[y], cx-c, axis=0)
    im = Image.fromarray(out)
    al = np.array(im)[...,3]; wds = (al > 10).sum(axis=1)
    t = np.median(wds[wds > 0]); s = target/t
    im = im.resize((max(1,int(im.width*s)), max(1,int(im.height*s))), Image.LANCZOS)
    im = trim(im)
    # usable region: rows at least 60% of target wide (drops tapered ends)
    al = np.array(im)[...,3]; wds = (al > 10).sum(axis=1)
    good = np.where(wds > 0.6*target)[0]
    lo, hi = (good.min(), good.max()) if len(good) else (0, im.height-1)
    usable = hi - lo + 1
    if anchor == "top":
        y0 = lo
    else:
        c = lo + int(usable*y_bias)
        y0 = int(np.clip(c - out_h//2, lo, max(lo, hi - out_h + 1)))
    seg = im.crop((0, y0, im.width, min(im.height, y0+out_h)))
    canvas = Image.new("RGBA", (out_w, out_h), (0,0,0,0))
    a2 = np.array(seg)[...,3]; cols = (a2 > 10).sum(axis=0)
    c = int(np.average(np.arange(seg.width), weights=cols))
    canvas.paste(seg, (out_w//2 - c, 0))
    canvas.save(dst)
    vc = (np.array(canvas)[...,3] > 40)
    rows_filled = vc.any(axis=1).sum()
    vis = vc.sum(axis=1); vis = vis[vis > 0]
    print(f"  {dst}: usable {usable}px, need {out_h}px, filled {rows_filled}/{out_h} rows, "
          f"width {np.median(vis):.0f}px = {np.median(vis)/3:.1f}px at dispW {out_w//3}")
    return canvas
