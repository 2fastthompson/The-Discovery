# The Discovery Exposer Kit
Most AI agent setups fail when untrusted prompt text can mint execution authority, replay receipts, or trigger tool calls nobody approved.

I'm a first-time developer. With AI, I built Discovery (v1.0–v1.1.8) to make that fail closed. Today the full build history and verification outputs are public:

• 3,315/3,315 receipt hashes verified (0 mismatches)
• 3,315/3,315 event signatures verified (0 failures)
• 3,060/3,060 attack-labeled cases blocked (0 executed)
• 255/255 valid controls executed (0 wrongly denied)


## About this kit

This kit is the public release of **Discovery v1.1.8**, together with the build history and the records of the
September 5, 2026 incident. The full folder list, with file counts and dates, is in [`INDEX.txt`](INDEX.txt).

**Who I am.** I'm Shawn Phillip Thompson, founder of Sentinel Risk Intelligence LLC. I spent about 30 years
in OEM collision repair. Discovery is the first software I've built, and I built it with AI tools.

**What SRI is.** Sentinel Risk Intelligence LLC (SRI) is a Minnesota LLC formed in January 2026. It builds
control and evidence tools for AI agents.

**What Discovery is.** It's a deterministic layer that checks each AI agent action against the authority the
agent was given, before the action runs. Details are below.

**What's in the kit.**
- `00_Evidence/` has the screenshots and photos, chat transcripts, the SEC whistleblower chat and the IC3 complaint.
- `01_Findings/` has the findings, the verification record and the v1.1.8 evidence.
- `02_DISCOVERY_VERSIONS/` has every Discovery build, v1.0 through v1.1.8.
- `03_examples/` has an illustrative SSM sample output.

**The September 5 incident.** On the night of September 5, 2026, from about 11:30 PM Central, I believe my PC
was accessed without my authorization while Discovery work was on it. My account records show a ChatGPT data
export started September 6 at 3:41 AM Central and OpenAI sign-in codes sent at 6:35 AM. I don't recall
requesting either one. These are the steps I took:
- I reported it to OpenAI on Case 14713357. Their September 9 reply said they found no suspicious logins.
- I filed an IC3 complaint on September 10.
- On September 11, I sent OpenAI a notice asking them to preserve their logs.
- On Case 17638799, I asked for a human reviewer and for the IP address, device and session records.

It has not been confirmed which files, if any, were taken or whether any data left the machine. This kit
makes no claim that OpenAI used or trained on this work. OpenAI Cases 14713357 and 17638799 are open, and
they are the place for those questions. The screenshots and chats in `00_Evidence/` are my own records of
what I saw and reported.

**What I'm asking for.**
- I'm asking OpenAI to answer the two open cases, including the session and IP records I asked for.
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
- `00_Evidence/` holds the screenshots, chats, SEC whistleblower chat and IC3 complaint
- `VERSION_HISTORY.md` is the version list

## Not included

Sentinel Gate and SSM implementation code are proprietary and not in this repository.
Patent pending. Copyright 2026 Sentinel Risk Intelligence LLC. All rights reserved.
