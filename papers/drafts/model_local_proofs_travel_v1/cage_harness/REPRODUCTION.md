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
