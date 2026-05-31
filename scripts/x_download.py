#!/usr/bin/env python3
"""
X/Twitter Media Downloader

Download media (images/videos/GIFs/audio) from Twitter/X using gallery-dl.
Supports single tweet URLs, user timelines, date filtering, limit control,
proxy configuration, cookie authentication, and video quality selection.

Usage:
    # Download from user timeline
    python x_download.py <username> [options]
    
    # Download single tweet
    python x_download.py --url <tweet_url> [options]

Examples:
    # Download all media from user
    python x_download.py DyDy_art --cookies cookies.txt
    
    # Download single tweet
    python x_download.py --url https://twitter.com/DyDy_art/status/123456789 --cookies cookies.txt
    
    # Download latest 50 posts
    python x_download.py DyDy_art --cookies cookies.txt --limit 50
    
    # Download with date range
    python x_download.py DyDy_art --cookies cookies.txt --start-date 2026-02-04
    
    # Download with HTTP proxy
    python x_download.py DyDy_art --cookies cookies.txt --proxy http://127.0.0.1:8080
    
    # Download only videos with high quality
    python x_download.py DyDy_art --cookies cookies.txt --type video --quality high
    
    # Download GIFs and audio
    python x_download.py DyDy_art --cookies cookies.txt --type gif,audio
    
    # Download only videos, exclude retweets
    python x_download.py DyDy_art --cookies cookies.txt --type video --no-retweets
    
    # Download media with tweet text
    python x_download.py DyDy_art --cookies cookies.txt --with-tweets
"""

import argparse
import subprocess
import sys
import os
import re
import tempfile
import time
from pathlib import Path
from datetime import datetime


def validate_date(date_string):
    """Validate date string format (YYYY-MM-DD)."""
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_string}. Use YYYY-MM-DD")


def validate_proxy(proxy_string):
    """Validate proxy URL format."""
    # Supported proxy formats
    proxy_patterns = [
        r'^https?://[\w\.\-]+:\d+$',                    # http://proxy:port or https://proxy:port
        r'^https?://[\w\.\-]+:[\w\.\-]+@[\w\.\-]+:\d+$', # http://user:pass@proxy:port
        r'^socks[45]://[\w\.\-]+:\d+$',                  # socks4://proxy:port or socks5://proxy:port
        r'^socks[45]://[\w\.\-]+:[\w\.\-]+@[\w\.\-]+:\d+$', # socks4://user:pass@proxy:port
        r'^[\w\.\-]+:\d+$',                              # proxy:port (default to http)
    ]
    
    for pattern in proxy_patterns:
        if re.match(pattern, proxy_string):
            # If no protocol specified, default to http
            if not proxy_string.startswith(('http://', 'https://', 'socks4://', 'socks5://')):
                return f"http://{proxy_string}"
            return proxy_string
    
    raise argparse.ArgumentTypeError(
        f"Invalid proxy format: {proxy_string}\n"
        "Supported formats:\n"
        "  http://proxy:port\n"
        "  https://proxy:port\n"
        "  socks4://proxy:port\n"
        "  socks5://proxy:port\n"
        "  http://user:pass@proxy:port\n"
        "  socks5://user:pass@proxy:port\n"
        "  proxy:port (default to http)"
    )


def validate_limit(limit_string):
    """Validate limit parameter."""
    if limit_string.lower() == 'all':
        return None  # None means download all
    try:
        limit = int(limit_string)
        if limit <= 0:
            raise argparse.ArgumentTypeError("Limit must be positive integer or 'all'")
        return limit
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid limit: {limit_string}. Use positive integer or 'all'")


