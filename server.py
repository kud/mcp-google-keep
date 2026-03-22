#!/usr/bin/env python3
import json
import os
from typing import Optional

import gkeepapi
import gkeepapi.node
import keyring
from mcp.server.fastmcp import FastMCP

KEYCHAIN_SERVICE = "mcp-google-keep"


def load_credentials() -> tuple[str, str]:
    email = os.environ.get("GOOGLE_KEEP_EMAIL")
    master_token = os.environ.get("GOOGLE_KEEP_MASTER_TOKEN")
    if email and master_token:
        return email, master_token

    raw = keyring.get_password(KEYCHAIN_SERVICE, "credentials")
    if not raw:
        raise RuntimeError("No credentials found. Run: python setup.py")

    creds = json.loads(raw)
    return creds["email"], creds["masterToken"]


email, master_token = load_credentials()
keep = gkeepapi.Keep()
keep.resume(email, master_token)

mcp = FastMCP("google-keep")


def serialise_label(label: gkeepapi.node.Label) -> dict:
    return {"id": label.id, "name": label.name}


def serialise_note(note: gkeepapi.node.TopLevelNode) -> dict:
    base = {
        "id": note.id,
        "title": note.title,
        "type": "list" if isinstance(note, gkeepapi.node.List) else "text",
        "pinned": note.pinned,
        "archived": note.archived,
        "trashed": note.trashed,
        "color": note.color.name if note.color else "DEFAULT",
        "labels": [label.name for label in note.labels.all()],
        "timestamps": {
            "created": note.timestamps.created.isoformat() if note.timestamps.created else None,
            "updated": note.timestamps.updated.isoformat() if note.timestamps.updated else None,
        },
    }
    base["collaborators"] = list(note.collaborators.all())
    if isinstance(note, gkeepapi.node.List):
        base["items"] = [
            {"id": item.id, "text": item.text, "checked": item.checked, "indented": item.indented}
            for item in note.items
            if not item.deleted
        ]
    else:
        base["text"] = note.text
    return base


# ─── Notes ───

@mcp.tool()
def list_notes(
    query: Optional[str] = None,
    labels: Optional[list[str]] = None,
    colors: Optional[list[str]] = None,
    pinned: Optional[bool] = None,
    archived: Optional[bool] = None,
    trashed: bool = False,
    max_results: Optional[int] = None,
) -> list[dict]:
    """List Google Keep notes. Filter by query text, label names, colors (e.g. RED, BLUE), pinned/archived/trashed state."""
    keep.sync()
    label_objects = (
        [obj for name in labels if (obj := keep.findLabel(name)) is not None]
        if labels
        else None
    )
    color_values = (
        [gkeepapi.node.ColorValue[c] for c in colors]
        if colors
        else None
    )
    notes = list(keep.find(
        query=query,
        labels=label_objects,
        colors=color_values,
        pinned=pinned,
        archived=archived,
        trashed=trashed,
    ))
    if max_results:
        notes = notes[:max_results]
    return [serialise_note(n) for n in notes]


@mcp.tool()
def get_note(id: str) -> dict:
    """Get a single Google Keep note by its ID."""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    return serialise_note(note)


@mcp.tool()
def create_text_note(text: str, title: str = "") -> dict:
    """Create a new text note in Google Keep."""
    note = keep.createNote(title, text)
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def create_list_note(items: list[dict], title: str = "") -> dict:
    """Create a new checklist note in Google Keep. Each item: {text: str, checked?: bool}"""
    note = keep.createList(title, [(i["text"], i.get("checked", False)) for i in items])
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def restore_note(id: str) -> dict:
    """Restore a trashed Google Keep note."""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    note.undelete()
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def delete_note(id: str, confirm: bool = False) -> dict:
    """Move a Google Keep note to trash. Requires confirm=True."""
    if not confirm:
        raise ValueError("Set confirm=True to delete this note")
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    note.delete()
    keep.sync()
    return {"deleted": id}


@mcp.tool()
def update_note(
    id: str,
    title: Optional[str] = None,
    text: Optional[str] = None,
    pinned: Optional[bool] = None,
    archived: Optional[bool] = None,
    color: Optional[str] = None,
    add_labels: Optional[list[str]] = None,
    remove_labels: Optional[list[str]] = None,
) -> dict:
    """Update a Google Keep note. Color values: DEFAULT, RED, ORANGE, YELLOW, GREEN, TEAL, BLUE, CERULEAN, PURPLE, PINK, BROWN, GRAY"""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    if title is not None:
        note.title = title
    if text is not None and isinstance(note, gkeepapi.node.Note):
        note.text = text
    if pinned is not None:
        note.pinned = pinned
    if archived is not None:
        note.archived = archived
    if color is not None:
        note.color = gkeepapi.node.ColorValue[color]
    if add_labels:
        for name in add_labels:
            label = keep.findLabel(name)
            if label:
                note.labels.add(label)
    if remove_labels:
        for name in remove_labels:
            label = keep.findLabel(name)
            if label:
                note.labels.remove(label)
    keep.sync()
    return serialise_note(note)


