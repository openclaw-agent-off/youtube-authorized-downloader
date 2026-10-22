# YouTube Authorized Downloader

A small, local command-line wrapper around `yt-dlp` for archiving **one YouTube video at a time**.

## Important use limits

Use this only for media you own or have clear permission to archive. Your permission may address copyright, but YouTube's Terms of Service and applicable law can impose separate conditions. This project is not affiliated with or approved by YouTube. The MIT license applies to this code only; it grants no rights to any downloaded media.

The tool intentionally:

- accepts only HTTPS individual YouTube watch links or `youtu.be` video links;
- rejects playlists, channels, credentials and deceptive hostnames;
- requires `--authorized` before it starts;
- does not accept cookies or arbitrary `yt-dlp` options;
- ignores local `yt-dlp` configuration and disables plugins;
- downloads to a local folder only.

## Prerequisites

- Python 3.10+
- `yt-dlp` on `PATH`
- `ffmpeg` on `PATH`

## Install

```bash
python3 -m pip install .
```

## Use

Validate a URL without downloading:

```bash
youtube-authorized-download --authorized --dry-run 'https://www.youtube.com/watch?v=VIDEO_ID'
```

Archive one authorized video locally:

```bash
youtube-authorized-download --authorized --output-dir ./downloads 'https://www.youtube.com/watch?v=VIDEO_ID'
```

Extract authorized audio as MP3:

```bash
youtube-authorized-download --authorized --audio-only 'https://youtu.be/VIDEO_ID'
```

Files are named by YouTube video ID. Existing files are not overwritten.

## Tests

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT. See [LICENSE](LICENSE).
