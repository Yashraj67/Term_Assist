def get_file_error_prompt(command, exit_code, error_text, context):
    return f"""
    You're an expert programmer with excellent debugging and analytical skills. 
    Given the following command and related information, help me to fix the error caused.

    <command>
    {command}
    </command> 

    <exit_code>
    {exit_code}
    </exit_code>

    <error_text>
    {error_text}
    </error_text>

    <file_context>
    {context}
    </file_context>
    """


def get_comman_error_prompt(command, exit_code, error_text):
    return f"""
    You're an expert programmer with excellent debugging and analytical skills. 
    Given the following command and related information, help me to fix the error caused.

    <command>
    {command}
    </command> 

    <exit_code>
    {exit_code}
    </exit_code>

    <error_text>
    {error_text}
    </error_text>

    """
