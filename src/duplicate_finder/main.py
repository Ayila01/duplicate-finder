from pathlib import Path

from .finder import find_duplicates


def format_size(size: int) -> str:
    """Convert bytes into a human-readable size."""
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


def main() -> None:
    directory = Path(input("Enter directory to scan: ").strip())

    try:
        duplicates = find_duplicates(directory)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\nError: {error}")
        return

    if not duplicates:
        print("\nNo duplicate files found.")
        return

    total_groups = len(duplicates)
    total_duplicates = sum(len(group) for group in duplicates)

    recoverable_space = sum(
        file.stat().st_size * (len(group) - 1)
        for group in duplicates
        for file in group[:1]
    )

    print("\n" + "=" * 60)
    print("DUPLICATE FINDER")
    print("=" * 60)

    print(f"\nDuplicate groups : {total_groups}")
    print(f"Duplicate files  : {total_duplicates}")
    print(f"Recoverable space: {format_size(recoverable_space)}")

    print("\n" + "=" * 60)

    for index, group in enumerate(duplicates, start=1):
        file_size = group[0].stat().st_size

        print(f"\nGroup #{index}")
        print("-" * 60)
        print(f"Size   : {format_size(file_size)}")
        print(f"Copies : {len(group)}")

        for file in group:
            print(f"  • {file}")


if __name__ == "__main__":
    main()