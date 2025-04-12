import os
import sys

sys.path.append("/home/yashraj/term_assist/term_assist/src/")

from term_assist.command_analyzer import get_command_type, sanitize_command
from term_assist.file_error_handler import get_file_context


def get_command_details():
    """
    Args:
      sys.argv[1] -> the exact command that was just run
      sys.argv[2] -> the command's exit code
      sys.argv[3] -> the path from which command is ran
      sys.argv[4..] -> any stderr text (could include spaces/newlines)
    """
    if len(sys.argv) < 4:
        return None, None, None, None

    command = sys.argv[1]
    exit_code = sys.argv[2]
    command_path = sys.argv[3]

    error_text = " ".join(sys.argv[4:])

    print("----- COMMAND LOG (Zsh) -----")
    print(f"Command Ran  : {command}")
    print(f"Exit Code    : {exit_code}")
    print(f"Error : {error_text}")
    print(f"command_path : {command_path}")
    if error_text.strip():
        print("Captured stderr:")
        print(error_text)
    print("--------------------------------")

    return command, exit_code, error_text, command_path


def main():
    command, exit_code, error_text, command_path = get_command_details()
    if error_text is not None and error_text.strip():
        clean_command = sanitize_command(command)
        file_path, extention = get_command_type(clean_command, command_path)
        context = get_file_context(error_text, file_path, extention)
        print(f"clean command : {clean_command}")


if __name__ == "__main__":
    main()
