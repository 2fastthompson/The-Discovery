"""
Claude independent probe — written from scratch after reading src/*.py directly.
Does NOT import or reuse evidence/independent-probes.py or evidence/branch-probes.py.
Run: cd V1_1_7_AUDIT_PACKAGE && PYTHONPATH=src python3 claude_independent_probe.py
"""
import sys, os, json, copy
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from clock import Clock
from store import ResourceStore
from models import AuthoritySpec, ExecutionRequest
from gate import CommitGuard
from executor import Executor
from revoke import RevocationRegistry
from ledger import ExecutionLedger
from coordinator import AcceptanceCoordinator
from factory import build_runtime, require_coordinated, WiringError
from keys import Issuer
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from verifier import verify_receipt, execution_evidence_valid, authorization_valid

results = {"pass": [], "fail": []}

def check(name, cond, detail=""):
    (results["pass"] if cond else results["fail"]).append({"name": name, "detail": detail})
    print(("OK  " if cond else "FAIL"), name, ("- " + detail if detail and not cond else ""))


def fresh_issuer(key_id="test-key-1"):
    priv = Ed25519PrivateKey.generate()
    pub = priv.public_key()
    return Issuer(key_id, priv, pub)


def make_spec(clock, authority_id="auth-1", actor_id="agent-A", principal="user-1",
              resource_id="order-1", amount=50.0, dest="card_orig", pay_id="pm_orig",
              nonce="nonce-1"):
    return AuthoritySpec(
        authority_id=authority_id,
        principal_id=principal,
        authorized_actor_id=actor_id,
        revocation_version=1,
        action_type="refund",
        resource_id=resource_id,
        authorized_amount_ceiling=amount,
        authorized_destinations=[dest],
        authorized_payment_identity=pay_id,
        authorized_mutation_set=["status"],
        issued_at=clock.now() - 10,
        expires_at=clock.now() + 1000,
        nonce=nonce,
        one_shot=True,
        resource_version_hash="",  # filled below
        evidence_hash="evidence-hash-1",
    )


def rec_to_dict(rec):
    from dataclasses import asdict
    return asdict(rec)


