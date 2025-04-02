#!/usr/bin/env python
import sys


def get_command_details():
    """
    Args:
      sys.argv[1] -> the exact command that was just run
      sys.argv[2] -> the command's exit code
      sys.argv[3..] -> any stderr text (could include spaces/newlines)
    """
    if len(sys.argv) < 3:
        return  # Not enough args, ignore

    command = sys.argv[1]
    exit_code = sys.argv[2]

    # The remaining args represent the stderr text.
    error_text = " ".join(sys.argv[3:])

    print("----- COMMAND LOG (Zsh) -----")
    print(f"Command Ran  : {command}")
    print(f"Exit Code    : {exit_code}")
    if error_text.strip():
        print("Captured stderr:")
        print(error_text)
    print("--------------------------------")

    return command, exit_code , error_text


def main():



if __name__ == "__main__":
    main()
