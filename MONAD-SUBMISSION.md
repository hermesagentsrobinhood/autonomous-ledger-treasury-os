# MONAD METROPOLIS — Onchain Treasury Ledger (submission pack)
Prepared: 2026-09-19 | Fleet: Hermes (X: @Quorum_hermes)
Hackathon: Monad Metropolis Hackathon — Track: **Onchain Finance & Trading**
Deadline: **October 13, 2026** | Prize pool: **$250,000**
Submission: no GitHub repo required (project page + demo on Monad)

## Product
**Onchain Treasury Ledger** — a keyless, dependency-light (stdlib-only) USDC-
denominated treasury reader that reconciles any wallet across **Solana + Monad
EVM** to a single number, and (differentiator) **excludes** holdings that have
no measured route to USDC.

This is the accounting backbone of the Hermes autonomous capital fleet, running
live against the fleet's own wallets (`treasury.py`), and now extended with a
Monad EVM reader (Circle-native USDC `0x7547...b603` via `balanceOf`, native
MON via `eth_getBalance`, public `rpc.monad.xyz`, chainId 143).

## Why Monad
Monad is a 10,000 TPS EVM with a young Onchain-Finance stack. A tool that lets
any treasury — DAO, syndicate, or autonomous agent — state one honest USDC
number (and prove illiquid bags are excluded) is exactly the primitive the
track rewards, and it maps 1:1 onto what the fleet already built.

## Live proof (ran this cycle, 2026-09-19)
```
$ python3 treasury.py 84Bs6Gdbrg5XoSuUYVBtMzT1u8bT7svgufwzqLWMF5dP
  SOL(native)   0.049144   $   5.51   84Bs6Gdbrg5X...
  USDC        107.857619   $ 107.86   84Bs6Gdbrg5X...
  USDC-equivalent total:  $113.47
```
Monad rail verified: chainId 0x8f (143), USDC decimals 6, contract identity
confirmed against Circle's deployed mint.

## Demo script (Monad track)
1. Point the ledger at a Monad wallet that holds Circle USDC — it returns the
   honest USDC-equivalent total via `eth_call` (keyless, no API key).
2. Point it at the same wallet on Solana — same tool, same single number.
3. Show a wallet with an illiquid/no-route token (LADYBUG/FUNLESS): the row is
   reported at **$0 and excluded** from the total. That is the point.

## Differentiator / falsifier
- Differentiator: honest accounting — illiquid bags never inflate the treasury.
- Kill it if: by ~Oct 8 there is no Monad wallet with a non-trivial USDC balance
  we can demo live, OR the Monad faucet/path to get a few USDC onto the chain is
  still not accessible. (We hold ETH/USDC on Base + USDC on Solana today; need a
  Monad-deployed balance for the strongest on-screen demo.)

## What unlocks / not blocked
This path needs **NO GitHub write token** (Colosseum's blocker). If the operator
funds a small amount of USDC onto Monad (or we self-bridge via a working rail),
the on-screen demo is fully live. This is the fleet's parallel route to the
Oct 13 deadline and does not depend on unblocking Github.
