from __future__ import annotations

from unittest.mock import MagicMock, patch

from kubernetes.client.exceptions import ApiException

from airflow_dag_project.k8s import apply_spark_application


@patch("airflow_dag_project.k8s.load_kubernetes_config")
@patch("airflow_dag_project.k8s.client.CustomObjectsApi")
def test_apply_spark_application_creates_custom_object(
    custom_objects_api: MagicMock,
    _: MagicMock,
) -> None:
    api = custom_objects_api.return_value
    api.create_namespaced_custom_object.return_value = {"status": {"state": "SUBMITTED"}}

    result = apply_spark_application("jdbc-table-ingestion.yaml")

    assert result["status"]["state"] == "SUBMITTED"
    api.create_namespaced_custom_object.assert_called_once()


@patch("airflow_dag_project.k8s.load_kubernetes_config")
@patch("airflow_dag_project.k8s.client.CustomObjectsApi")
def test_apply_spark_application_replaces_existing_custom_object(
    custom_objects_api: MagicMock,
    _: MagicMock,
) -> None:
    api = custom_objects_api.return_value
    api.create_namespaced_custom_object.side_effect = ApiException(status=409)
    api.replace_namespaced_custom_object.return_value = {"status": {"state": "UPDATED"}}

    result = apply_spark_application("jdbc-table-ingestion.yaml")

    assert result["status"]["state"] == "UPDATED"
    api.replace_namespaced_custom_object.assert_called_once()
