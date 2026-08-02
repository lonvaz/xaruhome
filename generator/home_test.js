const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const ctx = await b.newContext({ viewport:{width:1440,height:1050} });
  await ctx.addInitScript(()=>{try{localStorage.setItem('xaru_lang','1')}catch(e){}});
  const p = await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  const base='http://localhost:8899', o={};
  await p.goto(base+'/real-estate/', {waitUntil:'domcontentloaded'});
  await p.waitForSelector('.xr_mph_card'); await p.waitForTimeout(1000);
  o.statsBuy = await p.$$eval('.xr_mph_stat', n=>n.map(x=>x.textContent.trim()));
  o.typesBuy = await p.$$eval('.xr_mph_type option', n=>n.slice(0,4).map(x=>x.textContent));
  await p.$eval('[data-op="land"]', e=>e.click()); await p.waitForTimeout(600);
  o.statsLand = await p.$$eval('.xr_mph_stat', n=>n.map(x=>x.textContent.trim()));
  o.typesLand = await p.$$eval('.xr_mph_type option', n=>n.slice(0,4).map(x=>x.textContent));
  await p.$eval('[data-op="buy"]', e=>e.click()); await p.waitForTimeout(500);
  // busqueda combinada
  await p.selectOption('.xr_mph_type', await p.$eval('.xr_mph_type option:nth-child(2)', e=>e.value));
  await p.selectOption('.xr_mph_beds','4');
  await p.fill('.xr_mph_pmin','2000000');
  await p.fill('.xr_mph_q','Spain'); await p.waitForTimeout(400);
  await p.$eval('.xr_mph_go', e=>e.click()); await p.waitForTimeout(1600);
  o.url = (await p.url()).replace(base,'');
  await p.waitForSelector('.xr_mp_card, .xr_mp_empty', {timeout:12000});
  o.count = await p.$eval('.xr_mp_count', e=>e.textContent.trim());
  o.chips = await p.$$eval('.xr_mp_chip', n=>n.map(x=>x.textContent.trim()));
  o.errors = errs;
  console.log(JSON.stringify(o,null,1));
  await b.close();
})();
