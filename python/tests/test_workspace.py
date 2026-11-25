from pathlib import Path

import pytest

from dsa.domain import Difficulty
from dsa.errors import ProblemNotPicked
from dsa.workspace import Workspace

META = (
    '{"id": 217, "question_id": "217", "slug": "contains-duplicate", '
    '"title": "Contains Duplicate", "difficulty": "Easy", "topics": [], '
    '"signature": {"name": "f", "params": []}}'
)


def test_next_number_continues_after_highest(tmp_path: Path):
    easy = tmp_path / "easy"
    (easy / "__1_217_contains_duplicate").mkdir(parents=True)
    (easy / "__7_1_two_sum").mkdir()
    (easy / "notes").mkdir()

    assert Workspace(tmp_path).next_number(Difficulty.EASY) == 8


def test_next_number_in_empty_folder(tmp_path: Path):
    assert Workspace(tmp_path).next_number(Difficulty.HARD) == 1


def test_find_looks_in_every_difficulty(tmp_path: Path):
    folder = tmp_path / "medium" / "__3_155_min_stack"
    folder.mkdir(parents=True)

    workspace = Workspace(tmp_path)

    assert workspace.find(155) == folder
    # 55 is a suffix of 155, it must not match.
    assert workspace.find(55) is None


def test_create_writes_every_file(tmp_path: Path):
    folder = Workspace(tmp_path).create(
        "__1_217_contains_duplicate",
        Difficulty.EASY,
        {"meta.json": META, "cases.txt": "[1]\n"},
    )

    assert folder == tmp_path / "easy" / "__1_217_contains_duplicate"
    assert (folder / "cases.txt").read_text() == "[1]\n"
    assert not any(path.name.startswith(".") for path in folder.parent.iterdir())


def test_create_refuses_to_overwrite(tmp_path: Path):
    workspace = Workspace(tmp_path)
    workspace.create("__1_217_x", Difficulty.EASY, {"a": "1"})

    with pytest.raises(FileExistsError):
        workspace.create("__1_217_x", Difficulty.EASY, {"a": "2"})

    assert (tmp_path / "easy" / "__1_217_x" / "a").read_text() == "1"


def test_load_reads_meta(tmp_path: Path):
    folder = Workspace(tmp_path).create(
        "__1_217_x", Difficulty.EASY, {"meta.json": META}
    )

    local = Workspace(tmp_path).load(217)

    assert local.folder == folder
    assert local.slug == "contains-duplicate"


def test_load_unpicked(tmp_path: Path):
    with pytest.raises(ProblemNotPicked, match="dsa pick 9"):
        Workspace(tmp_path).load(9)
