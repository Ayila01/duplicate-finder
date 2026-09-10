from pathlib import Path

from duplicate_finder.finder import find_duplicates


def test_find_duplicates(tmp_path: Path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"
    file3 = tmp_path / "file3.txt"

    file1.write_text("Duplicate content")
    file2.write_text("Duplicate content")
    file3.write_text("Different content")

    duplicates = find_duplicates(tmp_path)

    assert len(duplicates) == 1
    assert len(duplicates[0]) == 2
    assert set(duplicates[0]) == {file1, file2}


def test_no_duplicates(tmp_path: Path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("World")

    duplicates = find_duplicates(tmp_path)

    assert duplicates == []