---
name: keep-todo
description: "Find a Google Keep checklist by name and manage it — view items, check things off, and add new ones."
---

## Step 1 — Find the list

If the user provided a list name (e.g. `/keep-todo Shopping`), call `list_notes` with that as the query.

If no argument was given, ask which list they want to work with.

If multiple lists match, show their titles and ask the user to pick one.

## Step 2 — Display the list

Show the list title and all non-deleted items, unchecked first:

```
📋 Shopping

☐ Oat milk
☐ Bread
☑ Coffee
```

## Step 3 — Act on the list

Ask what the user wants to do:

- **Add item** — call `add_list_item` with the item text
- **Check off item** — call `update_list_items` with that item set to `checked: true`, all others unchanged
- **Uncheck item** — call `update_list_items` with that item set to `checked: false`
- **Clear checked** — call `update_list_items` keeping only items where `checked: false`
- **Done** — end the skill

After each mutating action, show the updated list using the same format as Step 2.
