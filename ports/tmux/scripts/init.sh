#!/usr/bin/env bash
# Read a preset as data, validate all colors, then apply the shared layout.
set -euo pipefail
SOLI_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
# shellcheck source=helpers.sh
source "$SOLI_ROOT/scripts/helpers.sh"
soli_theme="${1:-$(get_tmux_option '@soli-theme' 'tekhelet')}"
case "$soli_theme" in
  tekhelet|shani|argaman|shekinah|horeb|eden|manna|mayim|zayit|shachar|yom|layla) ;;
  *) soli_error "Unknown theme '$soli_theme'. Choose tekhelet, shani, argaman, shekinah, horeb, eden, manna, mayim, zayit, shachar, yom, or layla."; exit 1 ;;
esac
soli_position="$(get_tmux_option '@soli-status-position' 'bottom')"
case "$soli_position" in
  top|bottom) ;;
  *) soli_error "Invalid status position '$soli_position'; use top or bottom."; exit 1 ;;
esac
preset="$SOLI_ROOT/themes/$soli_theme.tmuxtheme"
[ -r "$preset" ] || { soli_error "Cannot read preset: $preset"; exit 1; }
seen=' '
while IFS='=' read -r key value || [ -n "$key" ]; do
  case "$key" in ''|'#'*) continue ;; esac
  case "$key" in
    bg|surface|panel|selection|accent|fg|muted|border) ;;
    *) soli_error "Unknown palette role '$key' in $preset"; exit 1 ;;
  esac
  case "$seen" in *" $key "*) soli_error "Duplicate palette role '$key' in $preset"; exit 1 ;; esac
  soli_valid_color "$value" || { soli_error "Invalid color for '$key' in $preset"; exit 1; }
  printf -v "soli_$key" '%s' "$value"
  seen="$seen$key "
done < "$preset"
for key in bg surface panel selection accent fg muted border; do
  case "$seen" in *" $key "*) ;; *) soli_error "Missing palette role '$key' in $preset"; exit 1 ;; esac
  # The variable name is constructed only from the fixed role list above.
  variable="soli_$key"
  value="$(get_tmux_option "@soli-color-$key" "${!variable}")"
  soli_valid_color "$value" || { soli_error "Invalid @soli-color-$key; use #RRGGBB."; exit 1; }
  printf -v "$variable" '%s' "$value"
done

# Values interpolated below have been validated as colors or fixed enum values.
# tmux parses this configuration; preset files are never evaluated as shell code.
tmux source-file - <<CONFIG
set -g @soli-bg '$soli_bg'
set -g @soli-surface '$soli_surface'
set -g @soli-panel '$soli_panel'
set -g @soli-selection '$soli_selection'
set -g @soli-accent '$soli_accent'
set -g @soli-fg '$soli_fg'
set -g @soli-muted '$soli_muted'
set -g @soli-border '$soli_border'
set -g status-position '$soli_position'
CONFIG

tmux source-file - <<'CONFIG'
set -g status on
set -g status-justify left
set -gF status-style 'fg=#{@soli-fg},bg=#{@soli-surface}'
set -g status-left-length 0
set -g status-right-length 48
set -g status-left ''
set -gF status-right-style 'fg=#{@soli-fg},bg=#{@soli-panel}'
set -g status-right ' #h #[fg=#{@soli-bg},bg=#{@soli-accent},bold] #S #[default]#{?client_prefix, PREFIX ,}'
# The first session_stack index is active. Prefix dividers before it and suffix
# them after it, avoiding both active neighbors and outer edges, even with gaps.
set -gF @soli-divider '#[fg=#{@soli-accent},bg=#{@soli-surface},nobold,nounderscore]|#[default]'
setw -g window-status-separator ''
setw -gF window-status-style 'fg=#{@soli-muted},bg=#{@soli-surface},nounderscore'
setw -g window-status-format '#{?#{&&:#{e|<:#{window_index},#{s/,.*//:session_stack}},#{!=:#{window_start_flag},1}},#{E:@soli-divider},} #I #W#F #{?#{&&:#{e|>:#{window_index},#{s/,.*//:session_stack}},#{!=:#{window_end_flag},1}},#{E:@soli-divider},}'
setw -gF window-status-current-style 'fg=#{@soli-bg},bg=#{@soli-accent},bold'
setw -g window-status-current-format ' #I #W#{?window_zoomed_flag, [Z],} '
setw -gF window-status-last-style 'fg=#{@soli-muted},bg=#{@soli-surface},nounderscore'
setw -gF window-status-activity-style 'fg=#{@soli-fg},bg=#{@soli-panel},bold'
setw -gF window-status-bell-style 'fg=#{@soli-bg},bg=#{@soli-accent},bold'
setw -gF window-style 'fg=#{@soli-fg},bg=#{@soli-bg}'
setw -gF window-active-style 'fg=#{@soli-fg},bg=#{@soli-bg}'
setw -gF pane-border-style 'fg=#{@soli-border},bg=#{@soli-bg}'
setw -gF pane-active-border-style 'fg=#{@soli-accent},bg=#{@soli-bg}'
set -gF display-panes-colour '#{@soli-muted}'
set -gF display-panes-active-colour '#{@soli-accent}'
setw -gF mode-style 'fg=#{@soli-fg},bg=#{@soli-selection}'
set -gF message-style 'fg=#{@soli-fg},bg=#{@soli-panel}'
set -gF message-command-style 'fg=#{@soli-bg},bg=#{@soli-accent},bold'
setw -gF clock-mode-colour '#{@soli-accent}'
CONFIG
