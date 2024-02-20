# Glowl - Typing Mistakes Helper

Glowl is a Python script designed to assist with identifying typing mistakes by utilizing the [`tt`](https://github.com/lemnos/tt) (tested on v0.4.2) tool. This README provides an overview of the script's functionality, usage instructions, and customization options.

## Usage

To use Glowl, follow these steps:

1. Clone the repository to your local machine.
2. Ensure you have Python and [Poetry](https://python-poetry.org) installed (the script is compatible with Python 3.11.x).
3. Install the required dependencies by running `pip install .` or `poetry install` in script directory.
4. Execute the script by running `glowl` or `poetry run glowl` with appropriate arguments.

## Command-line Arguments

Glowl supports the following command-line arguments:

- `--typer-exe`: Path to the Typer executable. Defaults to `"tt"`.
- `--typer-max-sec`: Maximum seconds for each typing session. Defaults to `30`.
- `--typer-word-file`: Path to the word file used by Typer. Defaults (currently) to `"[script directory]/words/two_hundred.txt"`.
- `--counter-min-range`: Minimum range for incorrect word counter. Defaults to `2`.
- `--counter-max-range`: Maximum range for incorrect word counter. Defaults to `100`.
- `--counter-abs-limit-multiplier`: Absolute limit multiplier for incorrect word counter. Defaults to `3`.
- `--typer-max-words`: Word limit per run. Defaults to `30`.
- `-v`, `--verbosity`: Set verbosity. Defaults to `0`. Value range: `0-5`. `0` to disable logs.
- `-V`, `--version`: Show version code.

Example usages:
```bash
glowl --typer-max-sec 30 --counter-max-range 5
```
Setting verbosity to a higher level (e.g., 1) to enable more detailed logging:
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

---

Feel free to enhance Glowl according to your needs and contribute back to the project! If you encounter any issues or have suggestions for improvement, please open an issue on the repository. Thank you for using Glowl!
