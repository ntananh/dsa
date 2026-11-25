"""Problem folders under python/leetcode/{easy,medium,hard}/."""

import os
import re
import shutil
import tempfile
from collections.abc import Iterator, Mapping
from pathlib import Path

from dsa.domain import Difficulty, LocalProblem
from dsa.errors import ProblemNotPicked
from dsa.files.meta import parse_meta

HOME_ENV = "DSA_HOME"
DEFAULT_ROOT = Path(__file__).resolve().parents[2] / "leetcode"
META_FILE = "meta.json"
# "__{n}_{id}_{name}": n is the order within the difficulty, id is LeetCode's number.
FOLDER_NAME = re.compile(r"^__(\d+)_(\d+)_")


def default_root() -> Path:
    override = os.environ.get(HOME_ENV)
    return Path(override) if override else DEFAULT_ROOT


def folder_name(number: int, frontend_id: int, slug: str) -> str:
    return f"__{number}_{frontend_id}_{slug.replace('-', '_')}"


class Workspace:
    def __init__(self, root: Path) -> None:
        self._root = root

    def find(self, frontend_id: int) -> Path | None:
        for folder, _, problem_id in self._folders():
            if problem_id == frontend_id:
                return folder
        return None

    def next_number(self, difficulty: Difficulty) -> int:
        numbers = [
            n
            for folder, n, _ in self._folders()
            if folder.parent.name == difficulty.folder
        ]
        return max(numbers, default=0) + 1

    def create(
        self, name: str, difficulty: Difficulty, files: Mapping[str, str]
    ) -> Path:
        parent = self._root / difficulty.folder
        target = parent / name
        if target.exists():
            raise FileExistsError(target)

        # Write into a hidden temp folder first, so a failure leaves no half problem.
        parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix=".pick-", dir=parent))
        try:
            for file_name, content in files.items():
                (staging / file_name).write_text(content, encoding="utf-8")
            staging.rename(target)
        except BaseException:
            shutil.rmtree(staging, ignore_errors=True)
            raise
        return target

    def load(self, frontend_id: int) -> LocalProblem:
        folder = self.find(frontend_id)
        if folder is None:
            raise ProblemNotPicked(frontend_id)

        return parse_meta((folder / META_FILE).read_text(encoding="utf-8"), folder)

    def problems(self) -> list[LocalProblem]:
        return [
            parse_meta((folder / META_FILE).read_text(encoding="utf-8"), folder)
            for folder, _, _ in self._folders()
            if (folder / META_FILE).exists()
        ]

    def _folders(self) -> Iterator[tuple[Path, int, int]]:
        for difficulty in Difficulty:
            parent = self._root / difficulty.folder
            if not parent.is_dir():
                continue
            for folder in sorted(parent.iterdir()):
                match = FOLDER_NAME.match(folder.name)
                if folder.is_dir() and match:
                    yield folder, int(match.group(1)), int(match.group(2))
