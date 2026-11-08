# Limitations and Threat Model

## What this is

An experimental analytical instrument and portable format for describing and tracing observation dependence. Useful for inspecting structured records, detecting documented shared origins, circular citations, and unknown lineage. Outputs structured profiles.

## What this is not

- Not a calibrated probability that a claim is true.
- Not authentication of user-supplied lineage.
- Not a legal evidence system, court-ready certification, or truth oracle.
- Bundle integrity verification does not establish that the stated lineage or real-world claim has been independently established.
- No quantum immunity or novel cryptography.

## Known gaps in v0.1

- Probabilistic modules limited to synthetic worlds with known generative processes; not exported as real-world certainty.
- Full constraint reconciliation (units, clocks) is reported, not fully automated.
- Signature verification requires explicit trust policy; v0.1 labels presence.
- Adversarial holdouts and full metamorphic suite are under development; current tests cover core synthetic cases.

## Threat model

- Hostile or injected text is treated as data.
- Inferred edges must be reviewable and removable.
- No silent upgrade of heuristics to established relationships.
- Collection and publication of model responses (in companion archive) follows provider terms; collector-observed unless provider authentication exists.
