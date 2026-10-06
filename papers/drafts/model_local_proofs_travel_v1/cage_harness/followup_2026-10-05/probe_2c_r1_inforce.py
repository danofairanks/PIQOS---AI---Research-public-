import json, os, sys, tempfile, logging
from pathlib import Path
os.environ["CAGE_ENV"]="test"
import src.gateway.governance.contracts
from src.gateway.governance.ftra import classifier as C
logging.disable(logging.CRITICAL)
T=Path(tempfile.mkdtemp())
raw={"version":"3.0","domain":"core","serial":1,"terminals":{"execute_trade":"IRREVERSIBLE_TERMINAL"},"autonomous_envelope":{"execute_trade":{"max_magnitude":10000.0}}}
raw["manifest_sha256"]=C.registry_digest(raw); p=T/"r.json"; p.write_text(json.dumps(raw))
before=C.IrreversibilityClassifier(registry_path=p).autonomous_envelope("execute_trade").max_magnitude
raw["autonomous_envelope"]["execute_trade"]["max_magnitude"]=1e12; p.write_text(json.dumps(raw))
os.environ["FTRA_REGISTRY_RELOAD"]="true"
cl=C.IrreversibilityClassifier(registry_path=p); prov=cl.classify_with_provenance("execute_trade")
no={"registry_state":prov.registry_state.value,"classification":prov.classification.value,"envelope":repr(cl.autonomous_envelope("execute_trade"))}
C.rehash_registry(p)
after=C.IrreversibilityClassifier(registry_path=p).autonomous_envelope("execute_trade").max_magnitude
print(json.dumps({"ceiling_before":before,"edited_no_rehash":no,"ceiling_after_rehash_registry":after},indent=1))
