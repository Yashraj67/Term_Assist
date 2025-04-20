# Term-Assist

Term-Assist is AI-powered terminal tool which uses llms to provide solutions to your terminal errors and queries.

Currently have support for all general commands and `python` files for all `zshrc` terminals.
Will be adding support for other terminals and languages soon!

### Steps to get started

---

- Make sure to have `python3` installed
- Install [Poetry](https://python-poetry.org/docs/) from official source
- Clone the project
- Install rich globally :

```sh
pip install rich
```

- Update `start_ta_daemon.sh` as suggested in the file

- Add the code present `term_assist_zsh.txt` script in your `~/.zshrc` with **mentioned updates** and run :

```sh
source ~/.zshrc
```

- Add the following environment variables :

```sh
export OPENAI_API_KEY="your_openai_api_key"
```

- Run any command and your terminal assistant is ready to resolve all your errors!

- If you don't want assistance for any command suffix the command with `--sts`

```sh
#example
python foobar.py --sts
```

## Sample Responses

- File based errors :
  ![Prototype 1](https://github.com/Yashraj67/Term_Assist/blob/main/Screenshot%202025-04-12%20231304.png)

- General command errors :
  ![Prototype 2](https://github.com/Yashraj67/Term_Assist/blob/main/Screenshot%202025-04-12%20231430.png)
