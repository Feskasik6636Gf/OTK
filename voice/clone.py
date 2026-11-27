"""Clone the 'Quentin' voice with a local VoiceStudio backend and speak a test phrase."""
import json, sys, time, requests

B = "http://127.0.0.1:3900"
TEXT = sys.argv[1]
REF = "voice/quentin_ref_25s.wav"
OUT = "out/quentin_test.wav"
J = {"Content-Type": "application/json"}

def post(path, **kw):
    r = requests.post(B + path, timeout=kw.pop("timeout", 120), **kw)
    print(path, r.status_code, r.text[:300], flush=True)
    return r

# 1. model install (reviewed flow: prepare -> acknowledge -> commit -> install)
plan = post("/models/install/prepare", headers=J, data=json.dumps({"repo_id": "k2-fsa/OmniVoice"})).json()
post("/models/install/commit", headers=J, data=json.dumps({
    "plan_id": plan["plan_id"], "plan_digest": plan["plan_digest"],
    "acknowledged_document_ids": [d.get("id") for d in plan.get("documents", [])],
    "acknowledged": True}))
post("/models/install", headers=J, data=json.dumps({"repo_id": "k2-fsa/OmniVoice"}))
for _ in range(240):
    s = requests.get(B + "/models/install/status", timeout=30).json()
    print("install:", json.dumps(s)[:300], flush=True)
    if not s.get("active") and not s.get("installing") and s.get("state") in (None, "idle", "done", "complete", "installed"):
        break
    time.sleep(15)

# 2. clone profile
with open(REF, "rb") as f:
    p = post("/profiles", data={"name": "Quentin", "kind": "clone"}, files={"ref_audio": f}).json()
post(f"/profiles/{p['id']}/attestation", headers=J, data=json.dumps({"basis": "own_voice"}))

# 3. generate
with open(REF, "rb") as f:
    r = post("/generate", data={"text": TEXT, "language": "Auto"}, files={"ref_audio": f}, timeout=3000)
r.raise_for_status()
import os; os.makedirs("out", exist_ok=True)
open(OUT, "wb").write(r.content)
print("saved", OUT, len(r.content))
