#!/usr/bin/env python3
"""Validate palette structure, contrast, loader coverage, and generated files."""
import json
import re
from pathlib import Path
from generate import ROOT, UI, SCOPES, generate

SYNTAX = set(SCOPES) | {'warning'}


def luminance(color):
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    channels = [c / 12.92 if c <= .04045 else ((c + .055) / 1.055) ** 2.4 for c in channels]
    return sum(c * weight for c, weight in zip(channels, (.2126, .7152, .0722)))


def contrast(a, b):
    low, high = sorted((luminance(a), luminance(b)))
    return (high + .05) / (low + .05)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate key: {key}')
        result[key] = value
    return result


def validate():
    names = set()
    paths = sorted((ROOT / 'palettes').glob('*/*.json'))
    if not paths:
        raise ValueError('No palettes found')
    for path in paths:
        data = json.loads(path.read_text(), object_pairs_hook=unique_object)
        name = data.get('name')
        if not isinstance(name, str) or not re.fullmatch('[a-z][a-z0-9-]*', name):
            raise ValueError(f'{path}: invalid name')
        if name != path.stem or name in names or data.get('mode') != path.parent.name or data['mode'] not in ('day', 'night'):
            raise ValueError(f'{path}: inconsistent name/mode or duplicate palette')
        names.add(name)
        if set(data) != {'name', 'mode', 'ui', 'syntax'}:
            raise ValueError(f'{name}: unexpected palette fields')
        for section, roles in [('ui', set(UI)), ('syntax', SYNTAX)]:
            colors = data[section]
            if not isinstance(colors, dict) or set(colors) != roles:
                raise ValueError(f'{name}: invalid {section} roles')
            if any(not isinstance(c, str) or not re.fullmatch('#[0-9a-fA-F]{6}', c) for c in colors.values()):
                raise ValueError(f'{name}: invalid {section} color')
        ui = data['ui']
        pairs = [(ui['fg'], ui[b], 4.5, f'fg/{b}') for b in ('bg', 'surface', 'panel', 'selection')]
        pairs += [(ui['muted'], ui['surface'], 4.5, 'muted/surface'),
                  (ui['accent'], ui['bg'], 4.5, 'accent/bg'),
                  (ui['accent'], ui['surface'], 4.5, 'accent/surface'),
                  (ui['border'], ui['bg'], 3, 'border/bg')]
        pairs += [(color, ui['bg'], 4.5, f'{role}/bg') for role, color in data['syntax'].items()]
        for a, b, minimum, label in pairs:
            value = contrast(a, b)
            if value < minimum:
                raise ValueError(f'{name}: {label} contrast {value:.3f}:1 is below {minimum}:1')
    loader = (ROOT / 'ports/tmux/scripts/init.sh').read_text()
    match = re.search(r'case "\$soli_theme" in\n  ([a-z0-9|\-]+)\)', loader)
    if not match or set(match[1].split('|')) != names:
        raise ValueError('tmux loader allowlist does not match palettes')
    return len(paths)


if __name__ == '__main__':
    try:
        count = validate()
        outputs = generate(check=True)
        print(f'{count} palettes passed structure and contrast checks; {outputs} generated files match.')
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit(str(error))
