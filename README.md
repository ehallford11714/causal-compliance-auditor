<p align="center">
  <img src="assets/logo.svg" alt="Causal Compliance Auditor" width="96" height="96" />
</p>

# Causal Compliance Auditor

**Audit trail for causal claims — assumptions, instruments, sensitivity — with pass/fail certificates.**

Package: `causalaudit` · Product **P16** in the causal research suite.

## Install

```bash
cd CausalComplianceAuditor
pip install -e ".[dev]"
```

## Quick start

```bash
causalaudit audit examples/good_report.json
causalaudit audit examples/bad_report.json --no-write
```

## Docs

- [docs/SOTA.md](docs/SOTA.md) — state of the art notes for this product

## Suite

Part of the research product suite. Index: [PRODUCTS.md](../PRODUCTS.md) · GitHub: [causal-compliance-auditor](https://github.com/ehallford11714/causal-compliance-auditor)

## License

MIT