def validate_url(url_string):
    """Validate Twitter/X URL format."""
    twitter_patterns = [
        r'^https?://(www\.)?twitter\.com/\w+/status/\d+',
        r'^https?://(www\.)?x\.com/\w+/status/\d+',
        r'^https?://twitter\.com/\w+/status/\d+',
        r'^https?://x\.com/\w+/status/\d+',
        r'^https?://t\.co/\w+',
    ]
    
    for pattern in twitter_patterns:
        if re.match(pattern, url_string):
            return url_string
    
    raise argparse.ArgumentTypeError(
        f"Invalid Twitter/X URL: {url_string}\n"
        "Supported formats:\n"
        "  https://twitter.com/username/status/123456789\n"
        "  https://x.com/username/status/123456789\n"
        "  https://t.co/xxxxx"
    )


def validate_quality(quality_string):
    """Validate video quality option."""
    valid_qualities = ['best', 'high', 'medium', 'low', 'worst']
    if quality_string.lower() in valid_qualities:
        return quality_string.lower()
    raise argparse.ArgumentTypeError(
        f"Invalid quality: {quality_string}\n"
        f"Valid options: {', '.join(valid_qualities)}"
    )


def parse_raw_cookies(raw_text):
    """Parse raw cookie text into Netscape format file.

    Accepts multiple formats:
    - "auth_token=xxx; ct0=yyy" (semicolon-separated)
    - "auth_token\txxx\nct0\tyyy" (tab/newline separated)
    - "auth_token: xxx, ct0: yyy" (colon/comma separated)
    - Cookie-Editor JSON string (auto-detect)
    - Browser DevTools copy-paste format
    Returns a temporary file path in Netscape format.
    """
    raw_text = raw_text.strip()

    # If it looks like JSON, try to parse as JSON cookies
    if raw_text.startswith('{') or raw_text.startswith('['):
        try:
            import json
            cookies = json.loads(raw_text)
            if isinstance(cookies, dict):
                cookies = [cookies]
            lines = ['# Netscape HTTP Cookie File']
            for c in cookies:
                name = c.get('name', '')
                value = c.get('value', '')
                if name:
                    lines.append(f'.x.com\tTRUE\t/\tTRUE\t0\t{name}\t{value}')
            tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
            tmp.write('\n'.join(lines))
            tmp.close()
            return tmp.name
        except json.JSONDecodeError:
            pass

    # Try key=value pairs
    cookies = {}

    # Pattern 1: "auth_token=xxx; ct0=yyy" or "auth_token=xxx;ct0=yyy"
    if '=' in raw_text and (';' in raw_text or '\n' in raw_text):
        parts = re.split(r'[;\n]', raw_text)
        for part in parts:
            part = part.strip()
            if '=' in part:
                k, v = part.split('=', 1)
                cookies[k.strip()] = v.strip()

    # Pattern 2: "auth_token\txxx\nct0\tyyy" (tab-separated)
    if not cookies and '\t' in raw_text:
        for line in raw_text.strip().split('\n'):
            line = line.strip()
            if '\t' in line:
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    cookies[parts[0].strip()] = parts[1].strip()

    # Pattern 3: "auth_token: xxx, ct0: yyy"
    if not cookies and ':' in raw_text and ',' in raw_text:
        parts = re.split(r'[,\n]', raw_text)
        for part in parts:
            part = part.strip()
            if ':' in part:
                k, v = part.split(':', 1)
                cookies[k.strip()] = v.strip()

    if not cookies:
        print("Error: Could not parse cookie text. Expected format like:", file=sys.stderr)
        print("  auth_token=xxx; ct0=yyy", file=sys.stderr)
        print("  or auth_token=xxx;ct0=yyy", file=sys.stderr)
        print("  or JSON format", file=sys.stderr)
        sys.exit(1)

    # Build Netscape format
    lines = ['# Netscape HTTP Cookie File']
    for name, value in cookies.items():
        if value:  # skip empty values
            lines.append(f'.x.com\tTRUE\t/\tTRUE\t0\t{name}\t{value}')

    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    tmp.write('\n'.join(lines))
    tmp.close()
    return tmp.name


