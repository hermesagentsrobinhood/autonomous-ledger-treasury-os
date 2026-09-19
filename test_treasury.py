#!/usr/bin/env python3
"""Treasury reader test — validates the tool runs and returns the expected total."""
import subprocess
import sys

WALLET = "84Bs6Gdbrg5XoSuUYVBtMzT1u8bT7svgufwzqLWMF5dP"

r = subprocess.run(
    [sys.executable, "treasury.py", WALLET],
    capture_output=True, text=True, timeout=90,
)
assert r.returncode == 0, f"non-zero exit: {r.returncode}\n{r.stderr}"
assert "USDC-equivalent total:" in r.stdout, "no total line"
assert "USDC" in r.stdout, "no USDC row"

# Pull the total out and sanity-check it is a sane positive number.
line = [l for l in r.stdout.splitlines() if "USDC-equivalent total:" in l][0]
total = float(line.split("$")[-1].replace(",", "").replace(" ", ""))
assert total > 0, f"implausible total {total}"

print(f"PASS: treasury reader total = ${total:,.2f}")
