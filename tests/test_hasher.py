from pathlib import Path

from duplicate_finder.hasher import calculate_hash


def test_same_content_has_same_hash(tmp_path: Path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("Hello Duplicate Finder")
    file2.write_text("Hello Duplicate Finder")

    assert calculate_hash(file1) == calculate_hash(file2)


def test_different_content_has_different_hash(tmp_path: Path):
    file1 = tmp_path / "file1.txt"
    file2 = tmp_path / "file2.txt"

    file1.write_text("Hello")
    file2.write_text("Goodbye")

    assert calculate_hash(file1) != calculate_hash(file2)