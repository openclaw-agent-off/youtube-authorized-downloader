"""Small, restrictive wrapper for authorized, single-video downloads."""

from __future__ import annotations

from pathlib import Path
from urllib.parse import parse_qs, urlparse


class AuthorizationRequired(PermissionError):
    """Raised before any download when the user has not acknowledged rights."""


_ALLOWED_HOSTS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}


def validate_video_url(value: str) -> str:
    parsed = urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in _ALLOWED_HOSTS:
        raise ValueError("Use a valid HTTPS YouTube video URL.")
    if parsed.username or parsed.password or parsed.port or parsed.fragment:
        raise ValueError("The URL must not contain credentials, a port, or a fragment.")

    if parsed.hostname == "youtu.be":
        video_id = parsed.path.strip("/")
    elif parsed.path == "/watch":
        query = parse_qs(parsed.query, keep_blank_values=True)
        if "list" in query:
            raise ValueError("Playlists are not supported.")
        ids = query.get("v", [])
        video_id = ids[0] if len(ids) == 1 else ""
    else:
        raise ValueError("Only individual YouTube watch URLs are supported.")

    if not video_id or not all(char.isalnum() or char in "_-" for char in video_id):
        raise ValueError("The YouTube video ID is invalid.")
    return f"https://www.youtube.com/watch?v={video_id}"


def build_download_command(url: str, *, authorized: bool, audio_only: bool = False, output_dir: str = "downloads") -> list[str]:
    if not authorized:
        raise AuthorizationRequired("Pass --authorized only for content you own or are allowed to archive.")
    video_url = validate_video_url(url)
    destination = Path(output_dir).expanduser().resolve()
    command = [
        "yt-dlp", "--ignore-config", "--no-plugins", "--no-playlist", "--no-overwrites",
        "--restrict-filenames", "--retries", "2", "--output", str(destination / "%(id)s.%(ext)s"),
    ]
    if audio_only:
        command += ["--extract-audio", "--audio-format", "mp3"]
    else:
        command += ["--merge-output-format", "mp4"]
    return [*command, "--", video_url]
