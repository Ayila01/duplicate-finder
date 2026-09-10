from collections import defaultdict
from pathlib import Path

from .hasher import calculate_hash
from .scanner import scan_directory


def find_duplicates(directory: Path) -> list[list[Path]]:
    """
    Find groups of duplicate files in a directory.
    """
    files = scan_directory(directory)

    # Group files by size
    files_by_size: dict[int, list[Path]] = defaultdict(list)

    for file in files:
        try:
            size = file.stat().st_size
            files_by_size[size].append(file)
        except OSError:
            continue

    duplicates = []

    # Only hash files that share the same size
    for same_size_files in files_by_size.values():

        if len(same_size_files) < 2:
            continue

        files_by_hash: dict[str, list[Path]] = defaultdict(list)

        for file in same_size_files:
            try:
                file_hash = calculate_hash(file)
                files_by_hash[file_hash].append(file)
            except OSError:
                continue

        for same_hash_files in files_by_hash.values():
            if len(same_hash_files) > 1:
                duplicates.append(same_hash_files)

    return duplicates