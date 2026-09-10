from pathlib import Path

from duplicate_finder.scanner import scan_directory


def test_scan_directory_finds_files(tmp_path: Path):
    (tmp_path / "file1.txt").write_text("Hello")
    (tmp_path / "file2.txt").write_text("World")

    files = scan_directory(tmp_path)

    assert len(files) == 2


def test_scan_directory_finds_files_recursively(tmp_path: Path):
    subdirectory = tmp_path / "subdirectory"
    subdirectory.mkdir()

    (tmp_path / "file.txt").write_text("Hello")
    (subdirectory / "nested.txt").write_text("World")

    files = scan_directory(tmp_path)

    assert len(files) == 2