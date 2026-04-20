#!/usr/bin/env bash
set -euo pipefail

RELEASE_NAME="${SPARK_OPERATOR_RELEASE_NAME:-spark}"
RELEASE_NAMESPACE="${SPARK_OPERATOR_NAMESPACE:-spark-operator}"
CHART_VERSION="${SPARK_OPERATOR_CHART_VERSION:-1.6.0}"

if ! command -v helm >/dev/null 2>&1; then
  echo "helm is required but not installed" >&2
  exit 1
fi

if ! command -v kubectl >/dev/null 2>&1; then
  echo "kubectl is required but not installed" >&2
  exit 1
fi

helm repo add spark https://apache.github.io/spark-kubernetes-operator
helm repo update
kubectl create namespace "${RELEASE_NAMESPACE}" --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install "${RELEASE_NAME}" spark/spark-kubernetes-operator \
  --namespace "${RELEASE_NAMESPACE}" \
  --version "${CHART_VERSION}"
kubectl get crd sparkapplications.spark.apache.org
