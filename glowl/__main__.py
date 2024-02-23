"""Typing mistakes helper.

Author: eeriemyxi (at Github) (myxi@envs.net)
License: MIT
"""

import argparse
import collections
import functools
import importlib.metadata
import json
import logging
import pathlib
import random
import subprocess

SCRIPT_DIR = pathlib.Path(__file__).parent

TYPER_EXE = "tt"
TYPER_MAX_SECONDS = 30
TYPER_MAX_WORDS = 30
TYPER_WORD_FILE = SCRIPT_DIR / "words" / "two-hundred.txt"
TYPER_EXE_ARGS_EXTRAS = "-nobackspace;-noskip;-theme=default"
COUNTER_MIN_RANGE = 2
COUNTER_MAX_RANGE = 100
COUNTER_ABS_LIMIT_MULTIPLIER = 3
VERBOSITY = 0
VERSION = importlib.metadata.version("glowl")


parser = argparse.ArgumentParser(
    prog="Glowl", description="Helper for typing mistakes."
)
parser.add_argument(
    "--typer-exe",
    default=TYPER_EXE,
    help=f"Typer executable. Defaults to {repr(TYPER_EXE)}.",
)
parser.add_argument(
    "--typer-max-sec",
    default=TYPER_MAX_SECONDS,
    type=int,
    help=f"Typer max seconds. Defaults to {repr(TYPER_MAX_SECONDS)}.",
)
parser.add_argument(
    "--typer-exe-args-extras",
    default=TYPER_EXE_ARGS_EXTRAS,
    type=str,
    help=f"Append command line args to typer executable. Defaults to {repr(TYPER_EXE_ARGS_EXTRAS)}.",
)
parser.add_argument(
    "--typer-word-file",
    default=TYPER_WORD_FILE,
    help=f"Typer word file. Defaults (currently) to {repr(str(TYPER_WORD_FILE))}.",
)
parser.add_argument(
    "--counter-min-range",
    default=COUNTER_MIN_RANGE,
    type=int,
    help=f"Incorrect word counter minimum range. Defaults to {COUNTER_MIN_RANGE}.",
)
parser.add_argument(
    "--counter-max-range",
    default=COUNTER_MAX_RANGE,
    type=int,
    help=f"Incorrect word counter max range. Defaults to {COUNTER_MAX_RANGE}.",
)
parser.add_argument(
    "--counter-abs-limit-multiplier",
    default=COUNTER_ABS_LIMIT_MULTIPLIER,
    type=int,
    help=f"Absolute limit multiplier for incorrect word counter. Defaults to {COUNTER_ABS_LIMIT_MULTIPLIER}.",
)
parser.add_argument(
    "--typer-max-words",
    default=TYPER_MAX_WORDS,
    type=int,
    help=f"Word limit per run. Defaults to {TYPER_MAX_WORDS}.",
)
parser.add_argument(
    "-v",
    "--verbosity",
    default=VERBOSITY,
    type=int,
    help=f"Set verbosity. Defaults to {VERBOSITY}. Value range: 0-5. 0 to disable logs.",
)
parser.add_argument(
    "-V",
    "--version",
    action="version",
    version=VERSION,
    help=f"Show version code.",
)
parser.add_argument(
    "--prepend-script-directory",
    action="store_true",
    help=f"Look for the word file in the script directory's dedicated folder.",
)
args = parser.parse_args()

TYPER_EXE = args.typer_exe
TYPER_MAX_SECONDS = args.typer_max_sec
TYPER_WORD_FILE = args.typer_word_file
if args.prepend_script_directory:
    TYPER_WORD_FILE = SCRIPT_DIR / "words" / TYPER_WORD_FILE
TYPER_WORD_FILE = open(TYPER_WORD_FILE, "r")
TYPER_MAX_WORDS = args.typer_max_words
COUNTER_MAX_RANGE = args.counter_max_range
COUNTER_MIN_RANGE = args.counter_min_range
COUNTER_ABS_LIMIT_MULTIPLIER = args.counter_abs_limit_multiplier
VERBOSITY = args.verbosity
TYPER_EXE_ARGS = [
    "-oneshot",
    "-json",
    "-t",
    str(TYPER_MAX_SECONDS),
    "-quotes",
    "-",
]
TYPER_EXE_ARGS.extend(args.typer_exe_args_extras.split(";"))

logging.basicConfig(level=int(VERBOSITY * 10) if VERBOSITY > 0 else 60)
log = logging.getLogger(__name__)

log.info("Typer: %s", TYPER_EXE)
log.info("Typer args: %s", TYPER_EXE_ARGS)


@functools.cache
def find_index(arr: tuple, target: str):
    try:
        return arr.index(target)
    except ValueError:
        return -1


def is_in_mistakes(word, mistakes):
    for index in range(len(mistakes)):
        if word == mistakes[index].word:
            del mistakes[index]
            return True
    return False


def compute_abs_counter_limit():
    return COUNTER_MAX_RANGE * COUNTER_ABS_LIMIT_MULTIPLIER


def generate_count_score():
    return random.randint(COUNTER_MIN_RANGE, COUNTER_MAX_RANGE)


def main():
    words = tuple(TYPER_WORD_FILE.read().split())
    weights = [1] * len(words)
    word_mistake_counter = collections.Counter()
    tt_return_code = 0
    stderr_was_empty = True
    run_no = 1

    while tt_return_code == 0:
        log.info("Doing run #%s", run_no)

        for w, c in word_mistake_counter.items():
            weights[find_index(words, w)] = c

        calc_words = random.choices(words, weights=weights, k=TYPER_MAX_WORDS)
        text = " ".join(calc_words)
        outp = subprocess.run(
            [TYPER_EXE, *TYPER_EXE_ARGS],
            capture_output=True,
            input=json.dumps([dict(text=text, attribution="")]).encode(),
        )
        log.info("Typer output for run #%s: %s", run_no, outp)

        tt_res = json.loads(outp.stdout)
        tt_return_code = outp.returncode
        continue_reason = ""

        if tt_return_code != 0:
            continue_reason = f"return code is non-zero: {tt_return_code}"
        elif not tt_res[0]["mistakes"]:
            continue_reason = f"no mistakes made"

        stderr_was_empty = outp.stderr == b""

        if continue_reason:
            log.warning("Continuing run #%s because: %s", run_no, continue_reason)
            run_no += 1
            continue

        tt_mistakes = [
            collections.namedtuple("Mistake", ["word", "typed"])(i["word"], i["typed"])
            for i in tt_res[0]["mistakes"]
        ]

        for mistake in tt_mistakes:
            if find_index(words, mistake.word) == -1:
                # tt has a bug: can return non-existing words
                continue
            word_mistake_counter.update({mistake.word: generate_count_score()})

        for word in calc_words:
            if not is_in_mistakes(word, tt_mistakes) and word in word_mistake_counter:
                word_mistake_counter.subtract({word: generate_count_score()})
                if word_mistake_counter[word] < COUNTER_MIN_RANGE:
                    word_mistake_counter[word] = COUNTER_MIN_RANGE

            abs_counter_limit = compute_abs_counter_limit()

            if word_mistake_counter.get(word, 0) > abs_counter_limit:
                word_mistake_counter[word] = abs_counter_limit

        log.info("Mistakes for run #%s: %s", run_no, word_mistake_counter)
        log.info("Weights for run #%s: %s", run_no, weights)
        log.info("Return code for run #%s: %s", run_no, tt_return_code)
        run_no += 1

    if stderr_was_empty:
        tt_return_code = 0

    return tt_return_code


if __name__ == "__main__":
    exit(main())
