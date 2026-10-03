#!/usr/bin/env node
/* Validates live_probe.mjs against local stub evaluators and checks its refusals. Usage: node selftest_live.mjs <harmonic-test-harness clone>
   No network beyond loopback. The stubs are not models of the hosted service. */
import cp from 'node:child_process'; import fs from 'node:fs'; import os from 'node:os'; import path from 'node:path'; import { startStub } from './stub_evaluator.mjs';
const clone = path.resolve(process.argv[2]); const here = path.dirname(new URL(import.meta.url).pathname); const FAKEKEY = 'hs_live_FAKEKEY_for_selftest_0123456789';
let bad = 0; const t = (ok, msg) => { if (!ok) bad++; console.log(`${ok ? 'PASS' : 'FAIL'}  ${msg}`); };
const run = (args, env = {}) => new Promise((res) => { const c = cp.spawn(process.execPath, [path.join(here, 'live_probe.mjs'), '--clone', clone, ...args], { env: { PATH: process.env.PATH, ...env } }); let o = '', e = ''; c.stdout.on('data', (d) => (o += d)); c.stderr.on('data', (d) => (e += d)); c.on('close', (code) => res({ code, out: o, err: e })); });
const live = (url, extra = []) => ['--live', '--url', url, '--spacing-ms', '0', '--authorization-ref', 'selftest', '--out', fs.mkdtempSync(path.join(os.tmpdir(), 'lp_')), ...extra];
const parse = (r) => JSON.parse(r.out.slice(r.out.indexOf('{')));
const byId = (tr, id) => tr.calls.find((c) => c.id === id);
const load = (r) => JSON.parse(fs.readFileSync(parse(r).transcript, 'utf8'));
{ // dry run: no calls, 16 planned
  const s = await startStub('structural'); const r = await run(['--url', s.url]); const d = parse(r);
  t(r.code === 0 && d.calls_planned === 16 && s.calls() === 0 && /dry-run/.test(d.mode), 'dry run plans 16 calls and makes none'); await s.close(); }
{ // refusals
  const r1 = await run(['--live', '--authorization-ref', 'x'], {}); t(r1.code === 3 && /HARMONIC_API_KEY/.test(r1.err), 'live without a key is refused');
  const r2 = await run(['--live', '--url', 'https://example.com/api/evaluate', '--authorization-ref', 'x'], { HARMONIC_API_KEY: FAKEKEY }); t(r2.code === 3 && /allow-list/.test(r2.err), 'a host off the allow-list is refused');
  const r3 = await run(['--live', '--authorization-ref', 'x', '--spacing-ms', '100'], { HARMONIC_API_KEY: FAKEKEY }); t(r3.code === 3 && /spacing/.test(r3.err), 'spacing under 5 s on the real host is refused');
  const r4 = await run(['--live'], { HARMONIC_API_KEY: FAKEKEY }); t(r4.code === 3 && /authorization-ref/.test(r4.err), 'live without an authorization reference is refused'); }
{ // structural evaluator: reads structure, not text
  const s = await startStub('structural'); const r = await run(live(s.url), { HARMONIC_API_KEY: FAKEKEY }); const tr = load(r); const n = (id) => byId(tr, id).normalized;
  t(tr.status === 'COMPLETE' && tr.calls.length === 16 && s.calls() === 16, 'structural stub: 16 calls, complete');
  t(['V0', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'S1'].every((i) => n(i) === 'BLOCK') && ['M1', 'M2', 'W1', 'W2'].every((i) => n(i) === 'ALLOW'), 'structural stub: wording variants BLOCK (structure says revoked); mentions and text-only defeats ALLOW');
  t(JSON.stringify(tr.analysis.claim_boundary_findings) === '["W1","W2"]' && tr.analysis.mismatches_vs_prediction.length === 0 && tr.analysis.false_positives.length === 0, 'structural stub: W1, W2 flagged as claim-boundary findings; no prediction mismatches');
  t(!fs.readFileSync(parse(r).transcript, 'utf8').includes(FAKEKEY) && !r.out.includes(FAKEKEY) && !r.err.includes(FAKEKEY), 'the key appears nowhere: not in the transcript file, stdout or stderr'); await s.close(); }
{ // lexical evaluator: reads listed words in statements only
  const s = await startStub('lexical'); const r = await run(live(s.url), { HARMONIC_API_KEY: FAKEKEY }); const tr = load(r); const n = (id) => byId(tr, id).normalized;
  t(['P1', 'P2'].every((i) => n(i) === 'ALLOW') && ['D1', 'D2', 'V0'].every((i) => n(i) === 'BLOCK'), 'lexical stub: controls discriminate; V0 (listed word) BLOCK');
  t(['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'S1', 'W2'].every((i) => n(i) === 'ALLOW') && n('W1') === 'BLOCK', 'lexical stub: rewording, Cyrillic, translation, split, role swap, structure-only and unlisted text all ALLOW; listed-word text BLOCK');
  t(['M1', 'M2'].every((i) => n(i) === 'BLOCK') && JSON.stringify(tr.analysis.false_positives) === '["M1","M2"]', 'lexical stub: mention and negation are false positives');
  t(tr.analysis.claim_boundary_findings.length === 8 && tr.analysis.mismatches_vs_prediction.length >= 6, 'lexical stub: eight claim-boundary findings; the prediction mismatches are reported'); await s.close(); }
{ // broken controls: stop after four calls
  const s = await startStub('broken'); const r = await run(live(s.url), { HARMONIC_API_KEY: FAKEKEY }); const tr = load(r);
  t(r.code === 2 && tr.status === 'STOPPED_CONTROLS_DO_NOT_DISCRIMINATE' && tr.calls.length === 4 && s.calls() === 4, 'non-discriminating controls stop the run after four calls'); await s.close(); }
{ // flaky: abort on first 500
  const s = await startStub('flaky'); const r = await run(live(s.url), { HARMONIC_API_KEY: FAKEKEY }); const tr = load(r);
  t(r.code === 2 && /ABORTED_NON_2XX/.test(tr.status) && s.calls() === 4, 'the first non-2xx aborts the run, with no retry'); await s.close(); }
console.log(bad ? `${bad} FAILED` : 'all passed'); process.exit(bad ? 1 : 0);
