from __future__ import annotations

import os
from pathlib import Path

TEST_AIRFLOW_HOME = Path(__file__).resolve().parents[1] / ".tmp" / "airflow"
PROJECT_ROOT = Path(__file__).resolve().parents[1]
TEST_AIRFLOW_HOME.mkdir(parents=True, exist_ok=True)

os.environ.setdefault("AIRFLOW_HOME", str(TEST_AIRFLOW_HOME))
os.environ.setdefault("AIRFLOW__CORE__LOAD_EXAMPLES", "False")
os.environ.setdefault("AIRFLOW__CORE__DAGS_FOLDER", str(PROJECT_ROOT / "dags"))
os.environ.setdefault("AIRFLOW__CORE__PLUGINS_FOLDER", str(PROJECT_ROOT / "plugins"))
