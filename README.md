# The Discovery Exposer Kit
Most AI agent setups fail when untrusted prompt text can mint execution authority, replay receipts, or trigger tool calls nobody approved.

I'm a first-time developer. With AI, I built Discovery (v1.0–v1.1.8) to make that fail closed. Today the full build history and verification outputs are public:

• 3,315/3,315 receipt hashes verified (0 mismatches)
• 3,315/3,315 event signatures verified (0 failures)
• 3,060/3,060 attack-labeled cases blocked (0 executed)
• 255/255 valid controls executed (0 wrongly denied)


## Ran it? Submit your signed results

This kit does not phone home. Nothing is sent back unless you choose to share it.

1. Clone or download this repository and check the files with `sha256sum -c SHA256SUMS.txt` (on Windows, `certutil -hashfile <file> SHA256`). Unzip `02_DISCOVERY_VERSIONS/11_v1.1.8/V1_1_8_AUDIT_PACKAGE.zip`.
2. From the unzipped folder, run the quick check: `python tests/test_attacks.py`. It prints `UNIT_FAILS []` when every attack test passes. For the full replay, follow `REPRO.md` inside the package (`python3 harness/run_replay.py --corpus both`). That writes `results/scoreboard.json`, `results/SCOREBOARD.md`, `results/receipts.jsonl`, and `results/cases.jsonl`. Receipts are Ed25519-signed; the test public key is in `fixtures/test_ed25519.json`. You can also re-check receipts with `01_Findings/V1_1_8_evidence/evidence/claude_raw_reverify_v118.py`.
3. Open a [Submit your run](https://github.com/2fastthompson/The-Discovery/issues/new?template=submit-your-run.yml) issue, paste your `results/scoreboard.json` or quick-check output, and attach `results/receipts.jsonl`.

Submissions are voluntary. Testers who send a signed run can be listed below, or stay anonymous.

### Community results

Results below are self-reported until the attached receipts are verified.

| Date | Credit | Kit / commit | What was run | Summary | Receipts verified |
| --- | --- | --- | --- | --- | --- |

_No community runs listed yet._

## About this kit

This kit is the public release of **Discovery v1.1.8**, together with the build history. The full folder list, with file counts and dates, is in [`INDEX.txt`](INDEX.txt).

Records related to the September 5, 2026 incident are kept separately in [The-Discovery-Evidence](https://github.com/2fastthompson/The-Discovery-Evidence).

**Who I am.** I'm Shawn Phillip Thompson, founder of Sentinel Risk Intelligence LLC. I spent about 30 years
in OEM collision repair. Discovery is the first software I've built, and I built it with AI tools.

**What SRI is.** Sentinel Risk Intelligence LLC (SRI) is a Minnesota LLC formed in January 2026. It builds
control and evidence tools for AI agents.

**What Discovery is.** It's a deterministic layer that checks each AI agent action against the authority the
agent was given, before the action runs. Details are below.

**What's in the kit.**
- `00_Evidence/` holds the Claude build chat transcripts.
- `01_Findings/` has the findings, the verification record and the v1.1.8 evidence.
- `02_DISCOVERY_VERSIONS/` has every Discovery build, v1.0 through v1.1.8.
- `03_examples/` has an illustrative SSM sample output.

**What I'm asking for.**
- I'm asking readers to verify Discovery for themselves, using the steps below.

**Contact.** sri.execute@gmail.com

---

## Discovery v1.1.8

**Discovery** is a deterministic action-control layer for AI agents, built by Sentinel Risk Intelligence LLC.
Before an agent's action runs, Discovery checks it against the authority it was actually given, and allows,
holds or denies it. Every decision produces a verifiable receipt.

Built by a first-time developer, with AI.

## What Discovery does

- **Deterministic decisions.** The same input always gives the same result. No model sits in the decision path.
- **Authority comes only from the spec.** Text in a request can never grant itself authority.
- **Precedence is locked.** When rules conflict, the lower rank wins.
- **Mutations are handled strictly.** If an agent changes the amount or destination, it continues only at the authorized cap. If it changes the tool or operation, Discovery fails closed.
- **Single-use commits.** An approval can't be replayed.
- **Signed receipts.** Each decision gets an Ed25519 signature and a SHA-256 hash chain, so anyone can check that a decision happened and wasn't altered.

## How SSM fits in

SSM is SRI's reading and observation layer. **Discovery decides, SSM reads.** After a decision, SSM records what
happened. It has **no decision authority** and can't allow, deny or change anything. SSM code is not part of
this release. See `03_examples/SSM_SAMPLE_OUTPUT.md` for illustrative example records only.

## Verify this release

Release fingerprints (SHA-256):

- v1.1.8 audit package `02_DISCOVERY_VERSIONS/11_v1.1.8/V1_1_8_AUDIT_PACKAGE.zip`
  `4a9729ac92fa0542a41f4c528c9820d3e873cb96a51321ee0c62e837e95408a4`
- v1.1.8 evidence zip `02_DISCOVERY_VERSIONS/12_v1.1.8_evidence/V1_1_8_evidence.zip`
  `b83cf4d1c45852d26321c0e33e49e8713b5cca0e818e41d971c9e5b3f6ecdf29`

To check every file:

```
sha256sum -c SHA256SUMS.txt
```

On Windows: `certutil -hashfile <file> SHA256`

What the included suites prove and don't prove is listed honestly in `01_Findings/VERIFICATION.md`.

## Where to find the builds and version history

- Every Discovery build, v1.0 through v1.1.8, is in [`02_DISCOVERY_VERSIONS/`](02_DISCOVERY_VERSIONS/), one numbered folder per version.
- The current build is [`02_DISCOVERY_VERSIONS/11_v1.1.8/`](02_DISCOVERY_VERSIONS/11_v1.1.8/), and its evidence is in [`12_v1.1.8_evidence/`](02_DISCOVERY_VERSIONS/12_v1.1.8_evidence/).
- The full version list is in [`VERSION_HISTORY.md`](VERSION_HISTORY.md), and the findings are in [`01_Findings/`](01_Findings/).

## How to use

1. Clone or download this repository.
2. Verify the files: `sha256sum -c SHA256SUMS.txt` (on Windows, `certutil -hashfile <file> SHA256`).
3. Unzip `02_DISCOVERY_VERSIONS/11_v1.1.8/V1_1_8_AUDIT_PACKAGE.zip`.
4. Install Python 3.10 or newer. From the unzipped folder, run the quick check `python tests/test_attacks.py`. It prints `UNIT_FAILS []` when every attack test passes. For the full replay, follow `REPRO.md` inside the package.
5. Compare your results with the evidence outputs in [`01_Findings/V1_1_8_evidence/`](01_Findings/V1_1_8_evidence/).

## Repository map

- `02_DISCOVERY_VERSIONS/` holds the audit packages for every version, v1.0 through v1.1.8
- `01_Findings/` holds the findings, closure review, validation report and verification record
- `01_Findings/V1_1_8_evidence/` holds independent probe and re-verify outputs for v1.1.8
- `03_examples/` holds the SSM sample output (illustrative only)
- `00_Evidence/` holds the Claude build chat transcripts
- `VERSION_HISTORY.md` is the version list

## Not included

Sentinel Gate and SSM implementation code are proprietary and not in this repository.
Patent pending. Copyright 2026 Sentinel Risk Intelligence LLC. All rights reserved.
