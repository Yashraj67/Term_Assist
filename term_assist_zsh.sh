# ~~~~~~~~~~~~~~~ BEGIN TERM ASSIST ZSHRC SNIPPET ~~~~~~~~~~~~~~~

skip_trailing_sts() {
  if [[ $LBUFFER == *' --sts' ]]; then
      LBUFFER=${LBUFFER% --sts}
      SKIP_LOGGING=1
  else
      unset SKIP_LOGGING
  fi
}
zle -N zle-line-finish skip_trailing_sts

preexec_logger() {
    LOGGED_CMD=$1
    CMD_START_DIR=$PWD

    if [[ -z $SKIP_LOGGING ]]; then
        exec {ORIG_STDERR}>&2
        exec 2> >(tee "/tmp/cmd_stderr.$$" >&$ORIG_STDERR)
    fi
}
add-zsh-hook preexec  preexec_logger

precmd_logger() {
    local exit_code=$?

    if [[ -z $SKIP_LOGGING && -n ${ORIG_STDERR:-} ]]; then
        exec 2>&$ORIG_STDERR {ORIG_STDERR}>&-
    fi

    if [[ -z $SKIP_LOGGING ]]; then
        local error_output=""
        [[ -f "/tmp/cmd_stderr.$$" ]] && {
            error_output=$(< /tmp/cmd_stderr.$$)
            rm -f "/tmp/cmd_stderr.$$"
        }
        #update this with your's cloned project's client.py path
        if (( exit_code != 0 )) && [[ -n $error_output ]]; then
            python3 /home/yashraj/term_assist/term_assist/src/term_assist/client.py "$LOGGED_CMD" "$exit_code" "$CMD_START_DIR" "$error_output"
        fi
    fi

    unset LOGGED_CMD CMD_START_DIR SKIP_LOGGING ORIG_STDERR
}
add-zsh-hook precmd  precmd_logger

#update this with your's cloned project's start_ta_daemon.sh path
/home/yashraj/term_assist/term_assist/start_ta_daemon.sh

# ~~~~~~~~~~~~~~~ END TERM ASSIST ZSHRC SNIPPET ~~~~~~~~~~~~~~~
