# pipeline

Renderer for the carousel slides in this repo. Code only: the rules that drive it live outside this repository.

| file | what it does |
|---|---|
| `hosel.py` | Makes a club head's hosel vertical and measures the angle. Read the header before changing anything here. |
| `orient.py` | Coarse rotation so the shaft points down, the final axis nudge, and `render_scale()`. |
| `level.py` | Shared primitives (`trim`, `alpha`, `rot`) plus older levelling and crop helpers. `hosel.py` and `orient.py` import from it. |
| `make_strips.py` | Builds shaft and grip strips at 3x. |
| `cutout_white.py` | Flood-fill cutout for product shots on a white ground. |
| `export_png.py` | Export: 3240x4050 master, one Lanczos pass to exactly 1080x1350, UnsharpMask(0.8, 60, 3), PNG. Asserts the master is exactly 3x so a wrong `deviceScaleFactor` fails loudly. |
| `render.js` | Renders `slides.json` at `deviceScaleFactor 3`. Needs an ABSOLUTE outDir. |
| `template.js` | Slide templates and the twelve themes. v3.8. |

## Setup

```
npm install
```

Chromium is expected at `/opt/pw-browsers/chromium`, which `render.js` pins. Do not run `playwright install`.

Python needs `pillow`, `numpy` and `scipy`.

## Two invariants worth stating here

- **Band heights must sum to 1060.** Bands start at y=140 and must clear the footer and watermark at about y=1250.
- **Strip widths are derived, never fixed.** The shaft strip is built to the head's rendered hosel width and the grip follows the shaft. `dispW` on a strip item sets the rendered width. A fixed strip steps at the junction on every head except a driver, which is why it went unnoticed for weeks.
