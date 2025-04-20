import os
import socket
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from response_enhancer import pretty_print_llm
from spinner import Spinner

SOCKET_PATH = "/tmp/termassist.sock"


def send_to_daemon(command, exit_code, path, stderr):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    client.connect(SOCKET_PATH)
    message = f"{command}<<<DELIM>>>{exit_code}<<<DELIM>>>{path}<<<DELIM>>>{stderr}"
    if exit_code != 0:
        with Spinner("🔎  Asking LLM for fix... "):
            client.sendall(message.encode())
            response = client.recv(65535).decode()

        pretty_print_llm(response)


if __name__ == "__main__":
    send_to_daemon(*sys.argv[1:5])
