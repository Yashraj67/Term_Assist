# Term-Assist

Term-Assist is AI-powered terminal tool which uses llms to provide solutions to your terminal errors and queries.

Currently have support for all general commands and `python` files.
Will be adding support for other terminals and languages soon!

### Steps to get started

---

- Make sure to have `python3` installed
- Install [Poetry](https://python-poetry.org/docs/) from official source
- Clone the project
- Go to root of the project and run :

```sh
poetry shell
```

- Add the code present `term_assist_zsh.txt` script in your `~/.zshrc` and run :

```sh
source ~/.zshrc
```

- Add the following environment variables :

```sh
export OPENAI_API_KEY="your_openai_api_key"
```

- Run any command and your terminal assistant is ready to resolve all your errors!
