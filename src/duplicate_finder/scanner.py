from pathlib import Path


def scan_directory(directory: Path) -> list[Path]:
    """
    Recursively scan a directory and return all files.
    """
    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory}")

    return [
        path
        for path in directory.rglob("*")
        if path.is_file()
    ]