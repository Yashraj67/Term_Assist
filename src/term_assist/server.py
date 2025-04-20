import os
import socket
import sys
import threading

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from term_assist.__init__ import main

SOCKET_PATH = "/tmp/termassist.sock"


def handle_client(conn):
    try:
        data = conn.recv(65535).decode()
        if data:
            parts = data.split("<<<DELIM>>>")
            command, exit_code, path, stderr = parts
            result = main(command, exit_code, path, stderr)
            conn.send(result.encode())
    except Exception as e:
        conn.send(f"Error: {e}".encode())
    finally:
        conn.close()


def start_server():
    if os.path.exists(SOCKET_PATH):
        os.remove(SOCKET_PATH)

    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    server.bind(SOCKET_PATH)
    server.listen(5)

    while True:
        conn, _ = server.accept()
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()


if __name__ == "__main__":
    start_server()
