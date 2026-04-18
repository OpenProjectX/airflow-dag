from __future__ import annotations

import logging
import os

LOG_LEVEL = os.getenv("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO").upper()

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
