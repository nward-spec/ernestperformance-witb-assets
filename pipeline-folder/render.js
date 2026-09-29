// Renders every slide in slides.json at deviceScaleFactor 3 (3240x4050 masters).
// Usage: node render.js [slides.json] [outDir]  (outDir must be ABSOLUTE)
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { coverSlide, sectionSlide, outroSlide } = require("./template");

(async () => {
  const dataPath = process.argv[2] || path.join(__dirname, "slides.json");
  const outDir = process.argv[3] || path.join(__dirname, "out");
  fs.mkdirSync(outDir, { recursive: true });
  const data = JSON.parse(fs.readFileSync(dataPath, "utf8"));

  const pages = [];
  pages.push({ name: "01-cover", html: coverSlide(data) });
  data.slides.forEach((s, i) => {
    const slug = s.section.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    pages.push({ name: `${String(i + 2).padStart(2, "0")}-${slug}`, html: sectionSlide(data, s, i, data.slides.length) });
  });
  if (data.outro) pages.push({ name: `${String(pages.length + 1).padStart(2, "0")}-outro`, html: outroSlide(data) });

  const browser = await chromium.launch({
    executablePath: "/opt/pw-browsers/chromium",
    args: ["--force-color-profile=srgb"],
  });
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 3 });

  for (const p of pages) {
    const file = path.join(outDir, p.name + ".html");
    fs.writeFileSync(file, p.html);
    await page.goto("file://" + file, { waitUntil: "networkidle", timeout: 45000 }).catch(() => console.log(`  (networkidle timeout on ${p.name}, continuing)`));
    await page.waitForTimeout(600);
    const broken = await page.evaluate(() =>
      Array.from(document.images).filter(im => !im.complete || im.naturalWidth === 0).map(im => im.src));
    if (broken.length) console.log(`  BROKEN on ${p.name}:`, broken.join(" | "));
    await page.screenshot({ path: path.join(outDir, p.name + ".png") });
    console.log("rendered", p.name + ".png");
  }
  await browser.close();
})();
