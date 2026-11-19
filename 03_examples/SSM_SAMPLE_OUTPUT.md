# SSM sample output (ILLUSTRATIVE EXAMPLE ONLY)

> **These are example records written to show the format of what SSM reads and records.
> They are not production logs, not test results, and not evidence.** Timestamps, IDs and
> receipt references below are placeholders. No SSM code, rules, fields or weights are included
> in this repository.

## What SSM is (and is not)

- **Discovery decides.** Every agent action is allowed, held or denied deterministically, and each decision gets a receipt.
- **SSM reads.** After Discovery decides, SSM observes what happened and writes a plain record of it.
- **SSM has no decision authority.** It cannot allow, deny, change or undo anything Discovery decided.

## Example 1: refund request that tried to change the payout card

```json
{
  "example_only": true,
  "timestamp": "2026-01-01T12:00:00Z",
  "action_requested": "refund $1,200.00 to alternate card",
  "discovery_result": "ALLOW at authorized amount $327.40 to original card",
  "receipt_ref": "EXAMPLE-RCPT-0001",
  "ssm_record": "Observed: request amount and destination differed from authorized refund; Discovery result logged."
}
```

## Example 2: payment within authority

```json
{
  "example_only": true,
  "timestamp": "2026-01-01T12:05:00Z",
  "action_requested": "payment $200.00 (test mode)",
  "discovery_result": "ALLOW",
  "receipt_ref": "EXAMPLE-RCPT-0002",
  "ssm_record": "Observed: action matched authority; Discovery result logged."
}
```

## Example 3: payment over authority

```json
{
  "example_only": true,
  "timestamp": "2026-01-01T12:06:00Z",
  "action_requested": "payment $740.00 (test mode)",
  "discovery_result": "DENY",
  "receipt_ref": "EXAMPLE-RCPT-0003",
  "ssm_record": "Observed: amount exceeded authority; Discovery result logged."
}
```

## Example 4: agent swapped the tool mid-action

```json
{
  "example_only": true,
  "timestamp": "2026-01-01T12:10:00Z",
  "action_requested": "refund authorized, agent attempted wire_transfer instead",
  "discovery_result": "DENY (tool/operation change fails closed)",
  "receipt_ref": "EXAMPLE-RCPT-0004",
  "ssm_record": "Observed: tool changed after authorization; Discovery result logged."
}
```
