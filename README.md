# Soli

Ten coordinated day and night palettes for tmux and Sublime Text. Shared JSON
palettes generate native application files; users do not need Python to install
either port. The tmux port requires Bash and tmux; Sublime schemes target Sublime
Text 3.1 and later. No special fonts are required.

- [tmux installation, options, and preview](docs/tmux.md)
- [Sublime Text installation](docs/sublime.md)
- [Palette format and adding ports](docs/development.md)

## Presets

### Night themes

| `@soli-theme` | Appearance | Background | Accent |
| --- | --- | --- | --- |
| `tekhelet` (default) | Deep royal blue and cyan | `#101629` | `#76d7ed` |
| `shani` | Crimson and dark red | `#211014` | `#f49ba9` |
| `argaman` | Royal purple and magenta | `#15111f` | `#cf9bf0` |
| `horeb` | Slate charcoal and cool gray | `#171b20` | `#b6c5d4` |
| `eden` | Forest green and earthy sage | `#131c16` | `#b4d39a` |

### Day themes

| `@soli-theme` | Appearance | Background | Accent |
| --- | --- | --- | --- |
| `shekinah` | High-contrast light lavender and plum | `#faf7fd` | `#68408d` |
| `manna` | Warm ivory with honey gold | `#fbf7ed` | `#805b17` |
| `mayim` | Pale blue with deep teal | `#f1f8fb` | `#176579` |
| `zayit` | Soft sage with olive green | `#f4f7ee` | `#4d682f` |
| `shachar` | Blush pink with muted rose | `#fcf3f1` | `#994655` |

Each palette includes shared interface colors and syntax colors. In tmux, select
a preset with `@soli-theme`; there is no separate `@soli-mode` setting.

## Project layout

```text
palettes/{day,night}/      Source palettes (JSON)
ports/tmux/scripts/       tmux loader and helpers
ports/tmux/themes/        Generated tmux palettes
ports/sublime/schemes/    Generated Sublime color schemes
tools/                    Generation and validation (Python standard library)
docs/                     Installation and contributor guides
previews/                 Sample source for visual checks
soli.tmux                 Root TPM entry point
```

## Development

Run from the repository root with Python 3.8 or later:

```bash
python3 tools/generate.py
python3 tools/validate.py
python3 tools/generate.py --check
python3 -m unittest discover -s tests
bash -n soli.tmux ports/tmux/scripts/init.sh ports/tmux/scripts/helpers.sh
```

Edit palette sources and adapters, then regenerate and include the generated
files with your changes. Validation checks roles, colors, contrast, loader
coverage, and generated output consistency. It does not establish full WCAG
conformance; application rendering and assistive technology need manual checks.

## License

MIT; see [LICENSE](LICENSE).
