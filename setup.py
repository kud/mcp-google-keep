#!/usr/bin/env python3
"""Obtain a Google Keep master token and save everything to the macOS Keychain."""
import json
import logging
import sys
import webbrowser

import gpsoauth
import gkeepapi
import keyring
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.text import Text

logging.getLogger("gkeepapi").setLevel(logging.ERROR)

KEYCHAIN_SERVICE = "mcp-google-keep"
console = Console()

console.print(Panel.fit(
    "[bold white]Google Keep MCP[/] — Setup",
    border_style="bright_blue",
    padding=(0, 4),
))
console.print()

existing = keyring.get_password(KEYCHAIN_SERVICE, "credentials")
if existing:
    existing_email = json.loads(existing).get("email", "?")
    console.print(f"[yellow]Existing credentials found for:[/] [bold]{existing_email}[/]")
    if not Confirm.ask("Overwrite?", default=False):
        console.print("[dim]Aborted.[/]")
        sys.exit(0)
    console.print()

email = Prompt.ask("[bold]Google account email[/]")
console.print()

console.print("[bold]1.[/] Sign in to your Google account")
console.print("[bold]2.[/] The page will show an infinite loader — [bold]that's normal[/], ignore it")
console.print("[bold]3.[/] Open DevTools [dim](F12)[/] → [bold]Application[/] → [bold]Cookies[/] → [bold]accounts.google.com[/]")
console.print("[bold]4.[/] Find [bold]oauth_token[/] → double-click its value → copy it\n")
Prompt.ask("Press Enter to open the browser", default="", show_default=False)
webbrowser.open("https://accounts.google.com/EmbeddedSetup")
console.print()

oauth_token = Prompt.ask("[bold]Paste oauth_token[/]")
console.print()

with console.status("[dim]Exchanging for master token…[/]"):
    result = gpsoauth.exchange_token(email, oauth_token, "0000000000000000")
    master_token = result.get("Token")

if not master_token:
    console.print(f"[red]✗[/] Failed to get master token: {result}")
    console.print("[dim]The oauth_token may have expired — try again quickly after copying.[/]")
    sys.exit(1)

console.print("[green]✓[/] Master token obtained")

with console.status("[dim]Verifying with Google Keep…[/]"):
    keep = gkeepapi.Keep()
    try:
        keep.authenticate(email, master_token)
        keep.sync()
    except Exception as e:
        console.print(f"[red]✗[/] Authentication failed: {e}")
        sys.exit(1)

console.print("[green]✓[/] Google Keep connection verified")

keyring.set_password(KEYCHAIN_SERVICE, "credentials", json.dumps({"email": email, "masterToken": master_token}))
console.print("[green]✓[/] Saved to macOS Keychain")
console.print()

console.print(Panel.fit(
    Text("All done! You can now run the MCP server.", justify="center"),
    border_style="green",
    padding=(0, 2),
))
