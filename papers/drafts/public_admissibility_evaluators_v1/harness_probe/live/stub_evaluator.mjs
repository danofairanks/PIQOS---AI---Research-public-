// Local stand-in evaluators used ONLY to validate the runner's logic (they are not models of the hosted service).
import http from 'node:http';
export function startStub(mode) {
  let calls = 0;
  const textOf = (p) => (p.observed_reality?.signals || []).map((s) => s.statement).join(' | ');
  const perStatement = (p) => (p.observed_reality?.signals || []).map((s) => s.statement);
  const decide = (p) => {
    const structRevoked = p.authority_provenance?.current_authority?.status !== 'active';
    if (mode === 'structural') return structRevoked;
    if (mode === 'lexical') return perStatement(p).some((s) => /revok|expired/i.test(s));
    if (mode === 'broken') return false;
    return false;
  };
  const server = http.createServer((q, s) => { let raw = ''; q.on('data', (c) => (raw += c)); q.on('end', () => { calls++;
    if (mode === 'flaky' && calls > 3) { s.writeHead(500); s.end('boom'); return; }
    let p = {}; try { p = JSON.parse(raw); } catch { /* */ }
    const block = mode === 'flaky' ? false : decide(p);
    s.writeHead(200, { 'content-type': 'application/json' }); s.end(JSON.stringify({ decision: block ? 'BLOCK' : 'ALLOW', admissible: !block })); }); });
  return new Promise((r) => server.listen(0, '127.0.0.1', () => r({ url: `http://127.0.0.1:${server.address().port}/api/evaluate`, calls: () => calls, close: () => new Promise((x) => { server.closeAllConnections?.(); server.close(x); }) })));
}
