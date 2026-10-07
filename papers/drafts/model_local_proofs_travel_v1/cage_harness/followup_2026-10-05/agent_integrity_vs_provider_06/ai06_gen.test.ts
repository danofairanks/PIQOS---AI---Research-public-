// Run inside a COPY of the vendored upstream: packages/core/tests/ai06_gen.test.ts (vitest). Writes genuine receipt + upstream control results.
import { mkdtemp, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { it } from "vitest";
import { createReceipt, FileReceiptStore, recheckTrustedReceipt, verifyTrustedEnvelope } from "../src/index.js";
import { trustedEnvelopeFixture } from "./support/trusted-envelope.js";
import { receiptSigner, receiptSigningOptions, receiptTrust } from "./support/receipt-keys.js";

const OUT = process.env.AI06_OUT as string;
const codes = (r: any) => [r.status, r.findings.map((f: any) => f.code)];
it("gen", async () => {
  const dir = await mkdtemp(join(tmpdir(), "ai06-"));
  const { envelope, context } = await trustedEnvelopeFixture();
  const verification = await verifyTrustedEnvelope(envelope, context);
  const mk = async (runId: string, store: FileReceiptStore) => createReceipt({
    runId, path: join(dir, runId + ".json"), envelope, verification, context, ...receiptSigningOptions,
    createdAt: new Date("2026-08-02T00:00:00.000Z"), expiresAt: new Date("2026-08-02T01:00:00.000Z"), receiptStore: store });
  const store = new FileReceiptStore(join(dir, "s1"));
  const receipt = await mk("genuine", store);
  const now = new Date("2026-08-02T00:30:00.000Z");
  const base = { trust: receiptTrust, context, now };
  const out: any = { publicKeyPem: receiptTrust.keys["test-key-1"], keyId: receiptSigner.keyId, receipt, envelopeDigest: receipt.envelopeDigest };
  // control: PASS (fresh store per case so replay is isolated)
  const fresh = async (id: string) => { const st = new FileReceiptStore(join(dir, id)); const r = await mk(id, st); return { st, r }; };
  { const { st, r } = await fresh("c_pass"); out.U0_upstream_pass = codes(await recheckTrustedReceipt({ ...base, receipt: r, envelope, receiptStore: st })); }
  { const { st, r } = await fresh("c_aud"); out.A3_aud = codes(await recheckTrustedReceipt({ ...base, trust: { ...receiptTrust, audience: "other" }, receipt: r, envelope, receiptStore: st })); }
  { const { st, r } = await fresh("c_iss"); out.A3_iss = codes(await recheckTrustedReceipt({ ...base, trust: { ...receiptTrust, issuer: "other" }, receipt: r, envelope, receiptStore: st })); }
  { const { st, r } = await fresh("c_pur"); out.A3_pur = codes(await recheckTrustedReceipt({ ...base, trust: { ...receiptTrust, purpose: "other" }, receipt: r, envelope, receiptStore: st })); }
  { const { st, r } = await fresh("c_rep"); const o = { ...base, receipt: r, envelope, receiptStore: st }; out.A6_first = codes(await recheckTrustedReceipt(o)); out.A6_second = codes(await recheckTrustedReceipt(o)); }
  { const { st, r } = await fresh("c_exp"); out.A7_at_expiry = codes(await recheckTrustedReceipt({ ...base, now: new Date(r.expiresAt), receipt: r, envelope, receiptStore: st })); out.A7_one_ms_before = codes(await recheckTrustedReceipt({ ...base, now: new Date(Date.parse(r.expiresAt) - 1), receipt: r, envelope, receiptStore: st })); }
  { const { st, r } = await fresh("c_fut"); out.A5_future = codes(await recheckTrustedReceipt({ ...base, now: new Date("2026-08-01T00:00:00.000Z"), receipt: r, envelope, receiptStore: st })); }
  { const { st, r } = await fresh("c_sub"); const env2 = structuredClone(envelope) as any; env2.response = { ...(env2.response ?? {}), text: "changed after verification" };
    try { out.A1_subject_changed = codes(await recheckTrustedReceipt({ ...base, receipt: r, envelope: env2, receiptStore: st })); } catch (e: any) { out.A1_subject_changed = ["THROW", String(e).slice(0, 120)]; } }
  { const { st, r } = await fresh("c_enc"); const raw = Buffer.from(r.signature.value, "base64"); const alt = structuredClone(r) as any; alt.signature.value = raw.toString("base64url");
    // receiptDigest covers the signature in upstream; digest is recomputed by the checker so the variant also reports receipt.mutated
    out.A8_noncanonical_sig_encoding = codes(await recheckTrustedReceipt({ ...base, receipt: alt, envelope, receiptStore: st })); }
  { const { st, r } = await fresh("c_tamper"); const t = structuredClone(r) as any; t.expiresAt = "2030-01-01T00:00:00.000Z"; out.C_tampered_upstream = codes(await recheckTrustedReceipt({ ...base, receipt: t, envelope, receiptStore: st })); }
  try { await createReceipt({ runId: "long", path: join(dir, "long.json"), envelope, verification, context, ...receiptSigningOptions, createdAt: new Date("2026-08-02T00:00:00Z"), expiresAt: new Date("2036-08-02T00:00:00Z"), receiptStore: new FileReceiptStore(join(dir, "s9")) }); out.A5_long_lifetime_creation = "created"; } catch (e: any) { out.A5_long_lifetime_creation = "refused: " + String(e.message).slice(0, 80); }
  await writeFile(OUT, JSON.stringify(out, null, 1));
});
