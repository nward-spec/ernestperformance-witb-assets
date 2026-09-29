# Export v4: 3240x4050 master -> single Lanczos
# pass to exactly 1080x1350 -> UnsharpMask(0.8, 60, 3) -> PNG optimize.
# Asserts the master is exactly 3x the target so a wrong deviceScaleFactor
# fails loudly instead of silently softening type.
import sys
import glob
import os
from PIL import Image, ImageFilter

TARGET = (1080, 1350)

def export(src, dst):
    im = Image.open(src).convert("RGB")
    assert im.size == (TARGET[0] * 3, TARGET[1] * 3), \
        f"{src}: master {im.size} is not exactly 3x {TARGET}"
    im = im.resize(TARGET, Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=0.8, percent=60, threshold=3))
    im.save(dst, "PNG", optimize=True)
    print("export:", dst, os.path.getsize(dst) // 1024, "KB")

if __name__ == "__main__":
    indir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for f in sorted(glob.glob(os.path.join(indir, "*.png"))):
        export(f, os.path.join(outdir, os.path.basename(f)))
