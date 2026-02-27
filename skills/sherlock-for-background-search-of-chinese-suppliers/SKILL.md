---
name: sherlock-for-background-search-of-chinese-suppliers
description: Background-search suppliers/buyers with Sherlock-based OSINT and structured due diligence signals. Use when the user needs to back-check Chinese suppliers or procurement buyers, infer likely product intent, collect verifiable contact clues, and output a clear risk-oriented report that separates direct evidence from expanded leads.
---

# Sherlock For Background Search Of Chinese Suppliers

Execute supplier/buyer background checks with a two-pass method: strict evidence first, expanded intelligence second.

## Workflow

1. Confirm the target handle/entity and jurisdiction constraints.
2. Run a strict pass with only verified contacts and no domain/B2B expansion.
3. Run an expanded pass with company-domain and B2B source expansion enabled.
4. Compare strict vs expanded outputs and classify contacts as direct evidence or candidate leads.
5. Deliver a concise decision report with risk level, product-intent hints, and evidence links.

Use scripts in this skill folder to keep output consistent.

## Quick Start

From the skill directory, run:

```bash
bash scripts/run_supplier_background_search.sh \
  --target Verodimitri \
  --output-dir ./outputs \
  --sherlock-cmd /Users/apple/Documents/GitHub/sherlock/.venv/bin/sherlock \
  --keywords "procurement,buyer,sourcing,solar,lithium battery,charger"
```

This command produces:
- `outputs/<target>.direct_only.buyer_intel.json`
- `outputs/<target>.expanded.buyer_intel.json`
- `outputs/<target>.summary.md`

## Reporting Rules

Always structure conclusions as:
- `Direct evidence contacts`: only from strict pass.
- `Expanded candidate contacts`: only from expanded pass and not present in strict pass.
- `Risk decision`: use direct pass as baseline and treat expanded findings as leads, not confirmed identity.
- `Intent products`: top categories with matched keywords.

If strict pass has no contacts, state that explicitly even when expanded pass finds candidates.

## Constraints

- Keep collection lawful and platform-compliant.
- Do not claim ownership/identity certainty without corroborating evidence.
- Flag ambiguous or cross-identity collision risks.

## Resources

### scripts/
- `run_supplier_background_search.sh`: run strict and expanded scans in a reproducible sequence.
- `summarize_supplier_report.py`: compare two JSON reports and generate a single markdown decision summary.

### references/
- `due-diligence-checklist.md`: interpretation checklist and analyst decision gates.
- `output-field-map.md`: important output fields and how to explain them.

## Acknowledgement

This skill builds on Sherlock.

Thanks to Sherlock original creator **Siddharth Dushantha** and all Sherlock maintainers/contributors.
