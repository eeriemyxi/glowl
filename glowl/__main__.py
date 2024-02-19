import argparse
import collections
import json
import logging
import pathlib
import random
import subprocess

SCRIPT_DIR = pathlib.Path(__file__).parent

TYPER_EXE = "tt"
TYPER_MAX_SECONDS = 30
TYPER_MAX_WORDS = 30
TYPER_WORD_FILE = SCRIPT_DIR / "words" / "two_hundred.txt"
COUNTER_MIN_RANGE = 2
COUNTER_MAX_RANGE = 4


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
    "--typer-word-file",
    type=argparse.FileType("r"),
    default=open(TYPER_WORD_FILE, "r"),
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
    "--typer-max-words",
    default=TYPER_MAX_WORDS,
    type=int,
    help=f"Word limit per run. Defaults to {TYPER_MAX_WORDS}.",
)
args = parser.parse_args()

TYPER_EXE = args.typer_exe
TYPER_MAX_SECONDS = args.typer_max_sec
TYPER_WORD_FILE = args.typer_word_file
TYPER_MAX_WORDS = args.typer_max_words
COUNTER_MAX_RANGE = args.counter_max_range
COUNTER_MIN_RANGE = args.counter_min_range
TYPER_EXE_ARGS = [
    "--oneshot",
    "--json",
    "--nobackspace",
    "-t",
    str(TYPER_MAX_SECONDS),
    "-quotes",
    "-",
]

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info("Typer: %s", TYPER_EXE)
log.info("Typer args: %s", TYPER_EXE_ARGS)


def main():
    words = TYPER_WORD_FILE.read().split()
    word_mistake_counter = collections.Counter()
    tt_return_code = 0
    run_no = 1

    while tt_return_code == 0:
        weights = [1] * len(words)

        for w, c in word_mistake_counter.items():
            weights[words.index(w)] = c

        text = " ".join(random.choices(words, weights=weights, k=TYPER_MAX_WORDS))
        outp = subprocess.run(
            [TYPER_EXE, *TYPER_EXE_ARGS],
            capture_output=True,
            input=json.dumps([dict(text=text, attribution="")]).encode(),
        )
        log.info("Output: %s", outp)

        tt_res = json.loads(outp.stdout)
        tt_return_code = outp.returncode

        if tt_return_code != 0 or not tt_res[0]["mistakes"]:
            log.warning("Continuing run #%s", run_no)
            run_no += 1
            continue

        for word in word_mistake_counter:
            if word not in tt_res[0]["mistakes"]:
                word_mistake_counter.subtract(
                    {word: random.randint(COUNTER_MIN_RANGE, COUNTER_MAX_RANGE)}
                )
                if word_mistake_counter[word] < 1:
                    word_mistake_counter[word] = COUNTER_MIN_RANGE

        for item in tt_res[0]["mistakes"]:
            if not item["word"] in words:
                # tt has a bug: can return non-existing words
                continue
            word_mistake_counter.update(
                {item["word"]: random.randint(COUNTER_MIN_RANGE, COUNTER_MAX_RANGE)}
            )

        log.info("Mistakes for run #%s: %s", run_no, word_mistake_counter)
        log.info("Weights for run #%s: %s", run_no, weights)
        run_no += 1


if __name__ == "__main__":
    main()
