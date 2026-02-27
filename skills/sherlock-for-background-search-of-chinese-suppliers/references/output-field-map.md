# Output Field Map

## Top-Level

- `username`: searched handle
- `claimed_profile_count`: number of claimed sites
- `pages_analyzed`: total pages parsed by buyer-intel analysis
- `claimed_profiles`: profile URLs from Sherlock claims
- `collection_summary`: page counts split by strict profile/domain/B2B phases

## Domain Expansion

- `domain_lookup.enabled`: whether domain expansion is enabled
- `domain_lookup.domains`: inferred candidate company domains
- `domain_lookup.probe_urls`: generated URLs for domain evidence probing

## B2B Expansion

- `b2b_sources.enabled`: whether B2B expansion is enabled
- `b2b_sources.probe_urls`: generated B2B search URLs used in expansion

## Analysis

- `analysis.contacts`: final contacts after configured filter (for this workflow, usually verified only)
- `analysis.contacts_all`: raw extracted contacts before verification filter
- `analysis.verified_contacts`: contacts with score >= threshold
- `analysis.contact_confidence`: score/occurrence per extracted contact
- `analysis.product_intent`: ranked product categories with matched keywords
- `analysis.due_diligence`: confidence and risk signal summary
- `analysis.evidence_by_url`: per-URL evidence map for extracted fields

## Reporting Convention

- Use `analysis.contacts` as decision-facing contact output.
- Use `analysis.contacts_all` only for forensic review.
- Use `analysis.evidence_by_url` to cite source URLs in final report.