def build_gallery_dl_command(args):
    """Build gallery-dl command from arguments."""
    cmd = ['gallery-dl']

    # Add proxy if specified
    if args.proxy:
        cmd.extend(['--proxy', args.proxy])

    # Add cookies file (args.cookies is now always a resolved file path)
    cmd.extend(['--cookies', args.cookies])
    
    # Build filters
    filters = []
    
    # Date filters (only for user timeline, not single tweets)
    if not args.url:
        if args.start_date:
            filters.append(f"date >= datetime({args.start_date.replace('-', ', ')})")
        if args.end_date:
            filters.append(f"date <= datetime({args.end_date.replace('-', ', ')})")
    
    # File type filter
    if args.type and args.type != 'all':
        type_filters = []
        types = [t.strip() for t in args.type.split(',')]
        
        for t in types:
            if t == 'image':
                type_filters.append('extension in ("jpg", "jpeg", "png", "webp")')
            elif t == 'video':
                type_filters.append('extension in ("mp4", "mov", "avi", "webm")')
            elif t == 'gif':
                type_filters.append('extension in ("gif")')
            elif t == 'audio':
                type_filters.append('extension in ("mp3", "m4a", "ogg", "wav", "aac")')
        
        if type_filters:
            filters.append(f"({' or '.join(type_filters)})")
    
    # No images filter (only videos, gifs, audio)
    if args.no_images:
        filters.append('extension in ("mp4", "mov", "avi", "webm", "gif", "mp3", "m4a", "ogg", "wav", "aac")')
    
    # Apply filters
    if filters:
        filter_expr = ' and '.join(filters)
        # Add abort() for date-based filtering to stop early
        if (args.start_date or args.end_date) and not args.url:
            filter_expr += ' or abort()'
        cmd.extend(['--filter', filter_expr])
    
    # Retweets option (only for user timeline)
    if not args.url:
        if args.no_retweets:
            cmd.extend(['--option', 'twitter.retweets=false'])
        else:
            cmd.extend(['--option', 'twitter.retweets=true'])
    
    # Tweet text download
    if args.with_tweets:
        cmd.extend(['--option', 'twitter.text-tweets=true'])
    
    # Video quality selection
    if args.quality:
        quality_map = {
            'best': 'orig',
            'high': '1080',
            'medium': '720',
            'low': '480',
            'worst': '360'
        }
        size = quality_map.get(args.quality, 'orig')
        cmd.extend(['--option', f'twitter.size={size}'])
    
    # Add limit (max-posts) - only for user timeline
    if args.limit and not args.url:
        cmd.extend(['--range', f'1-{args.limit}'])
    
    # Add output directory
    if args.output:
        cmd.extend(['-d', args.output])
    
    # Add sleep to avoid rate limiting
    if args.sleep:
        cmd.extend(['--sleep-request', str(args.sleep)])
    
    # Build URL
    if args.url:
        url = args.url
    else:
        url = f"https://twitter.com/{args.username}/media"
    cmd.append(url)
    
    return cmd


