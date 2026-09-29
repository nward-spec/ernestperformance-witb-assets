from PIL import Image
import numpy as np
from scipy.ndimage import label, binary_fill_holes
def cut(src, dst, thr=228, maxdim=2400):
    im = Image.open(src).convert("RGB")
    im.thumbnail((maxdim, maxdim), Image.LANCZOS)
    arr = np.array(im)
    nw = (arr[...,0]>thr)&(arr[...,1]>thr)&(arr[...,2]>thr)
    lab,n = label(nw)
    border = set(lab[0,:]) | set(lab[-1,:]) | set(lab[:,0]) | set(lab[:,-1]); border.discard(0)
    bg = np.isin(lab, list(border)); fg = binary_fill_holes(~bg)
    lab2,n2 = label(fg)
    if n2>1:
        s = np.bincount(lab2.ravel()); s[0]=0; fg = lab2==s.argmax()
    out = Image.fromarray(np.dstack([arr,(fg*255).astype(np.uint8)]),"RGBA")
    ys,xs = np.where(fg); out = out.crop((xs.min(),ys.min(),xs.max()+1,ys.max()+1))
    out.save(dst); print("cut", dst, out.size)
    return out
