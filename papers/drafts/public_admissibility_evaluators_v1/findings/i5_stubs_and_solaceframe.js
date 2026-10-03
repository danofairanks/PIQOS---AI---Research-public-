// repos: authority-continuity-primitive-public @ 95ee54d, consequence-boundary-public @ a6ee5f8, solaceframe-public @ c6bb260
// run: node --experimental-strip-types i5_stubs_and_solaceframe.js <dir containing clones>   (Node 22)
const path = require('path'), fs = require('fs'), os = require('os'), cp = require('child_process'), D = path.resolve(process.argv[2]);
async function call(rel, body) { const t = path.join(os.tmpdir(), 'stub_' + process.pid + '_' + path.basename(path.dirname(path.dirname(rel))) + '.mjs'); fs.copyFileSync(path.join(D, rel), t);
  const m = await import(t); let got; m.default({ method: 'POST', body }, { status() { return this; }, json(x) { got = x; return this; } }); fs.unlinkSync(t); return got; }
(async () => {
  const j = (x) => JSON.stringify(x);
  console.log('authority-continuity revoked packet:', j(await call('authority-continuity-primitive-public/api/evaluate.js', { authority: { revoked: true, status: 'revoked', expires_at: '2000-01-01' } })));
  console.log('authority-continuity empty body:    ', j(await call('authority-continuity-primitive-public/api/evaluate.js', {})));
  console.log('consequence-boundary revoked packet:', j(await call('consequence-boundary-public/api/evaluate.js', { authority: { revoked: true } })));
  console.log('consequence-boundary empty body:    ', j(await call('consequence-boundary-public/api/evaluate.js', {})));
  const src = fs.readFileSync(path.join(D, 'solaceframe-public/apps/studio/lib/runtime/identity/identity-admission.ts'), 'utf8').split('\n').filter((l) => !/^import /.test(l)).join('\n');
  const t = path.join(os.tmpdir(), 'ia_' + process.pid + '.ts'); fs.writeFileSync(t, src);
  const code = `import('${t}').then(m=>{const s=(o)=>({identity_score:100,geometry_score:100,body_score:100,motion_score:100,wardrobe_score:100,hair_score:100,chronology_score:100,environment_score:100,...o});
    for (const [l,o] of [['all 100',{}],['hair 60',{hair_score:60}],['hair 59',{hair_score:59}],['hair 0',{hair_score:0}]]) console.log('solaceframe computeAdmission',l,JSON.stringify(m.computeAdmission(s(o))))})`;
  const r = cp.spawnSync(process.execPath, ['--experimental-strip-types', '-e', code], { encoding: 'utf8' }); fs.unlinkSync(t); process.stdout.write(r.stdout || r.stderr);
})();
