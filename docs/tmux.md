# Soli for tmux

## Installation with TPM

With [TPM](https://github.com/tmux-plugins/tpm) already installed, add this to your
main tmux configuration, before TPM's initialization line:

```tmux
set -g @soli-theme 'tekhelet'
set -g @soli-status-position 'bottom'
set -g @plugin 'larvymortera/soli'

# Keep TPM initialization at the bottom of the config.
run-shell '~/.tmux/plugins/tpm/tpm'
```

The plugin repository is `larvymortera/soli`. Keep your existing TPM
initialization if it uses a custom path; do not add a second one.
Reload the main configuration and press your prefix followed by uppercase `I`
to install plugins once the repository is available at that address.

TPM executes `soli.tmux` as a shell script. Do not load it with `source-file`.
For local development, use the isolated preview below.

If you use tmux-continuum, list tmux-soli before continuum in the plugin list so
continuum can append its saving integration after the theme sets `status-right`.
Reloading soli by itself resets that status option; reinitialize continuum after
soli when changing themes in a server using continuum. The preview server below
has no continuum plugin and can be reloaded directly.

## Options

| User option | Default | Values |
| --- | --- | --- |
| `@soli-theme` | `tekhelet` | One of the twelve preset names above |
| `@soli-status-position` | `bottom` | `top` or `bottom` |
| `@soli-color-bg` | Preset background | `#RRGGBB` |
| `@soli-color-surface` | Preset status surface | `#RRGGBB` |
| `@soli-color-panel` | Preset panel | `#RRGGBB` |
| `@soli-color-selection` | Preset selection | `#RRGGBB` |
| `@soli-color-accent` | Preset accent | `#RRGGBB` |
| `@soli-color-fg` | Preset foreground | `#RRGGBB` |
| `@soli-color-muted` | Preset secondary text | `#RRGGBB` |
| `@soli-color-border` | Preset inactive border | `#RRGGBB` |

Set options before TPM initializes the plugin. Empty options use defaults.
User color overrides persist across preset switches until unset. For example:

```tmux
set -g @soli-theme 'argaman'
set -g @soli-status-position 'top'
set -g @soli-color-accent '#b995e8'
```

Use `set -gu @soli-color-accent` and rerun the plugin to restore that preset's
accent. Resolved colors are stored in internal `@soli-bg`, `@soli-surface`,
`@soli-panel`, `@soli-selection`, `@soli-accent`, `@soli-fg`, `@soli-muted`, and
`@soli-border` options; `@soli-divider` is the derived divider style. Configure
colors through `@soli-color-*`, rather than editing these resolved options.

Unknown presets, invalid positions, malformed palettes, and invalid overrides
produce an error before theme settings change. No preset path is evaluated as
shell code, and preset names cannot select files outside `ports/tmux/themes/`.

## Status layout

```text
 0 editor-   1 terminal [Z]   2 notes | 3 logs            devbox  preview  PREFIX
```

- Windows use `index name`, with no colon or active asterisk.
- Active windows have an accent background and bold text; inactive windows have
  no underline. A zoomed active window shows `[Z]`.
- Accent-colored `|` dividers appear only between adjacent inactive windows,
  including when window indexes have gaps. Both sides of the active window stay
  clear, with no divider at the outer edges.
- Hostname, session, and conditional `PREFIX` appear on the right. No status clock.
- Tmux's standard flags remain visible on inactive windows.

The engine styles pane backgrounds/borders, selections, messages, and tmux's
separate built-in clock mode. It does not change keys, mouse behavior, `TERM`,
terminal capabilities, or your terminal's ANSI palette. Applications using their
own colors retain them. Use a true-color terminal for the intended shades.
Narrow terminals may truncate status segments.

## Local preview and switching

From the repository root, create or reuse an isolated preview:

```bash
tmux -L soli-preview has-session -t preview 2>/dev/null || tmux -L soli-preview new-session -d -s preview
tmux -L soli-preview run-shell -c "$PWD" './soli.tmux'
tmux -L soli-preview attach-session -t preview
```

To switch the preview to light mode from another terminal in this directory:

```bash
tmux -L soli-preview set -g @soli-theme 'shekinah'
tmux -L soli-preview run-shell -c "$PWD" './soli.tmux'
tmux -L soli-preview attach-session -t preview
```

Use `argaman` for the purple/magenta preset, or another name from the matrix.
`run-shell` applies the theme but does not attach; `attach-session` opens it.
The plugin targets the tmux server that invokes it, including named preview
servers. It does not create sessions, install software, or modify files in HOME.

## Verification

```bash
bash -n soli.tmux ports/tmux/scripts/init.sh ports/tmux/scripts/helpers.sh
```

Run these commands from the repository root. Use the isolated preview above to
check each palette, active windows, zoom indicators, and dividers.
