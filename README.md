# 🐦 X/Twitter Media Downloader - Hermes Agent Skill

<p align="center">
  <img src="https://img.shields.io/badge/Hermes-Agent-Skill-blue" alt="Hermes Agent Skill">
  <img src="https://img.shields.io/badge/Python-3.8+-green" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/gallery--dl-latest-orange" alt="gallery-dl">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License MIT">
</p>

一个强大的 Hermes Agent 技能，用于从 Twitter/X 下载媒体内容（图片、视频、GIF、音频）。基于 [gallery-dl](https://github.com/mikf/gallery-dl) 构建，提供更简洁的命令行接口和丰富的过滤选项。

---

## ✨ 功能特性

| 功能 | 描述 |
|------|------|
| 📷 **多媒体支持** | 下载图片、视频、GIF、音频文件 |
| 👤 **用户时间线** | 批量下载某个用户的所有媒体 |
| 🔗 **单条推文** | 下载指定推文的所有媒体 |
| 📅 **日期过滤** | 按时间范围筛选推文 |
| 🎬 **视频质量** | 支持 5 种画质选择（原画/1080p/720p/480p/360p） |
| 🔄 **转推控制** | 包含或排除转推内容 |
| 📝 **推文文本** | 可同时保存推文文字和链接 |
| 🌐 **代理支持** | HTTP/HTTPS/SOCKS4/SOCKS5 代理 |
| 🔐 **Cookie 认证** | 支持登录态访问私密内容 |
| ⏱️ **请求限速** | 自定义请求间隔，避免被封 |

---

## 📋 前置要求

### 1. 安装 gallery-dl

```bash
# 使用 pip 安装
pip install gallery-dl

# 或者使用 pipx（推荐）
pipx install gallery-dl
```

### 2. 安装 SOCKS 代理支持（可选）

如果你需要使用 SOCKS 代理，需要安装 PySocks：

```bash
pip install pysocks
```

### 3. 导出 Twitter Cookies

由于 Twitter 需要登录才能访问大部分内容，你需要导出浏览器中的 cookies：

#### 方法一：使用 Cookie-Editor 浏览器扩展

1. 安装 [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 扩展
2. 登录 Twitter/X 网站
3. 点击扩展图标
4. 点击 **Export** → 选择 **Export as JSON**
5. 保存为 `cookies.json`

#### 方法二：使用浏览器开发者工具

1. 登录 Twitter/X
2. 按 `F12` 打开开发者工具
3. 切换到 **Application** 标签
4. 在左侧找到 **Cookies** → `https://x.com`
5. 复制以下关键 cookie：
   - `auth_token`
   - `ct0`

### 4. 转换 Cookie 格式

gallery-dl 需要 **Netscape 格式**的 cookie 文件。使用以下脚本转换：

```python
#!/usr/bin/env python3
import json
import sys

def convert_cookies_json_to_netscape(json_file, output_file):
    with open(json_file, 'r') as f:
        cookies = json.load(f)
    
    lines = ['# Netscape HTTP Cookie File']
    for cookie in cookies:
        domain = cookie['domain']
        flag = 'TRUE' if domain.startswith('.') else 'FALSE'
        path = cookie.get('path', '/')
        secure = 'TRUE' if cookie.get('secure', False) else 'FALSE'
        expiration = str(int(cookie.get('expirationDate', 0)))
        name = cookie['name']
        value = cookie['value']
        lines.append(f'{domain}\t{flag}\t{path}\t{secure}\t{expiration}\t{name}\t{value}')
    
    with open(output_file, 'w') as f:
        f.write('\n'.join(lines))

# 使用方法
convert_cookies_json_to_netscape('cookies.json', 'cookies.txt')
```

---

## 🚀 快速开始

### 基本用法

```bash
# 下载某个用户的所有媒体
python scripts/x_download.py <username> --cookies cookies.txt

# 下载单条推文
python scripts/x_download.py --url https://twitter.com/user/status/123456789 --cookies cookies.txt

# 下载最近 50 条推文
python scripts/x_download.py <username> --cookies cookies.txt --limit 50
```

### 常用示例

```bash
# 下载指定日期之后的内容
python scripts/x_download.py DyDy_art --cookies cookies.txt --start-date 2026-01-01

# 使用代理下载
python scripts/x_download.py DyDy_art --cookies cookies.txt --proxy socks5://127.0.0.1:7890

# 只下载视频，排除图片
python scripts/x_download.py DyDy_art --cookies cookies.txt --type video

# 下载高质量视频
python scripts/x_download.py filmmaker --cookies cookies.txt --type video --quality high

# 排除转推，只下载原创
python scripts/x_download.py DyDy_art --cookies cookies.txt --no-retweets

# 下载媒体同时保存推文文本
python scripts/x_download.py artist --cookies cookies.txt --with-tweets

# 下载 GIF 和音频
python scripts/x_download.py creator --cookies cookies.txt --type gif,audio
```

---

## ⚙️ 配置选项

### 命令行参数

```
用法: python scripts/x_download.py <username|--url URL> [选项]

必填参数（二选一）:
  username              Twitter/X 用户名（不带 @）
  --url URL             单条推文 URL

可选参数:
  --cookies FILE        Cookie 文件路径（Netscape 格式）
  --proxy URL           代理地址（http/https/socks4/socks5）
  --start-date DATE     开始日期（YYYY-MM-DD 格式）
  --end-date DATE       结束日期（YYYY-MM-DD 格式）
  --limit N             下载数量限制（整数或 "all"）
  --output DIR          输出目录（默认: ./downloads）
  --type TYPE           媒体类型筛选：image, video, gif, audio（默认: all）
  --quality QUALITY     视频质量：best, high, medium, low, worst（默认: best）
  --no-retweets         排除转推内容
  --no-images           只下载视频/gif/audio（排除图片）
  --with-tweets         下载推文文本和链接
  --sleep SECONDS       请求间隔时间（默认: 1.0 秒）
  --dry-run             预览命令，不执行下载
```

### 媒体类型说明

| 类型 | 扩展名 | 说明 |
|------|--------|------|
| `image` | jpg, jpeg, png, webp | 静态图片 |
| `video` | mp4, mov, avi, webm | 视频文件 |
| `gif` | gif | 动图 |
| `audio` | mp3, m4a, ogg, wav, aac | 音频文件 |
| `all` | 以上所有 | 下载所有媒体 |

### 视频质量说明

| 质量 | 分辨率 | 说明 |
|------|--------|------|
| `best` | 原始分辨率 | 最高画质 |
| `high` | 1080p | 全高清 |
| `medium` | 720p | 高清 |
| `low` | 480p | 标清 |
| `worst` | 360p | 低清 |

---

## 🌐 代理配置

### 支持的代理格式

```bash
# HTTP 代理
--proxy http://127.0.0.1:8080

# HTTPS 代理
--proxy https://proxy.example.com:443

# SOCKS4 代理
--proxy socks4://127.0.0.1:1080

# SOCKS5 代理
--proxy socks5://127.0.0.1:7897

# 带认证的代理
--proxy http://user:password@proxy:8080
--proxy socks5://user:password@proxy:1080

# 简写格式（默认 HTTP）
--proxy 127.0.0.1:8080
```

### 常见代理配置

```bash
# Clash 默认端口
--proxy socks5://127.0.0.1:7890

# Shadowsocks 默认端口
--proxy socks5://127.0.0.1:1080

# V2Ray 默认端口
--proxy socks5://127.0.0.1:10808
```

### 环境变量方式

```bash
# 设置环境变量后可省略 --proxy 参数
export HTTP_PROXY=http://proxy:8080
export HTTPS_PROXY=http://proxy:8080
export ALL_PROXY=socks5://proxy:1080

gallery-dl "https://twitter.com/username/media"
```

---

## 🍪 Cookie 配置详解

### 为什么需要 Cookie？

Twitter/X 的大部分内容需要登录才能访问。使用 Cookie 可以：
- 访问用户的私密推文
- 下载高质量原图
- 避免被限流

### 必需的 Cookie 字段

| Cookie 名 | 说明 | 是否必需 |
|-----------|------|----------|
| `auth_token` | 认证令牌（长期有效） | ✅ 必需 |
| `ct0` | CSRF 令牌（会话有效） | ✅ 必需 |
| `twid` | 用户 ID | ⚠️ 推荐 |
| `guest_id` | 访客标识 | ❌ 可选 |

### 验证 Cookie 文件

```bash
# 检查 auth_token
grep -q "auth_token" cookies.txt && echo "✓ auth_token found" || echo "✗ auth_token missing"

# 检查 ct0
grep -q "ct0" cookies.txt && echo "✓ ct0 found" || echo "✗ ct0 missing"
```

### Cookie 文件格式示例

```
# Netscape HTTP Cookie File
.x.com	TRUE	/	TRUE	1234567890	auth_token	your_auth_token_here
.x.com	TRUE	/	TRUE	1234567890	ct0	your_ct0_token_here
```

---

## 🔧 高级用法

### 使用 gallery-dl 原生命令

对于更复杂的场景，可以直接使用 gallery-dl：

```bash
# 下载用户媒体时间线
gallery-dl --cookies cookies.txt "https://twitter.com/username/media"

# 下载用户点赞
gallery-dl --cookies cookies.txt "https://twitter.com/username/likes"

# 下载书签（需登录）
gallery-dl --cookies cookies.txt "https://twitter.com/i/bookmarks"

# 使用日期过滤
gallery-dl --cookies cookies.txt \
  --filter "date >= datetime(2026, 1, 1) or abort()" \
  "https://twitter.com/username/media"

# 排除转推
gallery-dl --cookies cookies.txt \
  --option "twitter.retweets=false" \
  "https://twitter.com/username/media"

# 保存推文文本
gallery-dl --cookies cookies.txt \
  --option "twitter.text-tweets=true" \
  "https://twitter.com/username/media"

# 自定义输出目录
gallery-dl --cookies cookies.txt -d ./my_downloads "https://twitter.com/username/media"

# 下载指定数量
gallery-dl --cookies cookies.txt --range 1-50 "https://twitter.com/username/media"
```

### gallery-dl 配置文件

创建 `~/.config/gallery-dl/config.json` 进行持久化配置：

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
        "proxy": "socks5://127.0.0.1:7890",
        "sleep-request": 1.0,
        "retries": 3
    }
}
```

---

## 🐛 故障排除

### 常见问题

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `AuthRequired` 错误 | Cookie 无效或过期 | 重新从浏览器导出 Cookie |
| `Missing dependencies for SOCKS support` | 缺少 PySocks | `pip install pysocks` |
| `NotFoundError` | 用户名不存在或账户私密 | 验证用户名和账户状态 |
| `Invalid URL` | 推文 URL 格式不正确 | 使用完整格式：`https://twitter.com/user/status/123456789` |
| 下载中断 | 被限流或网络问题 | 增加 `--sleep` 值（如 `--sleep 2.0`） |
| 下载不完整 | 有 `.part` 文件残留 | 删除 `.part` 文件后重新下载 |
| 视频画质低 | 原视频本身分辨率低 | 检查原视频是否有更高画质版本 |

