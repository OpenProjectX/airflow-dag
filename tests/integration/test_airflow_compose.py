from __future__ import annotations

import os
import time

import pytest
import requests
from testcontainers.compose import DockerCompose

pytestmark = pytest.mark.integration


@pytest.mark.skipif(
    os.getenv("RUN_DOCKER_TESTS") != "1",
    reason="Set RUN_DOCKER_TESTS=1 to execute Docker-backed integration tests.",
)
def test_airflow_webserver_healthcheck() -> None:
    compose = DockerCompose(context=".", compose_file_name="docker-compose.yml")
    compose.start()
    try:
        deadline = time.time() + 180
        url = "http://localhost:8080/health"
        last_error: Exception | None = None
        while time.time() < deadline:
            try:
                response = requests.get(url, timeout=5)
                if response.ok:
                    payload = response.json()
                    assert payload["metadatabase"]["status"] == "healthy"
                    assert payload["scheduler"]["status"] in {"healthy", "unhealthy"}
                    return
            except Exception as exc:  # pragma: no cover - retries are the point here
                last_error = exc
            time.sleep(5)
        raise AssertionError(f"Airflow webserver did not become healthy: {last_error}")
    finally:
        compose.stop()
