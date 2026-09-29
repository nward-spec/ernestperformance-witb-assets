// Ernest Performance — WITB carousel template v3.8
// v3.8 (2 Sep 2026): strip widths are driven by `dispW` so the shaft and grip
// match the head's rendered hosel width. See witb-shaft-width-fix.md.
const path = require("path");

const GREEN = "#1D2714";      // EP Woods Green (canonical)
const SAND = "#DBD2CB";
const GREEN_DEEP = "#142A0F";   // EP Moss
const MIDNIGHT = "#0D0D0D";     // EP Midnight
const DUSK = "#22333B";         // EP Dusk
const BREEZE = "#445A61";       // EP Breeze
const FOREST = "#31411B";       // EP Forest
const PINE = "#425A29";         // EP Pine
const RICH_BLACK = "#0A0908";   // EP Rich Black
const BUNKER = "#A9927D";       // EP Bunker Brown
const SUNRISE = "#D99544";      // EP Sunrise

const THEMES = {
  classic: {
    dark: true,
    bodyBg: GREEN, fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: SAND, chipFg: GREEN, divider: SAND + "26",
    logo: "cutouts/wm-ep.png", shadow: "rgba(0,0,0,0.45)", tint: GREEN,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1200px 800px at 20% 0%, rgba(219,210,203,0.07), transparent 60%),radial-gradient(900px 700px at 90% 100%, rgba(219,210,203,0.05), transparent 60%);"></div>`,
  },
  sand: {
    dark: false,
    bodyBg: SAND, fg: GREEN, fgMuted: GREEN + "B3", faint: GREEN + "66",
    chipBg: GREEN, chipFg: SAND, divider: GREEN + "26",
    logo: "cutouts/wm-ep-green.png", shadow: "rgba(20,31,27,0.35)", tint: GREEN,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1400px 900px at 80% 0%, rgba(20,31,27,0.06), transparent 60%),linear-gradient(180deg, rgba(20,31,27,0.03) 0%, transparent 30%, transparent 70%, rgba(20,31,27,0.05) 100%);"></div>`,
  },
  contour: {
    dark: true,
    bodyBg: `linear-gradient(170deg, ${GREEN} 0%, ${GREEN_DEEP} 100%)`, fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: SAND, chipFg: GREEN, divider: SAND + "26",
    logo: "cutouts/wm-ep.png", shadow: "rgba(0,0,0,0.45)", tint: GREEN,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;opacity:0.55;background:repeating-radial-gradient(ellipse 1600px 1150px at 118% -8%, transparent 0px, transparent 66px, rgba(219,210,203,0.075) 66px, rgba(219,210,203,0.075) 68px),repeating-radial-gradient(ellipse 1300px 900px at -15% 112%, transparent 0px, transparent 82px, rgba(219,210,203,0.055) 82px, rgba(219,210,203,0.055) 84px);"></div>`,
  },
  blueprint: {
    dark: true,
    bodyBg: MIDNIGHT, fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: SAND, chipFg: GREEN, divider: SAND + "33",
    logo: "cutouts/wm-ep.png", shadow: "rgba(0,0,0,0.5)", tint: MIDNIGHT,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:repeating-linear-gradient(0deg, transparent 0px, transparent 89px, rgba(219,210,203,0.05) 89px, rgba(219,210,203,0.05) 90px),repeating-linear-gradient(90deg, transparent 0px, transparent 89px, rgba(219,210,203,0.05) 89px, rgba(219,210,203,0.05) 90px);"></div><div style="position:absolute;inset:36px;z-index:1;pointer-events:none;border:1px solid rgba(219,210,203,0.16);"></div>`,
  },
  sunrise: {
    dark: true,
    bodyBg: RICH_BLACK, fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: SUNRISE, chipFg: RICH_BLACK, divider: SUNRISE + "40",
    logo: "cutouts/wm-ep.png", shadow: "rgba(0,0,0,0.55)", tint: RICH_BLACK,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1300px 700px at 50% 108%, rgba(217,149,68,0.16), transparent 62%),radial-gradient(900px 500px at 85% 112%, rgba(217,149,68,0.10), transparent 60%);"></div><div style="position:absolute;left:0;right:0;bottom:0;height:5px;z-index:2;background:linear-gradient(90deg, transparent, ${SUNRISE}AA, transparent);"></div>`,
  },
  bunker: {
    dark: false,
    bodyBg: BUNKER, fg: RICH_BLACK, fgMuted: RICH_BLACK + "B3", faint: RICH_BLACK + "73",
    chipBg: RICH_BLACK, chipFg: SAND, divider: RICH_BLACK + "33",
    logo: "cutouts/wm-ep-green.png", shadow: "rgba(10,9,8,0.35)", tint: RICH_BLACK,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1400px 900px at 15% -5%, rgba(244,241,236,0.18), transparent 55%),linear-gradient(180deg, transparent 60%, rgba(10,9,8,0.10) 100%);"></div>`,
  },
  lake: {
    dark: true,
    bodyBg: "#010D27", fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: SAND, chipFg: "#010D27", divider: SAND + "26",
    logo: "cutouts/wm-ep.png", shadow: "rgba(0,0,0,0.55)", tint: "#010D27",
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1300px 800px at 78% -8%, rgba(68,90,97,0.30), transparent 60%),radial-gradient(1000px 700px at 12% 108%, rgba(219,210,203,0.05), transparent 62%);"></div>`,
  },
  slate: {
    dark: true,
    bodyBg: "#383E4A", fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: SAND, chipFg: "#383E4A", divider: SAND + "2E",
    logo: "cutouts/wm-ep.png", shadow: "rgba(10,9,8,0.45)", tint: "#383E4A",
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1400px 900px at 20% -6%, rgba(68,90,97,0.35), transparent 58%),linear-gradient(180deg, transparent 65%, rgba(1,13,39,0.20) 100%);"></div>`,
  },
  breeze: {
    dark: true,
    bodyBg: BREEZE, fg: SAND, fgMuted: SAND + "B3", faint: SAND + "73",
    chipBg: SAND, chipFg: DUSK, divider: SAND + "33",
    logo: "cutouts/wm-ep.png", shadow: "rgba(1,13,39,0.45)", tint: DUSK,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1400px 900px at 82% -8%, rgba(219,210,203,0.10), transparent 58%),radial-gradient(1100px 800px at 8% 110%, rgba(1,13,39,0.35), transparent 62%);"></div>`,
  },
  zone: {
    dark: false,
    bodyBg: "#D9D9D9", fg: GREEN, fgMuted: GREEN + "B3", faint: GREEN + "66",
    chipBg: GREEN, chipFg: "#D9D9D9", divider: GREEN + "26",
    logo: "cutouts/wm-ep-green.png", shadow: "rgba(29,39,20,0.30)", tint: GREEN,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1400px 900px at 80% 0%, rgba(68,90,97,0.10), transparent 60%),linear-gradient(180deg, rgba(29,39,20,0.03) 0%, transparent 30%, transparent 70%, rgba(29,39,20,0.06) 100%);"></div>`,
  },
  dusk: {
    dark: true,
    bodyBg: `linear-gradient(180deg, ${DUSK} 0%, #17232A 100%)`, fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: SAND, chipFg: DUSK, divider: BREEZE + "66",
    logo: "cutouts/wm-ep.png", shadow: "rgba(0,0,0,0.5)", tint: DUSK,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1300px 800px at 80% -10%, rgba(68,90,97,0.35), transparent 60%),radial-gradient(1000px 700px at 10% 110%, rgba(1,13,39,0.45), transparent 65%);"></div>`,
  },
  forest: {
    dark: true,
    bodyBg: `linear-gradient(165deg, ${FOREST} 0%, ${GREEN_DEEP} 85%)`, fg: SAND, fgMuted: SAND + "B3", faint: SAND + "66",
    chipBg: PINE, chipFg: SAND, divider: SAND + "26",
    logo: "cutouts/wm-ep.png", shadow: "rgba(0,0,0,0.5)", tint: GREEN,
    deco: `<div style="position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(1200px 800px at 20% 0%, rgba(66,90,41,0.30), transparent 60%),radial-gradient(900px 700px at 90% 100%, rgba(219,210,203,0.05), transparent 60%);"></div>`,
  },
};
function theme(data) { return THEMES[data.theme] || THEMES.classic; }

