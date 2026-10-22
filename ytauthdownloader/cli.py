from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

from .core import AuthorizationRequired, build_download_command


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Download one YouTube video only when you are authorized to archive it.")
    parser.add_argument("url", help="Individual HTTPS YouTube watch URL")
    parser.add_argument("--authorized", action="store_true", help="Confirm that you own or are authorized to archive this content")
    parser.add_argument("--audio-only", action="store_true", help="Create an MP3 instead of a video file")
    parser.add_argument("--output-dir", default="downloads", help="Destination directory (default: downloads)")
    parser.add_argument("--dry-run", action="store_true", help="Validate and show the command without downloading")
    args = parser.parse_args(argv)
    try:
        command = build_download_command(args.url, authorized=args.authorized, audio_only=args.audio_only, output_dir=args.output_dir)
    except (AuthorizationRequired, ValueError) as error:
        parser.error(str(error))
    if args.dry_run:
        print("Validated. Download command prepared for:", command[-1])
        return 0
    if not shutil.which("yt-dlp"):
        print("Error: yt-dlp is required and was not found in PATH.", file=sys.stderr)
        return 2
    if not shutil.which("ffmpeg"):
        print("Error: ffmpeg is required and was not found in PATH.", file=sys.stderr)
        return 2
    Path(args.output_dir).expanduser().mkdir(parents=True, exist_ok=True)
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())
