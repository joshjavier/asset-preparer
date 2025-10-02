#!/usr/bin/env python3
import os
import re
import zipfile
import argparse

ILLEGAL_CHARS = r"[/$|\"]"


def scan_large_images(src_dir, size_limit):
    large_files = []
    for root, _, files in os.walk(src_dir):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                path = os.path.join(root, f)
                if os.path.getsize(path) > size_limit:
                    large_files.append(path)
    return large_files


def sanitize_directories(src_dir):
    renamed = []
    for root, dirs, _ in os.walk(src_dir, topdown=False):
        for d in dirs:
            new_name = re.sub(ILLEGAL_CHARS, "", d)
            if new_name != d:
                old_path = os.path.join(root, d)
                new_path = os.path.join(root, new_name)
                if not os.path.exists(new_path):
                    os.rename(old_path, new_path)
                    renamed.append((old_path, new_path))
    return renamed


def create_zip(src_dir, zip_name):
    abs_zip = os.path.abspath(zip_name)
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _, files in os.walk(src_dir):
            for f in files:
                path = os.path.join(root, f)
                # Skip junk and the output zip itself
                if (
                    f == ".DS_Store"
                    or f.startswith("__MACOSX")
                    or os.path.abspath(path) == abs_zip
                ):
                    continue
                arcname = os.path.relpath(path, src_dir)
                zf.write(path, arcname)


def main():
    parser = argparse.ArgumentParser(description="Prepare assets for upload.")
    parser.add_argument(
        "src_dir", nargs="?", default=".", help="Source directory containing assets"
    )
    parser.add_argument(
        "output_file",
        nargs="?",
        default="assets_ready.zip",
        help="Name of the output zip file (default: assets_ready.zip)",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=95,
        help="Maximum allowed image size in KB (default: 95)",
    )
    parser.add_argument(
        "--allow-oversize",
        action="store_true",
        help="Allow images larger than the size limit (default: strict mode)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Only check for oversize images; no renaming or zip creation",
    )
    args = parser.parse_args()

    src_dir = args.src_dir
    zip_name = args.output_file
    size_limit = args.max_size * 1024  # KB -> bytes

    if not os.path.isdir(src_dir):
        print(f"❌ Error: {src_dir} is not a valid directory")
        exit(1)

    # Check for large images
    large = scan_large_images(src_dir, size_limit)
    if large:
        print("⚠️ Found images over {args.max_size}KB:")
        for f in large:
            rel_path = os.path.relpath(f, src_dir)
            print(" -", rel_path)
        if args.check:
            print("ℹ️ Check mode: no directories renamed, no zip created.")
            exit(2)
        elif not args.allow_oversize:
            print(
                "❌ Exiting because oversize images are not allowed. Use --allow-oversize to override."
            )
            exit(1)
    else:
        print(f"✅ All images within {args.max_size}KB.")
        if args.check:
            print("ℹ️ Check mode: no directories renamed, no zip created.")
            exit(0)

    # Rename illegal dirs
    renamed = sanitize_directories(src_dir)
    for old, new in renamed:
        rel_old = os.path.relpath(old, src_dir)
        rel_new = os.path.relpath(new, src_dir)
        print(f"Renamed: {rel_old} -> {rel_new}")

    # Zip
    create_zip(src_dir, zip_name)
    print(f"🎉 Done. Output: {zip_name}")


if __name__ == "__main__":
    main()
