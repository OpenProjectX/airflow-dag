from __future__ import annotations

from pathlib import Path

import yaml

from airflow_dag_project.settings import DEFAULT_SPARK_K8S_NAMESPACE, SPARK_APPLICATIONS_DIR


def spark_application_path(filename: str) -> Path:
    return SPARK_APPLICATIONS_DIR / filename


def load_spark_application(filename: str) -> dict:
    with spark_application_path(filename).open("r", encoding="utf-8") as handle:
        manifest = yaml.safe_load(handle)

    manifest.setdefault("metadata", {})
    manifest["metadata"].setdefault("namespace", DEFAULT_SPARK_K8S_NAMESPACE)
    return manifest


def spark_application_identity(filename: str) -> tuple[str, str]:
    manifest = load_spark_application(filename)
    metadata = manifest["metadata"]
    return metadata["namespace"], metadata["name"]
