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

### Search, create, and manage your Google Keep notes

### directly from Claude, Cursor, or any MCP-compatible AI.

[Features](#features) · [Quick Start](#quick-start) · [Tools](#available-tools) · [Installation](#installation) · [Auth](#authentication) · [Development](#development)

</div>

---

## Why this exists

Google Keep has no official API for personal accounts. This server uses [gkeepapi](https://github.com/kiwiz/gkeepapi) — a battle-tested Python library that speaks Keep's private sync protocol — to give your AI assistant full read/write access to your notes.

Your credentials never touch disk: the master token is stored in the **macOS Keychain**.

---

## Features

- 📝 **List & search** notes by text, label, colour, or state (pinned/archived/trashed)
- ✏️ **Create** text notes and checklist notes
- ✅ **Manage list items** — add, check/uncheck, or replace all items
- 🏷️ **Full label support** — list, create, delete, assign, and remove labels
- 🎨 **Colour filters** — find all your red, blue, or yellow notes
- 🔐 **Credentials in macOS Keychain** — nothing written to disk
- 🛡️ **Destructive actions** require explicit `confirm: true`
- 11 tools total — covering the full gkeepapi surface

---

## Quick Start

**1. Install**

```bash
uv tool install git+https://github.com/kud/mcp-google-keep
```

Or clone if you prefer:

```bash
git clone https://github.com/kud/mcp-google-keep.git
cd mcp-google-keep && uv sync
```

**2. Authorise**

```bash
mcp-google-keep-setup
```

The setup script walks you through a browser-based OAuth flow and saves your credentials to the macOS Keychain. Ready in about 2 minutes.

**3. Add to Claude Code**

```bash
claude mcp add google-keep mcp-google-keep
```

**3. Ask Claude anything**

> _"Search my Keep notes for 'grocery list'"_
> _"Create a shopping list with milk, eggs, and bread"_
> _"Pin my Ideas note and colour it yellow"_
> _"Show me all my red notes"_

---

## Available Tools

### Notes

| Tool               | Description                                                                             |
| ------------------ | --------------------------------------------------------------------------------------- |
| `list_notes`       | List / search notes — filter by text query, labels, colors, pinned / archived / trashed |
| `get_note`         | Fetch a single note by ID                                                               |
| `create_text_note` | Create a plain-text note with optional title                                            |
| `create_list_note` | Create a checklist note with initial items                                              |
| `update_note`      | Update title, text, pin, archive, colour, or add / remove labels                        |
| `delete_note`      | Move to trash — requires `confirm: true`                                                |

### List Items

| Tool                | Description                                               |
| ------------------- | --------------------------------------------------------- |
| `add_list_item`     | Append a single item to an existing checklist             |
| `update_list_items` | Replace all items in a checklist (full state replacement) |

### Labels

| Tool           | Description                                                            |
| -------------- | ---------------------------------------------------------------------- |
| `list_labels`  | List all labels                                                        |
| `create_label` | Create a new label                                                     |
| `delete_label` | Delete a label and remove it from all notes — requires `confirm: true` |

**Total: 11 Tools**

---

## Installation

<details>
<summary><strong>Claude Code CLI (recommended)</strong></summary>

```bash
claude mcp add google-keep -- uv --directory /path/to/mcp-google-keep run python server.py
```

Or if installed via `uv tool install`, use the entry point directly:

```json
{
  "mcpServers": {
    "google-keep": {
      "command": "mcp-google-keep"
    }
  }
}
```

Or with `uvx` (ephemeral — no install required):

```json
{
  "mcpServers": {
    "google-keep": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/kud/mcp-google-keep",
        "mcp-google-keep"
      ]
    }
  }
}
```

</details>

<details>
<summary><strong>Claude Desktop — macOS</strong></summary>

Edit `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "google-keep": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-google-keep",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

</details>

<details>
<summary><strong>Cursor</strong></summary>

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "google-keep": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-google-keep",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

</details>

<details>
<summary><strong>Windsurf</strong></summary>

Add to `~/.codeium/windsurf/mcp_config.json`:

```json
{
  "mcpServers": {
    "google-keep": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/mcp-google-keep",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

</details>

<details>
<summary><strong>VSCode (Cline / Roo)</strong></summary>

```json
{
  "google-keep": {
    "command": "uv",
    "args": [
      "--directory",
      "/path/to/mcp-google-keep",
      "run",
      "python",
      "server.py"
    ]
  }
}
```

</details>

---

## Authentication

Google Keep has no official API for personal Gmail accounts. This server uses the **private sync protocol** via [gkeepapi](https://github.com/kiwiz/gkeepapi) + [gpsoauth](https://github.com/simon-weber/gpsoauth).

### One-time setup

```bash
# After uv tool install:
mcp-google-keep-setup

# From source:
uv run python keep_setup.py
```

The script will:

1. Ask for your Google account email
2. Open `accounts.google.com/EmbeddedSetup` in your browser
3. Sign in — ignore the infinite loader, that's expected
4. Open DevTools (F12) → **Application** → **Cookies** → **accounts.google.com**
5. Find `oauth_token` → double-click its value → copy it
6. Paste it into the terminal
7. Exchange it for a long-lived master token
8. Save to macOS Keychain under `mcp-google-keep`

> **Note:** `oauth_token` is an `HttpOnly` cookie — it only appears in the DevTools **Application** panel, not the Console.

### Alternative: environment variables

```bash
export GOOGLE_KEEP_EMAIL="you@gmail.com"
export GOOGLE_KEEP_MASTER_TOKEN="aas_et/..."
uv run python server.py
```

---

## Example Conversations

| Prompt                                        | What happens                                           |
| --------------------------------------------- | ------------------------------------------------------ |
| _"Show me all my notes"_                      | Lists all non-trashed notes                            |
| _"Search my notes for 'recipe'"_              | Finds notes containing "recipe"                        |
| _"Show me my pinned yellow notes"_            | `list_notes(pinned=True, colors=["YELLOW"])`           |
| _"Create a shopping list: milk, eggs, bread"_ | Creates a checklist note with 3 items                  |
| _"Add 'butter' to my shopping list"_          | Calls `add_list_item` on the existing note             |
| _"Check off 'milk'"_                          | `update_list_items` with updated checked states        |
| _"Label my Ideas note with 'work'"_           | `update_note(add_labels=["work"])`                     |
| _"What labels do I have?"_                    | `list_labels()`                                        |
| _"Archive all my travel notes"_               | Finds travel notes, calls `update_note(archived=True)` |
| _"Delete note abc123"_                        | `delete_note(confirm=True)` after you confirm          |

---

## Development

### Project structure

```
mcp-google-keep/
├── server.py        # FastMCP server — all 11 tools
├── keep_setup.py    # Interactive Keychain credential setup
├── pyproject.toml   # Python project & dependencies
├── uv.lock          # Locked dependency tree
├── .mcp.json        # Local MCP config (gitignored)
└── CLAUDE.md        # AI assistant context
```

### Scripts

| Command                   | Description                   |
| ------------------------- | ----------------------------- |
| `mcp-google-keep-setup`   | Run the credential setup flow |
| `uv run python server.py` | Start the MCP server          |
| `uv sync`                 | Install / sync dependencies   |

### Dependencies

| Package    | Purpose                      |
| ---------- | ---------------------------- |
| `mcp[cli]` | FastMCP server framework     |
| `gkeepapi` | Google Keep private sync API |
| `gpsoauth` | Google Play Services OAuth   |
| `keyring`  | macOS Keychain integration   |
| `rich`     | Terminal UI for setup script |

---

## Troubleshooting

**Server not appearing in Claude**

- Verify the `--directory` path is absolute and correct
- Run `uv run python server.py` directly to check for startup errors
- Restart Claude Desktop or reload the MCP client

**`No credentials found` error**

- Run `mcp-google-keep-setup`

**`oauth_token` missing from DevTools**

- It's `HttpOnly` — only visible under **Application → Cookies**, not the Console
- Sign in again if it's missing; it appears right after authentication

**Token expired or invalid**

- Re-run `mcp-google-keep-setup` and choose to overwrite

**Where are the logs?**

- All server output goes to stderr
- Claude Desktop: `~/Library/Logs/Claude/mcp-server-google-keep.log`

---

## Security

- Credentials live in **macOS Keychain** — never written to disk
- The master token grants full Google account access — treat it like a password
- Revoke at [myaccount.google.com/permissions](https://myaccount.google.com/permissions) if compromised
- `.mcp.json` is gitignored — never committed even if it contains config

---

## Tech Stack

| Layer              | Choice                                      |
| ------------------ | ------------------------------------------- |
| Runtime            | Python ≥ 3.11                               |
| Package manager    | uv                                          |
| MCP framework      | FastMCP                                     |
| Keep library       | gkeepapi                                    |
| Auth flow          | gpsoauth — EmbeddedSetup + `exchange_token` |
| Credential storage | macOS Keychain via `keyring`                |
| Setup UI           | `rich`                                      |

---

## Contributing

Issues and PRs welcome — [github.com/kud/mcp-google-keep](https://github.com/kud/mcp-google-keep/issues).

## License

MIT © [kud](https://github.com/kud)

## Acknowledgments

Built on [gkeepapi](https://github.com/kiwiz/gkeepapi) by [@kiwiz](https://github.com/kiwiz), [FastMCP](https://github.com/jlowin/fastmcp), and [gpsoauth](https://github.com/simon-weber/gpsoauth).

---

<div align="center">

Made with ❤️ for AI-assisted productivity

⭐ **Star this repo if it saves you time!**

[Back to top](#)

</div>
