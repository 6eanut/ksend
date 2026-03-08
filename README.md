
# ksend

ksend is a small helper tool for sending Linux kernel patch series.

It automates a common workflow:

1. Run `scripts/get_maintainer.pl` on patches
2. Collect maintainers and mailing lists
3. Remove duplicates
4. Generate a ready-to-use `git send-email` command

This avoids manually copying email addresses when sending patches.

## Features

- Automatically runs `get_maintainer.pl`
- Merges recipients from multiple patches
- Removes duplicate addresses
- Separates mailing lists (`--to`) and individuals (`--cc`)
- Supports patch series including cover letters
- Generates a complete `git send-email` command

## Requirements

- Python 3
- Linux kernel source tree (for `scripts/get_maintainer.pl`)
- `git send-email` configured

## Usage

Run the script inside a Linux kernel tree:

```bash
python3 ksend.py 000*.patch
```
