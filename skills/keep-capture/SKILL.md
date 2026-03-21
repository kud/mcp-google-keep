---
name: keep-capture
description: "Quickly capture a thought, idea, or note to Google Keep. Accepts freeform text or a title: body format."
---

## Step 1 — Resolve the content

If the user invoked with an argument (e.g. `/keep-capture Buy oat milk`), use that as the note body.

If no argument was given, ask what they would like to capture.

If the text matches `<title>: <body>` (colon separator with a short title before it), split it into title + body. Otherwise use the full text as the body with no title.

## Step 2 — Create the note

Call `create_text_note` with the resolved title (empty string if none) and body.

## Step 3 — Confirm

Reply with a single confirmation line, e.g.:

> ✓ Saved to Google Keep.

If a title was set, include it: > ✓ Saved "Buy oat milk" to Google Keep.