const FONT_HEAD = `'Archivo', 'Helvetica Neue', Arial, sans-serif`;

function resolveImg(p) {
  if (/^https?:\/\//.test(p) || p.startsWith("file://")) return p;
  return "file://" + path.join(__dirname, p);
}

function baseHead(t, extraCss = "") {
  const fontDir = path.join(__dirname, "node_modules/@fontsource/archivo/files");
  const faces = [400, 500, 700, 800, 900].map(w =>
    `@font-face { font-family:'Archivo'; font-weight:${w}; font-style:normal;
      src: url('file://${fontDir}/archivo-latin-${w}-normal.woff2') format('woff2'); }`).join("\n");
  return `<!doctype html><html><head><meta charset="utf-8">
  <style>
  ${faces}
    * { margin:0; padding:0; box-sizing:border-box; }
    html,body { width:1080px; height:1350px; overflow:hidden; }
    body { background:${t.bodyBg}; font-family:${FONT_HEAD}; color:${t.fg}; position:relative; }
    .watermark { position:absolute; right:44px; bottom:40px; z-index:50; opacity:0.95; }
    .watermark img { height:62px; }
    ${extraCss}
  </style></head><body>`;
}

function watermark(t) {
  return `<div class="watermark"><img src="${resolveImg(t.logo)}"></div>`;
}

// ---------- SECTION SLIDE: vertical full club ----------
function sectionSlide(data, slide, index, total) {
  const t = theme(data);
  // Band heights must always sum to 1060 (bands start at y=140 and must clear
  // the footer and watermark at y~1250). Redistributing toward the shaft makes
  // the club read longer without growing the head.
  const bh = data.bandHeights || [450, 340, 270];
  const bands = [
    { key: "head",  label: slide.head.labelOverride  || "HEAD",  h: bh[0], item: slide.head  },
    { key: "shaft", label: slide.shaft.labelOverride || "SHAFT", h: bh[1], item: slide.shaft },
    { key: "grip",  label: slide.grip.labelOverride  || "GRIP",  h: bh[2], item: slide.grip  },
  ];

  const cell = (b) => {
    const it = b.item;
    const rot = it.vrotate || 0;
    const zoom = it.vzoom || 1;
    if (it.strip) {
      // Strips are authored at 3x and displayed at dispW so they stay crisp at
      // deviceScaleFactor 3. dispW must match the head's hosel width at its
      // rendered size, or the club steps at the junction.
      return `<div class="imgband" style="height:${b.h}px">
        <img class="plain" src="${resolveImg(it.img)}" style="width:${it.dispW || 160}px;">
      </div>`;
    }
    if (b.key === "head" && !it.noRotate) {
      return `<div class="imgband" style="height:${b.h}px; align-items:flex-end;">
        <img class="plain" src="${resolveImg(it.img)}" style="max-height:${b.h - 16}px; max-width:${it.maxW || 440}px; margin-bottom:2px;">
      </div>`;
    }
    if (it.noRotate) {
      return `<div class="imgband" style="height:${b.h}px">
        <img class="plain" src="${resolveImg(it.img)}" style="max-height:${b.h - 24}px; max-width:440px;">
      </div>`;
    }
    const boxW = it.boxW || 150;
    const shiftY = it.shiftY === undefined ? -50 : it.shiftY;
    return `<div class="imgband" style="height:${b.h}px">
      <div class="vbox" style="width:${boxW}px; height:${b.h - 10}px;">
        <img src="${resolveImg(it.img)}"
             style="width:${b.h}px; height:${b.h}px; transform: translate(-50%,${shiftY}%) rotate(${rot}deg) scale(${zoom});">
      </div>
    </div>`;
  };

  const bandsHtml = bands.map(b => `
    <div class="band" style="height:${b.h}px">
      <div class="clubcol">${cell(b)}</div>
      <div class="txtcol">
        <div class="chip">${b.label}</div>
        <div class="pname">${b.item.name}</div>
        <div class="pspec">${b.item.spec || ""}</div>
      </div>
    </div>`).join("");

  const css = `
    .topbar { height:140px; display:flex; align-items:center; justify-content:space-between; padding:0 56px; position:relative; z-index:5; }
    .section { font-size:62px; font-weight:900; letter-spacing:0.02em; text-transform:uppercase; }
    .meta { text-align:right; }
    .meta .p { font-size:25px; font-weight:700; letter-spacing:0.14em; }
    .meta .e { font-size:17px; font-weight:500; letter-spacing:0.2em; color:${t.faint}; margin-top:6px; }
    .bands { position:relative; z-index:5; padding:0 48px 0 40px; }
    .band { display:flex; align-items:center; }
    .clubcol { width:470px; height:100%; display:flex; align-items:center; justify-content:center; }
    .imgband { display:flex; align-items:center; justify-content:center; width:100%; }
    .imgband img.plain { filter: drop-shadow(0 18px 30px ${t.shadow}); }
    .vbox { position:relative; overflow:hidden; }
    .vbox img { position:absolute; top:50%; left:50%; object-fit:contain; filter: drop-shadow(0 10px 20px ${t.shadow}); }
    .txtcol { flex:1; display:flex; flex-direction:column; justify-content:center; gap:13px; padding-left:36px; border-left:1px solid ${t.divider}; height:72%; }
    .chip { align-self:flex-start; background:${t.chipBg}; color:${t.chipFg}; font-weight:800; font-size:19px; letter-spacing:0.18em; padding:7px 15px; border-radius:6px; }
    .pname { font-size:32px; font-weight:800; line-height:1.16; }
    .pspec { font-size:23px; font-weight:500; line-height:1.3; color:${t.fgMuted}; }
    .foot { position:absolute; left:56px; bottom:44px; font-size:17px; letter-spacing:0.16em; color:${t.faint}; font-weight:600; z-index:5; }
  `;

  return baseHead(t, css) + `
    ${t.deco}
    <div class="topbar">
      <div class="section">${slide.section}</div>
      <div class="meta"><div class="p">${data.player}</div><div class="e">${data.event}</div></div>
    </div>
    <div class="bands">${bandsHtml}</div>
    <div class="foot">${total > 1 ? (index + 1) + " / " + total + " &nbsp;&middot;&nbsp; " : ""}${data.source.toUpperCase()}</div>
    ${watermark(t)}
  </body></html>`;
}

// ---------- COVER (theme-aware since v3.2) ----------
function coverDark(data, t) {
  const heroes = data.cover.heroClubs.map((c) => `
    <div class="hero">
      <div class="heroimg"><img src="${resolveImg(c.img)}"></div>
      <div class="herolabel">${c.label}</div>
    </div>`).join("");

  const css = `
    .bg { position:absolute; inset:0; z-index:0; }
    .bg img { width:100%; height:100%; object-fit:cover; object-position:${data.cover.objectPosition || "55% 12%"}; }
    .shade { position:absolute; inset:0; z-index:2;
      background: linear-gradient(180deg, ${t.tint}E6 0%, ${t.tint}66 30%, ${t.tint}59 55%, ${t.tint}F5 88%); }
    .content { position:absolute; inset:0; z-index:10; display:flex; flex-direction:column; padding:64px 56px; }
    .kicker { font-size:30px; font-weight:700; letter-spacing:0.34em; color:${SAND}; }
    .title { font-size:118px; font-weight:900; line-height:0.98; letter-spacing:0.01em; margin-top:14px; text-transform:uppercase; color:${SAND}; }
    .sub { margin-top:16px; font-size:25px; font-weight:600; letter-spacing:0.18em; color:${SAND}CC; }
    .heroes { margin-top:auto; display:flex; gap:20px; align-items:flex-end; padding-bottom:100px; }
    .hero { flex:1; display:flex; flex-direction:column; gap:14px; align-items:center; }
    .heroimg { height:300px; display:flex; align-items:flex-end; justify-content:center; }
    .heroimg img { max-height:300px; max-width:300px; object-fit:contain; filter: drop-shadow(0 20px 34px rgba(0,0,0,0.55)); }
    .herolabel { font-size:20px; font-weight:700; letter-spacing:0.06em; text-align:center; color:${SAND}; }
    .swipe { position:absolute; left:56px; bottom:44px; z-index:12; font-size:22px; font-weight:800; letter-spacing:0.22em; color:${SAND}; }
  `;

  return baseHead(t, css) + `
    <div class="bg"><img src="${resolveImg(data.cover.backgroundUrl)}"></div>
    <div class="shade"></div>
    <div class="content">
      <div class="kicker">${data.coverKicker || "WHAT'S IN THE BAG"}</div>
      <div class="title">${data.player}</div>
      <div class="sub">${data.coverEvent || data.event}</div>
      <div class="heroes">${heroes}</div>
    </div>
    <div class="swipe">${data.coverSwipe || "SWIPE FOR THE FULL BAG"} &nbsp;&raquo;&raquo;</div>
    ${watermark(t)}
  </body></html>`;
}

function coverLight(data, t) {
  const heroes = data.cover.heroClubs.map((c) => `
    <div class="hero">
      <div class="heroimg"><img src="${resolveImg(c.img)}"></div>
      <div class="herolabel">${c.label}</div>
    </div>`).join("");

  const css = `
    .content { position:absolute; inset:0; z-index:10; display:flex; flex-direction:column; padding:60px 56px 0; }
    .kicker { font-size:26px; font-weight:700; letter-spacing:0.34em; color:${t.fgMuted}; }
    .title { font-size:96px; font-weight:900; line-height:0.98; letter-spacing:0.01em; margin-top:12px; text-transform:uppercase; color:${t.fg}; }
    .sub { margin-top:12px; font-size:25px; font-weight:600; letter-spacing:0.22em; color:${t.fgMuted}; }
    .panel { margin-top:36px; height:580px; position:relative; border:1px solid ${t.fg}40; box-shadow: 0 26px 48px ${t.shadow}; }
    .panel img { width:100%; height:100%; object-fit:cover; object-position:${data.cover.objectPosition || "50% 20%"}; }
    .panel .tick { position:absolute; width:26px; height:26px; border-color:${t.fg}; border-style:solid; z-index:3; }
    .tick.tl { top:-7px; left:-7px; border-width:3px 0 0 3px; }
    .tick.tr { top:-7px; right:-7px; border-width:3px 3px 0 0; }
    .tick.bl { bottom:-7px; left:-7px; border-width:0 0 3px 3px; }
    .tick.br { bottom:-7px; right:-7px; border-width:0 3px 3px 0; }
    .heroes { margin-top:30px; display:flex; gap:20px; align-items:flex-end; }
    .hero { flex:1; display:flex; flex-direction:column; gap:12px; align-items:center; }
    .heroimg { height:230px; display:flex; align-items:flex-end; justify-content:center; }
    .heroimg img { max-height:230px; max-width:260px; object-fit:contain; filter: drop-shadow(0 18px 28px ${t.shadow}); }
    .herolabel { font-size:19px; font-weight:700; letter-spacing:0.06em; text-align:center; color:${t.fg}; }
    .swipe { position:absolute; left:56px; bottom:44px; z-index:12; font-size:22px; font-weight:800; letter-spacing:0.22em; color:${t.fg}; }
  `;

  return baseHead(t, css) + `
    ${t.deco}
    <div class="content">
      <div class="kicker">${data.coverKicker || "WHAT'S IN THE BAG"}</div>
      <div class="title">${data.player}</div>
      <div class="sub">${data.coverEvent || data.event}</div>
      <div class="panel">
        <img src="${resolveImg(data.cover.backgroundUrl)}">
        <div class="tick tl"></div><div class="tick tr"></div><div class="tick bl"></div><div class="tick br"></div>
      </div>
      <div class="heroes">${heroes}</div>
    </div>
    <div class="swipe">${data.coverSwipe || "SWIPE FOR THE FULL BAG"} &nbsp;&raquo;&raquo;</div>
    ${watermark(t)}
  </body></html>`;
}

function coverSlide(data) {
  const t = theme(data);
  return t.dark ? coverDark(data, t) : coverLight(data, t);
}

// ---------- OUTRO (v3.4) ----------
function outroSlide(data) {
  const t = theme(data);
  const css = `
    .wrap { position:absolute; inset:0; display:flex; flex-direction:column; align-items:center; justify-content:center; padding:0 96px; z-index:10; text-align:center; }
    .lockup { margin-bottom:64px; }
    .lockup img { height:190px; }
    .h { font-size:76px; font-weight:900; line-height:1.06; }
    .b { margin-top:34px; font-size:30px; line-height:1.5; font-weight:500; color:${t.fgMuted}; max-width:820px; }
    .tagline { margin-top:56px; font-size:36px; font-weight:900; letter-spacing:0.14em; text-transform:uppercase; }
    .tagrule { width:72px; height:3px; background:${t.fg}; margin:18px auto 0; }
    .handle { margin-top:22px; font-size:25px; font-weight:800; letter-spacing:0.12em; color:${t.fgMuted}; }
  `;
  return baseHead(t, css) + `
    ${t.deco}
    <div class="wrap">
      <div class="lockup"><img src="${resolveImg(t.logo)}"></div>
      <div class="h">${data.outro.headline}</div>
      <div class="b">${data.outro.body}</div>
      <div class="tagline">${data.outro.tagline}</div>
      <div class="tagrule"></div>
      <div class="handle">${data.outro.handle}</div>
    </div>
  </body></html>`;
}

module.exports = { coverSlide, sectionSlide, outroSlide, THEMES };
