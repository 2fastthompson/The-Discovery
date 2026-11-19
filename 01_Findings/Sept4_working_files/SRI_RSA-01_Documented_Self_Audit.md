# SRI Recursive Self-Audit — RSA-01

**Date:** 2026-08-18
**Classification:** SRI-INTERNAL retrospective documented execution
**Frozen protocol hash:** `6049e1583963e65b`

## Method
The audit treated major SRI Discovery/Impact development decisions as the objects being adjudicated. Units were scrambled before reporting. Each unit was evaluated against evidence available when the decision was made, later executed/internal evidence, the strongest obvious baseline, economic relevance, and whether the decision should be KEEP, NARROW, HOLD, or KILL. No failed historical result was rewritten.

## Results
### K — HOLD
**Decision audited:** Use probability estimates directly in option economics
**Evidence then:** Probabilistic option value requires P(success).
**Later evidence:** Execution exposed probability quality itself as the dominant integrity risk; no calibration source has been demonstrated.
**Baseline:** Calibrated forecasting / empirical frequencies
**Economic relevance:** Potentially powerful but currently vulnerable to guessed probabilities.
**Reason:** Do not expand until probability provenance/calibration is tested.

### H — KEEP
**Decision audited:** Distinguish MISSED_VALUE from DO_NOT_ACT
**Evidence then:** v0.2 conflated no worthwhile action with valuable action whose window had already closed.
**Later evidence:** v0.3 and temporal testing preserved lost opportunity separately and supported intervention-window analysis.
**Baseline:** Opportunity-cost accounting
**Economic relevance:** Improves economic attribution and temporal diagnosis.
**Reason:** Executed tests showed the distinction carries information lost by a single DO_NOT_ACT label.

### I — NARROW
**Decision audited:** Introduce PRESERVE_OPTION for low-evidence/rising-exposure states
**Evidence then:** Temporal test showed economic windows can close before evidence reaches final-action sufficiency.
**Later evidence:** Option test routed cheap reversible actions without authorizing final intervention; causality test showed benefit only when preservation changes later feasibility.
**Baseline:** Real-options / staged decision-making
**Economic relevance:** Potentially valuable but not uniquely Discovery and not real-world demonstrated.
**Reason:** Retain only when the reversible action has evidence of changing future feasibility; otherwise it becomes extra cost.

### E — KILL
**Decision audited:** Add Profit/Loss logic inside the frozen Discovery core
**Evidence then:** Commercial value required economic consequences to be measured.
**Later evidence:** Testing showed technical adjudication and economic action can diverge; baseline attribution also matters.
**Baseline:** Standard ROI / expected-value analysis
**Economic relevance:** Economics necessary, but combining it with adjudication would contaminate the core.
**Reason:** Economic logic belongs downstream; frozen Discovery should remain independent.

### J — KILL
**Decision audited:** Use deterministic success/failure for option preservation
**Evidence then:** Initial causality test modeled preserve feasibility as binary.
**Later evidence:** Probabilistic test showed expected value changes materially with success probability and can reject headline-dollar traps.
**Baseline:** Probabilistic expected-value analysis
**Economic relevance:** Binary assumption is unrealistic.
**Reason:** Later executed test directly superseded deterministic preservation as an economic model.

### G — KILL
**Decision audited:** Treat any positive incremental value as sufficient for Discovery-attributable action
**Evidence then:** v0.1 used >0 as the action threshold.
**Later evidence:** PL-09 exposed a +$2K case where estimation error/friction could swamp the apparent gain; v0.2 added margin.
**Baseline:** Margin-of-safety decision thresholds
**Economic relevance:** Overly permissive threshold could manufacture marginal wins.
**Reason:** The executed synthetic test directly exposed this rule as too weak.

### A — KEEP
**Decision audited:** Freeze DH-02.1 rather than modify core after scorer disagreements
**Evidence then:** Independent scorer-transfer work showed strong but imperfect transfer; disagreements exposed calibration boundaries.
**Later evidence:** Subsequent experiments repeatedly used K, A/D, and W/P/C/S without requiring a core rewrite.
**Baseline:** Version control / scientific preregistration discipline
**Economic relevance:** Preserves interpretability and prevents hindsight contamination.
**Reason:** Later work benefited from a stable adjudication core; no executed result required changing it.

### L — KILL
**Decision audited:** Continue adding new economic layers before integrated system test
**Evidence then:** Each synthetic run exposed another boundary and suggested another component.
**Later evidence:** Architecture now has enough components that incremental feature tests risk complexity without proving system-level value.
**Baseline:** Integrated adversarial testing
**Economic relevance:** Marginal feature additions now have declining information value.
**Reason:** The next information gain should come from integration and hostile mixed cases, not another feature.

### F — KEEP
**Decision audited:** Create a separate Profit/Loss Impact Layer
**Evidence then:** Correct Discovery findings can still be uneconomic to act on.
**Later evidence:** v0.1-v0.3 separated Discovery-attributable action, baseline action, negative economics and missed value.
**Baseline:** Expected-value / cost-benefit analysis
**Economic relevance:** Adds commercial gating, not demonstrated commercial advantage.
**Reason:** Necessary for testing value claims, while its own superiority remains unproven.

### C — KILL
**Decision audited:** Pursue runway-incursion severity classification as a Discovery lane
**Evidence then:** Large FAA dataset with severity labels appeared attractive for scale testing.
**Later evidence:** FAA severity methodology already captures proximity, reaction time, evasive action and related variables.
**Baseline:** FAA runway-incursion severity classification
**Economic relevance:** Low incremental value identified.
**Reason:** Strong incumbent baseline makes post-event severity classification a poor incremental-value lane.

### B — NARROW
**Decision audited:** Use famous catastrophes as Discovery application evidence
**Evidence then:** Dali, East Palestine, DCA and 9/11 have rich public retrospective records.
**Later evidence:** Reconstructions exposed useful patterns but could not establish blind discrimination, prevention, or superiority.
**Baseline:** Expert accident investigation and existing safety methods
**Economic relevance:** Useful for boundary discovery, weak for commercial proof.
**Reason:** Retain only as hypothesis/boundary-generation material, not evidence of prevention or market value.

### D — KEEP
**Decision audited:** Shift focus from event prediction to longitudinal decision-transition detection
**Evidence then:** Across unrelated reconstructions, recurring pattern was failure to revise an earlier decision as evidence accumulated.
**Later evidence:** Temporal synthetic tests coherently represented first actionable point, peak feasible value and missed-value transition.
**Baseline:** Existing longitudinal risk monitoring / expert review remains untested head-to-head.
**Economic relevance:** Potentially useful but superiority unproven.
**Reason:** This is the most coherent recurring functional hypothesis, but still requires real baseline comparison.

## Verdict distribution
- KEEP: 4
- NARROW: 2
- HOLD: 1
- KILL: 5

## Audit conclusion
The self-audit does not support continued feature accretion. It supports retaining the frozen Discovery core, retaining a separate Profit/Loss layer, retaining MISSED_VALUE, narrowing option preservation, holding probabilistic economics until probability quality is calibrated, killing runway-incursion severity as an incremental-value lane, and moving next to an integrated adversarial system test.

**Status:** SRI-INTERNAL retrospective evidence only. Not external validation, market validation, accident-prevention evidence, or demonstrated profitability.