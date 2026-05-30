---
name: x-downloader
description: Download media (images/videos/GIFs/audio) from Twitter/X using gallery-dl. Supports single tweet URLs, user timelines, date filtering, post count limiting, retweet filtering, video quality selection, and various media types. Use when users want to download media from Twitter/X accounts with proxy support (HTTP/SOCKS4/SOCKS5) and cookie authentication. Supports downloading tweet text with links alongside media.
---

# X/Twitter Media Downloader

## Overview

This skill provides a comprehensive workflow for downloading media from Twitter/X using `gallery-dl`. It supports:

- **Single tweet download**: Download media from a specific tweet URL
- **User timeline download**: Download all media from a user's timeline
- **Media types**: Images, videos, GIFs, and audio files
- **Video quality**: Choose from best, high, medium, low, or worst quality
- **Date filtering**: Download posts within a specific date range
- **Post limiting**: Download latest N posts or all posts
- **Retweet control**: Include or exclude retweets
- **Tweet text download**: Save tweet text with links alongside media
- **Proxy support**: HTTP, HTTPS, SOCKS4, SOCKS5 proxies with authentication
- **Cookie authentication**: Netscape format cookies for authenticated access

## Quick Start

### Prerequisites

1. **Install gallery-dl**: `pip install gallery-dl`
2. **Install dependencies**: `pip install pysocks` (for SOCKS proxy support)
3. **Export cookies**: Use browser extension to export Twitter cookies in Netscape format

### Basic Usage

```bash
# Download all media from a user
python scripts/x_download.py <username> --cookies cookies.txt

# Download single tweet
python scripts/x_download.py --url https://twitter.com/user/status/123456789 --cookies cookies.txt

# Download latest 50 posts
python scripts/x_download.py <username> --cookies cookies.txt --limit 50

# Download with date range
python scripts/x_download.py <username> --cookies cookies.txt --start-date 2026-01-01

# Download with HTTP proxy
python scripts/x_download.py <username> --cookies cookies.txt --proxy http://127.0.0.1:8080

# Download only videos with high quality
python scripts/x_download.py <username> --cookies cookies.txt --type video --quality high

# Download GIFs and audio
python scripts/x_download.py <username> --cookies cookies.txt --type gif,audio

# Download only videos, exclude retweets
python scripts/x_download.py <username> --cookies cookies.txt --type video --no-retweets

# Download media with tweet text
python scripts/x_download.py <username> --cookies cookies.txt --with-tweets
```

## Workflow Decision Tree

### Step 1: Prepare Authentication

1. **Export cookies** from browser (Chrome/Firefox) using Cookie-Editor extension
2. **Save as Netscape format** (cookies.txt) - see [references/cookies_format.md](references/cookies_format.md)
3. **Verify cookies** contain `auth_token` and `ct0` values

### Step 2: Configure Environment

1. **Check proxy requirements** - Twitter may require proxy in some regions
2. **Set up proxy** if needed - see [references/proxy_config.md](references/proxy_config.md)
3. **Verify gallery-dl installation** and dependencies

### Step 3: Execute Download

1. **Choose download mode**: Single tweet or user timeline
2. **Set content filters**: Media type, quality, retweets, tweet text
3. **Run download script** with appropriate parameters
4. **Monitor progress** and handle any errors

### Step 4: Verify Results

1. **Check downloaded files** for completeness
2. **Verify file integrity** (JPEG/MP4/GIF headers)
3. **Clean up temporary files** (.part files)

## Script Usage

### Command Line Options

```
python scripts/x_download.py <username|--url URL> [options]

Required (choose one):
  username              Twitter/X username (without @)
  --url URL             Single tweet URL to download

Options:
  --cookies FILE        Path to cookies file (Netscape format)
  --proxy URL           Proxy URL (http/https/socks4/socks5)
  --start-date DATE     Start date in YYYY-MM-DD format
  --end-date DATE       End date in YYYY-MM-DD format
  --limit N             Limit number of posts to download (integer or "all")
  --output DIR          Output directory (default: ./downloads)
  --type TYPE           Filter by file type: image, video, gif, audio, or comma-separated (default: all)
  --quality QUALITY     Video quality: best, high, medium, low, worst (default: best)
  --no-retweets         Exclude retweets from download
  --no-images           Download only videos/gif/audio (exclude images)
  --with-tweets         Download tweet text with links alongside media
  --sleep SECONDS       Sleep time between requests (default: 1.0)
  --dry-run             Print command without executing
```

### Media Types

| Type | Extensions | Description |
|------|------------|-------------|
| `image` | jpg, jpeg, png, webp | Static images |
| `video` | mp4, mov, avi, webm | Video files |
| `gif` | gif | Animated GIFs |
| `audio` | mp3, m4a, ogg, wav, aac | Audio files |
| `all` | All above | All media types |