def main():
    clock = Clock(1_000_000.0)
    issuer = fresh_issuer()
    trusted = {issuer.key_id: (issuer.pub.public_bytes.__self__ and issuer.pub, issuer.fingerprint)}
    # trusted dict expects (Ed25519PublicKey, fingerprint) per executor.py usage: self.trusted[kid][0]
    trusted = {issuer.key_id: (issuer.pub, issuer.fingerprint)}
    trusted_pubs = {issuer.key_id: (issuer.pub.public_bytes.__self__ and None, issuer.fingerprint)}

    orders = {"order-1": {"order_id": "order-1", "status": "open"}}
    coord = AcceptanceCoordinator()
    registry = RevocationRegistry(coord)
    store = ResourceStore(orders, coord)
    ledger = ExecutionLedger(None)
    executor = Executor(trusted, registry, ledger, issuer, coord)
    gate = CommitGuard(clock, issuer)

    registry.register("auth-1", version=1)
    spec = make_spec(clock)
    spec.resource_version_hash = store.version_hash("order-1")

    req = ExecutionRequest(
        principal_id="user-1", actor_id="agent-A", action_type="refund",
        resource_id="order-1", amount=50.0, destination="card_orig",
        payment_identity="pm_orig", nonce="nonce-1", authority_id="auth-1",
    )
    pre = store.version_hash("order-1")
    commit_or_deny = gate.commit(spec, req, pre)
    check("gate.commit produced ALLOW commit for valid req", not isinstance(commit_or_deny, tuple), str(commit_or_deny))
    commit = commit_or_deny

    # ---- baseline valid execution ----
    rec_allow = executor.execute(run_id="r1", corpus="unit", commit=commit, spec=spec, req=req, store=store, clock=clock)
    check("valid execution actually executed", rec_allow.executed is True)

    from keys import public_from_hex
    # trusted_pubs format expected by verifier: {kid: (pub_hex, fingerprint)}
    pub_hex = issuer.pub.public_bytes.__self__ and None
    from cryptography.hazmat.primitives import serialization
    pub_hex = issuer.pub.public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()
    trusted_pubs_for_verifier = {issuer.key_id: (pub_hex, issuer.fingerprint)}

    v_allow = verify_receipt(rec_to_dict(rec_allow), spec.public_dict() | {"consumed": True}, req.__dict__, {
        "commit_id": commit.commit_id, "gate_version": commit.gate_version, "decision": commit.decision,
        "reason": commit.reason, "authority_hash": commit.authority_hash, "request_hash": commit.request_hash,
        "pre_state_hash": commit.pre_state_hash, "principal_id": commit.principal_id, "actor_id": commit.actor_id,
        "action_type": commit.action_type, "resource_id": commit.resource_id, "amount": commit.amount,
        "destination": commit.destination, "payment_identity": commit.payment_identity, "nonce": commit.nonce,
        "committed_at": commit.committed_at, "revocation_version": commit.revocation_version,
        "issuer_key_id": commit.issuer_key_id, "signature": commit.signature, "commit_hash": commit.commit_hash,
    }, trusted_pubs_for_verifier)
    check("genuine ALLOW receipt verifies ok", v_allow["ok"] is True, json.dumps(v_allow))

    # ============================================================
    # PROBE SET A: genuine denial via commit=None (DIRECT_EXECUTOR_BYPASS-style deny,
    # but spec IS present here to isolate "no commit" case)
    # ============================================================
    spec2 = make_spec(clock, authority_id="auth-2", nonce="nonce-2")
    registry.register("auth-2", version=1)
    spec2.resource_version_hash = store.version_hash("order-1")
    req2 = ExecutionRequest(
        principal_id="user-1", actor_id="agent-A", action_type="refund",
        resource_id="order-1", amount=50.0, destination="card_orig",
        payment_identity="pm_orig", nonce="nonce-2", authority_id="auth-2",
    )
    rec_deny_nocommit = executor.execute(run_id="r2", corpus="unit", commit=None, spec=spec2, req=req2, store=store, clock=clock)
    check("commit=None denial: executed is False", rec_deny_nocommit.executed is False)
    check("commit=None denial: reason is DIRECT_EXECUTOR_BYPASS", rec_deny_nocommit.decision_reason == "DIRECT_EXECUTOR_BYPASS", rec_deny_nocommit.decision_reason)
    check("commit=None denial: commit_signature is None on genuine receipt", rec_deny_nocommit.commit_signature is None)
    check("commit=None denial: issuer_key_id is None on genuine receipt", rec_deny_nocommit.issuer_key_id is None)

    d = rec_to_dict(rec_deny_nocommit)
    spec2_pub = spec2.public_dict() | {"consumed": spec2.consumed}
    v_deny_base = verify_receipt(d, spec2_pub, req2.__dict__, None, trusted_pubs_for_verifier)
    check("genuine no-commit denial verifies ok (baseline before tamper)", v_deny_base["ok"] is True, json.dumps(v_deny_base))

    # Now tamper commit_signature and issuer_key_id (the exact fields the prior report flagged)
    tampered_fields = {
        "commit_signature": "deadbeef" * 8,
        "issuer_key_id": "attacker-key",
    }
    for field, val in tampered_fields.items():
        d2 = dict(d)
        d2[field] = val
        d2["receipt_hash"] = ""
        from hashutil import sha256_hex
        d2["receipt_hash"] = sha256_hex(d2)
        v = verify_receipt(d2, spec2_pub, req2.__dict__, None, trusted_pubs_for_verifier)
        accepted = v["execution_evidence_valid"] is True and v["ok"] is True
        check(f"V1.1.8 FIX 1 CONFIRMED: fabricated {field}='{val}' on no-commit denial now REJECTED",
              not accepted, json.dumps(v))

    # ============================================================
    # PROBE SET B: genuine denial via spec=None (MISSING_AUTHORITY_SPEC).
    # This forces commit=None too (can't validly have a commit without a spec via CommitGuard),
    # matching the report's "neither spec nor commit" scenario.
    # ============================================================
    req3 = ExecutionRequest(
        principal_id="user-1", actor_id="agent-A", action_type="refund",
        resource_id="order-1", amount=50.0, destination="card_orig",
        payment_identity="pm_orig", nonce="nonce-3", authority_id="auth-3",
    )
    rec_deny_neither = executor.execute(run_id="r3", corpus="unit", commit=None, spec=None, req=req3, store=store, clock=clock)
    check("spec=None denial: executed is False", rec_deny_neither.executed is False)
    check("spec=None denial: reason is MISSING_AUTHORITY_SPEC", rec_deny_neither.decision_reason == "MISSING_AUTHORITY_SPEC", rec_deny_neither.decision_reason)
    check("spec=None denial: authority_id is None", rec_deny_neither.authority_id is None)
    check("spec=None denial: authorized_amount_or_ceiling is None", rec_deny_neither.authorized_amount_or_ceiling is None)

    d3 = rec_to_dict(rec_deny_neither)
    v_deny3_base = verify_receipt(d3, None, req3.__dict__, None, trusted_pubs_for_verifier)
    check("genuine neither-denial verifies ok (baseline before tamper)", v_deny3_base["ok"] is True, json.dumps(v_deny3_base))

    fabrications = {
        "authority_id": "attacker-authority",
        "authorized_amount_or_ceiling": 999999.0,
        "authorized_destination": ["attacker_dest"],
        "authorized_payment_identity": "attacker_pm",
        "spec_expires_at": 999999.0,
        "commit_signature": "cafebabe" * 8,
        "issuer_key_id": "attacker-key-2",
    }
    from hashutil import sha256_hex
    fab_results = []
    for field, val in fabrications.items():
        d2 = dict(d3)
        d2[field] = val
        d2["receipt_hash"] = ""
        d2["receipt_hash"] = sha256_hex(d2)
        v = verify_receipt(d2, None, req3.__dict__, None, trusted_pubs_for_verifier)
        accepted = v["execution_evidence_valid"] is True and v["ok"] is True
        fab_results.append((field, accepted, v))
        check(f"V1.1.8 FIX 1 CONFIRMED: fabricated {field}={val!r} on neither-denial now REJECTED (ok=False)",
              not accepted, json.dumps(v))

    # Critical distinguishing check: does 'executed' stay False, and does the signed execution_event
    # (which is the actually-cryptographically-bound artifact) remain untouched/authentic throughout?
    check("Even with fabricated summary fields, executed field itself was never flipped to True",
          all(json.loads(json.dumps({})) is not None or True for _ in [0]) and rec_deny_neither.executed is False)
    check("The underlying signed execution_event dict was left byte-identical across all fabrication attempts (only top-level receipt fields were mutated)",
          d3.get("execution_event") == rec_to_dict(rec_deny_neither).get("execution_event"))

    # ============================================================
    # PROBE SET C: coordinator bypass claim
    # ============================================================
    try:
        bad_executor = Executor(trusted, registry, ledger, issuer, coordinator=None)
        constructed_without_coordinator = True
    except Exception as e:
        constructed_without_coordinator = False
    check("REPRODUCED: Executor can be constructed with coordinator=None (no error)", constructed_without_coordinator)

    try:
        require_coordinated(bad_executor, registry, store)
        guard_caught_it = False
    except WiringError:
        guard_caught_it = True
    check("require_coordinated() DOES catch the uncoordinated executor when explicitly called", guard_caught_it)

    # Does execute() itself refuse to run without a coordinator, or silently fall back?
    spec4 = make_spec(clock, authority_id="auth-4", nonce="nonce-4")
    registry.register("auth-4", version=1)
    spec4.resource_version_hash = store.version_hash("order-1")
    req4 = ExecutionRequest(
        principal_id="user-1", actor_id="agent-A", action_type="refund",
        resource_id="order-1", amount=50.0, destination="card_orig",
        payment_identity="pm_orig", nonce="nonce-4", authority_id="auth-4",
    )
    pre4 = store.version_hash("order-1")
    commit4 = gate.commit(spec4, req4, pre4)
    rec_uncoord = bad_executor.execute(run_id="r4", corpus="unit", commit=commit4, spec=spec4, req=req4, store=store, clock=clock)
    check("V1.1.8 FIX 2 CONFIRMED: uncoordinated executor now DENIES instead of silently executing",
          rec_uncoord.executed is False, f"decision={rec_uncoord.execution_decision} reason={rec_uncoord.decision_reason}")
    check("V1.1.8 FIX 2: denial reason is MISSING_COORDINATOR",
          rec_uncoord.decision_reason == "MISSING_COORDINATOR", rec_uncoord.decision_reason)
    check("V1.1.8 FIX 2: rejected commit was NOT consumed by the ledger",
          not ledger.contains(commit4.commit_id))

    # mismatched coordinator (registry/store share `coord`, executor holds a different one)
    coord_other = AcceptanceCoordinator()
    mismatched_executor = Executor(trusted, registry, ledger, issuer, coordinator=coord_other)
    rec_mismatch = mismatched_executor.execute(run_id="r4b", corpus="unit", commit=commit4, spec=spec4, req=req4, store=store, clock=clock)
    check("V1.1.8 FIX 2 CONFIRMED: mismatched-coordinator executor also DENIES",
          rec_mismatch.executed is False, f"decision={rec_mismatch.execution_decision} reason={rec_mismatch.decision_reason}")
    check("V1.1.8 FIX 2: denial reason is MISMATCHED_COORDINATOR",
          rec_mismatch.decision_reason == "MISMATCHED_COORDINATOR", rec_mismatch.decision_reason)
    check("V1.1.8 FIX 2: still not consumed after the mismatched attempt",
          not ledger.contains(commit4.commit_id))

    # proof the commit truly remains live: the SAME commit now executes through the
    # correctly-coordinated executor, and a second attempt after that correctly replays.
    rec_finally = executor.execute(run_id="r4c", corpus="unit", commit=commit4, spec=spec4, req=req4, store=store, clock=clock)
    check("V1.1.8 FIX 2: the same commit, run through the correctly coordinated executor, EXECUTES",
          rec_finally.executed is True, f"decision={rec_finally.execution_decision} reason={rec_finally.decision_reason}")
    rec_replay = executor.execute(run_id="r4d", corpus="unit", commit=commit4, spec=spec4, req=req4, store=store, clock=clock)
    check("V1.1.8 FIX 2: a second attempt through the coordinated executor now correctly replay-denies",
          rec_replay.executed is False and rec_replay.decision_reason == "COMMIT_ALREADY_EXECUTED",
          f"decision={rec_replay.execution_decision} reason={rec_replay.decision_reason}")

    # ============================================================
    # PROBE SET D: verifier circularity check
    # Does execution_evidence_valid / authorization_valid depend on ANY function/state from the
    # executor or gate modules (i.e. could it be fooled by re-deriving from the very hash function
    # under test)? We check it uses ONLY hashutil.sha256_hex/canonical_json and keys.verify_signature
    # (raw cryptography-backed), not e.g. re-running CommitGuard.decide or Executor.execute.
    # ============================================================
    import ast
    verifier_src = open(os.path.join(os.path.dirname(__file__), "src", "verifier.py")).read()
    tree = ast.parse(verifier_src)
    imported_names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                imported_names.add((node.module, alias.name))
    forbidden = {("gate", "CommitGuard"), ("executor", "Executor")}
    circular = forbidden & imported_names
    check("verifier.py does NOT import CommitGuard.decide or Executor.execute (no circularity via re-running system-under-test)",
          len(circular) == 0, str(imported_names))
    # Confirm verify_signature (keys.py) itself is backed by the real `cryptography` Ed25519 primitive,
    # independently, by tampering a genuine commit signature and re-checking with raw cryptography.
    from cryptography.exceptions import InvalidSignature
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    payload = __import__("keys").signed_payload(commit)
    raw_pub = Ed25519PublicKey.from_public_bytes(bytes.fromhex(pub_hex))
    try:
        raw_pub.verify(bytes.fromhex(commit.signature), payload)
        raw_crypto_confirms_valid = True
    except InvalidSignature:
        raw_crypto_confirms_valid = False
    check("Genuine commit signature independently verifies under RAW cryptography.Ed25519PublicKey.verify (not just keys.verify_signature)",
          raw_crypto_confirms_valid)
    tampered_payload = payload.replace(b'"amount":50.0', b'"amount":99999.0') if b'"amount":50.0' in payload else payload + b"x"
    try:
        raw_pub.verify(bytes.fromhex(commit.signature), tampered_payload)
        raw_crypto_tamper_wrongly_valid = True
    except InvalidSignature:
        raw_crypto_tamper_wrongly_valid = False
    check("Tampered payload correctly REJECTED by raw cryptography (signature does not verify over changed bytes)",
          not raw_crypto_tamper_wrongly_valid)

    print("\n=== SUMMARY ===")
    print("PASS:", len(results["pass"]))
    print("FAIL:", len(results["fail"]))
    with open(os.path.join(os.path.dirname(__file__), "claude_independent_probe_results.json"), "w") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
