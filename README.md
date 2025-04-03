# Term-Assist

Term-Assist is AI-powered terminal tool which uses llms to provide solutions to your terminal errors and queries.

### Steps to get started

---

- Make sure to have `python3` installed
- Clone the project
- Add the following code to your `~/.zshrc` file:

```
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
    exec 2> "/tmp/cmd_stderr.$$"
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
        #update this path to your cloned project's __init__.py file path
        python3  /home/yashraj/term_assist/term_assist/src/term_assist/__init__.py  \
            "$LOGGED_CMD" "$exit_code" "$error_output"
    fi

    unset LOGGED_CMD
    unset SKIP_LOGGING
}

# ~~~~~~~~~~~~~~~ END TERM ASSIST ZSHRC SNIPPET ~~~~~~~~~~~~~~~
```

Then run:

```
source ~/.zshrc
```
