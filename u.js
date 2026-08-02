const { chromium } = require('/opt/node-tools/node_modules/playwright');
(async()=>{const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await(await b.newContext({viewport:{width:1440,height:900},locale:'es-ES'})).newPage();
await p.goto('http://127.0.0.1:8899/es/real-estate/private-properties/',{waitUntil:'domcontentloaded'});
await p.waitForTimeout(2200);
console.log('URL final:',p.url());
console.log(await p.evaluate(()=>{const a=document.querySelector('.xr_mp_preview_more a');
 return {texto:a&&a.textContent.trim(), href:a&&a.getAttribute('href'),
 titulo:(document.querySelector('.xr_mp_preview')||{})&&document.querySelectorAll('.xr_mp_preview .xr_mp_card').length};}));
await b.close();})();
