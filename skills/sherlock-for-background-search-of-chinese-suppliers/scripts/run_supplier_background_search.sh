#!/usr/bin/env bash
set -euo pipefail

TARGET=""
OUTPUT_DIR="./outputs"
SHERLOCK_CMD="${SHERLOCK_CMD:-sherlock}"
MAX_PAGES="20"
TIMEOUT="10"
KEYWORDS=""

usage() {
  cat <<USAGE
Usage:
  bash scripts/run_supplier_background_search.sh --target <handle> [options]

Options:
  --target <value>         Required. Username or handle to search.
  --output-dir <dir>       Output folder (default: ./outputs).
  --sherlock-cmd <cmd>     Sherlock executable path (default: sherlock).
  --max-pages <n>          Max pages for buyer-intel expansion (default: 20).
  --timeout <sec>          Request timeout seconds (default: 10).
  --keywords <csv>         Optional keyword CSV for intent inference.
  -h, --help               Show help.
USAGE
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target)
      TARGET="${2:-}"
      shift 2
      ;;
    --output-dir)
      OUTPUT_DIR="${2:-}"
      shift 2
      ;;
    --sherlock-cmd)
      SHERLOCK_CMD="${2:-}"
      shift 2
      ;;
    --max-pages)
      MAX_PAGES="${2:-}"
      shift 2
      ;;
    --timeout)
      TIMEOUT="${2:-}"
      shift 2
      ;;
    --keywords)
      KEYWORDS="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$TARGET" ]]; then
  echo "--target is required" >&2
  usage
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

if ! "$SHERLOCK_CMD" --help 2>/dev/null | rg -q -- '--buyer-intel'; then
  echo "ERROR: Sherlock command does not support --buyer-intel. Use the enhanced Sherlock build." >&2
  exit 1
fi

DIRECT_OUT="$OUTPUT_DIR/${TARGET}.direct_only.buyer_intel.json"
EXPANDED_OUT="$OUTPUT_DIR/${TARGET}.expanded.buyer_intel.json"
SUMMARY_OUT="$OUTPUT_DIR/${TARGET}.summary.md"

common_args=(
  "$TARGET"
  --local
  --timeout "$TIMEOUT"
  --buyer-intel
  --buyer-intel-only-verified-contact
  --buyer-intel-max-pages "$MAX_PAGES"
  --folderoutput "$OUTPUT_DIR"
)

if [[ -n "$KEYWORDS" ]]; then
  common_args+=(--buyer-intel-keywords "$KEYWORDS")
fi

echo "[1/3] Running direct-only pass..."
"$SHERLOCK_CMD" "${common_args[@]}" --buyer-intel-output "$DIRECT_OUT"

echo "[2/3] Running expanded pass (company domains + B2B sources)..."
"$SHERLOCK_CMD" "${common_args[@]}" \
  --buyer-intel-company-domains \
  --buyer-intel-b2b-sources \
  --buyer-intel-output "$EXPANDED_OUT"

echo "[3/3] Building comparison summary..."
python3 "$(dirname "$0")/summarize_supplier_report.py" \
  --direct "$DIRECT_OUT" \
  --expanded "$EXPANDED_OUT" \
  --target "$TARGET" \
  > "$SUMMARY_OUT"

echo "Done."
echo "- Direct report:   $DIRECT_OUT"
echo "- Expanded report: $EXPANDED_OUT"
echo "- Summary:         $SUMMARY_OUT"
