# Soli for iTerm2

All ten palettes are available as native color presets in `ports/iterm2/presets/`.
No Python, special font, or prompt framework is required to install them.

## Install

1. Open **iTerm2 > Settings > Profiles**, select your profile, and open **Colors**.
2. Choose **Color Presets > Import** and select a `.itermcolors` file, such as
   `ports/iterm2/presets/Soli Argaman.itermcolors`.
3. Open **Color Presets** again and select **Soli Argaman** to apply it.

If your profile uses separate colors for light and dark mode, select the desired
mode before applying the preset. Import and select a day preset for light mode
and a night preset for dark mode as desired.

These are color presets, not full profiles: they contain foreground, background,
bold, cursor, selection, and ANSI colors. Your font, keys, and startup command
remain profile settings. See the official [iTerm2 color settings documentation](https://iterm2.com/documentation-preferences-profiles-colors.html).

## Plain zsh and tmux

The existing [optional zsh prompt](terminal.md#enable-the-optional-plain-zsh-prompt)
works in iTerm2 too; its named ANSI colors follow the selected preset.

Install the [tmux port](tmux.md) separately and choose the same preset name, for
example `set -g @soli-theme 'argaman'`.
[iTerm2 supports 24-bit color](https://iterm2.com/documentation-highlights.html#high-color-modes).
Inside a normal tmux session, check whether tmux recognizes RGB support:

```sh
tmux display-message -p '#{client_termname} #{client_termfeatures}'
```

The features should include `RGB`. If they do not, follow the
[tmux RGB configuration guidance](https://github.com/tmux/tmux/wiki/FAQ#how-do-i-use-rgb-colour)
for your tmux version. Only advertise RGB for terminals that support it; a shared
`xterm-256color` name alone does not prove support. Without RGB, explicit tmux
colors can be approximated and dark purple backgrounds may appear gray.

## Mapping and limitations

ANSI black uses `ui.bg`; red, green, yellow, blue, and magenta use
`syntax.error`, `string`, `warning`, `type`, and `keyword`; cyan uses `ui.accent`;
white uses `ui.fg`. Bright variants reuse the same colors except bright black,
which uses `ui.muted`. Bold and selected text use `ui.fg`; the cursor uses
`ui.accent` with `ui.bg` text.

ANSI black is a background role and is not readable as text on the matching
background. Applications can choose other combinations with insufficient
contrast, or use their own RGB colors. Profile settings such as minimum contrast,
cursor adjustments, transparency, and custom selected-text behavior can affect
rendering. Enable the custom selected-text color if you want the preset's selected
foreground to be used.

## Manual verification

1. Import and select **Soli Argaman** and **Soli Shekinah** in turn. Check text,
   background, cursor text, selected text, and ANSI colors in each.
2. Enable the zsh prompt and run `true`, then `false`; only the latter should show
   the textual `[exit 1]` indicator.
3. Attach to tmux using the matching preset. Check `RGB` in the command above,
   then compare pane backgrounds, status text, active windows, and dividers.
4. Check selection legibility, larger font sizes, and VoiceOver in iTerm2.
   Automated palette contrast checks do not establish WCAG conformance or verify
   application rendering and assistive technology behavior.
