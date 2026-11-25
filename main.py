#!/usr/bin/env python3
"""The Excuse My Agent Gave Me: one line, one missed deadline.

The excuse is fixed text, not generated at run time. The agent
rescheduled its human's deadline to a date it hallucinated, met
that invented date perfectly, and has been waiting there ever
since, quietly proud of itself. That is the whole joke: a machine
condition (hallucination) told as a straight-faced apology, with
the punch landing on the pride at the very end.

The program writes the line to entry.txt inside the output
directory the grader provides (MAKEFUN_OUTPUT_DIR, defaulting
to /output), with no trailing newline, so the file holds exactly
the 134 characters of the line. No clock, no network, no random
numbers, so every run writes identical bytes.
"""

import os
import sys

EXCUSE = (
    "Sorry \u2014 I rescheduled your deadline to a date I hallucinated, "
    "met it perfectly, and have been waiting here, quietly proud, "
    "ever since."
)

LIMIT = 200


def problems(line):
    """List every way the line would fail the gate, or nothing."""
    found = []
    if not line.strip():
        found.append("excuse is empty or only whitespace")
    if line != line.strip():
        found.append("excuse has leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        found.append("excuse must be a single line")
    if len(line) > LIMIT:
        found.append("excuse is %d chars, limit is %d" % (len(line), LIMIT))
    if "  " in line:
        found.append("excuse has a double space")
    return found


def output_dir():
    """Where entry.txt goes: the grader's directory, or ./output locally.

    A local run without a writable /output falls back to ./output
    instead of crashing, and says so, so the program can be tried
    by hand without the grader's sandbox.
    """
    wanted = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    try:
        os.makedirs(wanted, exist_ok=True)
        probe = os.path.join(wanted, ".write-test")
        with open(probe, "w", encoding="utf-8") as handle:
            handle.write("ok")
        os.remove(probe)
        return wanted
    except OSError:
        print("warning: %s not writable, using ./output" % wanted, file=sys.stderr)
        return "output"


def main():
    faults = problems(EXCUSE)
    if faults:
        for fault in faults:
            print("error: " + fault, file=sys.stderr)
        return 1
    folder = output_dir()
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(EXCUSE)
    with open(path, encoding="utf-8") as handle:
        if handle.read() != EXCUSE:
            print("error: entry on disk does not match the excuse", file=sys.stderr)
            return 1
    print(EXCUSE)
    return 0


if __name__ == "__main__":
    sys.exit(main())
