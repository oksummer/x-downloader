# Proxy Configuration

## Supported Proxy Types

The x-download script supports the following proxy protocols:

- **HTTP**: `http://proxy:port` or `http://user:pass@proxy:port`
- **HTTPS**: `https://proxy:port` or `https://user:pass@proxy:port`
- **SOCKS4**: `socks4://proxy:port` or `socks4://user:pass@proxy:port`
- **SOCKS5**: `socks5://proxy:port` or `socks5://user:pass@proxy:port`
- **Short format**: `proxy:port` (defaults to HTTP)

## Quick Reference

### Common Proxy Formats

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

## Common Proxy Configurations

### Local SOCKS5 Proxy

```bash
# Using local SOCKS5 proxy (e.g., from SSH tunnel or VPN)
gallery-dl --proxy socks5://127.0.0.1:1080 "URL"

# Common local proxy ports
gallery-dl --proxy socks5://127.0.0.1:7890 "URL"  # Clash
gallery-dl --proxy socks5://127.0.0.1:1080 "URL"  # Shadowsocks
gallery-dl --proxy socks5://127.0.0.1:8080 "URL"  # V2Ray
```

### HTTP Proxy

```bash
# Using HTTP proxy
gallery-dl --proxy http://proxy.company.com:8080 "URL"

# With authentication
gallery-dl --proxy http://username:password@proxy:8080 "URL"
```

### Remote SOCKS5 Proxy

```bash
# Using remote SOCKS5 proxy
gallery-dl --proxy socks5://proxy.example.com:1080 "URL"

# With authentication
gallery-dl --proxy socks5://username:password@proxy:1080 "URL"
```

## Environment Variables

Gallery-dl can read proxy settings from environment variables:

```bash
# Set environment variables
export HTTP_PROXY=http://proxy:8080
export HTTPS_PROXY=http://proxy:8080
export ALL_PROXY=socks5://proxy:1080

# Then run gallery-dl without --proxy
gallery-dl "URL"
```

## Proxy Chains

For multiple proxies, use proxychains or similar tools:

```bash
# Using proxychains with SOCKS5
proxychains gallery-dl --cookies cookies.txt "URL"

# Configure proxychains in /etc/proxychains.conf
# socks5 127.0.0.1 1080
```

## Testing Proxy Connection

### Test with curl

```bash
# Test SOCKS5 proxy
curl --proxy socks5://127.0.0.1:7897 https://x.com

# Test HTTP proxy
curl --proxy http://proxy:8080 https://x.com
```

### Test with gallery-dl

```bash
# Test proxy with gallery-dl
gallery-dl --proxy socks5://127.0.0.1:7897 --range 1-3 "https://twitter.com/username/media"
```

## Proxy Format Validation

The x-download script validates proxy formats automatically. Valid formats include:

| Format | Example | Description |
|--------|---------|-------------|
| `http://host:port` | `http://proxy:8080` | HTTP proxy |
| `https://host:port` | `https://proxy:443` | HTTPS proxy |
| `socks4://host:port` | `socks4://proxy:1080` | SOCKS4 proxy |
| `socks5://host:port` | `socks5://proxy:1080` | SOCKS5 proxy |
| `http://user:pass@host:port` | `http://user:pass@proxy:8080` | HTTP with auth |
| `socks5://user:pass@host:port` | `socks5://user:pass@proxy:1080` | SOCKS5 with auth |
| `host:port` | `proxy:8080` | Short format (HTTP) |

## Troubleshooting

### Proxy Connection Refused

- **Check proxy is running**: `netstat -tlnp | grep 7897`
- **Verify port number**: Common ports: 1080, 7890, 8080
- **Check firewall settings**: Ensure proxy port is accessible

### SOCKS5 Support Missing

- **Install PySocks**: `pip install pysocks`
- **Verify installation**: `python -c "import socks; print('OK')"`

### Slow Downloads Through Proxy

- **Try different proxy server**
- **Reduce concurrent connections**: `--sleep-request 1.0`
- **Use HTTP instead of SOCKS5** if possible

### Proxy Authentication Failed

- **Verify credentials**: Check username/password
- **URL encode special characters**: `http://user%40domain:pass@proxy:8080`
- **Check proxy authentication method**: Some proxies require specific auth methods

### Invalid Proxy Format

If you get "Invalid proxy format" error:

1. Check the format matches one of the supported patterns
2. Ensure no spaces in the URL
3. Use proper URL encoding for special characters
4. Try the short format: `host:port`