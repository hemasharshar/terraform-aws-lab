"""Run `terraform validate` in every folder that contains .tf files.

Called by pre-commit (see .pre-commit-config.yaml). Plain Python, so it works
the same on Windows, macOS and Linux (and later in CI).
"""
import subprocess
import sys
from pathlib import Path

SKIP = {".terraform", ".git"}


def terraform_dirs(root: Path) -> list[Path]:
    dirs = set()
    for tf_file in root.rglob("*.tf"):
        if SKIP.intersection(tf_file.parts):
            continue
        dirs.add(tf_file.parent)
    return sorted(dirs)


def run(cmd: list[str], folder: Path) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=folder, capture_output=True, text=True)


def main() -> int:
    failed = False
    for folder in terraform_dirs(Path(".")):
        # validate needs the providers downloaded. Only init folders that were
        # never initialized: an existing .terraform/ may point to the S3 backend,
        # and touching it would need AWS credentials.
        if not (folder / ".terraform").is_dir():
            init = run(["terraform", "init", "-backend=false", "-input=false", "-no-color"], folder)
            if init.returncode != 0:
                print(f"[init failed] {folder}\n{init.stderr}")
                failed = True
                continue

        result = run(["terraform", "validate", "-no-color"], folder)
        if result.returncode != 0:
            print(f"[invalid] {folder}\n{result.stderr}{result.stdout}")
            failed = True
        else:
            print(f"[ok] {folder}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
