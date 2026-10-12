# Re-run of passes 1 to 2c at a later commit (2026-10-12)

Pinned commit: `1903a20f84f8f42af52c8fa3a6f46307fe38df59` (main after #467), repository named in `../../PINS.txt`. The probe scripts are those in `../followup_2026-10-05/`, unmodified, except the three copies here:
- `probe_2b_s_o_g_1903a20f.py`: the 1 MB OCSF metadata case is wrapped in try/except (it now raises a validation error, which aborted the rest of the script).
- `probe_part_b_1903a20f.py`: the forged-JWT revoke call is wrapped the same way.
- `probe_part_b_1903a20f_spaced.py`: as above, with a 1.05 s pause before each seal is minted. HMAC seals minted in the same second with the same arguments are identical, so without the pause later cases hit an earlier case's consumed nonce (noted in `../REPRODUCTION.md`); the spaced copy reproduces the intended order.
`probe_2a_p_runtime.py` was run unmodified and aborts at adapter construction with a RuntimeError naming the posture; that is the behaviour under test, so it has no output file.

Run as in `../REPRODUCTION.md`: `PYTHONPATH=<repo>:<repo>/tests CAGE_ENV=test`, local `redis-server` on 6379 and `--port 6391`. `jdiff.py OLD.json NEW.json` lists differing leaves between a recorded output in `../followup_2026-10-05/` and the file here; keys that look like timings, nonces, ids or hashes are listed as volatile and not counted. `out_*.json` are the raw outputs of this re-run (`out_2c_r1_inforce.json` is the script's stdout).
Same-source caveat as for the rest of the companion: scripts, predictions and this comparison were written by the model that drafted the paper.
