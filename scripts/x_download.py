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


def build_gallery_dl_command(args):
    """Build gallery-dl command from arguments."""
    cmd = ['gallery-dl']
    
    # Add proxy if specified
    if args.proxy:
        cmd.extend(['--proxy', args.proxy])
    
    # Add cookies file
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
    
    parser.add_argument('--cookies', required=True, help='Path to cookies file (Netscape format)')
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
    
    # Validate cookies file exists
    if not os.path.exists(args.cookies):
        print(f"Error: Cookies file not found: {args.cookies}", file=sys.stderr)
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


if __name__ == '__main__':
    main()