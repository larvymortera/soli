"""Exercise actual shell loaders with a local tmux stand-in; no server changes."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
from generate import load_palettes, generate
from validate import validate


class PortsTest(unittest.TestCase):
    def test_sources_and_outputs(self):
        self.assertEqual(validate(), 10)
        self.assertEqual(generate(check=True), 20)

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
