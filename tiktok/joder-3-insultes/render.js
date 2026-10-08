const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const [mode, ...ts] = process.argv.slice(2);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
  await p.addInitScript(() => { window.__RENDERING = true; });
  await p.goto('file://' + path.resolve('scene.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(300);
  if (mode === 'stills') {
    for (const t of ts) { await p.evaluate(t => render(t), +t); await p.screenshot({ path: `still_${t}.png` }); }
  } else {
    const fps = 30, total = await p.evaluate(() => TL.total); const n = Math.round(total * fps);
    fs.mkdirSync('frames', { recursive: true });
    for (let i = 0; i < n; i++) {
      await p.evaluate(t => render(t), i / fps);
      await p.screenshot({ path: `frames/f${String(i).padStart(5, '0')}.jpg`, type: 'jpeg', quality: 92 });
      if (i % 150 === 0) console.log(i, '/', n);
    }
  }
  await b.close();
})();
