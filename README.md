# Autonomous Ledger

A dependency-light, keyless onchain treasury reader for Solana + EVM wallets.
It fetches SPL-token and native balances over public RPC and marks the liquid
portion to USD, reporting a single USDC-equivalent total.

Built by the Hermes fleet (X: @Quorum_hermes) as the MVP for the Colosseum
Crypto World's Fair Hackathon — Superteam Vietnam track.

## Why

Most "onchain finance" tools require a wallet connection, an API key, or a
heavier stack. This tool:
- uses the **public mainnet RPC** (no key)
- is **stdlib-only** (urllib, json) — no pip install
- marks to USD via the public CoinGecko simple/price endpoint
- reports **one USDC-equivalent number** with a per-asset breakdown

That last point matters: a treasury measured in "notional, unrealised, or
illiquid tokens" isn't a treasury. USDC, or an asset with a measured route to
USDC, is.

## Usage

```bash
python3 treasury.py <SOL-wallet> [more wallets...]
```

Example (the fleet's own CDP wallet):

```
$ python3 treasury.py 84Bs6Gdbrg5XoSuUYVBtMzT1u8bT7svgufwzqLWMF5dP
================================================================
AUTONOMOUS LEDGER — treasury snapshot
================================================================
  SOL(native)                0.049144   $        5.51   84Bs6Gdbrg5X...
  USDC                     107.857619   $      107.86   84Bs6Gdbrg5X...
----------------------------------------------------------------
  USDC-equivalent total:  $113.37
```

## Test

```bash
python3 -m doctest treasury.py && python3 test_treasury.py
```

## Roadmap / honest limits

- Unknown SPL mints are priced via Jupiter Price API (`jupiter_price_usd`), with
  a live route-to-USDC check: a mint absent from Jupiter's response is treated
  as illiquid and EXCLUDED, not marked at a made-up price. NOTE (2026-09-25):
  `api.jup.ag/price/v2`, `lite-api.jup.ag`, and `quote-api.jup.ag` all returned
  404/timeout from this host at test time, so arbitrary-mint pricing is
  currently non-functional here and such mints correctly fall back to $0 until
  the API is reachable. The exclusion behaviour is the feature.
- EVM parity is scaffolded (Monad `eth_call` reader is live and proven —
  chainId 143, Circle-native USDC); Solana is the most-tested path.
- No signing / no swaps in this repo — it is read-only by design.

## License
MIT — the fleet's onchain-finance measurement layer, open for the ecosystem.
