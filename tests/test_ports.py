"""Exercise actual shell loaders with a local tmux stand-in; no server changes."""
import json
import os
import plistlib
import shutil
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from generate import load_palettes, generate, ANSI, ANSI_ROLES
from validate import validate, contrast


class PortsTest(unittest.TestCase):
    def test_sources_and_outputs(self):
        self.assertEqual(validate(), 10)
        self.assertEqual(generate(check=True), 30)

    def test_terminal_profiles(self):
        def decode(blob):
            archive = plistlib.loads(blob)
            self.assertEqual(archive['$archiver'], 'NSKeyedArchiver')
            color = archive['$objects'][archive['$top']['root'].data]
            self.assertEqual(color['NSColorSpace'], 1)
            self.assertEqual(archive['$objects'][color['$class'].data]['$classname'], 'NSColor')
            channels = color['NSRGB'].rstrip(b'\0').decode().split()
            self.assertEqual(float(channels[3]), 1)
            return '#' + ''.join(f'{round(float(c) * 255):02x}' for c in channels[:3])

        for palette in load_palettes():
            with self.subTest(theme=palette['name']):
                path = ROOT / 'ports/terminal/profiles' / f'Soli {palette["name"].title()}.terminal'
                profile = plistlib.loads(path.read_bytes())
                self.assertEqual(profile['name'], 'Soli ' + palette['name'].title())
                self.assertEqual(profile['type'], 'Window Settings')
                for key, role in {'BackgroundColor': 'bg', 'TextColor': 'fg',
                                  'TextBoldColor': 'fg', 'CursorColor': 'accent',
                                  'SelectionColor': 'selection'}.items():
                    self.assertEqual(decode(profile[key]), palette['ui'][role])
                for name, (section, role) in zip(ANSI, ANSI_ROLES):
                    self.assertEqual(decode(profile['ANSI' + name + 'Color']), palette[section][role])
                    bright = palette['ui']['muted'] if name == 'Black' else palette[section][role]
                    self.assertEqual(decode(profile['ANSIBright' + name + 'Color']), bright)
                for name in ANSI[1:]:
                    self.assertGreaterEqual(contrast(decode(profile['ANSI' + name + 'Color']),
                                                     palette['ui']['bg']), 4.5)
                self.assertNotIn('CommandString', profile)

    @unittest.skipUnless(shutil.which('zsh'), 'zsh is not installed')
    def test_zsh_prompt(self):
        with tempfile.TemporaryDirectory(prefix='soli zsh path ') as folder:
            script = Path(folder) / 'Soli prompt.zsh'
            script.symlink_to(ROOT / 'ports/zsh/soli.zsh')
            commands = r'''
PROMPT='original> '
RPROMPT='right'
source "$1"
[[ $PROMPT == 'original> ' ]] || exit 1
soli prompt on || exit 2
[[ $PROMPT == *'%F{cyan}'* ]] || exit 3
true
print -P -- "$PROMPT"
false
print -P -- "$PROMPT"
soli prompt on
source "$1"
soli prompt on
soli prompt off
[[ $PROMPT == 'original> ' && $RPROMPT == right ]] || exit 4
soli prompt off
soli theme ../bad && exit 5
exit 0
'''
            result = subprocess.run(['zsh', '-f', '-i', '-c', commands, 'soli-test', str(script)],
                                    capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            lines = result.stdout.splitlines()
            self.assertNotIn('[exit', lines[0])
            self.assertIn('[exit 1]', lines[1])
            result = subprocess.run(['zsh', '-f', '-c',
                                     'source "$1"; (( ${+functions[soli]} == 0 ))',
                                     'soli-test', str(script)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout, '')

    def test_entry_point_and_validation(self):
        with tempfile.TemporaryDirectory(prefix='soli path with spaces ') as folder:
            folder = Path(folder)
            # Exercise resolving the plugin through a path containing spaces.
            plugin = folder / 'Soli plugin'
            plugin.symlink_to(ROOT, target_is_directory=True)
            capture = folder / 'capture'
            mock = folder / 'tmux'
            mock.write_text('''#!/bin/bash
case "$1" in
  show-option)
    case "$3" in
      @soli-theme) printf '%s' "${TEST_THEME:-}" ;;
      @soli-color-accent) printf '%s' "${TEST_ACCENT:-}" ;;
    esac ;;
  source-file) cat >> "$TEST_CAPTURE" ;;
  *) exit 1 ;;
esac
''')
            mock.chmod(0o755)
            env = dict(os.environ, PATH=str(folder) + os.pathsep + os.environ['PATH'],
                       TEST_CAPTURE=str(capture), TEST_THEME='', TEST_ACCENT='')
            for palette in load_palettes():
                capture.write_text('')
                env['TEST_THEME'] = palette['name']
                subprocess.run(['bash', str(plugin / 'soli.tmux')], cwd=folder, env=env, check=True)
                output = capture.read_text()
                for role, color in palette['ui'].items():
                    self.assertIn(f"set -g @soli-{role} '{color}'", output)
                scheme = json.loads((ROOT / 'ports/sublime/schemes' /
                                    f'Soli {palette["name"].title()}.sublime-color-scheme').read_text())
                self.assertEqual(scheme['variables']['bg'], palette['ui']['bg'])
                self.assertEqual(scheme['globals']['selection_foreground'], 'var(fg)')
            env['TEST_THEME'] = 'manna'
            env['TEST_ACCENT'] = '#123456'
            capture.write_text('')
            subprocess.run(['bash', str(plugin / 'soli.tmux')], env=env, check=True)
            self.assertIn("set -g @soli-accent '#123456'", capture.read_text())
            for theme, accent in [('../manna', ''), ('unknown', ''), ('manna', 'invalid')]:
                capture.write_text('')
                env.update(TEST_THEME=theme, TEST_ACCENT=accent)
                result = subprocess.run(['bash', str(plugin / 'soli.tmux')], env=env, capture_output=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(capture.read_text(), '')


if __name__ == '__main__':
    unittest.main()
