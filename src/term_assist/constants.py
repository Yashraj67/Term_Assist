import os

LINE_REGEX_PATTERNS = [
    r"line (\d+)",  # Common Python traceback: 'File "x.py", line 10'
    r":(\d+):",  # Common in Ruby: 'x.rb:10:in `<main>`'
    r":(\d+)$",  # Some CLI tools show file:line
    r"\(line (\d+)\)",  # Generic fallback
]

FILE_EXTENTIONS = [
    ".c",
    ".cpp",
    ".java",
    ".cs",
    ".js",
    ".py",
    ".go",
    ".rb",
    ".php",
    ".swift",
    ".rs",
    ".ts",
    ".sh",
    ".ps1",
    ".m",
    ".mm",
    ".kt",
    ".kts",
    ".jsx",
    ".tsx",
    ".dart",
    ".lua",
    ".r",
    ".pl",
    ".ex",
    ".exs",
    ".clj",
    ".groovy",
    ".scala",
    ".jl",
    ".cr",
    ".nim",
    ".hx",
]

OPENAI_API_KEY = os.environ.get(
    "OPENAI_API_KEY",
    "Your_openai_api_key",
)

GPT4O = "gpt-4o"
GPT4O_MINI = "gpt-4o-mini"
