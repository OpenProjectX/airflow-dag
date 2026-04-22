from __future__ import annotations

from typing import Any

from airflow.providers.cncf.kubernetes.hooks.kubernetes import KubernetesHook
from kubernetes import client
from kubernetes.client.exceptions import ApiException

from airflow_dag_project.spark import load_spark_application

SPARK_APPLICATION_GROUP = "spark.apache.org"
SPARK_APPLICATION_VERSION = "v1"
SPARK_APPLICATION_PLURAL = "sparkapplications"


def apply_spark_application(
    filename: str,
    kubernetes_conn_id: str = "kubernetes_default",
) -> dict[str, Any]:
    manifest = load_spark_application(filename)
    metadata = manifest["metadata"]
    namespace = metadata["namespace"]
    name = metadata["name"]

    hook = KubernetesHook(kubernetes_conn_id=kubernetes_conn_id)
    api = client.CustomObjectsApi(api_client=hook.get_conn())
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
