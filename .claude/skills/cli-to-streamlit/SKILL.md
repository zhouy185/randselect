---
name: cli-to-streamlit
description: Use when adding a Streamlit front end to an existing
  command-line tool, or converting a CLI into a Streamlit app.
  Covers argparse-to-widget mapping and rerun-safe state. Not for
  building a Streamlit app from scratch, not for CLI-only changes.
---


## Step 1 — Extract pure core
Move all computation into a module with no I/O, no printing, no
Streamlit imports. Test the CLI and confirm that it still runs and
produces a sensible draw before proceeding.

## Step 2 — Map the interface

| CLI | Streamlit |
|---|---|
| positional arg | widget; validate before computing |
| `--flag` | checkbox or selectbox, same default as the CLI |
| `print(result)` | `st.write`, outside the event block |
| file path arg | `st.file_uploader` or path input — pick one |
| `sys.exit(1)` | `st.error(...)` then `st.stop()` |

Defaults must match the CLI's, so both front ends behave the same
out of the box.

## Step 3 — State discipline

Streamlit reruns the whole script on every widget interaction.

- Any `if st.button(...)` block should **mutate state only**.
- Rendering happens outside those blocks, reading from
  `st.session_state` unconditionally.
- Anything the user would be annoyed to lose on a rerun goes in
  session state — including the currently displayed result, not
  just accumulated history.

## Done when

- [ ] `cli.py` still works
- [ ] The Streamlit app has been tested — click the main action,
      then interact with any other widget on the page, and confirm
      the result doesn't disappear.
