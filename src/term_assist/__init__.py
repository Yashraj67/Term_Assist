import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from term_assist.command_analyzer import get_command_type, sanitize_command
from term_assist.file_error_handler import get_file_context
from term_assist.llm import GPT4, get_openai_client, get_response_from_llm_with_fallback
from term_assist.prompts import get_comman_error_prompt, get_file_error_prompt

openai_client = get_openai_client()


def main(command, exit_code, command_path, error_text):
    if exit_code != "0":
        clean_command = sanitize_command(command)
        file_path, extention = get_command_type(clean_command, command_path)
        if extention != None:
            context = get_file_context(error_text, file_path, extention)
            prompt = get_file_error_prompt(command, exit_code, error_text, context)
        else:
            prompt = get_comman_error_prompt(command, exit_code, error_text)

        response = get_response_from_llm_with_fallback(GPT4, prompt, openai_client)
        return response
