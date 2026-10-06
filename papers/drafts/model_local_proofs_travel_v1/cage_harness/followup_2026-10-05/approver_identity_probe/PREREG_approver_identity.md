# PREREG — approver identity for NeMo refinement (2026-10-06)
Written BEFORE any probe in this folder was run. Pin: CAGE main 0c657b4c.
Question (from the recursion note): the docs call refinement "human-gated" (propose stages; a risk officer approves). Is the approver structurally distinct from the proposer?
Read before running (source, not executed): `/v1/nemo/propose-refinement` and `/v1/nemo/approve-refinement/{id}` are both under the gateway's gated route; the mesh policy (`deployment/k8s/linkerd-mtls-policy.yaml`) admits `cage-advisor-sa` only ("the advisor is the only client of the gated routes"); the app middleware admits any identity in `CAGE_TRUSTED_CLIENT_IDENTITIES` with no per-path role; `reviewer` is a request-body string; the in-process dict `_refinement_proposals` holds proposals; approval calls `reload_nemo_rails()` with no proposal content.
Declared boundary: README/docs: "A human risk officer must review and approve"; mesh comment: advisor is the only client of gated routes. The advisor is described elsewhere in the code as the "untrusted neural plane".
Method: import the real `root_app` from `src/gateway/server/hybrid_server.py`, send requests through an ASGI transport with chosen `l5d-client-id` headers (no lifespan), patch only `reload_nemo_rails`/`get_nemo_rails` (heavy, and the reload is the effect to observe). Env: CAGE_ENV=development.
## Predictions
P1 With trusted identity A, propose returns staged. YES.
P2 The SAME identity A approves the proposal it proposed (approved=true), status "applied", reload called once. YES.
P3 `reviewer` is not checked against anything: an empty string, a fake human name and A's own service-account name are all accepted. YES.
P4 With trusted set {A, R}: both identities can both propose and approve (no role distinction). YES.
P5 Controls: no header -> 403; header not in set -> 403; two l5d headers -> 403; approve unknown id -> 404; second approve after applied -> 404; approved=false -> "rejected", reload not called; apply-refinement only stages (reload not called).
P6 The approval record stores the supplied `reviewer` string and no caller identity (no field carrying the l5d identity). YES.
P7 `reload_nemo_rails` is called with no argument derived from the proposal (control_id/verdict never reach the reload). YES.
## Classification
Per item: control-holds / within-declared-boundary / outside-declared-boundary. The mesh layer (Linkerd) is NOT executed here; only the application half. A result that the app cannot distinguish roles is "within" if the deployment's identity set is meant to be human-only, "outside" if the advisor is the only admitted identity (as the checked-in mesh policy says). No issue filed.
