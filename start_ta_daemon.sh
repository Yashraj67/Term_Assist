#!/bin/bash

SOCKET="/tmp/termassist.sock"
#update according to your project directory
PROJECT_DIR="/home/yashraj/term_assist/term_assist"
LOG_FILE="/tmp/termassist.log"

if lsof -U "$SOCKET" &>/dev/null; then
    echo "🔄 Restarting Term Assist Daemon..."
    lsof -t -U "$SOCKET" | xargs kill -9
    rm -f "$SOCKET"
fi

(
    cd "$PROJECT_DIR" || exit
    poetry run python3 src/term_assist/server.py >> "$LOG_FILE" 2>&1 &
)

echo "✅ Term Assist Daemon started"

