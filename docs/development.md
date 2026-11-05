# Developing Soli

## Palette sources

`palettes/day/*.json` and `palettes/night/*.json` are the source of truth. Each
file has a lowercase `name` matching its filename, a `mode` matching its parent
folder, and two color maps. Every color is a six-digit hex value.

- `ui`: `bg`, `surface`, `panel`, `selection`, `accent`, `fg`, `muted`, `border`.
- `syntax`: `comment`, `keyword`, `string`, `number`, `function`, `type`, `error`,
  `warning`.

UI roles represent background, status surface, elevated panel, selected text
background, accent, primary text, secondary text, and inactive boundary.
Syntax and diagnostic colors are chosen per palette. They may share values with
UI roles, but adapters must not invent a separate palette.

## Generate and validate

Run `python3 tools/generate.py` after editing source palettes or mappings in
`tools/generate.py`. Commit generated native files alongside source changes.
Consumers use these native files directly; generation is a contributor step.
`python3 tools/generate.py --check` checks without writing. Unexpected generated
files are reported rather than automatically deleted.

`python3 tools/validate.py` checks schema, duplicate keys, names, required roles,
hex colors, tmux allowlist coverage, and generated-file consistency. It checks
4.5:1 for primary text on all text surfaces, secondary text on the status surface,
accent text on the background/status surface, and syntax colors on the editor
background; inactive borders require 3:1 against the pane background. Selected
Sublime text uses the primary foreground for predictable contrast.

The root `soli.tmux` remains the TPM entry point. Its loader reads only the eight
UI roles from `ports/tmux/themes/`; the option names and status layout are retained.
Python is never called by the tmux runtime.

## Add a palette or port

For a palette, add its JSON source under the appropriate mode and register its
name in the allowlist and error message in `ports/tmux/scripts/init.sh`. Update
the README list, regenerate, and validate. Check it in each actual application.

For a port, add an output adapter to `tools/generate.py`, using semantic roles
from the palette. Put its native files in `ports/<application>/`, extend generated
file checks and tests, and add installation instructions in `docs/`. Keep
application-specific behavior and scope mappings in the adapter. Avoid runtime
build dependencies for end users.

## Terminal and zsh port

`tools/generate.py` also generates twelve `.terminal` profiles using stdlib
`plistlib`, with embedded keyed NSColor archives. ANSI mapping lives in
`ANSI_ROLES`; no separate palette or runtime Python is required. See
[Terminal documentation](terminal.md) for the mapping and manual checks.
The standalone `ports/zsh/soli.zsh` prompt uses named ANSI colors and is maintained
directly. Test runtime behavior with zsh when available.

## iTerm2 port

The generator writes twelve XML `.itermcolors` presets to `ports/iterm2/presets/`
using stdlib `plistlib`. Each color uses normalized sRGB components and full
alpha. ANSI colors reuse `ANSI_ROLES`, including muted text for bright black.
Tests cover native plist structure, palette round trips, text/selection/cursor
contrast, and missing/stale/unexpected outputs. See [iTerm2 installation](iterm2.md)
for usage and manual checks.

## Codex CLI port

The generator writes twelve XML TextMate `.tmTheme` files to `ports/codex/themes/`
using stdlib `plistlib`. Global settings map shared UI roles, syntax rules reuse
`SCOPES`, and inserted/deleted/changed markup uses string/error/warning colors.
Generated-file checks cover missing, stale, and unexpected Codex themes. See
[Codex installation](codex.md) for usage, rendering limits, and manual checks.

## Claude Code port

The generator writes twelve native JSON themes to `ports/claude/themes/`. Each
selects a light or dark base from the source mode and maps documented interface
tokens to shared UI and diagnostic roles. Syntax and diff colors fall through to
the base preset. Shimmer tokens reuse their corresponding base colors; no new
shades are invented. `subtle` uses muted text because it also renders text.
Tests cover JSON structure, intended contrast pairs, and stale/missing/unexpected
outputs. See [Claude Code installation](claude.md) for scope and manual checks.

## OpenCode port

The generator writes twelve native JSON themes to `ports/opencode/themes/` with
literal hex values. Each file is a fixed preset in either appearance mode.
Interface, Markdown, syntax, and diff mappings live in `opencode_theme`.
Panel and element backgrounds use `surface` to keep secondary text readable.
Diff backgrounds use `bg`, preserving source colors and foreground contrast;
added/removed foreground hues and +/- markers distinguish changes. Tests cover
intended contrast pairs and missing/stale/unexpected outputs. See
[OpenCode installation](opencode.md) for usage and manual checks.
