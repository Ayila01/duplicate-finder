import hashlib
from pathlib import Path


def calculate_hash(file_path: Path, chunk_size: int = 8192) -> str:
    """
    Calculate the SHA-256 hash of a file.
    """
    sha256 = hashlib.sha256()

    with file_path.open("rb") as file:
        while chunk := file.read(chunk_size):
            sha256.update(chunk)

    return sha256.hexdigest()