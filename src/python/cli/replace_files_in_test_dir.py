import argparse
import shutil
from pathlib import Path


def replace_files(source_dir: str, target_dir: str, only_in_target: bool = True) -> None:
    """Copy files from source_dir into target_dir.

    Args:
        only_in_target: When True, only copy files that already exist in target_dir.
    """
    source = Path(source_dir)
    target = Path(target_dir)
    target_names = {p.name for p in target.iterdir()} if only_in_target else None

    for src_file in source.iterdir():
        if only_in_target and src_file.name not in target_names:
            print(f"Skipping {src_file.name}: not in {target}")
            continue
        print(f"Copying {src_file.name} → {target}")
        shutil.copy(src_file, target / src_file.name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source_dir", required=True, help="Directory with new files.")
    parser.add_argument("--target_dir", required=True, help="Directory to update.")
    parser.add_argument(
        "--only_in_target",
        action="store_true",
        default=True,
        help="Only replace files already present in target_dir (default: true).",
    )
    args = parser.parse_args()
    replace_files(args.source_dir, args.target_dir, only_in_target=args.only_in_target)


if __name__ == "__main__":
    main()
