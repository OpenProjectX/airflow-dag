#!/usr/bin/env bash
set -euo pipefail

CLUSTER_NAME="${KIND_CLUSTER_NAME:-airflow-dag-local}"
CONFIG_FILE="${KIND_CONFIG_FILE:-config/kind/cluster.yaml}"

if ! command -v kind >/dev/null 2>&1; then
  echo "kind is required but not installed" >&2
  exit 1
fi

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl is required but not installed" >&2
  exit 1
fi

kind create cluster --name "${CLUSTER_NAME}" --config "${CONFIG_FILE}"
kubectl cluster-info --context "kind-${CLUSTER_NAME}"
