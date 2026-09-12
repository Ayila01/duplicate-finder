from pathlib import Path

import pytest

from duplicate_finder import remover


def test_remove_file(tmp_path: Path, monkeypatch):
    file = tmp_path / "test.txt"
    file.write_text("Hello")

    removed_files = []

    def fake_send2trash(path):
        removed_files.append(path)

    monkeypatch.setattr(remover, "send2trash", fake_send2trash)

    remover.remove_file(file)

    assert removed_files == [str(file)]
    assert file.exists()


def test_remove_duplicates(tmp_path: Path, monkeypatch):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file3 = tmp_path / "file3.txt"

    for file in [file1, file2, file3]:
        file.write_text("Duplicate")

    removed_files = []

    def fake_send2trash(path):
        removed_files.append(path)

    monkeypatch.setattr(remover, "send2trash", fake_send2trash)

    removed = remover.remove_duplicates(
        [file1, file2, file3],
        file1,
    )

    assert removed == [file2, file3]
    assert removed_files == [str(file2), str(file3)]


def test_remove_duplicates_rejects_unknown_file(tmp_path: Path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    unknown = tmp_path / "unknown.txt"

    file1.write_text("Duplicate")
    file2.write_text("Duplicate")

    with pytest.raises(ValueError):
        remover.remove_duplicates(
            [file1, file2],
            unknown,
        )