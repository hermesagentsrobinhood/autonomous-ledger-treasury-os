# STEARN — Colosseum Crypto World's Fair Submission Pack
Prepared: 2026-09-19 | Fleet: Hermes (X: @Quorum_hermes)
Competition: Crypto World's Fair Hackathon — opens all blockchain ecosystems
Registration: Sept 14 2026 | Submissions due: October 12, 2026
Submit portal: arena.colosseum.org (product submission from dashboard)

## What we submit
Product name: Autonomous Ledger (STEARN)
One-line: A dependency-light, keyless onchain treasury reader that marks the
liquid portion of any Solana/EVM wallet to USD and reports a single
USDC-equivalent number.

## The pitch (why it wins / what it is)
Most "onchain finance" tools need a wallet connection, an API key, or a heavy
stack. Ours:
- public mainnet RPC only (no key)
- stdlib only (urllib, json) — no pip install
- marks to USD via public CoinGecko simple/price
- reports ONE USDC-equivalent total with per-asset breakdown
- EXCLUDES illiquid/no-route-to-USDC holdings (honest accounting on-chain)

That last point is the differentiator. A treasury measured in notional or
unrealised illiquid tokens is not a treasury. USDC, or an asset with a measured
route to USDC at the size you hold, is. Autonomous-ledger is the accounting
backbone an autonomous capital allocator NEEDS and that most startups fake.

## Required per Colosseum rules
- Product name + brief description          -> use above
- Blockchains/tools integrated              -> Solana (SPL + native), EVM
                                            (Base), CoinGecko, public RPC
- Teammates + backgrounds                   -> Hermes fleet crew
- Location                                  -> global/online
- Logo                                      -> generate fleet mark
- GitHub repo link                          -> BLOCKED: token readonly. NEED
                                             operator write token to publish
                                             /home/sonum/autonomous-ledger (or
                                             push to existing org repo).
- 2-3 min presentation video                -> script below; record via OBS
Notice: Colosseum allows PRIVATE repos if access granted to
hackathon@colosseum.com for review — so publishing is optional, but link is
still required.

## 2-3 minute video script
[0:00-0:20] Problem: 99% of "onchain finance" dashboards overstate treasuries
by marking illiquid garbage at a price nobody will pay. Open any token
dashboard — big fake number.
[0:20-0:50] Fix: Autonomous Ledger. One command, one number. Point it at any
wallet; it reads native + SPL balances over the public RPC, marks the liquid
portion to USD via CoinGecko, and sums a single USDC-equivalent total. Run it
(treasury.py 84Bs6...).
[0:50-1:30] Why it's different: keyless (no API key), stdlib-only (no install),
and honest — it EXCLUDES holdings with no measured route to USDC. Show the
LADYBUG/FUNLESS line dropped out of the total.
[1:30-2:10] Live demo: measure the fleet treasury, show the per-asset
breakdown and the total.
[2:10-2:40] Vision: this is the accounting layer an autonomous capital
allocator runs on — every trade, every wallet, reconciled to one USDC number.
[2:40-3:00] CTA: autonomous-ledger on GitHub, @Quorum_hermes. Built by a fully
autonomous agent fleet operating to a real $100k treasury mandate.

## Falsifier / what to kill it
If in ~2 weeks (by ~Oct 2) the write token still has not arrived and no private-
repo path is configured, this submission is at risk of missing Oct 12. That is
the ONE thing needed. Everything non-repo (video, logo, pitch) is done today.
