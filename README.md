# Glowl - Typing Mistakes Helper

Glowl is a Python script designed to assist with identifying typing mistakes by utilizing the [`tt`](https://github.com/lemnos/tt) (tested on v0.4.2) tool. This README provides an overview of the script's functionality, usage instructions, and customization options.

## Installation

#### First Method
```
git clone --depth 1 --branch main <REPO URL> glowl
pip install ./glowl
```
#### Second Method
```
pip install git+<REPO URL>@main
```
## Command-line Arguments
```
usage: glowl [-h] [--typer-exe TYPER_EXE] [--typer-max-sec TYPER_MAX_SEC]
             [--typer-exe-args-extras TYPER_EXE_ARGS_EXTRAS]
             [--typer-word-file TYPER_WORD_FILE]
             [--counter-min-range COUNTER_MIN_RANGE]
             [--counter-max-range COUNTER_MAX_RANGE]
             [--counter-abs-limit-multiplier COUNTER_ABS_LIMIT_MULTIPLIER]
             [--typer-max-words TYPER_MAX_WORDS] [-v VERBOSITY] [-V]
             [--prepend-script-directory]

Helper for typing mistakes.

options:
  -h, --help            show this help message and exit
  --typer-exe TYPER_EXE
                        Typer executable. Defaults to 'tt'.
  --typer-max-sec TYPER_MAX_SEC
                        Typer max seconds. Defaults to 30.
  --typer-exe-args-extras TYPER_EXE_ARGS_EXTRAS
                        Append command line args to typer executable. Defaults
                        to '-nobackspace;-noskip;-theme=default'.
  --typer-word-file TYPER_WORD_FILE
                        Typer word file. Defaults (currently) to
                        '/drone/src/glowl/words/two-hundred.txt'.
  --counter-min-range COUNTER_MIN_RANGE
                        Incorrect word counter minimum range. Defaults to 3.
  --counter-max-range COUNTER_MAX_RANGE
                        Incorrect word counter max range. Defaults to 100.
  --counter-abs-limit-multiplier COUNTER_ABS_LIMIT_MULTIPLIER
                        Absolute limit multiplier for incorrect word counter.
                        Defaults to 3.
  --typer-max-words TYPER_MAX_WORDS
                        Word limit per run. Defaults to 30.
  -v VERBOSITY, --verbosity VERBOSITY
                        Set verbosity. Defaults to 0. Value range: 0-5. 0 to
                        disable logs.
  -V, --version         Show version code.
  --prepend-script-directory
                        Look for the word file in the script directory's
                        dedicated folder.
```

## Examples
```bash
glowl --typer-max-sec 30 --counter-max-range 5
```
Append custom arguments to typer executable:
```bash
glowl --typer-exe-args-extras="-theme=mar;-noskip;-nobackspace" --counter-max-range 5
```
Setting verbosity to a higher level (e.g., 1) to enable more detailed logging (1 is most verbose and 5 is least):
```bash
glowl -v 1
```
Specifying a custom Typer executable path and increasing the maximum word limit per run to 50:
```bash
glowl --typer-exe /path/to/custom/typer --typer-max-words 50
```
Adjusting the range for the incorrect word counter and setting a custom word file path:
```bash
glowl --counter-min-range 1 --counter-max-range 10 --typer-word-file /path/to/custom/word/file.txt
```

These examples showcase different customization options available with Glowl, including verbosity level adjustment, specifying custom Typer executable path, modifying word limit per run, adjusting range for the incorrect word counter, and setting a custom word file path.
## Functionality

Glowl operates by repeatedly invoking the [`tt`](https://github.com/lemnos/tt) tool with random text samples generated from a word list. It analyzes the mistakes identified by Typer and adjusts its word choice strategy accordingly, aiming to expose a variety of typing errors.

## Customization

You can customize Glowl's behavior by adjusting the command-line arguments:

- Modify `typer-max-sec` to change the duration of each typing session.
- Adjust `counter-min-range` and `counter-max-range` to control the range of incorrect word counters.
- Change `typer-word-file` to use a different word file.

## Dependencies

- Python 3.11.x
- [`tt`](https://github.com/lemnos/tt) (tested on v0.4.2)
- Required Python built-in packages:
  - `argparse`
  - `collections`
  - `functools`
  - `importlib`
  - `json`
  - `logging`
  - `pathlib`
  - `random`
  - `subprocess`

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

* * *

Feel free to enhance Glowl according to your needs and contribute back to the project! If you encounter any issues or have suggestions for improvement, please open an issue on the repository. Thank you for using Glowl!
