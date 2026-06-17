```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║          ██████╗ ██╗  ██╗███████╗███████╗██████╗          ║
║         ██╔════╝ ██║ ██╔╝██╔════╝██╔════╝██╔══██╗         ║
║         ██║  ███╗█████╔╝ █████╗  █████╗  ██████╔╝         ║
║         ██║   ██║██╔═██╗ ██╔══╝  ██╔══╝  ██╔═══╝          ║
║         ╚██████╔╝██║  ██╗███████╗███████╗██║               ║
║          ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚═╝               ║
║                                                           ║
║                ███╗   ███╗ ██████╗██████╗                 ║
║                ████╗ ████║██╔════╝██╔══██╗                ║
║                ██╔████╔██║██║     ██████╔╝                ║
║                ██║╚██╔╝██║██║     ██╔═══╝                 ║
║                ██║ ╚═╝ ██║╚██████╗██║                     ║
║                ╚═╝     ╚═╝ ╚═════╝╚═╝                     ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

<div align="center">

[![Python](https://img.shields.io/badge/Python-≥3.11-3776AB?logo=python&logoColor=white)](https://python.org/)
[![uv](https://img.shields.io/badge/uv-package_manager-DE5FE9)](https://docs.astral.sh/uv/)
[![MCP](https://img.shields.io/badge/MCP-FastMCP-8B5CF6)](https://modelcontextprotocol.io/)
[![License](https://img.shields.io/badge/license-MIT-22C55E)](LICENSE)

</div>

> Search, create, and manage your Google Keep notes directly from Claude, Cursor, or any MCP-compatible AI — 18 tools, credentials in the macOS Keychain.

## Install

```bash
uv tool install git+https://github.com/kud/mcp-google-keep
mcp-google-keep-setup
claude mcp add google-keep mcp-google-keep
```

`mcp-google-keep-setup` runs the one-time Google credential flow and stores your master token in the macOS Keychain.

## Development

```bash
git clone https://github.com/kud/mcp-google-keep.git
cd mcp-google-keep && uv sync
uv run python server.py        # start the MCP server
uv run python keep_setup.py    # run the credential setup flow
```

The server lives in `server.py` (FastMCP, all 18 tools); credential setup lives in `keep_setup.py`.

---

📚 **Full documentation → https://kud.io/projects/mcp-google-keep/docs**
