# ~~~~~~~~~~~~~~~ BEGIN TERM ASSIST ZSHRC SNIPPET ~~~~~~~~~~~~~~~

function skip_trailing_sts() {
  if [[ "$LBUFFER" =~ '[[:space:]]--sts'$ ]]; then
    LBUFFER="${LBUFFER% --sts}"
    export SKIP_LOGGING=1
  else
    unset SKIP_LOGGING
  fi
}

zle -N zle-line-finish skip_trailing_sts

function preexec() {
    export LOGGED_CMD="$1"
    export CMD_START_DIR=$PWD
    exec 2> "/tmp/cmd_stderr.$$"
}

poetry_term_assist() {
    # Update this with cloned project's root path
    poetry --directory /home/yashraj/term_assist/term_assist "$@"
}

function precmd() {
    local exit_code=$?

    exec 2>&1

    local error_output=""
    if [[ -f "/tmp/cmd_stderr.$$" ]]; then
        error_output="$(cat /tmp/cmd_stderr.$$)"
        rm -f "/tmp/cmd_stderr.$$" 2>/dev/null
    fi

    if [[ -n "$SKIP_LOGGING" ]]; then
        :
    else
        # Update this with cloned project's "__init__.py" file path in your machine
        poetry_term_assist run python3  /home/yashraj/term_assist/term_assist/src/term_assist/__init__.py  \
            "$LOGGED_CMD" "$exit_code" "$CMD_START_DIR" "$error_output"
    fi

    unset CMD_START_DIR
    unset LOGGED_CMD
    unset SKIP_LOGGING
}
