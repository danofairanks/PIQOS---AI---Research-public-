# Approver identity for NeMo refinement — results (2026-10-06)
Pin: CAGE main 0c657b4c (mcp pinned <2 in my venv to import the app; no repo change). PREREG written first. Probe: `probe_approver_identity.py` -> `out_approver_identity.json`. Real `root_app` through an ASGI transport with chosen `l5d-client-id` headers; only `reload_nemo_rails`/`get_nemo_rails` patched. The Linkerd mesh layer is NOT executed; this is the application half only.

## Results (all predictions held)
| id | observed | classification |
|---|---|---|
| controls | no header, untrusted identity, two headers -> 403; unknown id and second approve -> 404; approved=false -> "rejected", no reload; apply-refinement only stages (no reload); blank rationale -> 400 | control-holds |
| P1 | advisor identity proposes: 200 staged | within design |
| P2 | the SAME identity approves its own proposal: 200 "applied", reload called once | outside the docs' "human risk officer must approve"; within what the mesh policy admits (below) |
| P3 | `reviewer` accepted as "" / "x" / the advisor's own service-account name / "Jane Doe, Chief Risk Officer"; stored verbatim | outside: attribution is a free-text field |
| P4 | with trusted set {advisor, risk-officer-sa}: all four proposer/approver pairings succeed; the app has no per-path or per-role rule | outside: no structural separation of roles in the app |
| P6 | the approval record has no field carrying the caller's `l5d-client-id` | outside: the authenticated identity is not recorded |
| P7 | `reload_nemo_rails()` is called with no argument; `_refinement_proposals` is read only by the three endpoints, so the proposal's `control_id`/`verdict` are used nowhere else in `src` | "applied" means "rails reloaded from the on-disk config"; whether some other process writes that config is not visible here |
Also (read, not run): the checked-in mesh policy (`deployment/k8s/linkerd-mtls-policy.yaml`) admits exactly one identity to every gated route, `cage-advisor-sa`, with the comment "The advisor is the only client of the gated routes"; propose and approve are both gated routes. The code elsewhere calls the advisor the "untrusted neural plane". No src caller of `approve-refinement` exists (docs only), so nothing shows the advisor does approve; the point is that the deployed policy lets it. Proposals live in an in-process dict (lost on restart; per-replica).

## Reading
The recursion fix is real at the pipeline (it stages instead of applying), but "human-gated" is a convention carried by a free-text `reviewer` string: under the policy the repo ships, the only identity that can reach `approve-refinement` is the advisor workload that the code treats as untrusted, and the handler cannot tell proposer from approver or record who approved. Boundary: mesh half untested; a deployment that routes humans through a different path or identity set is not visible in this checkout (note the app half would still not distinguish roles, P4). Not filed (held; candidate alongside the other held findings).
