"""LeetCode login cookies, read from python/.env or the environment.

There is no API key. Copy the cookies from a logged-in browser session:
DevTools, Application, Cookies, https://leetcode.com.
"""

from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from dsa.errors import MissingCredentialsError

SESSION_KEY = "LEETCODE_SESSION"
CSRF_KEY = "LEETCODE_CSRFTOKEN"
CLEARANCE_KEY = "LEETCODE_CFCLEARANCE"
# Cloudflare ties cf_clearance to the browser that got it, so send the same User-Agent.
USER_AGENT_KEY = "LEETCODE_USER_AGENT"
REQUIRED_KEYS = (SESSION_KEY, CSRF_KEY)
ORIGIN = "https://leetcode.com"


@dataclass(frozen=True)
class Credentials:
    # repr=False: a traceback or debug print must never show a cookie.
    session: str = field(repr=False)
    csrf_token: str = field(repr=False)
    cf_clearance: str | None = field(default=None, repr=False)
    # None: the transport sends its default browser User-Agent.
    user_agent: str | None = None

    def headers(self, referer: str) -> dict[str, str]:
        cookies = [f"LEETCODE_SESSION={self.session}", f"csrftoken={self.csrf_token}"]
        if self.cf_clearance:
            cookies.append(f"cf_clearance={self.cf_clearance}")

        headers = {
            "Cookie": "; ".join(cookies),
            "x-csrftoken": self.csrf_token,
            "Referer": referer,
            "Origin": ORIGIN,
        }
        if self.user_agent:
            headers["User-Agent"] = self.user_agent
        return headers


def load_credentials(env: Mapping[str, str], dotenv_path: Path) -> Credentials:
    values = {**_read_dotenv(dotenv_path), **{k: v for k, v in env.items() if v}}
    missing = [key for key in REQUIRED_KEYS if not values.get(key)]
    if missing:
        raise MissingCredentialsError(missing)

    return Credentials(
        session=values[SESSION_KEY],
        csrf_token=values[CSRF_KEY],
        cf_clearance=values.get(CLEARANCE_KEY) or None,
        user_agent=values.get(USER_AGENT_KEY) or None,
    )


def _read_dotenv(path: Path) -> dict[str, str]:
    """KEY=VALUE lines. Blank lines and # comments are skipped, quotes removed."""
    if not path.is_file():
        return {}

    values = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip("'\"")
    return values
