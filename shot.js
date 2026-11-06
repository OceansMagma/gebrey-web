const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const base = 'file://' + path.resolve('dist') + '/';
  const only = process.argv[2];
  const configs = [
    ['d', 1440, 900, 'dark'],
    ['m', 390, 844, 'dark'],
    ['l', 1440, 900, 'light'],
    ['s', 1280, 620, 'dark'],
  ];
  const stops = (process.argv[3] || '0,0.5,1,1.45,2,2.5,3,3.6,4,4.5,5,5.6').split(',').map(Number);
  for (const [name, w, h, scheme] of configs) {
    if (only && !only.split(',').includes(name)) continue;
    const ctx = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1, colorScheme: scheme });
    const page = await ctx.newPage();
    const errors = [];
    page.on('pageerror', e => errors.push('pageerror: ' + e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push('console: ' + m.text()); });
    page.on('requestfailed', r => errors.push('reqfail: ' + r.url().slice(0, 90)));
    await page.goto(base + 'index.html', { waitUntil: 'load' });
    await page.waitForTimeout(2600);
    for (const k of stops) {
      await page.evaluate((y) => window.scrollTo({ top: y, behavior: 'instant' }), Math.round(k * h));
      await page.waitForTimeout(450);
      await page.screenshot({ path: `shots/${name}-${String(k).replace('.', '_')}.png` });
    }
    const sw = await page.evaluate(() => document.documentElement.scrollWidth);
    const sh = await page.evaluate(() => document.documentElement.scrollHeight);
    const fonts = await page.evaluate(() => Array.from(document.fonts).filter(f => f.status === 'loaded').map(f => f.family).filter((v, i, a) => a.indexOf(v) === i));
    const names = await page.evaluate(() => Array.from(document.querySelectorAll('[data-fit]')).map(e => [e.getAttribute('data-fit'), e.style.getPropertyValue('--w'), getComputedStyle(e).fontSize, e.getBoundingClientRect().width, e.parentElement.getBoundingClientRect().width]));
    console.log(name, 'scroll', sw, 'x', sh, 'fonts', JSON.stringify(fonts), JSON.stringify(names), errors.length ? errors.slice(0, 5) : 'no errors');
    await ctx.close();
  }
  await browser.close();
})();
