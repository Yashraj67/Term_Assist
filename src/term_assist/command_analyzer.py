import os
import re
import shlex
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from term_assist.constants import FILE_EXTENTIONS


def remove_env_assignments(command: str) -> str:
    """
    Remove all tokens that define an environment variable in the form VAR=val.
    e.g.,
       'FOO=bar some_command' => 'some_command'
       'export BAZ=stuff' => 'export'  (though typically 'export BAZ=stuff' is two tokens in shell)
       'FOO=bar BAZ=cat CMD' => 'CMD'
    """
    tokens = shlex.split(command)
    filtered_tokens = []
    for token in tokens:
        if re.match(r"^[A-Za-z_][A-Za-z0-9_]*=.*", token):
            continue
        else:
            filtered_tokens.append(token)

    return " ".join(shlex.quote(t) for t in filtered_tokens)


def sanitize_command(command: str) -> str:
    """
    Attempt to remove or redact any credentials that appear in the command string.
    For example:
     - Credentials in a URL:  https://username:password@host.com
     - -p password (common for mysql, sshpass)
     - --password=somepassword
     - environment variables referencing secrets
    """

    command = remove_env_assignments(command)

    # 1) Redact common credential patterns in URLs: user:pass@...
    #    Example: https://myuser:mypass@github.com => https://myuser:****@github.com
    #    We'll capture the group "username:password@" so we can replace "password" with "****"
    url_pattern = re.compile(r"(https?:\/\/[^:\s]+):([^@\s]+)@")
    command = url_pattern.sub(lambda m: f"{m.group(1)}:****@", command)

    # 2) Redact mysql/sshpass-like usage: -p yourpassword OR --password=yourpassword
    #    Patterns:
    #       -p Secret
    #       --password=Secret
    #    We'll replace the password part with ****.
    password_pattern_1 = re.compile(r"(\s-\w*p\s+)(\S+)")
    command = password_pattern_1.sub(r"\1****", command)

    password_pattern_2 = re.compile(r"(\s--password=)(\S+)")
    command = password_pattern_2.sub(r"\1****", command)

    # For the case like `-pSomePassword` with no space:
    password_pattern_3 = re.compile(r"(\s-p)(\S+)")
    command = password_pattern_3.sub(r"\1****", command)

    env_pattern = re.compile(
        r"(\$[A-Z0-9_]*(?:SECRET|PASSWORD|TOKEN)[A-Z0-9_]*)", re.IGNORECASE
    )
    command = env_pattern.sub("****", command)
    return command


def get_command_type(command: str, command_path):
    tokens = shlex.split(command)
    for token in tokens:
        if token.endswith(tuple(FILE_EXTENTIONS)):
            absolute_path = command_path + "/" + token
            _, extension = os.path.splitext(token)
            return absolute_path, extension

    return None, None
