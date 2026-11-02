# macOS Terminal and plain zsh

## Install a profile on your Mac

No Python, prompt framework, or special font is required.

1. In Terminal, open **Terminal > Settings > Profiles**.
2. Use the action menu to **Import** a file from `ports/terminal/profiles/`,
   for example `Soli Tekhelet.terminal`.
3. Open a new window using that profile via **Shell > New Window**.
   Optionally make the profile the default in Settings for future windows.

All ten palettes have profiles. Selecting a different profile changes the
terminal palette; the zsh prompt below follows its ANSI colors automatically.
There is no shell command that imports or switches your macOS profile.
Profiles contain colors, not startup commands or a bundled font.

Apple's [profile import instructions](https://support.apple.com/guide/terminal/trml4299c696/mac)
cover importing and exporting `.terminal` files.

## Enable the optional plain-zsh prompt

Add these lines to `~/.zshrc`, replacing the example path with your checkout:

```zsh
source "/path/to/soli/ports/zsh/soli.zsh"
soli prompt on
```

Start a new zsh session. The prompt shows the current directory and the usual
`%` marker (`#` for root). A failed command adds a red `[exit N]` label with its
exit code. Directory text uses ANSI cyan, mapped to the palette's accent.
Sourcing the script alone leaves your prompt unchanged; repeated enabling is
safe. Use `soli prompt off` to restore the prompt saved when first enabled.
The script adds no hooks, launches no subprocesses, and does nothing in a
noninteractive shell. Load it after other prompt configuration.

## Remote shells, VMs, and containers

When you open a remote shell or an interactive shell in a VM or container within
an existing Terminal window, the active macOS Terminal profile stays in effect.
The local Terminal app continues to render the output using its configured colors.

Each environment may have its own shell and startup files. To use the Soli prompt,
ensure zsh is installed there, then add the source/enable lines above to that
user's `~/.zshrc`. Use a checkout path accessible in that environment, or copy the
standalone `soli.zsh` file there. Do not assume your Mac's paths or configuration
are available. The `.terminal` profile is installed only in macOS Terminal.

Applications using the ANSI 16 colors follow the profile. Programs choosing
256-color or explicit RGB colors, editor themes, and tmux styles may use other
colors and need their own configuration. Avoid overriding `TERM` to claim
capabilities your terminal does not support.

## Color mapping and limitations

ANSI black maps to `ui.bg`; red/green/yellow/blue/magenta map to
`syntax.error/string/warning/type/keyword`; cyan maps to `ui.accent`; white maps
to `ui.fg`. Bright variants reuse those colors, except bright black maps to
`ui.muted`. Light palettes therefore give black/white semantic background/text
roles rather than literal black/white hues. Bold text uses the primary foreground.

Source validation checks text colors against the palette background. ANSI black
is a background role and is not readable as text on that same background.
Arbitrary applications can select combinations with insufficient contrast.
Profile import, selection rendering, VoiceOver, and visual appearance need checking
in macOS Terminal; automated checks do not establish WCAG conformance.

## Manual verification

1. Import a night profile and a day profile; check their background, text,
   cursor, selection, and ANSI colors in actual Terminal windows.
2. Enable the prompt; run `true`, then `false`. Only the latter should display
   `[exit 1]`. Try a long path, resize the window, and edit a wrapped command.
3. Run `soli prompt on` twice, then `soli prompt off`: the original prompt
   and right prompt should return.
4. Open a remote shell or a shell in a VM or container, enable the prompt there,
   and repeat `false`. The profile colors should match the local shell in the
   same Terminal window. Check legibility with your chosen font/size
   and VoiceOver; failure must remain understandable without color.