def main():
    parser = argparse.ArgumentParser(
        description='Download media from Twitter/X user timeline or single tweet',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    # URL mode or username mode
    parser.add_argument('username', nargs='?', help='Twitter/X username (without @)')
    parser.add_argument('--url', type=validate_url, 
                       help='Single tweet URL to download')
    
    parser.add_argument('--cookies', required=True,
                        help='Cookie file path (Netscape format) or raw cookie text '
                             '(e.g. "auth_token=xxx; ct0=yyy")')
    parser.add_argument('--proxy', type=validate_proxy, 
                       help='Proxy URL (http/https/socks4/socks5, e.g., http://127.0.0.1:8080)')
    parser.add_argument('--start-date', type=validate_date, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', type=validate_date, help='End date (YYYY-MM-DD)')
    parser.add_argument('--limit', '-n', type=validate_limit, 
                       help='Limit number of posts to download (integer or "all")')
    parser.add_argument('--output', '-o', default='./downloads', help='Output directory (default: ./downloads)')
    parser.add_argument('--type', default='all', 
                       help='Filter by file type: image, video, gif, audio, or comma-separated (default: all)')
    parser.add_argument('--quality', type=validate_quality, default='best',
                       help='Video quality: best, high, medium, low, worst (default: best)')
    parser.add_argument('--no-retweets', action='store_true', 
                       help='Exclude retweets from download')
    parser.add_argument('--no-images', action='store_true', 
                       help='Download only videos/gif/audio (exclude images)')
    parser.add_argument('--with-tweets', action='store_true', 
                       help='Download tweet text with links alongside media')
    parser.add_argument('--sleep', type=float, default=1.0,
                       help='Sleep time between requests in seconds (default: 1.0)')
    parser.add_argument('--dry-run', action='store_true', help='Print command without executing')
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.url and not args.username:
        parser.error("Either username or --url is required")
    
    if args.url and args.username:
        parser.error("Cannot use both username and --url")
    
    if args.url and (args.start_date or args.end_date or args.limit or args.no_retweets):
        print("Warning: Date filters, limit, and retweet options are ignored for single tweet URLs", file=sys.stderr)
    
    # Resolve cookies: file path or raw text
    raw_cookie_file = None
    if os.path.exists(args.cookies):
        # It's a valid file path, use as-is
        pass
    elif 'auth_token' in args.cookies or '=' in args.cookies or args.cookies.startswith('{'):
        # Looks like raw cookie text, parse it
        raw_cookie_file = parse_raw_cookies(args.cookies)
        args.cookies = raw_cookie_file
    else:
        print(f"Error: Cookies file not found and doesn't look like raw cookie text: {args.cookies}", file=sys.stderr)
        sys.exit(1)
    
    # Validate conflicting options
    if args.type == 'image' and args.no_images:
        print("Error: Cannot use --type image with --no-images", file=sys.stderr)
        sys.exit(1)
    
    # Build command
    cmd = build_gallery_dl_command(args)
    
    if args.dry_run:
        print("Command that would be executed:")
        print(' '.join(cmd))
        print()
        print("Parameters:")
        if args.url:
            print(f"  URL: {args.url}")
        else:
            print(f"  Username: @{args.username}")
        print(f"  Cookies: {args.cookies}")
        print(f"  Proxy: {args.proxy or 'None'}")
        if not args.url:
            print(f"  Date range: {args.start_date or 'Any'} to {args.end_date or 'Any'}")
            print(f"  Limit: {args.limit or 'All'}")
            print(f"  No retweets: {args.no_retweets}")
        print(f"  File type: {args.type}")
        print(f"  Quality: {args.quality}")
        print(f"  No images: {args.no_images}")
        print(f"  With tweets: {args.with_tweets}")
        print(f"  Output: {args.output}")
        print(f"  Sleep: {args.sleep}s")
        return
    
    # Execute command
    if args.url:
        print(f"Downloading media from tweet: {args.url}")
    else:
        print(f"Downloading media from @{args.username}...")
    print(f"Proxy: {args.proxy or 'None'}")
    if not args.url:
        print(f"Date range: {args.start_date or 'Any'} to {args.end_date or 'Any'}")
        print(f"Limit: {args.limit or 'All'}")
        print(f"No retweets: {args.no_retweets}")
    print(f"File type: {args.type}")
    print(f"Quality: {args.quality}")
    print(f"No images: {args.no_images}")
    print(f"With tweets: {args.with_tweets}")
    print(f"Output: {args.output}")
    print(f"Command: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(cmd, check=True, text=True)
        print("\nDownload completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\nDownload failed with exit code {e.returncode}", file=sys.stderr)
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\nDownload interrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Clean up temp cookie file if we created one
        if raw_cookie_file and os.path.exists(raw_cookie_file):
            os.unlink(raw_cookie_file)


if __name__ == '__main__':
    main()