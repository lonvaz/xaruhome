const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const ctx=await b.newContext({viewport:{width:1440,height:1100},locale:'es-ES'});
const p=await ctx.newPage(); const errs=[]; p.on('pageerror',e=>errs.push(e.message));
console.log('=== ENLACE PROFUNDO AL FILTRO DEL PILAR');
for (const [u,k,v] of [
  ['/real-estate/commercial-hospitality/?operating=halted','operating','halted'],
  ['/real-estate/commercial-hospitality/?operating=operational','operating','operational'],
  ['/real-estate/commercial-hospitality/?structure=recapitalisation-jv','structure','recapitalisation-jv'],
  ['/es/real-estate/commercial-hospitality/?operating=halted','operating','halted'],
  ['/real-estate/commercial-hospitality/?operating=inventado','operating','inventado'],
]) {
  await p.goto('http://127.0.0.1:8899'+u,{waitUntil:'domcontentloaded'});
  await p.waitForTimeout(2200);
  const d=await p.evaluate(([k])=>{
    const c=document.querySelector('.xr_catalog');
    const s=c.querySelector('[data-f="'+k+'"]');
    return { valor:s?s.value:'(sin selector)',
             visibles:[...c.querySelectorAll('.xr_opp_col')].filter(x=>x.offsetParent).length,
             conteo:(c.querySelector('.xr_count_now')||{}).textContent };
  },[k]);
  const ok = (v==='inventado') ? (d.valor==='') : (d.valor===v && d.visibles>0);
  console.log(' '+(ok?'ok  ':'MAL ')+u.padEnd(62)+' select='+String(d.valor).padEnd(22)+' visibles='+d.visibles+' conteo='+d.conteo);
}
console.log('\n=== EL FILTRO ESCRIBE LA URL');
await p.goto('http://127.0.0.1:8899/real-estate/commercial-hospitality/',{waitUntil:'domcontentloaded'});
await p.waitForTimeout(2000);
await p.selectOption('.xr_catalog [data-f="operating"]','halted');
await p.waitForTimeout(500);
console.log('  tras elegir "halted":', p.url().replace('http://127.0.0.1:8899',''));
await p.click('.xr_catalog .xr_filter_reset'); await p.waitForTimeout(400);
console.log('  tras Restablecer   :', p.url().replace('http://127.0.0.1:8899',''));
console.log('errores JS:',errs);
await b.close();})();
