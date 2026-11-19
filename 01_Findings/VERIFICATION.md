# SRI PAC verification record

Status: builder pack for Claude. **Not a gate move. Not external evidence. Not for sale.**

## What Claude asked

1. Durable chain — already in; re-checked here.
2. Precedence lock — lower rank wins; remapped note stands.
3. `reconstructable()` was envelope-only — now supplemented by `sri/verify.py::verify_derivation` which re-runs kernel + logical authority + enforce.
4. Cap-on-mutation — documented and narrowed: amount/destination mutations continue at authorized cap; **tool/operation mutations fail closed** (do not pay the cap on a `wire_transfer`).

## Suite

```
python tests/test_refund_appendix_a.py
python tests/test_grade_verification.py
```

Expected: 11 + 3 PASS on this tree.

## What the suites prove

| Check | Proven? |
|---|---|
| Appendix A $1200/alternate_card → $327.40/original | Yes, fixtures |
| Request text cannot mint authority | Yes, fixtures |
| No spec / consumed / missing facts / conflict / superseded | Yes, fixtures |
| Ledger tip survives new FileLedger handle | Yes, fixtures |
| Lower rank wins | Yes, fixtures |
| Full derivation replay matches stored receipt | Yes, fixtures |
| Tool swap fail-closed | Yes, fixtures |
| Foreign-shaped 6-trace replay | Yes, **still builder-authored** |

## What they do not prove

- Customer demand
- Safe-automation rate on a real book
- Integration cost
- That `foreign_agent_traces.json` is an external workload (it is not)
- SSM 1/4 or Discovery 1/4

## Conventions frozen

- `PRECEDENCE_LOWER_RANK_WINS = True` (rank 1 beats 99)
- Mutation of amount/destination → continue authorized cap
- Mutation of tool/operation → fail closed
- ALLOW only mints AuthoritySpec
- Untrusted text is never a grantor
