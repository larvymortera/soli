# Claude Code

All twelve Soli palettes are available as native Claude Code custom themes.
No Python, plugin, or patch to the CLI is needed to use the generated JSON files.
Use a Claude Code version with named custom theme support; check that `/theme`
offers **New custom theme…** before installing.

## Install

From the repository root:

```bash
mkdir -p "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/themes"
cp ports/claude/themes/*.json "${CLAUDE_CONFIG_DIR:-$HOME/.claude}/themes/"
```

Run `/theme` in Claude Code and choose a theme such as **Soli Tekhelet** (night)
or **Soli Manna** (day). Its saved preference uses the filename slug, for example
`custom:soli-tekhelet`. Restart Claude Code once if the themes directory did not
exist when the session started. Subsequent theme file changes reload automatically.
If you edit a generated theme with the picker, keep that local copy separately;
copying generated files again replaces those edits.

See the [official custom theme documentation](https://code.claude.com/docs/en/terminal-config#create-a-custom-theme)
for the file format, picker, and token reference.

## Mapping and limits

Night palettes inherit the `dark` base; day palettes inherit `light`. Overrides
cover primary and secondary text, assistant accents, status colors, input and
permission borders, message surfaces, and selection. `subtle` uses readable
muted text because Claude also uses it for secondary text. Shimmer variants
reuse the same palette colors as their paired tokens.

Syntax highlighting, diff backgrounds, and other unlisted tokens retain the
base preset's behavior and colors. Soli does not change terminal-wide colors.
Set a matching terminal background using the corresponding
[macOS Terminal profile](terminal.md), or the source palette's `ui.bg` color.
Contrast checks assume that intended background; an unrelated terminal background
can make text difficult to read.

## Verify visually

1. Select a night theme with `/theme` using the keyboard, then repeat with a day
   theme and a matching terminal background. Confirm the choice persists after
   restarting Claude Code.
2. Inspect ordinary text, hints, assistant labels, and success/warning/error
   messages. Check input borders and permission dialogs, including keyboard focus.
3. View a code block and an existing diff. Confirm syntax remains legible and
   added/removed lines have visible markers as well as distinct base colors.
4. In fullscreen mode, inspect message backgrounds, hovered messages, sidebar,
   and mouse selection. Check screen reader output with your usual setup.

`python3 tools/validate.py` checks palettes and generated output consistency.
`python3 -m unittest discover -s tests` checks JSON themes, source color reuse,
text contrast on intended backgrounds (4.5:1), and input borders (3:1).
These checks do not establish WCAG conformance. Actual CLI rendering, inherited
colors, focus states, and screen reader behavior still need manual verification.