### 调试模式

使用 `--dry-run` 预览命令而不执行：

```bash
# 预览用户下载命令
python scripts/x_download.py username --cookies cookies.txt --dry-run

# 预览单条推文下载命令
python scripts/x_download.py --url https://twitter.com/user/status/123 --cookies cookies.txt --dry-run
```

### 详细日志

```bash
# gallery-dl 详细输出
gallery-dl -v --cookies cookies.txt "https://twitter.com/username/media"

# 静默模式
gallery-dl -q --cookies cookies.txt "https://twitter.com/username/media"
```

---

## 📁 项目结构

```
x-downloader/
├── README.md                    # 本文档
├── SKILL.md                     # Hermes Agent 技能描述文件
├── scripts/
│   └── x_download.py           # 主下载脚本
└── references/
    ├── cookies_format.md       # Cookie 格式说明
    ├── gallery-dl_docs.md      # gallery-dl 高级选项
    └── proxy_config.md         # 代理配置详解
```

---

## 🤝 集成到 Hermes Agent

### 安装技能

```bash
# 将整个目录复制到 Hermes 技能目录
cp -r x-downloader ~/.hermes/skills/

# 或者使用符号链接
ln -s $(pwd)/x-downloader ~/.hermes/skills/x-downloader
```

### 在对话中使用

安装后，Hermes Agent 会自动识别此技能。你可以直接说：

- "帮我下载 @username 的所有推文图片"
- "下载这条推文的视频：https://twitter.com/user/status/123"
- "下载 @artist 最近 100 条推文，只要视频"

---

## 📄 相关文档

- [Cookie 文件格式](references/cookies_format.md) - Cookie 导出和转换详细说明
- [Gallery-dl 高级选项](references/gallery-dl_docs.md) - gallery-dl 的完整功能参考
- [代理配置详解](references/proxy_config.md) - 各种代理类型的配置方法

---

## 📜 许可证

MIT License - 可自由使用、修改和分发。

---

## 🙏 致谢

- [gallery-dl](https://github.com/mikf/gallery-dl) - 强大的媒体下载工具
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) - 智能代理框架

---

## ⚠️ 免责声明

本工具仅用于个人学习和研究目的。请遵守 Twitter/X 的服务条款和相关法律法规。用户需自行承担使用本工具产生的一切责任。
