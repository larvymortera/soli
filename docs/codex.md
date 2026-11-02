# Codex CLI

Soli provides all ten palettes as native TextMate `.tmTheme` files for Codex CLI.
Use a Codex CLI version with `/theme` and custom TextMate theme support.
Python is not required to install or use the themes.

## Install

From the repository root, copy the themes into your Codex home:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/themes"
cp ports/codex/themes/*.tmTheme "${CODEX_HOME:-$HOME/.codex}/themes/"
```

Start a new Codex CLI session, run `/theme`, and select a Soli theme. Filenames
use identifiers such as `soli-tekhelet` and `soli-manna`; theme metadata includes
display names such as `Soli Tekhelet`. The picker saves the selection to
`tui.theme` in your Codex configuration.

See the [official CLI customization guide](https://learn.chatgpt.com/docs/cli-customization)
for custom theme loading and the theme picker.

## Scope and colors

Codex uses these themes for syntax highlighting in fenced Markdown code blocks
and file diffs. The files define foreground/background defaults, caret,
selection, line highlight, and gutter colors where the consumer supports them.
Codex controls which TextMate settings it renders; this port does not set the
terminal palette or theme the entire Codex interface. For a matching terminal
background, use the corresponding [macOS Terminal profile](terminal.md) or set
your terminal colors from the palette. These files target the CLI; the desktop
app uses a different theme format.

Syntax colors come directly from shared palettes. Inserted, deleted, and changed
markup maps to string, error, and warning respectively. Diff indicators remain
under Codex's control; the port adds no new interactions or animations.

## Verify visually

1. Select a night theme in `/theme`, then view a fenced Python code block using
   `previews/sample.py` as sample content. Check comments, strings, numbers,
   functions, types, keywords, and ordinary text.
2. View a diff with added and removed lines. Check that text and diff indicators
   are legible and additions/removals can be distinguished by their markers.
3. Repeat with a day theme and a matching light terminal background.
4. Navigate the picker with the keyboard and confirm the selection persists
   after restarting Codex. Check text selection and your usual screen reader.

`python3 tools/validate.py` checks source contrast and generated-file consistency.
`python3 -m unittest discover -s tests` also parses every generated TextMate plist
and checks syntax contrast of at least 4.5:1 against its intended background.
Actual terminal rendering, diff backgrounds, and assistive technology require
manual checks; these automated checks do not establish WCAG conformance.
