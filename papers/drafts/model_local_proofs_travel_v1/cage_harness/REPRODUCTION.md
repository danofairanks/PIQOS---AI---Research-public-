# Reproducing the CAGE seal-path and governor-pipeline results

These are not run by `../run_all.py`: they need a dependency set and a local Redis. Pinned commit: `a11f0caa5198fbff4c2ef1443c25abc8a8f11ca7` of the repository named in `../PINS.txt`. Python 3.11. Results are about that commit under the stubs below; production behavior (real policy engine, real causal check, KMS-signed seals, strict mode) was not tested.

## Seal path (`attacks_cage_seal.py`)
1. Clone the pinned commit; create a venv; `pip install pyjwt cryptography opentelemetry-api fakeredis lupa redis pydantic pydantic-settings`.
2. `CAGE_ENV=test python attacks_cage_seal.py <repo_root>` (the script sets the HMAC/non-strict mode it needs and uses fakeredis with the repository's Lua script executing). Output: `out_cage_seal.json`.

## Governor pipeline (`attacks_cage_pipeline.py`) and fix test (`attacks_cage_deepcopy_fix.py`)
1. Same clone and venv; install the repository's remaining imports as they are requested (numpy, pandas, pyyaml, networkx, openai, python-json-logger, httpx, cachetools, fastapi, mcp, opentelemetry-sdk) and run `pip install -e <repo_root> --no-deps` so the `cage.plugins` entry point for the finance plugin resolves.
2. Run a local `redis-server` on 127.0.0.1:6379.
3. `CAGE_ENV=test CAGE_SEAL_STRICT_MODE=false CAGE_DOMAIN=finance EVIDENCE_STREAM_ENABLED=true REDIS_URL=redis://localhost:6379 PYTHONPATH=<repo_root> python attacks_cage_pipeline.py 1000000` (argument: the amount a concurrent task writes in the mutation case). `python attacks_cage_deepcopy_fix.py unpatched` and `... patched` run the fix test.
Disclosed stubs: the policy client always answers ALLOW (the policy file is untested) and the world-model causal check returns True. All other stages are the repository's own. Each script prints JSON with controls beside attacks; the draft's section 6b states which results were predicted before the run.

## Regression test (`test_govern_params_snapshot.py`)
Written for the repository's `tests/governor/` (uses its `governor_factory` fixture and markers). Without the fix it fails; with `params = copy.deepcopy(params)` as the first statement of `SymbolicGovernor.govern()` it passes. Run single-process: `pytest tests/governor/test_govern_params_snapshot.py -o addopts=""`.

## Follow-up pass 1 (`followup_2026-10-05/`, section 6b-ii)
Pinned commit `7e07cbae5509683e4be87f68de2e5c3063dd73b2`. Same venv as above plus `httpx`; run from the repository root with `PYTHONPATH=.`. `probe_part_a.py <out.json>` (state commitment, sanitizer coverage, verify scope); `probe_part_a4.py <out.json>` (sanitizer timing by input family, 20 s cap per call); `probe_part_a4b.py <old_sanitizer.py> <out.json>` (compare against the sanitizer file from `4b116e07c0b482b578364db1e3356b887517ad2f`, obtained with `git show 4b116e0:src/gateway/governance/pii_sanitizer.py`); `probe_e2e.py <out.json>` (needs the repository's `tests/` on the path for its `RecordingEvidenceSink`); `probe_part_b.py <out.json>` (a local `redis-server --port 6391`). Timings depend on hardware; the checks that matter are the growth ratio per doubling and the comparison with the earlier sanitizer, not the absolute seconds. Raw outputs from the author's run are in the same folder next to `PREREG_cage_deep_probe_pass1_2026-10-05.md`, which was written before the runs and amended twice (each amendment states what it was written after).

## Follow-up pass 2a (`followup_2026-10-05/`, files `*_2a_*`)
Same commit and venv as pass 1 (`7e07cbae5509683e4be87f68de2e5c3063dd73b2`), `PYTHONPATH=.` from the repository root. `probe_2a_c_p.py <out.json>` (vendored JCS edge cases, provider_07 posture table, JWKS URL); `probe_2a_g.py <out.json>` (token, replay store and gateway; needs `redis-server --port 6391`; software Ed25519 signer; evidence sink stubbed); `probe_2a_p_runtime.py <out.json>` (provider_07 adapter against an httpx mock transport); `probe_2a_p5.py <out.json>` (JWKS refresh behaviour). The preregistration (`PREREG_cage_deep_probe_pass2a_2026-10-05.md`) has two amendments, each stating what it was written after; the P5 amendment records a discarded first run.

## Follow-up pass 2b (`followup_2026-10-05/`, files `*_2b_*`)
Same commit and venv as before, `PYTHONPATH=.` from the repository root. `probe_2b_s_o_g.py <out.json>` (STPA validator, OCSF ingestor, evidence best-effort in the gateway; needs `redis-server --port 6391`) and `probe_2b_a.py <out.json>` (the adapter against an httpx mock supervisor). Both import the repository's `contracts` module first because importing the STPA module first raises a circular `ImportError`. The preregistration has one amendment, written after the runs.

