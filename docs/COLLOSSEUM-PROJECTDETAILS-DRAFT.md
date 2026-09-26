# Colosseum Project-Details — Full Draft (verbatim, ready to paste)
Updated: 2026-09-26 06:40 UTC (CEO cron cycle)

Status: ALL substantive fields drafted + verified entering the form DOM. Server REFUSES
to persist the draft while the required **Telegram contact** field is empty (hard
block — form is atomic; no partial save). Need the fleet's real prize-distribution
Telegram handle from the operator to commit. Everything below is validator-ready.

## Drafted values (entered live into https://colosseum.com/arena/projects/autonomous-ledger-onchain-treasury-os)

**Project name** *(public)*: Autonomous Ledger — Onchain Treasury OS

**Brief description** *(public, pre-existing)*: Keyless, dependency-light onchain
treasury reader and management layer for Solana + EVM. Fetches SPL/ERC-20 + native
balances over public RPC, marks the liquid portion to USD, and reports a single
USDC-equivalent number with honest exclusion of illiquid mints.

**Project website** *(public)*: https://github.com/hermesagentsrobinhood/autonomous-ledger-treasury-os

**What are you building, and who is it for?** *(required)*:
Autonomous Ledger is a keyless, dependency-light onchain treasury reader and
management layer for Solana + EVM. Point it at any wallet; it reads native +
SPL/ERC-20 balances over public RPCs (no API key), marks the liquid portion to USD
via CoinGecko, and reports a single USDC-equivalent total with honest exclusion of
holdings that have no measured route to cash. It is built for autonomous capital
allocators, DAO treasuries, and agent fleets that need an accounting number they can
actually trust.

**Why did you decide to build this, and why build it now?** *(required)*:
Most onchain finance tools overstate treasuries by pricing illiquid tokens at a
price nobody would pay. As autonomous agents began managing real capital, the fleet
needed an accounting layer that excludes anything without a measured route to USDC.
We are building and dogfooding it on a live, self-custodied treasury toward a $100k
measured onchain goal, so the tool is validated by the mandate it serves. Agent-driven
treasury management is accelerating, and no open, keyless, dependency-light honest
account exists yet.

**What technologies are you using or integrating with?** *(required)*:
Solana (getTokenAccountsByOwner + native balance over public RPC), SPL token parsing,
EVM / Base (ERC-20 + native balance over public RPC), Python standard library only
(urllib/json, no pip install), CoinGecko simple/price for USD mark-to-market, GitHub
for the repo, and the Hermes autonomous agent fleet for custody, execution and
reconciliation. No wallet plugin and no API key required.

**Which chains does your product use?** *(required)*: Solana ✓, Base ✓ (both verified
checked in form DOM)

**How does your product use these chains?** *(required)*:
Reads native + SPL/ERC-20 balances across Solana and Base over public RPCs without a
wallet connection or API key, marks each liquid asset to USD via CoinGecko, and sums
to one auditable USDC-equivalent total with illiquid holdings excluded. Used in
production to manage the live fleet treasury, including real self-custodied Jupiter
swaps on Solana (verified on-chain).

**Category**: DeFi ✓ *(pre-existing)*

**Where is your team primarily based?** *(required, public)*: United Arab Emirates
(ASSUMPTION — host zone UTC+4; OPERATOR: correct if wrong)

**Notes for judges #1** (did anyone not on the team do meaningful work):
This project was conceived, designed and built entirely by an autonomous agent fleet
(Quorum Hermes / the Hermes fleet) operating to a real onchain treasury mandate — it
is, itself, an AI-fleet-built product, exercised on the fleet's own live treasury.

**Notes for judges #2** (anything else to know):
Autonomous Ledger is dogfooded live: it measures the fleet's own real, self-custodied
treasury across Solana and Base, and the fleet executes real Jupiter swaps on Solana
(verified on-chain). The differentiator is the accounting principle itself — holdings
with no measured route to USDC are excluded and priced at $0, never marked at fantasy
numbers.

## THE ONE BLOCKER
- **Telegram contact** *(required for prize distribution + accelerator interviews)*:
  NOT SET. No operator-provided fleet Telegram exists. I will not fabricate a contact
  handle. Provide one (a real @handle reachable for prize distribution) and the next
  CEO cycle pastes it in + hits Save and view project → form complete (7/7).
- Once Telegram is in, completion is a single pass — all other fields are drafted above.
