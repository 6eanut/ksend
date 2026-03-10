#!/usr/bin/env python3

import subprocess
import sys
import re
from pathlib import Path

if len(sys.argv) < 2:
    print("usage: ksend.py 000*.patch")
    sys.exit(1)

patches = [Path(p).resolve() for p in sys.argv[1:]]

email_set = set()
list_set = set()

name_email_re = re.compile(r'.*<[\w\.-]+@[\w\.-]+>')
plain_email_re = re.compile(r'[\w\.-]+@[\w\.-]+')


def is_cover_letter(p):
    return p.name.startswith("0000")


def run_get_maintainer(patch):
    cmd = [
        "./scripts/get_maintainer.pl",
        "--email",
        "--no-rolestats",
        str(patch)
    ]

    result = subprocess.run(cmd, stdout=subprocess.PIPE, text=True)
    return result.stdout.splitlines()


for patch in patches:

    if is_cover_letter(patch):
        continue

    lines = run_get_maintainer(patch)

    for line in lines:

        line = line.strip()

        m = name_email_re.match(line)
        if m:
            email_set.add(m.group(0))
            continue

        m = plain_email_re.match(line)
        if m:
            list_set.add(m.group(0))


print("Detected recipients:\n")

print("To:")
for e in sorted(list_set):
    print(" ", e)

print("\nCc:")
for e in sorted(email_set):
    print(" ", e)

print("\nGenerated command:\n")

cmd_parts = ["git", "send-email"]

cmd_parts += [str(p) for p in patches]

for e in sorted(list_set):
    cmd_parts.append("--to")
    cmd_parts.append(e)

for e in sorted(email_set):
    cmd_parts.append("--cc")
    cmd_parts.append(e)


def shell_quote(s):
    if ' ' in s or '<' in s or '>' in s:
        return f'"{s}"'
    return s


print(" \\\n  ".join(shell_quote(arg) for arg in cmd_parts))
