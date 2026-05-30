# Gallery-dl Advanced Options

## Twitter-Specific Options

### Timeline Options

```bash
# Download from media timeline
gallery-dl "https://twitter.com/username/media"

# Download from likes
gallery-dl "https://twitter.com/username/likes"

# Download from bookmarks (requires authentication)
gallery-dl "https://twitter.com/i/bookmarks"
```

### Content Filtering

```bash
# Include retweets
gallery-dl --option "twitter.retweets=true" "URL"

# Include quoted tweets
gallery-dl --option "twitter.quoted=true" "URL"

# Include replies
gallery-dl --option "twitter.replies=true" "URL"

# Download only original media (no retweets)
gallery-dl --option "twitter.retweets=false" "URL"
```

### Image Quality

```bash
# Prefer original size
gallery-dl --option "twitter.size=orig" "URL"

# Fallback chain
gallery-dl --option "twitter.size=['orig', '4096x4096', 'large']" "URL"
```

## Date Filtering

### Using datetime Objects

```bash
# Download after specific date
gallery-dl --filter "date >= datetime(2026, 1, 1) or abort()" "URL"

# Download before specific date
gallery-dl --filter "date <= datetime(2026, 12, 31)" "URL"

# Download within date range
gallery-dl --filter "date >= datetime(2026, 1, 1) and date <= datetime(2026, 12, 31)" "URL"
```

### Using String Comparison

```bash
# Download after date string
gallery-dl --filter "str(date) >= '2026-01'" "URL"

# Download before date string
gallery-dl --filter "str(date) < '2026-06'" "URL"
```

### Advanced Date Filtering

```bash
# Stop downloading when reaching old posts
gallery-dl --filter "date >= datetime(2026, 1, 1) or abort()" "URL"

# Skip posts before date but continue
gallery-dl --filter "date >= datetime(2026, 1, 1)" "URL"

# Combine with other filters
gallery-dl --filter "date >= datetime(2026, 1, 1) and likes > 100" "URL"
```

## Download Options

### Output Directory

```bash
# Custom output directory
gallery-dl -d /path/to/downloads "URL"

# Create subdirectories by username
gallery-dl -d ./downloads/{user} "URL"

# Organize by date
gallery-dl -d ./downloads/{date:%Y/%m} "URL"
```

### File Naming

```bash
# Custom filename pattern
gallery-dl -f "{tweet_id}_{num}.{extension}" "URL"

# Include date in filename
gallery-dl -f "{date:%Y%m%d}_{tweet_id}.{extension}" "URL"

# Include username
gallery-dl -f "{user}_{tweet_id}.{extension}" "URL"
```

### Resume Downloads

```bash
# Skip existing files (default behavior)
gallery-dl "URL"

# Force re-download
gallery-dl --no-skip "URL"

# Archive downloaded URLs
gallery-dl --download-archive archive.txt "URL"
```

## Rate Limiting

### Request Throttling

```bash
# Sleep between requests
gallery-dl --sleep-request 1.0 "URL"

# Random sleep interval
gallery-dl --sleep-request "1.0-3.0" "URL"

# Sleep between different extractors
gallery-dl --sleep-extractor 5.0 "URL"
```

### Handling Rate Limits

```bash
# Wait time after 429 (Too Many Requests)
gallery-dl --sleep-429 60 "URL"

# Maximum retries
gallery-dl --retries 3 "URL"

# Retry timeout
gallery-dl --timeout 30 "URL"
```

## Metadata and Logging

### Save Metadata

```bash
# Write metadata to JSON files
gallery-dl --write-metadata "URL"

# Write info file
gallery-dl --write-info-json "URL"

# Custom metadata format
gallery-dl --write-metadata --metadata-json "URL"
```

### Logging

```bash
# Verbose output
gallery-dl -v "URL"

# Quiet mode
gallery-dl -q "URL"

# Log to file
gallery-dl --log-file download.log "URL"
```

## Error Handling

### Skip Errors

```bash
# Continue on errors
gallery-dl --ignore-errors "URL"

# Skip specific errors
gallery-dl --skip 404,403 "URL"
```

### Abort Conditions

```bash
# Abort after N consecutive skips
gallery-dl --abort 10 "URL"

# Abort on specific conditions
gallery-dl --filter "abort() if error else True" "URL"
```

## Performance Tuning

### Concurrent Downloads

```bash
# Number of concurrent downloads (default: 4)
gallery-dl --jobs 4 "URL"

# Reduce for slow connections
gallery-dl --jobs 2 "URL"
```

### Buffer Size

```bash
# Adjust buffer size for large files
gallery-dl --buffer-size 65536 "URL"
```

### Connection Settings

```bash
# Custom user agent
gallery-dl --user-agent "Mozilla/5.0..." "URL"

# Custom headers
gallery-dl --header "Authorization: Bearer token" "URL"
```

## Configuration File

Create `~/.config/gallery-dl/config.json` for persistent settings:

```json
{
    "extractor": {
        "twitter": {
            "cookies": "/path/to/cookies.txt",
            "retweets": false,
            "quoted": false,
            "replies": false,
            "size": "orig"
        }
    },
    "downloader": {
        "proxy": "socks5://127.0.0.1:7897",
        "sleep-request": 1.0,
        "retries": 3
    }
}
```