# ─── List items ───

@mcp.tool()
def add_list_item(id: str, text: str, checked: bool = False) -> dict:
    """Add a single item to an existing Google Keep checklist note."""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    if not isinstance(note, gkeepapi.node.List):
        raise ValueError(f"Note {id} is not a list note")
    note.add(text, checked)
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def sort_list_items(id: str) -> dict:
    """Sort items in a Google Keep checklist note alphabetically."""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    if not isinstance(note, gkeepapi.node.List):
        raise ValueError(f"Note {id} is not a list note")
    note.sort_items()
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def indent_list_item(note_id: str, item_id: str, parent_item_id: str) -> dict:
    """Nest a list item under a parent item in a Google Keep checklist. Use item IDs from list_notes or get_note."""
    keep.sync()
    note = keep.get(note_id)
    if note is None:
        raise ValueError(f"Note not found: {note_id}")
    if not isinstance(note, gkeepapi.node.List):
        raise ValueError(f"Note {note_id} is not a list note")
    item = next((i for i in note.items if i.id == item_id), None)
    parent = next((i for i in note.items if i.id == parent_item_id), None)
    if item is None:
        raise ValueError(f"Item not found: {item_id}")
    if parent is None:
        raise ValueError(f"Parent item not found: {parent_item_id}")
    parent.indent(item)
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def dedent_list_item(note_id: str, item_id: str, parent_item_id: str) -> dict:
    """Remove indentation from a nested list item in a Google Keep checklist. Use item IDs from list_notes or get_note."""
    keep.sync()
    note = keep.get(note_id)
    if note is None:
        raise ValueError(f"Note not found: {note_id}")
    if not isinstance(note, gkeepapi.node.List):
        raise ValueError(f"Note {note_id} is not a list note")
    item = next((i for i in note.items if i.id == item_id), None)
    parent = next((i for i in note.items if i.id == parent_item_id), None)
    if item is None:
        raise ValueError(f"Item not found: {item_id}")
    if parent is None:
        raise ValueError(f"Parent item not found: {parent_item_id}")
    parent.dedent(item)
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def update_list_items(id: str, items: list[dict]) -> dict:
    """Replace all items in a Google Keep checklist note. Each item: {text: str, checked?: bool}"""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    if not isinstance(note, gkeepapi.node.List):
        raise ValueError(f"Note {id} is not a list note")
    for item in note.items:
        if not item.deleted:
            item.delete()
    for item in items:
        note.add(item["text"], item.get("checked", False))
    keep.sync()
    return serialise_note(note)


# ─── Labels ───

@mcp.tool()
def list_labels() -> list[dict]:
    """List all labels in Google Keep."""
    keep.sync()
    return [serialise_label(label) for label in keep.labels()]


@mcp.tool()
def create_label(name: str) -> dict:
    """Create a new label in Google Keep."""
    keep.sync()
    label = keep.createLabel(name)
    keep.sync()
    return serialise_label(label)


@mcp.tool()
def rename_label(name: str, new_name: str) -> dict:
    """Rename an existing label in Google Keep."""
    keep.sync()
    label = keep.findLabel(name)
    if label is None:
        raise ValueError(f"Label not found: {name}")
    label.name = new_name
    keep.sync()
    return serialise_label(label)


# ─── Collaborators ───

@mcp.tool()
def add_collaborator(id: str, email: str) -> dict:
    """Share a Google Keep note with another user by email."""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    note.collaborators.add(email)
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def remove_collaborator(id: str, email: str) -> dict:
    """Remove a collaborator from a Google Keep note by email."""
    keep.sync()
    note = keep.get(id)
    if note is None:
        raise ValueError(f"Note not found: {id}")
    note.collaborators.remove(email)
    keep.sync()
    return serialise_note(note)


@mcp.tool()
def delete_label(name: str, confirm: bool = False) -> dict:
    """Delete a label from Google Keep (removes it from all notes). Requires confirm=True."""
    if not confirm:
        raise ValueError("Set confirm=True to delete this label")
    keep.sync()
    label = keep.findLabel(name)
    if label is None:
        raise ValueError(f"Label not found: {name}")
    keep.deleteLabel(label.id)
    keep.sync()
    return {"deleted": name}


def main():
    mcp.run()


if __name__ == "__main__":
    main()
