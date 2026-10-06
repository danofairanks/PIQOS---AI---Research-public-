#!/usr/bin/env bash
# Clones the pinned commits into work/, runs each repository's own tests as the control, runs both probes, and diffs against the committed outputs.
# Needs git, network, Python 3.10+. About 3-5 minutes (Project-AI is ~100 MB shallow).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"; W="$HERE/work"; mkdir -p "$W"; cd "$W"
RA_SHA=26893c293e579a4d31f6d5183ea52bec3efc7b95; PA_SHA=7650aa14dd8e3832e9dfd4d438000dd4e1f273d8
fetch() { # url sha dir
  [ -d "$3/.git" ] || { mkdir -p "$3" && git -C "$3" init -q && git -C "$3" remote add origin "$1"; }
  git -C "$3" fetch -q --depth 1 --filter=blob:limit=1m origin "$2" && git -C "$3" checkout -q FETCH_HEAD; }
echo "== reference implementation"; fetch https://github.com/grahamb-ai/runtime-authority-reference-implementation.git $RA_SHA ra
python3 -m venv ra_venv && ra_venv/bin/pip -q install "fastapi>=0.115" pydantic sqlmodel pdfplumber python-docx python-dotenv python-multipart pytest httpx alembic 2>&1 | tail -1
( cd ra && DATABASE_URL=sqlite:///$W/ra_test.db ../ra_venv/bin/python -m pytest -q -p no:cacheprovider 2>&1 | tail -1 )
rm -f ra_probe.db; ( cd ra && ENV=production DATABASE_URL=sqlite:///$W/ra_probe.db PYTHONPATH=. ../ra_venv/bin/python "$HERE/reference_impl/probe_reference_impl.py" 2>/dev/null > "$W/ra_out.json" )
python3 "$HERE/check_outputs.py" "$W/ra_out.json" "$HERE/reference_impl/out_reference_impl.json"; RA_RC=$?
echo "== Project-AI"; fetch https://github.com/IAmSoThirsty/Project-AI.git $PA_SHA pa
python3 -m venv pa_venv && pa_venv/bin/pip -q install pytest pyyaml cryptography 2>&1 | tail -1
( cd pa && PYTHONPATH=src ../pa_venv/bin/python -m pytest -q -p no:cacheprovider tests/test_safe_allow_calibration.py tests/test_conversation_threat_register.py tests/test_threat_model.py tests/test_authorization_separation.py tests/test_capability_tokens.py tests/test_policy_registry.py tests/test_invariant_severity.py tests/test_governance_mode.py tests/test_evidence_bundle.py tests/test_degraded_mode.py tests/test_governance_liveness.py tests/test_replay_protection.py tests/test_governance_observability.py tests/test_policy_mutation_control.py tests/test_semantic_collision.py tests/test_state_branching.py tests/test_genesis_reanchor.py tests/test_time_trust.py tests/test_governance_contract.py 2>&1 | tail -1 )
( cd pa && PYTHONPATH=src:. ../pa_venv/bin/python "$HERE/project_ai/probe_project_ai.py" 2>/dev/null > "$W/pa_out.json" )
python3 "$HERE/check_outputs.py" "$W/pa_out.json" "$HERE/project_ai/out_project_ai.json"; PA_RC=$?
echo "reference_impl rc=$RA_RC  project_ai rc=$PA_RC"; exit $((RA_RC + PA_RC))
