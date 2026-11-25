"""Failures the CLI reports to the user as one line, without a traceback."""


class DsaError(Exception):
    pass


class ProblemNotFound(DsaError):
    def __init__(self, ref: int | str) -> None:
        super().__init__(f"problem {ref} not found on LeetCode")


class PaidOnlyProblem(DsaError):
    def __init__(self, slug: str) -> None:
        super().__init__(f"{slug} is a premium problem, its content is not public")


class UnsupportedProblem(DsaError):
    pass


class LeetCodeUnavailable(DsaError):
    def __init__(self, reason: str, status: int | None = None) -> None:
        super().__init__(f"LeetCode unavailable: {reason}")
        self.status = status


class AuthExpired(DsaError):
    def __init__(self) -> None:
        super().__init__(
            "LeetCode refused the request. Copy fresh cookies into python/.env "
            "(LEETCODE_SESSION, LEETCODE_CSRFTOKEN). If Cloudflare blocks it, also set "
            "LEETCODE_CFCLEARANCE and LEETCODE_USER_AGENT from the same browser"
        )


class MissingCredentials(DsaError):
    def __init__(self, keys: list[str]) -> None:
        super().__init__(f"missing in python/.env: {', '.join(keys)}")


class ProblemNotPicked(DsaError):
    def __init__(self, frontend_id: int) -> None:
        super().__init__(
            f"problem {frontend_id} is not picked, run: dsa pick {frontend_id}"
        )


class InvalidCasesFile(DsaError):
    pass


class InvalidSolution(DsaError):
    pass
