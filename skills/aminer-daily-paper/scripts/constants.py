from __future__ import annotations

import os

DEFAULT_TOP_K = 10

AMINER_AUTHOR_URL_TEMPLATE = "https://www.aminer.cn/profile/{author_id}"
AMINER_PAPER_URL_TEMPLATE = "https://www.aminer.cn/pub/{paper_id}"
# AMiner API gateway: set AMINER_API_BASE_URL to the server that serves
# the /aminer/api/* routes (see SKILL.md).
AMINER_API_BASE_URL = os.environ.get("AMINER_API_BASE_URL", "")
DEFAULT_REC5_URL = f"{AMINER_API_BASE_URL}/api/v3/paper/rec5"
