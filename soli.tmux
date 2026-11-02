#!/usr/bin/env bash
# TPM executes this entry point; it is a shell script, not a tmux config file.
set -euo pipefail
SOLI_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=ports/tmux/scripts/helpers.sh
source "$SOLI_ROOT/ports/tmux/scripts/helpers.sh"
soli_theme="$(get_tmux_option '@soli-theme' 'tekhelet')"
exec "$SOLI_ROOT/ports/tmux/scripts/init.sh" "$soli_theme"
