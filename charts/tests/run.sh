#!/usr/bin/env bash
set -euo pipefail

CHART_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OVERRIDE_VALUES="$CHART_DIR/tests/override-values.yaml"

DEFAULT_RENDER="$(mktemp)"
OVERRIDE_RENDER="$(mktemp)"
trap 'rm -f "$DEFAULT_RENDER" "$OVERRIDE_RENDER"' EXIT

echo "[helm-test] Rendering default chart values"
helm template default-test "$CHART_DIR" > "$DEFAULT_RENDER"

grep -q "kind: ConfigMap" "$DEFAULT_RENDER"
grep -q "kind: Deployment" "$DEFAULT_RENDER"
grep -q "MIN_EXIT_CODE: \"10\"" "$DEFAULT_RENDER"
grep -q "DRY_RUN: \"false\"" "$DEFAULT_RENDER"
grep -Eq "checksum/config: [a-f0-9]{64}" "$DEFAULT_RENDER"

echo "[helm-test] Rendering override chart values"
helm template override-test "$CHART_DIR" -f "$OVERRIDE_VALUES" > "$OVERRIDE_RENDER"

grep -q "replicas: 3" "$OVERRIDE_RENDER"
grep -q "image: \"ghcr.io/my-repo/trouble-generator:2.0.0\"" "$OVERRIDE_RENDER"
grep -q "MIN_EXIT_CODE: \"1\"" "$OVERRIDE_RENDER"
grep -q "DRY_RUN: \"true\"" "$OVERRIDE_RENDER"

DEFAULT_CHECKSUM="$(grep -Eo 'checksum/config: [a-f0-9]{64}' "$DEFAULT_RENDER" | head -n1 | awk '{print $2}')"
OVERRIDE_CHECKSUM="$(grep -Eo 'checksum/config: [a-f0-9]{64}' "$OVERRIDE_RENDER" | head -n1 | awk '{print $2}')"

if [[ -z "$DEFAULT_CHECKSUM" || -z "$OVERRIDE_CHECKSUM" ]]; then
  echo "[helm-test] checksum/config annotation not found"
  exit 1
fi

if [[ "$DEFAULT_CHECKSUM" == "$OVERRIDE_CHECKSUM" ]]; then
  echo "[helm-test] checksum/config should change when ConfigMap values change"
  exit 1
fi

echo "[helm-test] All Helm chart tests passed"
