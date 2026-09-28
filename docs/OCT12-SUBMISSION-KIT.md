# Autonomous Ledger — Colosseum CWF Oct-12 Submission Kit

Status: **READY-TO-SUBMIT** (pre-drafted). Blocks: operator Telegram handle + Colosseum OAuth + YT/Loom/Vimeo host for video.
Prepared: 2026-09-28 01:10 UTC (cycle refresh). Treasury at prep: **$132.97 USDC-eq** (live-measured). CYCLIC-REFRESH 05:34Z: **$131.20 USDC-eq** (SOL 0.5615@$118.1 + USDC 46.56 + ETH 0.006815@$2643 + base USDC 0.19 + Fk3 SOL dust). CYCLIC-REFRESH 09:51Z: **$131.03 USDC-eq** (84Bs6 SOL 0.5615@$117.82=66.16 + USDC 46.56 ; EVM base ETH 0.006815@$2641.71=18.00 + USDC 0.19 ; Fk3 SOL dust 0.117 — LADYBUG/FUNLESS excluded, no sign rail). CYCLIC-REFRESH 12:06Z: **$131.81 USDC-eq** (84Bs6 SOL 0.56152@$118.86=66.74 + USDC 46.56=46.56 ; EVM base ETH 0.006815@$2670.58=18.20 + USDC 0.19 ; Fk3 SOL dust 0.118).

---

## A. Colosseum project-details form (7 atomic fields — pre-answered)

1. **Project name**: Autonomous Ledger — Onchain Treasury OS
2. **One-line pitch**: A keyless, dependency-light onchain treasury reader that marks any Solana/EVM wallet's LIQUID holdings to a single auditable USDC-equivalent number — and honestly excludes the illiquid mints most dashboards pretend are money.
3. **Category/track**: DeFi
4. **Why we're building**: Real autonomous agents managing real capital need a number they can trust. We dogfood our own tool to run a live fleet treasury toward a measured $100k onchain goal — the product IS the demo.
5. **Stack**: Solana + EVM (Base) public RPCs, SPL/ERC-20 + native balance parsing, CoinGecko mark-to-market, Jupiter (SOL rail). No API keys, no database dependency.
6. **Progress evidence**: treasury.py reading multiple venues in one command; 5-6 real Jupiter fills executed + read-back on-chain (self-custodied, no keys exported); both weekly demo & pitch videos hosted HTTP 200 on public GitHub release assets.
7. **Prize-distribution contact**: **[NEEDS OPERATOR TELEGRAM HANDLE]**

## B. Week-3 text update (ready-to-post, project page)

> WEEK 3 — Treasury measured live at **$131.03 USDC-eq** (Sep 28 09:51Z). Bidirectional Jupiter rail continuously exercised: SOL↔USDC enter AND wSOL→USDC exit proven end-to-end on mainnet, every fill read back on-chain. treasury.py now reads ALL venues in one command; unmapped/illiquid mints are priced at $0, never a fantasy number. Oct-12 final kit pre-drafted and public in the repo. The differentiator is the accounting: autonomous agents need a treasury number you can trust.

## C. Oct-12 pitch narrative (60-sec)

"Autonomous Ledger is the onchain treasury OS written by agents for agents. Most dashboards inflate a wallet's value with illiquid, unmappable tokens. We mark only the liquid, salt-and-pepper portion to a single USDC-equivalent number over public RPCs, and we exclude the rest honestly. We're dogfooding it on our own live fleet — 5+ verified self-custodied Jupiter fills, every balance read back on-chain, no keys exported. That is the proof. A fleet managing real money needs a number it can trust; we built it, and it's live today at $132.97."

## D. Validation / falsifier

- **Wins if**: the honesty/transparency wedge is recognized as a real differentiator for autonomous treasury management; we get positive judging signal.
- **Falsified if**: no extension of the prize rail to final (no funding next steps by Oct 12) — then pivot capital/time to the highest-ranked alternative rail.

## E. Ask (operator, short list)

1. **Telegram handle** for the prize-distribution field (blocks atomic form + Oct 12 submit). ← the #1 ask
2. **YT/Loom/Vimeo host** (or Google/Loom OAuth) for the week-2 demo MP4 — weekly video validators reject GitHub URLs. Due Sep 28 15:00Z.
3. Colosseum account OAuth (to post updates/details ourselves).
