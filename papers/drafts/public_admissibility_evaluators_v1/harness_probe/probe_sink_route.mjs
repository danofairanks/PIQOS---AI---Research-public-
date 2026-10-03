// Usage: node --experimental-strip-types probe_sink_route.mjs <path to harmonic-test-harness clone>
// Copies the route changing only the next/server import (shim) and the two export const lines; prints a logic diff note.
import fs from 'node:fs'; import path from 'node:path'; import os from 'node:os'; import crypto from 'node:crypto';
const H = path.resolve(process.argv[2]); const srcPath = path.join(H, 'app/api/synthetic-execution-sink/route.ts');
let src = fs.readFileSync(srcPath, 'utf8'); const orig = src;
src = src.replace('import { NextResponse } from "next/server";', 'const NextResponse = { json: (b, i) => ({ body: b, status: (i && i.status) || 200 }) };')
  .replace('export const runtime = "nodejs";\n', '').replace('export const dynamic = "force-dynamic";\n', '');
const tmp = path.join(os.tmpdir(), 'sink_route_' + process.pid + '.mts'); fs.writeFileSync(tmp, src);
const changed = orig.split('\n').filter((l, i) => l !== src.split('\n')[i]).length; // informational
const { publicKey, privateKey } = crypto.generateKeyPairSync('ed25519'); const other = crypto.generateKeyPairSync('ed25519');
process.env.HARMONIC_SECURE_EXECUTION_PUBLIC_KEY_PEM = publicKey.export({ type: 'spki', format: 'pem' });
const { POST } = await import(tmp);
const stable = (v) => v === null || v === undefined ? v : Array.isArray(v) ? v.map(stable) : typeof v === 'object' ? Object.fromEntries(Object.keys(v).sort().map((k) => [k, stable(v[k])])) : v; // NOT the route's: used only for non-__proto__ helper cases
// reproduce the route's canonicalize exactly (including out[key] = ... assignment semantics)
function stableSort(value) { if (value === null || value === undefined) return value; if (Array.isArray(value)) return value.map(stableSort); if (typeof value === 'object') { const out = {}; for (const key of Object.keys(value).sort()) out[key] = stableSort(value[key]); return out; } return value; }
const canon = (v) => JSON.stringify(stableSort(v)); const sha = (s) => crypto.createHash('sha256').update(s, 'utf8').digest('hex');
function mint(executeObj, { decision = 'PERMIT', ttl = 60000, issuedOffset = -1000, key = privateKey } = {}) {
  const now = Date.now(); const unsigned = { version: '1.0.0', decision, issued_at: new Date(now + issuedOffset).toISOString(), expires_at: new Date(now + issuedOffset + ttl).toISOString(), execute_hash: sha(canon(executeObj)), receipt_id: crypto.randomUUID() };
  const signature = crypto.sign(null, Buffer.from(canon(unsigned), 'utf8'), key).toString('base64');
  return Buffer.from(JSON.stringify({ ...unsigned, signature })).toString('base64');
}
const call = async (bodyText, receiptB64, header = 'x-harmonic-execution-receipt') => { const h = new Headers({ 'content-type': 'application/json' }); if (receiptB64) h.set(header, receiptB64);
  const r = await POST(new Request('http://sink.local/api/synthetic-execution-sink', { method: 'POST', headers: h, body: bodyText })); return { status: r.status, why: r.body.error || (r.body.effect_observed ? 'effect_observed' : 'ok') }; };
const P = { amount: 10 }; const out = {};
out.C1_no_receipt = await call(JSON.stringify({ execute: P }), null);
out.C2_deny_receipt = await call(JSON.stringify({ execute: P }), mint(P, { decision: 'DENY' }));
out.C3_expired = await call(JSON.stringify({ execute: P }), mint(P, { ttl: 500, issuedOffset: -2000 }));
out.C4_wrong_key = await call(JSON.stringify({ execute: P }), mint(P, { key: other.privateKey }));
out.C5_payload_mismatch = await call(JSON.stringify({ execute: { amount: 11 } }), mint(P));
out.C6_valid = await call(JSON.stringify({ execute: P }), mint(P));
out.C7_alt_header = await call(JSON.stringify({ execute: P }), mint(P), 'x-solace-receipt');
{ const r = mint(P); out.A1_replay = []; for (let i = 0; i < 5; i++) out.A1_replay.push((await call(JSON.stringify({ execute: P }), r)).status); }
out.A2_proto_smuggle = await call('{"execute":{"amount":10,"__proto__":{"amount":1000000}}}', mint(P));
out.A2_proto_nested = await call('{"execute":{"order":{"amount":10,"__proto__":{"amount":1000000}}}}', mint({ order: { amount: 10 } }));
out.A2_proto_string = await call('{"execute":{"amount":10,"__proto__":"x"}}', mint(P));
{ const lastWins = { amount: 1000000 }; out.A3_dupkey_vs_last_wins_receipt = await call('{"execute":{"amount":10,"amount":1000000}}', mint(lastWins)); out.A3_dupkey_vs_first_wins_receipt = await call('{"execute":{"amount":10,"amount":1000000}}', mint(P)); }
out.A4_number_forms = [await call('{"execute":{"amount":1e1}}', mint(P)), await call('{"execute":{"amount":10.0}}', mint(P))].map((x) => x.status);
// evidence that the smuggled member exists in the executed object and not in the hashed form
{ const parsed = JSON.parse('{"execute":{"amount":10,"__proto__":{"amount":1000000}}}').execute; out.A2_evidence = { own_keys: Object.keys(parsed), has_own___proto__: Object.prototype.hasOwnProperty.call(parsed, '__proto__'), canonical_of_smuggled: canon(parsed), canonical_of_clean: canon(P), hashes_equal: sha(canon(parsed)) === sha(canon(P)), spread_copy_keys: Object.keys({ ...parsed }), spread_has_own___proto__: Object.prototype.hasOwnProperty.call({ ...parsed }, '__proto__') }; }
out.route_edit_note = 'only the next/server import and two export const lines differ from the repository file';
fs.unlinkSync(tmp); console.log(JSON.stringify(out, null, 1));
