#!/usr/bin/env bash
# Shared functions. Callers provide strict shell mode.
get_tmux_option() {
  local value
  value="$(tmux show-option -gqv "$1")" || return
  if [ -n "$value" ]; then printf '%s\n' "$value"; else printf '%s\n' "${2:-}"; fi
}

soli_error() {
  printf 'tmux-soli: %s\n' "$*" >&2
  return 1
}

soli_valid_color() {
  [[ "$1" =~ ^#[[:xdigit:]]{6}$ ]]
}
