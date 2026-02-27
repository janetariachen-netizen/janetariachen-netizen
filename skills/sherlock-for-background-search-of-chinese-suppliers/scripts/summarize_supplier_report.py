#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: str) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def get_contacts(report: dict[str, Any]) -> dict[str, list[str]]:
    default = {
        "emails": [],
        "phones": [],
        "whatsapp": [],
        "telegram": [],
        "wechat": [],
        "linkedin": [],
    }
    analysis = report.get("analysis", {})
    contacts = analysis.get("contacts", {})
    for key in default:
        value = contacts.get(key, [])
        default[key] = value if isinstance(value, list) else []
    return default


def set_minus(left: list[str], right: list[str]) -> list[str]:
    right_set = set(right)
    return [x for x in left if x not in right_set]


def fmt_list(values: list[str]) -> str:
    if not values:
        return "- none"
    return "\n".join(f"- {v}" for v in values)


def top_intents(report: dict[str, Any], top_n: int = 5) -> list[str]:
    intents = report.get("analysis", {}).get("product_intent", [])
    lines: list[str] = []
    for row in intents[:top_n]:
        category = row.get("category", "unknown")
        score = row.get("score", 0)
        kws = ", ".join(row.get("matched_keywords", [])[:8])
        lines.append(f"- {category} (score={score}; keywords={kws})")
    return lines


def find_contact_evidence(report: dict[str, Any], contact: str) -> list[str]:
    evidence = report.get("analysis", {}).get("evidence_by_url", {})
    hits: list[str] = []
    for url, payload in evidence.items():
        if not isinstance(payload, dict):
            continue
        for values in payload.values():
            if isinstance(values, list) and contact in values:
                hits.append(url)
                break
    return hits


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare direct and expanded buyer-intel reports.")
    parser.add_argument("--direct", required=True)
    parser.add_argument("--expanded", required=True)
    parser.add_argument("--target", required=True)
    args = parser.parse_args()

    direct = load_json(args.direct)
    expanded = load_json(args.expanded)

    direct_contacts = get_contacts(direct)
    expanded_contacts = get_contacts(expanded)

    direct_emails = direct_contacts["emails"]
    direct_phones = direct_contacts["phones"]
    expanded_emails = set_minus(expanded_contacts["emails"], direct_emails)
    expanded_phones = set_minus(expanded_contacts["phones"], direct_phones)

    direct_risk = direct.get("analysis", {}).get("due_diligence", {})
    expanded_risk = expanded.get("analysis", {}).get("due_diligence", {})
    domains = expanded.get("domain_lookup", {}).get("domains", [])

    print(f"# Supplier Background Search Summary: {args.target}")
    print()
    print("## Decision")
    print(f"- strict baseline risk: {direct_risk.get('risk_level', 'unknown')} (confidence={direct_risk.get('confidence', 'n/a')})")
    print(f"- expanded risk: {expanded_risk.get('risk_level', 'unknown')} (confidence={expanded_risk.get('confidence', 'n/a')})")
    if direct_emails or direct_phones:
        print("- direct contact status: available")
    else:
        print("- direct contact status: not found")
    print()

    print("## Direct Evidence Contacts")
    print("### Emails")
    print(fmt_list(direct_emails))
    print("### Phones")
    print(fmt_list(direct_phones))
    print()

    print("## Expanded Candidate Contacts (Not In Direct Pass)")
    print("### Emails")
    print(fmt_list(expanded_emails))
    print("### Phones")
    print(fmt_list(expanded_phones))
    print()

    print("## Product Intent Signals")
    lines = top_intents(expanded)
    print("\n".join(lines) if lines else "- none")
    print()

    print("## Domain/B2B Expansion")
    if domains:
        print("### Candidate Company Domains")
        print(fmt_list(domains))
    else:
        print("- no candidate company domain inferred")
    print()

    print("## Evidence URLs For Direct Emails")
    if not direct_emails:
        print("- none")
    else:
        for email in direct_emails:
            urls = find_contact_evidence(expanded, email)
            if urls:
                print(f"- {email}")
                for url in urls:
                    print(f"  - {url}")
            else:
                print(f"- {email} (no URL evidence found in expanded report map)")


if __name__ == "__main__":
    main()
