"""Clone the 'Quentin' voice with a local VoiceStudio backend and speak a test phrase."""
import json, sys, time, requests

B = "http://127.0.0.1:3900"
TEXT = sys.argv[1]
REF = "voice/quentin_ref_8s.wav"
OUT = "out/quentin_test.wav"
J = {"Content-Type": "application/json"}

def post(path, **kw):
    r = requests.post(B + path, timeout=kw.pop("timeout", 120), **kw)
    print(path, r.status_code, r.text[:300], flush=True)
    return r

# 1. model installs: TTS model + Whisper (to transcribe the reference clip)
for repo in ("k2-fsa/OmniVoice", "Systran/faster-whisper-large-v3"):
    post("/models/install", headers=J, data=json.dumps({"repo_id": repo}))
    time.sleep(5)
    for _ in range(240):
        s = requests.get(B + "/models/install/status", timeout=30).json()
        print("install:", json.dumps(s)[:300], flush=True)
        if not any(j.get("state") in ("downloading", "queued", "installing", "verifying") for j in s.get("jobs", [])):
            break
        time.sleep(15)

# 2. clone profile
with open(REF, "rb") as f:
    p = post("/profiles", data={"name": "Quentin", "kind": "clone"}, files={"ref_audio": f}).json()
post(f"/profiles/{p['id']}/attestation", headers=J, data=json.dumps({"basis": "own_voice"}))

# 3. generate (accept the model licence on the 403 prompt: owner-approved, non-commercial use)
def gen():
    with open(REF, "rb") as f:
        return post("/generate", data={"text": TEXT, "language": "Auto"}, files={"ref_audio": f}, timeout=3000)
r = gen()
if r.status_code == 403 and "model_licence_required" in r.text:
    for m in r.json()["detail"]["models"]:
        post("/models/licenses/accept", headers=J, data=json.dumps(
            {"repo_id": m["repo_id"], "fingerprint": m["fingerprint"], "accepted": True}))
    r = gen()
r.raise_for_status()
import os; os.makedirs("out", exist_ok=True)
open(OUT, "wb").write(r.content)
print("saved", OUT, len(r.content))
