import os
import sys
import time

from term_assist.response_enhancer import pretty_print_llm
from term_assist.spinner import Spinner

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from term_assist.command_analyzer import get_command_type, sanitize_command
from term_assist.file_error_handler import get_file_context
from term_assist.llm import GPT4, get_openai_client, get_response_from_llm_with_fallback
from term_assist.prompts import get_comman_error_prompt, get_file_error_prompt

openai_client = get_openai_client()
done = True


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
    print(error_text)
    return command, exit_code, error_text, command_path


def main():
    command, exit_code, error_text, command_path = get_command_details()
    if exit_code != "0":
        clean_command = sanitize_command(command)
        file_path, extention = get_command_type(clean_command, command_path)
        if extention != None:
            context = get_file_context(error_text, file_path, extention)
            prompt = get_file_error_prompt(command, exit_code, error_text, context)
        else:
            prompt = get_comman_error_prompt(command, exit_code, error_text)

        with Spinner("🔎  Asking LLM for fix... "):
            response = get_response_from_llm_with_fallback(GPT4, prompt, openai_client)

        pretty_print_llm(response)


if __name__ == "__main__":
    main()
