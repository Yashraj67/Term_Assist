## Term-Assist

---

Term-Assist is AI-powered terminal tool which uses llms to provide solutions to your terminal errors and queries.

### Steps to get started

---

- Clone the project
- Add the following code to your `~/.zshrc` file:

```
# ~~~~~~~~~~~~~~~ BEGIN TERM ASSIST ZSHRC SNIPPET ~~~~~~~~~~~~~~~

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

    python /path/to/term_assist/__init__.py "$LOGGED_CMD" "$exit_code" "$error_output"  # Don't forget to update this path

    unset LOGGED_CMD
}

# ~~~~~~~~~~~~~~~ END TERM ASSIST ZSHRC SNIPPET ~~~~~~~~~~~~~~~

```
