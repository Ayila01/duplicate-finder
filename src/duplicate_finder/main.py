import argparse
from pathlib import Path

from .remover import remove_duplicates
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


def display_group(group: list[Path], index: int, total: int) -> None:
    """Display one duplicate group."""

    try:
        file_size = group[0].stat().st_size
    except OSError:
        return

    print("\n" + "=" * 60)
    print(f"GROUP #{index} / {total}")
    print("=" * 60)

    print(f"\nSize   : {format_size(file_size)}")
    print(f"Copies : {len(group)}")

    print()

    for file_index, file in enumerate(group, start=1):
        print(f"  [{file_index}] {file}")


def manage_group(group: list[Path]) -> str:
    """Allow the user to choose which duplicate file to keep."""

    print("\nWhich file do you want to KEEP?")
    print("[1-{}] Select file   [S] Skip   [Q] Quit".format(len(group)))

    choice = input("\nChoice: ").strip().lower()

    if choice == "s":
        print("\nSkipped.")
        return "skip"

    if choice == "q":
        return "quit"

    if not choice.isdigit():
        print("\nInvalid choice.")
        return "stay"

    selected_index = int(choice) - 1

    if selected_index < 0 or selected_index >= len(group):
        print("\nInvalid file number.")
        return "stay"

    keep = group[selected_index]

    files_to_remove = [
        file
        for file in group
        if file != keep
    ]

    print("\nYou selected:")
    print(f"  {keep}")

    print("\nThe following files will be moved to the Trash:")

    for file in files_to_remove:
        print(f"  • {file}")

    confirmation = input("\nConfirm? [y/N]: ").strip().lower()

    if confirmation != "y":
        print("\nNo files were removed.")
        return "stay"

    try:
        removed = remove_duplicates(group, keep)

        print(f"\n✓ {len(removed)} file(s) moved to the Trash.")
        return "done"

    except (FileNotFoundError, ValueError, OSError) as error:
        print(f"\nError: {error}")
        return "stay"
        

def browse_duplicates(duplicates: list[list[Path]]) -> None:
    """Allow the user to browse and manage duplicate groups."""

    current = 0
    total = len(duplicates)

    while True:
        group = duplicates[current]

        display_group(group, current + 1, total)

        print("\n" + "-" * 60)
        print("[N] Next   [P] Previous   [A] Manage   [Q] Quit")

        choice = input("\nChoice: ").strip().lower()

        if choice == "n":
            if current < total - 1:
                current += 1
            else:
                print("\nYou are already at the last group.")

        elif choice == "p":
            if current > 0:
                current -= 1
            else:
                print("\nYou are already at the first group.")

        elif choice == "a":
            result = manage_group(group)

            if result == "quit":
                print("\nExiting...")
                break

            if result in ("done", "skip"):
                if current < total - 1:
                    current += 1
                else:
                    print("\n✓ All duplicate groups have been processed.")
                    break

        elif choice == "q":
            print("\nExiting...")
            break

        else:
            print("\nInvalid choice. Please choose N, P, A or Q.")


def scan_command(directory: Path) -> None:
    """Scan a directory and display duplicate files."""

    print("\n" + "=" * 60)
    print("DUPLICATE FINDER")
    print("=" * 60)

    print(f"\nScanning: {directory}")

    try:
        duplicates = find_duplicates(directory)
    except (FileNotFoundError, NotADirectoryError) as error:
        print(f"\nError: {error}")
        return

    if not duplicates:
        print("\n✓ No duplicate files found.")
        return

    total_groups = len(duplicates)
    total_duplicates = sum(len(group) for group in duplicates)

    recoverable_space = sum(
        group[0].stat().st_size * (len(group) - 1)
        for group in duplicates
    )

    print("\n✓ Scan completed")

    print(f"\nDuplicate groups : {total_groups}")
    print(f"Duplicate files  : {total_duplicates}")
    print(f"Recoverable space: {format_size(recoverable_space)}")

    browse_duplicates(duplicates)


def main() -> None:
    """Entry point for the CLI."""

    parser = argparse.ArgumentParser(
        prog="duplicate-finder",
        description="Find duplicate files on your computer.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a directory for duplicate files.",
    )

    scan_parser.add_argument(
        "directory",
        type=Path,
        help="Directory to scan.",
    )

    args = parser.parse_args()

    if args.command == "scan":
        scan_command(args.directory)


if __name__ == "__main__":
    main()