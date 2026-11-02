# Soli plain-zsh prompt. Source this file; enable with: soli prompt on
# ANSI names follow the active terminal profile, including in remote shells.
[[ -o interactive ]] || return 0

soli() {
  emulate -L zsh
  if (( $# != 2 )) || [[ $1 != prompt || ( $2 != on && $2 != off ) ]]; then
    print -u2 -r -- 'Usage: soli prompt on|off'
    return 1
  fi
  if [[ $2 == on ]]; then
    if (( ! ${+_soli_saved_prompt} )); then
      typeset -g _soli_saved_prompt=$PROMPT _soli_saved_rprompt=$RPROMPT
    fi
    # Expand only zsh's prompt escapes, with no substitutions or external commands.
    # The literal failure label and exit code supplement the red color.
    PROMPT='%(?..%F{red}[exit %?]%f )%F{cyan}%~%f %# '
    RPROMPT=''
  elif (( ${+_soli_saved_prompt} )); then
    PROMPT=$_soli_saved_prompt
    RPROMPT=$_soli_saved_rprompt
    unset _soli_saved_prompt _soli_saved_rprompt
  fi
}
