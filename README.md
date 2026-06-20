<div align="center">

![TypeScript](https://img.shields.io/badge/Python-≥3.11-3776AB?style=flat-square&logo=python&logoColor=white)
![MCP](https://img.shields.io/badge/MCP-FastMCP-8B5CF6?style=flat-square)
![MIT](https://img.shields.io/badge/licence-MIT-22C55E?style=flat-square)

**Search, create, and manage your Google Keep notes directly from Claude, Cursor, or any MCP-compatible AI — 18 tools, credentials in the macOS Keychain.**

<a href="https://kud.io/projects/mcp-google-keep">Website</a> · <a href="https://kud.io/projects/mcp-google-keep/docs">Documentation</a>

</div>

## Features

- **Full note management** — create text notes and checklists, update content, colour, and pinned/archived state in one call
- **Rich filtering** — search notes by query text, label, colour, or pinned/archived/trashed status
- **Checklist tools** — add, replace, sort, indent, and dedent list items without touching the whole note
- **Label management** — create, rename, and delete labels; apply or remove them from any note
- **Collaboration** — share notes with other Google accounts and revoke access by email
- **Secure credentials** — one-time OAuth flow stores your master token in the macOS Keychain; no plaintext secrets

## Install

```sh
uv tool install git+https://github.com/kud/mcp-google-keep
mcp-google-keep-setup
claude mcp add google-keep mcp-google-keep
```

`mcp-google-keep-setup` runs the one-time Google credential flow and stores your master token in the macOS Keychain.

## Usage

Add the server to your MCP client config:

```json
{
  "mcpServers": {
    "google-keep": {
      "command": "mcp-google-keep"
    }
  }
}
```

Available tools:

| Tool                  | Description                                                                    |
| --------------------- | ------------------------------------------------------------------------------ |
| `list_notes`          | List notes; filter by query, label, colour, pinned, archived, or trashed state |
| `get_note`            | Fetch a single note by ID                                                      |
| `create_text_note`    | Create a new text note                                                         |
| `create_list_note`    | Create a new checklist note                                                    |
| `update_note`         | Update title, text, colour, pinned/archived state, or labels                   |
| `delete_note`         | Move a note to trash (requires `confirm=true`)                                 |
| `restore_note`        | Restore a trashed note                                                         |
| `add_list_item`       | Append an item to a checklist                                                  |
| `update_list_items`   | Replace all items in a checklist                                               |
| `sort_list_items`     | Sort checklist items alphabetically                                            |
| `indent_list_item`    | Nest a list item under a parent item                                           |
| `dedent_list_item`    | Remove indentation from a nested list item                                     |
| `list_labels`         | List all labels                                                                |
| `create_label`        | Create a new label                                                             |
| `rename_label`        | Rename an existing label                                                       |
| `delete_label`        | Delete a label (requires `confirm=true`)                                       |
| `add_collaborator`    | Share a note with another user by email                                        |
| `remove_collaborator` | Remove a collaborator from a note                                              |

## Development

```sh
git clone https://github.com/kud/mcp-google-keep.git
cd mcp-google-keep
uv sync
uv run python server.py
```

Run the credential setup flow separately:

```sh
uv run python keep_setup.py
```

The server lives in `server.py` (FastMCP, all 18 tools); credential setup lives in `keep_setup.py`.

📚 **Full documentation → [mcp-google-keep/docs](https://kud.io/projects/mcp-google-keep/docs)**
