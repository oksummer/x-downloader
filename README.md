# 🐦 X/Twitter Media Downloader - Hermes Agent Skill

<p align="center">
  <img src="https://img.shields.io/badge/Hermes-Agent-Skill-blue" alt="Hermes Agent Skill">
  <img src="https://img.shields.io/badge/Python-3.8+-green" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/gallery--dl-latest-orange" alt="gallery-dl">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License MIT">
</p>

## 🎯 一键安装配置（复制此提示词给 AI）

> **将以下提示词复制粘贴给 AI 助手，AI 会自动完成所有安装和配置，你只需提供 Cookie 即可。**

```
请帮我克隆 https://github.com/oksummer/x-downloader.git 这个skill并自动安装配置 x-downloader（X/Twitter 媒体下载工具）。
我的 Cookie：[浏览器插件导出的Cookie纯文本]
请自动完成以下所有步骤，不需要我手动执行任何命令：
1. 检测并安装 gallery-dl（pip install gallery-dl）
2. 检测并安装 pysocks（如果需要代理）
3. 用我提供的 Cookie 生成配置
4. 执行一次测试下载验证配置
5. 告诉我结果和可用的命令示例

如果遇到代理问题，自动配置代理。
如果缺少 Python 环境，自动安装。
总之：自动搞定一切，我只需要提供 Cookie。
```

> 💡 **你只需要做一件事**：用 EditThisCookie 扩展导出纯文本 Cookie，粘贴到上面的提示词里。其余所有安装、配置、测试全部由 AI 自动完成。

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

## 🍪 Cookie 配置详解

### 快速获取 Cookie（30秒完成）

1. 安装 [EditThisCookie v3](https://chromewebstore.google.com/detail/editthiscookie-v3/ojfebgpkimhlhcblbalbfjblapadhbol) 扩展
2. 浏览器登录 [x.com](https://x.com)
3. 点击扩展图标 → 导出纯文本
4. 粘贴使用

就这么简单！EditThisCookie 直接导出纯文本，无需转换。

### 支持的 Cookie 输入格式

| 格式 | 示例 | 说明 |
|------|------|------|
| 纯文本 `key=value` | `auth_token=xxx; ct0=yyy` | ⭐ 最简单，直接粘贴 |
| JSON 数组 | `[{"name":"auth_token","value":"xxx"}]` | Cookie-Editor 导出 |
| JSON 对象 | `{"auth_token":"xxx","ct0":"yyy"}` | 单个 cookie 对象 |
| Netscape 文件 | `cookies.txt` 文件路径 | 传统格式，依然支持 |

> 💡 只需 `auth_token` 和 `ct0` 两个值即可正常工作。

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
