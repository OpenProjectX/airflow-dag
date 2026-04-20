from __future__ import annotations

import os
from typing import Any

from kubernetes import client, config
from kubernetes.client.exceptions import ApiException

from airflow_dag_project.spark import load_spark_application

SPARK_APPLICATION_GROUP = "spark.apache.org"
SPARK_APPLICATION_VERSION = "v1"
SPARK_APPLICATION_PLURAL = "sparkapplications"


def load_kubernetes_config() -> None:
    if os.getenv("K8S_IN_CLUSTER", "false").lower() == "true":
        config.load_incluster_config()
        return
    config.load_kube_config(config_file=os.getenv("KUBECONFIG") or None)


def apply_spark_application(filename: str) -> dict[str, Any]:
    load_kubernetes_config()

    manifest = load_spark_application(filename)
    metadata = manifest["metadata"]
    namespace = metadata["namespace"]
    name = metadata["name"]

    api = client.CustomObjectsApi()
    try:
        return api.create_namespaced_custom_object(
            group=SPARK_APPLICATION_GROUP,
            version=SPARK_APPLICATION_VERSION,
            namespace=namespace,
            plural=SPARK_APPLICATION_PLURAL,
            body=manifest,
        )
    except ApiException as exc:
        if exc.status != 409:
            raise
        return api.replace_namespaced_custom_object(
            group=SPARK_APPLICATION_GROUP,
            version=SPARK_APPLICATION_VERSION,
            namespace=namespace,
            plural=SPARK_APPLICATION_PLURAL,
            name=name,
            body=manifest,
        )