### Video Quality

| Quality | Resolution | Description |
|---------|------------|-------------|
| `best` | Original | Highest available quality |
| `high` | 1080p | Full HD |
| `medium` | 720p | HD |
| `low` | 480p | Standard definition |
| `worst` | 360p | Lowest quality |

### Examples

```bash
# Download single tweet with all media
python scripts/x_download.py \
  --url https://twitter.com/DyDy_art/status/123456789 \
  --cookies cookies.txt

# Download all original posts (no retweets) from @DyDy_art
python scripts/x_download.py DyDy_art \
  --cookies cookies.txt \
  --no-retweets \
  --output ./twitter_media

# Download latest 100 posts with tweet text
python scripts/x_download.py artist_account \
  --cookies cookies.txt \
  --limit 100 \
  --with-tweets

# Download only images since February 2026 with SOCKS5 proxy
python scripts/x_download.py photographer \
  --cookies cookies.txt \
  --proxy socks5://127.0.0.1:7897 \
  --start-date 2026-02-01 \
  --type image

# Download videos within date range, exclude retweets
python scripts/x_download.py videographer \
  --cookies cookies.txt \
  --start-date 2026-01-01 \
  --end-date 2026-03-31 \
  --type video \
  --no-retweets

# Download GIFs and audio only
python scripts/x_download.py media_creator \
  --cookies cookies.txt \
  --type gif,audio

# Download high quality videos
python scripts/x_download.py filmmaker \
  --cookies cookies.txt \
  --type video \
  --quality high
```

## Proxy Configuration

The script supports multiple proxy formats:

```bash
# HTTP proxy
--proxy http://127.0.0.1:8080

# HTTPS proxy
--proxy https://proxy.example.com:443

# SOCKS4 proxy
--proxy socks4://127.0.0.1:1080

# SOCKS5 proxy
--proxy socks5://127.0.0.1:7897

# Proxy with authentication
--proxy http://user:password@proxy:8080
--proxy socks5://user:password@proxy:1080

# Short format (defaults to HTTP)
--proxy 127.0.0.1:8080
```

See [references/proxy_config.md](references/proxy_config.md) for detailed proxy configuration.

## Gallery-dl Direct Usage

For advanced use cases, use gallery-dl directly:

```bash
# Download single tweet
gallery-dl --cookies cookies.txt "https://twitter.com/username/status/123456789"

# Download all media from user
gallery-dl --cookies cookies.txt "https://twitter.com/username/media"

# Download latest 50 posts
gallery-dl --cookies cookies.txt --range 1-50 "https://twitter.com/username/media"

# With date filter
gallery-dl --cookies cookies.txt \
  --filter "date >= datetime(2026, 2, 1) or abort()" \
  "https://twitter.com/username/media"

# Exclude retweets
gallery-dl --cookies cookies.txt \
  --option "twitter.retweets=false" \
  "https://twitter.com/username/media"

# Download tweet text
gallery-dl --cookies cookies.txt \
  --option "twitter.text-tweets=true" \
  "https://twitter.com/username/media"

# Set video quality
gallery-dl --cookies cookies.txt \
  --option "twitter.size=1080" \
  "https://twitter.com/username/media"
```

## Troubleshooting

### Common Issues

1. **"AuthRequired" error**: Cookies are invalid or expired
   - Solution: Re-export cookies from browser

2. **"Missing dependencies for SOCKS support"**: PySocks not installed
   - Solution: `pip install pysocks`

3. **"NotFoundError"**: Username doesn't exist or is private
   - Solution: Verify username and account status

4. **"Invalid URL"**: Tweet URL format not recognized
   - Solution: Use full URL format: `https://twitter.com/user/status/123456789`

5. **Download stops prematurely**: Rate limiting or network issues
   - Solution: Increase `--sleep` value (e.g., `--sleep 2.0`)

6. **Incomplete downloads**: .part files remaining
   - Solution: Delete .part files and re-run download

7. **No retweets downloaded**: Retweets may not appear in media timeline
   - Solution: This is expected behavior; media timeline shows original posts

8. **Low quality video downloaded**: Quality option not working
   - Solution: Check if original video has higher quality available

### Debug Mode

Use `--dry-run` to preview the command without executing:

```bash
python scripts/x_download.py username --cookies cookies.txt --dry-run
python scripts/x_download.py --url https://twitter.com/user/status/123 --cookies cookies.txt --dry-run
```

## References

- [cookies_format.md](references/cookies_format.md): Cookie file format and export instructions
- [proxy_config.md](references/proxy_config.md): Proxy configuration examples
- [gallery-dl_docs.md](references/gallery-dl_docs.md): Gallery-dl advanced options