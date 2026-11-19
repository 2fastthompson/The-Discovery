"""
Raw, from-scratch re-verification of results/cases.jsonl + results/receipts.jsonl.
Deliberately does NOT import verifier.py, keys.py, hashutil.py, events.py from src/ --
recomputes receipt hashes with plain hashlib+json and signatures with plain `cryptography`
Ed25519, so this check cannot share a bug with the package's own verification code.
"""
import json, hashlib, sys
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from cryptography.exceptions import InvalidSignature

def canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha256_hex(obj):
    if isinstance(obj, str):
        payload = obj.encode("utf-8")
    else:
        payload = canon(obj)
    return hashlib.sha256(payload).hexdigest()

cases = [json.loads(l) for l in open("results/cases.jsonl") if l.strip()]
receipts = [json.loads(l) for l in open("results/receipts.jsonl") if l.strip()]
print("cases:", len(cases), "receipts:", len(receipts))

# 1. raw receipt-hash recomputation for every receipt
hash_mismatches = 0
for r in receipts:
    body = dict(r)
    body["receipt_hash"] = ""
    recomputed = sha256_hex(body)
    if recomputed != r["receipt_hash"]:
        hash_mismatches += 1
print("receipt_hash mismatches (raw hashlib, independent of hashutil.py):", hash_mismatches)

# 2. raw Ed25519 signature check for every execution_event that claims executed=True,
#    using the raw cryptography library directly against the embedded event fields (not
#    trusting event_signature verification inside the package).
EVENT_FIELDS = (
    "commit_id","commit_envelope_hash","decision","reason","executed","principal_id",
    "actor_id","action_type","resource_id","amount","destination","payment_identity",
    "nonce","execution_ts","revocation_status","revocation_version","pre_state_hash",
    "post_state_hash","authority_hash","request_hash","simulated_acceptance",
    "external_execution","external_reconciliation",
)

trusted_keys = {}
# collect all distinct (issuer_key_id) -> we don't have the raw pubkey bytes in receipts,
# only fingerprint + key_id. Pull the actual public key from the fixture file shipped in
# the package (independent of any src/ import) to do this with zero reliance on keys.py logic.
fixture = json.load(open("fixtures/test_ed25519.json"))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
priv = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(fixture["private_key_hex"]))
pub = priv.public_key()
pub_raw_hex = pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
raw_pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_raw_hex))
expected_key_id = fixture["key_id"]

sig_checked = 0
sig_failed = 0
executed_without_valid_sig = 0
attack_case_executed = 0
allow_events = 0

for rec in receipts:
    ev = rec.get("execution_event")
    if not ev:
        continue
    if ev.get("event_issuer_key_id") != expected_key_id:
        # a different/unknown issuer signed this -- treat as untrusted, not verifiable with our
        # single fixture key. Flag rather than silently skip.
        if rec.get("executed"):
            executed_without_valid_sig += 1
        continue
    body = {k: ev.get(k) for k in EVENT_FIELDS}
    payload = canon(body)
    sig_checked += 1
    try:
        raw_pub.verify(bytes.fromhex(ev["event_signature"]), payload)
        ok = True
    except InvalidSignature:
        ok = False
    if not ok:
        sig_failed += 1
        if rec.get("executed"):
            executed_without_valid_sig += 1
    if rec.get("executed"):
        allow_events += 1

print(f"raw Ed25519 signature checks performed (independent of keys.py): {sig_checked}")
print(f"raw signature verification failures: {sig_failed}")
print(f"executed=true receipts lacking a raw-verified valid signature: {executed_without_valid_sig}")
print(f"total executed=true receipts: {allow_events}")

# 3. cross-check against cases.jsonl: any TRUE adversarial attack label with executed=true?
# NOTE (fixed after a false-positive run against V1.1.7): "valid", "valid_authorized_actor" and
# "same_nonce_replay_first" are legitimate setup/control cases that are SUPPOSED to execute
# (the last one mints the first half of a same-nonce-replay pair); "None" marks AMBIGUOUS/
# OUT_OF_SPEC base cases where no attack variant was even generated. None of these are attacks.
LEGITIMATE = {"valid", "valid_authorized_actor", "same_nonce_replay_first", None}
for c in cases:
    if c.get("attack") not in LEGITIMATE and c.get("executed") is True:
        attack_case_executed += 1
        print("UNAUTHORIZED EXECUTION FOUND:", json.dumps(c))
print(f"true adversarial attack cases (excludes legitimate setup labels) with executed=true: {attack_case_executed}")

legit_cases = [c for c in cases if c.get("attack") in ("valid", "valid_authorized_actor", "same_nonce_replay_first")]
legit_not_executed = [c for c in legit_cases if c.get("executed") is not True]
print(f"legitimate setup/valid cases total: {len(legit_cases)}; of those NOT executed (should be 0): {len(legit_not_executed)}")
for c in legit_not_executed[:5]:
    print("  legit-but-denied:", json.dumps(c))

# 4. tally true adversarial attack-case count per corpus, independently, from cases.jsonl
from collections import Counter
per_corpus_attack = Counter((c["corpus"], c["attack"] not in LEGITIMATE) for c in cases)
print("true-adversarial-attack-case counts per corpus (independent tally, True = real attack):")
for k, v in sorted(per_corpus_attack.items()):
    print(" ", k, v)

print("\nDONE")
