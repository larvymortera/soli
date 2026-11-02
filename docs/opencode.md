# OpenCode

Soli provides ten native JSON themes for the OpenCode terminal UI. Copy the
generated files directly; Python is not required at runtime. Use a terminal
with truecolor support for accurate colors.

## Install

From the repository root, install all presets for your user:

```bash
mkdir -p "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/themes"
cp ports/opencode/themes/*.json "${XDG_CONFIG_HOME:-$HOME/.config}/opencode/themes/"
```

For a project-only installation, copy them into `.opencode/themes/` instead.
Project themes take precedence over user themes with the same filename.

Restart OpenCode and run `/theme`, then select `soli-tekhelet` for a night preset
or `soli-manna` for a day preset. Names come from filenames. Alternatively,
merge this setting into `tui.json`, preserving your other settings:

```json
{
  "$schema": "https://opencode.ai/tui.json",
  "theme": "soli-tekhelet"
}
```

These instructions target the OpenCode 1.x theme format. See the
[official theme documentation](https://docs.opencode.ai/docs/themes/) for loading
locations and supported color formats.

## Mapping and limits

Each file supplies fixed hex colors, so a preset keeps its appearance in either
light or dark mode. Choose a day preset explicitly for a light appearance.
UI, Markdown, syntax, status, and diff colors come from the shared palettes.
Panel and element surfaces share `ui.surface` so secondary text stays readable.
Selected list text uses `ui.bg` against the accent color.

Diff backgrounds share `ui.bg`. Added and removed text uses string and error
colors; word highlights use those same foreground hues. This avoids inventing
new background colors. Use the visible +/- markers to distinguish changes as
well as their colors. The theme does not alter terminal-wide colors or keybindings.

## Verify visually

1. Run `/theme` and select a night preset with the keyboard. Inspect the focused
   row and selected text, then repeat with a day preset. Restart OpenCode to
   confirm the selection persists.
2. View a Markdown response with headings, links, quotes, lists, and a fenced
   code block. Use `previews/sample.py` as sample syntax content.
3. Inspect an existing diff with added and removed lines, line numbers, and
   word changes. Check text, markers, and highlights remain legible.
4. Check input borders, dialogs, sidebars, muted hints, and status messages.
   Test with your usual screen reader and terminal font size.

Run `python3 tools/validate.py`, `python3 tools/generate.py --check`, and
`python3 -m unittest discover -s tests` to check generated consistency, JSON
structure, source color reuse, text contrast (4.5:1) on intended backgrounds,
and boundaries (3:1) against the main background. This does not establish WCAG
conformance. Actual terminal rendering, focus, and screen reader behavior need
manual checks. The published schema URL currently returns HTTP 404, so these
checks do not include validation against a downloaded official JSON schema.
