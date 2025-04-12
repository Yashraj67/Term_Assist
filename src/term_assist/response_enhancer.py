import re
import textwrap

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.syntax import Syntax

console = Console()


def pretty_print_llm(text: str, title: str = "💡 Suggested Fix") -> None:

    text = textwrap.dedent(text).strip()

    fence = re.compile(r"```(\w+)?\n(.*?)```", re.S)

    console.rule(title, style="green")

    pos = 0
    for m in fence.finditer(text):
        if m.start() > pos:
            md_chunk = text[pos : m.start()].strip()
            if md_chunk:
                console.print(Markdown(md_chunk))

        lang = m.group(1) or "text"
        code = m.group(2).rstrip()
        syntax = Syntax(code, lang, line_numbers=True, theme="monokai")
        console.print(Panel(syntax, style="on grey23"))
        pos = m.end()

    tail = text[pos:].strip()
    if tail:
        console.print(Markdown(tail))
