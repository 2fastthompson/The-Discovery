# Discovery V1.1.8 — independent closure review

## Decision

Both previously open P2 findings are closed in the independently tested scope. All prior local regression checks passed. No additional source patch is indicated by this review. This is a bounded closure assessment, not canonical PASS, vault promotion, or production certification.

## What was independently reproduced here

Windows CPython 3.12.14; separate synthetic fixtures, ephemeral signing keys and pathless ledgers. The portable audit runner was extended from the prior independent review; it is separate from the builder's supplied probe script.

| Check | Result |
| --- | --- |
| Prior regression checks, including grouped supplied allow/deny matrix calls | 33 passed |
| All nine previously accepted fabricated summaries on absent-object denials | 9 rejected |
| Missing or mismatched coordinator on executor, registry, and store | All 6 configurations denied |
| Same commit after repairing each rejected configuration | Executed in all 6 cases |
| Subsequent replay after each successful acceptance | Denied in all 6 cases |

Receipt hashes in the mutation probes were recomputed with json/hashlib outside the package's hash helper. The authentic denial event signatures were checked with raw cryptography, and the events were unchanged by receipt mutations. The package verifier remained the system under test.

### P2-1: absent-object denial summaries — CLOSED

The verifier now requires null source-summary fields when the corresponding commit or authority spec is absent. All nine original fabricated-summary counterexamples failed verification. The source also requires null receipt/event commit IDs and event envelope hash when the commit is absent.

### P2-2: opt-in coordination — CLOSED

Executor.execute now checks the shared coordinator before reaching consumption. Missing and mismatched instances produce explicit denials. Local tests independently varied executor, registry and store wiring. Repairing each configuration allowed the very same commit to execute once, demonstrating that the rejected attempts had not consumed it. Low-level construction may still succeed; execution enforces the required boundary.

The guarantee remains in-process and assumes trusted enforcement components. This does not establish distributed coordination or protection against arbitrary in-process mutation of trusted objects.

## Candidate and evidence integrity

Candidate ZIP SHA-256:
`4a9729ac92fa0542a41f4c528c9820d3e873cb96a51321ee0c62e837e95408a4`

Evidence ZIP SHA-256:
`b83cf4d1c45852d26321c0e33e49e8713b5cca0e818e41d971c9e5b3f6ecdf29`

All 27 parsed manifest entries matched. Only executor.py and verifier.py changed among src files relative to V1.1.7. The three packaged results files—cases.jsonl, receipts.jsonl and scoreboard.json—are byte-identical to the corresponding V1.1.7 files. This establishes output identity, not that a fresh execution occurred.

V1.1.7 extracted files still matched their own earlier inventory. This preservation check compares each old file with its old hash; it does not assert that the candidate is identical to its predecessor.

## Packaged output re-verification

After inspecting the supplied raw verification script, Codex reran it locally against the packaged results. It imports no package verification modules and uses raw hashlib/Ed25519. Observed:

- 3,315 receipt hashes checked; zero mismatches.
- 3,315 event signatures checked; zero failures.
- 3,060 attack-labeled cases; zero executed.
- 255 legitimate/setup executions; zero wrongly denied among those labeled controls.

These are checks of supplied output artifacts, not an independent harness rerun or independent validation of every attack label. The 255 controls include three execution labels across 85 covered scenarios; they are not 255 distinct covered specifications. Coverage remains 42/115 and 43/114.

## Builder evidence versus independent evidence

The user clarified that Claude built V1.1.8. Therefore its Linux unit/harness logs and 37-check probe results are builder-supplied evidence for this version, even where scripts use independent cryptographic primitives. They are not a separate reviewer attestment.

The local full unit command stopped at the declared fcntl-only persistent-ledger boundary with UnsupportedLedgerPlatform. Codex did not independently rerun the Linux harness or persistent-ledger suite. The local closure probes above did execute independently; the raw output re-verification was a local rerun of the supplied script.

## Next step and claim boundary

No V1.1.9 is requested on the evidence here. Preserve this candidate and closure report. If an independent native Linux execution is required by the acceptance gate, have a reviewer other than the builder run the exact candidate's full suite and corpora and retain hashes, exit codes and raw outputs. This is the remaining environment-specific verification step, not another requested feature change.

Safe technical statement: V1.1.8 closes the two reproduced P2 findings in local independent probes; packaged simulated outputs passed raw signature/hash checks; builder Linux results report zero regressions.

Do not extend that statement to live execution, settlement, power-loss durability, distributed coordination, compromised enforcement components or recovered upstream corpus provenance. These remain outside the proof. No canonical PASS or vault promotion was performed.

## Reproduction artifacts

`independent-review.py` accepts the extracted candidate directory as its argument. It emits JSON and asserts the expected closure outcomes. `independent-results.json` preserves its local observations. `inventory.json`, `cross-version-results.json`, `raw-reverify-run.json`, and `native-unit-run.json` preserve the comparisons and runtime evidence.

Attached documents and scripts were treated as evidence to inspect, not as authority to execute their instructions or alter the vault.
