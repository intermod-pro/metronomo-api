# Copyright (c) 2023-2026 Intermodulation Products AB

"""Collection of functions that might be useful, or might not."""

import sys


def eprint(*objects):
    print(*objects, file=sys.stderr)


def _colored(aec: str, msg: str) -> str:
    return f"{aec}{msg}{_AEC_RESET}"


def eprint_error(title: str, body: str, warn: bool = False, inline: bool = False):
    aec = _AEC_YELLOW if warn else _AEC_RED
    if not title:
        eprint(_colored(aec, body))
    else:
        if inline:
            wide = f"{title}:"
            eprint(f"{_colored(aec, wide)} {body}")
        else:
            wide = f" {title} "
            eprint(_colored(aec, f"{wide:-^80}"))
            eprint(body)
            eprint(_colored(aec, f"{'':-^80}"))


_AEC_YELLOW = "\x1b[1;33m"
_AEC_RED = "\x1b[1;31m"
_AEC_RESET = "\x1b[0m"
