from __future__ import annotations
import argparse, shutil
from pathlib import Path

NO_EXT_DIR = "no_ext"

def uniquify(path: Path) -> Path:
    if not path.exists():
        return path
    stem, suffix = path.stem, path.suffix
    i = 1
    while True:
        p = path.with_name(f"{stem}_{i}{suffix}")
        if not p.exists():
            return p
        i += 1

def copy_tree(src: Path, dst_root: Path, stats: dict[str, int]) -> None:
    try:
        for entry in src.iterdir():
            if entry.is_dir():
                copy_tree(entry, dst_root, stats)
            else:
                ext = entry.suffix.lower().lstrip(".")
                subdir = ext if ext else NO_EXT_DIR
                target_dir = dst_root / subdir
                target_dir.mkdir(parents=True, exist_ok=True)
                target = uniquify(target_dir / entry.name)
                try:
                    shutil.copy2(entry, target)
                    stats[subdir] = stats.get(subdir, 0) + 1
                except PermissionError:
                    print(f"[WARN] access denied: {entry}")
                except OSError as e:
                    print(f"[WARN] copy failed {entry}: {e}")
    except PermissionError:
        print(f"[WARN] access denied: {src}")
    except OSError as e:
        print(f"[WARN] dir error {src}: {e}")

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument("src", type=Path)
    p.add_argument("dest", nargs="?", default="dist", type=Path)
    return p.parse_args()

def dest_inside_src(src: Path, dest: Path) -> bool:
    src_r = src.resolve()
    dest_r = dest.resolve()
    try:
        return dest_r == src_r or dest_r.is_relative_to(src_r)
    except AttributeError:
        try:
            dest_r.relative_to(src_r)
            return True
        except ValueError:
            return False

def main():
    args = parse_args()
    src, dest = args.src, args.dest
    if not src.exists() or not src.is_dir():
        raise SystemExit(f"[ERROR] invalid src: {src}")
    dest.mkdir(parents=True, exist_ok=True)
    if dest_inside_src(src, dest):
        raise SystemExit("[ERROR] dest cannot be inside src")
    stats = {}
    copy_tree(src, dest, stats)
    total = sum(stats.values())
    print("=== SUMMARY ===")
    print(f"files: {total}")
    for k, v in sorted(stats.items()):
        label = f".{k}" if k != NO_EXT_DIR else "(no ext)"
        print(f"{label:<16} -> {v}")
    print(f"dest: {dest}")

if __name__ == "__main__":
    main()
