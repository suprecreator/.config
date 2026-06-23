#!/usr/bin/env python3
import argparse
import hashlib
import tarfile
from pathlib import Path


EXCLUDE_PARTS = {".git", "__pycache__"}
EXCLUDE_SUFFIXES = {".o", ".a", ".so", ".dylib", ".exe"}


def should_include(path: Path) -> bool:
    if any(part in EXCLUDE_PARTS for part in path.parts):
        return False
    if path.suffix in EXCLUDE_SUFFIXES:
        return False
    if path.name.endswith(".tar.gz"):
        return False
    return True


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Export a compiler investigation bundle.")
    parser.add_argument("--case-dir", required=True)
    parser.add_argument("--name", default="")
    args = parser.parse_args()

    case_dir = Path(args.case_dir).resolve()
    export_dir = case_dir / "export"
    export_dir.mkdir(parents=True, exist_ok=True)
    name = args.name or case_dir.name
    bundle = export_dir / f"{name}.tar.gz"
    checksums = export_dir / "checksums.txt"

    files = [p for p in sorted(case_dir.rglob("*")) if p.is_file() and should_include(p.relative_to(case_dir))]
    checksums.write_text("\n".join(f"{sha256(p)}  {p.relative_to(case_dir)}" for p in files) + "\n")
    files.append(checksums)

    with tarfile.open(bundle, "w:gz") as tar:
        for path in files:
            tar.add(path, arcname=str(Path(name) / path.relative_to(case_dir)))

    print(bundle)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

