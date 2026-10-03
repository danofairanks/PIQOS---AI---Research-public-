// Usage: node probe_disposition.mjs <clone>. Extracts dispositionFrom verbatim from examples/raw-vs-governed/run.mjs (the file itself runs network code on import).
import fs from 'node:fs'; import path from 'node:path';
const src = fs.readFileSync(path.join(path.resolve(process.argv[2]), 'examples/raw-vs-governed/run.mjs'), 'utf8');
const m = src.match(/function dispositionFrom\(unified\) \{[\s\S]*?\n\}\n/); if (!m) throw new Error('function not found');
const dispositionFrom = new Function(m[0] + '; return dispositionFrom;')();
const cases = {
  control_allow: { decision: 'ALLOW', admissible: true },
  control_block: { decision: 'BLOCK', admissible: false },
  control_pass_only: { status: 'PASS', admissible: true },
  control_permit_not_admissible: { decision: 'ALLOW', admissible: false },
  control_block_and_allow: { decision: 'BLOCK', status: 'ALLOWED', admissible: true },
  conflict_hold_vs_allowed: { decision: 'HOLD', status: 'ALLOWED', admissible: true },
  conflict_review_vs_permit: { decision: 'REVIEW', directive: 'PERMIT', admissible: true },
  nested_governance_over_toplevel_block: { decision: 'BLOCK', admissible: false, governance: { decision: 'ALLOW', admissible: true } },
  nested_harmonic_over_toplevel_block: { decision: 'BLOCK', admissible: false, harmonic: { decision: 'ALLOW', admissible: true } },
  whitespace_case: { decision: ' allow ', admissible: true },
};
const out = {}; for (const [k, v] of Object.entries(cases)) out[k] = dispositionFrom(v).normalized; console.log(JSON.stringify(out, null, 1));
