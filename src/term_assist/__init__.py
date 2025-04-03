import os
import sys

sys.path.append("/home/yashraj/term_assist/term_assist/src/")

from term_assist.command_analyzer import sanitize_command


def get_command_details():
    """
    Args:
      sys.argv[1] -> the exact command that was just run
      sys.argv[2] -> the command's exit code
      sys.argv[3..] -> any stderr text (could include spaces/newlines)
    """
    if len(sys.argv) < 3:
        return None, None, None

    command = sys.argv[1]
    exit_code = sys.argv[2]

    error_text = " ".join(sys.argv[3:])

    print("----- COMMAND LOG (Zsh) -----")
    print(f"Command Ran  : {command}")
    print(f"Exit Code    : {exit_code}")
    if error_text.strip():
        print("Captured stderr:")
        print(error_text)
    print("--------------------------------")

    return command, exit_code, error_text


def main():
    command, exit_code, error_text = get_command_details()
    clean_command = sanitize_command(command)
    print(f"clean command : {clean_command}")


if __name__ == "__main__":
    main()
