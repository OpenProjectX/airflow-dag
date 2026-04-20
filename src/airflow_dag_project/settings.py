from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_REPO_ROOT = Path(os.getenv("AIRFLOW_REPO_ROOT", PROJECT_ROOT))
SPARK_APPLICATIONS_DIR = RUNTIME_REPO_ROOT / "include" / "spark-applications"
DEFAULT_SPARK_K8S_NAMESPACE = os.getenv("SPARK_K8S_NAMESPACE", "analytics")
