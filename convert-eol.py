#!/usr/bin/env python3
"""
Smart line ending converter
Detects LF, CRLF, or mixed line endings, shows statistics,
and converts interactively or via command-line flags.

Usage:
  python eol_converter.py [--help] <file-path>
  python eol_converter.py [--to-lf | --to-crlf] <file-path>

Examples:
  python eol_converter.py script.sh
  python eol_converter.py --to-lf windows_file.txt
  python eol_converter.py --to-crlf unix_file.txt
"""

import sys
import argparse
from pathlib import Path
import tempfile
import shutil

def detect_line_endings(file_path):
    """Detect line ending type and return stats."""
    lf_count = 0
    crlf_count = 0
    total_lines = 0

    with open(file_path, "rb") as f:
        for line in f:
            total_lines += 1
            if line.endswith(b"\r\n"):
                crlf_count += 1
            elif line.endswith(b"\n"):
                lf_count += 1

    if crlf_count > 0 and lf_count > 0:
        mode = "MIXED"
    elif crlf_count > 0:
        mode = "CRLF"
    else:
        mode = "LF"

    return mode, lf_count, crlf_count, total_lines


def convert_file(file_path, to="lf"):
    """Convert a file’s line endings safely in a streaming fashion."""
    tmp_fd, tmp_path = tempfile.mkstemp()
    with open(file_path, "rb") as src, open(tmp_path, "wb") as dst:
        for line in src:
            # Normalize first to LF
            line = line.replace(b"\r\n", b"\n")
            if to == "crlf":
                line = line.replace(b"\n", b"\r\n")
            dst.write(line)
    shutil.move(tmp_path, file_path)


def main():
    parser = argparse.ArgumentParser(
        description="Smart line ending detector and converter.",
        add_help=False
    )
    parser.add_argument("file", nargs="?", help="Path to the file to process")
    parser.add_argument("--to-lf", action="store_true", help="Convert to LF endings (non-interactive)")
    parser.add_argument("--to-crlf", action="store_true", help="Convert to CRLF endings (non-interactive)")
    parser.add_argument("--help", action="help", help="Show this help message and exit")

    args = parser.parse_args()

    if not args.file:
        parser.print_help()
        sys.exit(1)

    file_path = Path(args.file)
    if not file_path.is_file():
        print(f"Error: File '{file_path}' not found!", file=sys.stderr)
        sys.exit(1)

    mode, lf_count, crlf_count, total_lines = detect_line_endings(file_path)

    print(f"\nDetected line endings for '{file_path}': {mode}")
    print(f"  Total lines: {total_lines}")
    print(f"  LF-only lines: {lf_count}")
    print(f"  CRLF lines: {crlf_count}\n")

    # Handle non-interactive mode
    if args.to_lf:
        convert_file(file_path, to="lf")
        print(f"✅ Converted '{file_path}' to LF successfully.")
        return
    if args.to_crlf:
        convert_file(file_path, to="crlf")
        print(f"✅ Converted '{file_path}' to CRLF successfully.")
        return

    # Interactive mode
    if mode == "CRLF":
        answer = input("Convert CRLF → LF? [y/N]: ").strip().lower()
        if answer == "y":
            convert_file(file_path, to="lf")
            print(f"✅ Converted '{file_path}' to LF successfully.")
        else:
            print("Conversion skipped.")
    elif mode == "LF":
        answer = input("Convert LF → CRLF? [y/N]: ").strip().lower()
        if answer == "y":
            convert_file(file_path, to="crlf")
            print(f"✅ Converted '{file_path}' to CRLF successfully.")
        else:
            print("Conversion skipped.")
    else:  # MIXED
        print("⚠️ File has mixed line endings.")
        answer = input("Normalize to LF? [y/N]: ").strip().lower()
        if answer == "y":
            convert_file(file_path, to="lf")
            print(f"✅ Normalized '{file_path}' to LF successfully.")
        else:
            print("Conversion skipped.")


if __name__ == "__main__":
    main()
