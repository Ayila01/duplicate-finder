from pathlib import Path

from send2trash import send2trash


def remove_file(file_path: Path) -> None:
    """
    Move a file to the system trash.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise ValueError(f"Not a file: {file_path}")

    send2trash(str(file_path))


def remove_duplicates(
    group: list[Path],
    keep: Path,
) -> list[Path]:
    """
    Move all duplicate files except the selected file to the system trash.
    """

    if keep not in group:
        raise ValueError("The file to keep is not part of the duplicate group.")

    removed = []

    for file in group:
        if file == keep:
            continue

        remove_file(file)
        removed.append(file)

    return removed