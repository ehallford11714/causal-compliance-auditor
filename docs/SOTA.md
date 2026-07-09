# SOTA brief — Causal Compliance Auditor (P16)

## Sensitivity analysis

Point estimates alone are not credible causal claims. Sensitivity tools quantify how strong unobserved confounding (or exclusion violations) must be to overturn conclusions:

- Rosenbaum bounds / Γ
- Cinelli–Hazlett partial R² / robustness values
- E-values (VanderWeele & Ding)
- IV-specific sensitivity to exclusion / measurement error

This auditor **requires** a sensitivity block in the claim JSON for a passing grade.

## Reporting standards for causal claims

Good practice (journals, CONSORT-ish causal checklists, industry model risk) converges on:

1. Clear **estimand** (ATE / ATT / LATE / …)
2. Named **treatment** and **outcome**
3. Explicit **assumptions** (unconfoundedness, exclusion, SUTVA, overlap)
4. **Identification strategy** (backdoor, IV, DiD, RDD, …)
5. **Instruments** when IV is claimed
6. **Limitations** and external validity notes

## Model cards for causal systems

Predictive model cards (Mitchell et al.) omit identification. A **causal model card** should add: DAG / assumptions, estimand, identification proof sketch, diagnostics (F, overlap), sensitivity, and prohibited claims. This MVP’s certificate is a lightweight causal card; richer templates are later work.

## This MVP

Deterministic checklist over JSON claims; artifacts under `runs/`; no network required.

## References (starting points)

- Cinelli & Hazlett; Rosenbaum; VanderWeele & Ding (e-values)
- Pearl / Hernán & Robins on reporting estimands and assumptions
- Mitchell et al., Model Cards; Gebru et al., Datasheets for Datasets
- Journal causal reporting guidelines and AEA data/code policies
