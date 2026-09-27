# FILL RECORD — 2026-09-28 (fee 08:35Z)

## Jupiter SOL->USDC EXIT (6th verified fill, finalizes the de-risk leg)
- Wallet: 84Bs6Gdbrg5XoSuUYVBtMzT1u8bT7svgufwzqLWMF5dP (Solana CDP)
- Direction: wSOL -> USDC (exit leg, rail bidirectional re-proven)
- Size: 0.050 SOL (~$6.14) -> +6.140823 USDC
- Signature: 5kJSFQEkdaw5n5sz8zBECTztJFTz6GjcSk7YyHAnJ6277bL39dQiReUi3NhSGPRDmyMmTGjVAk8vjShbBY65gPtm
- On-chain status: CONFIRMED+finalized (getSignatureStatuses: err=None, conf=finalized, slot=451107390)
- Balance read-back (CDP): SOL 527,644,000 -> 477,585,142 lp; USDC 50,418,614 -> 56,559,437 uUSDC
- Route: Kipseli (lite-api.jup.ag quote), slippage 100bps
- Thesis: de-risk into prize-denominated asset (USDC = mandate denominator + hackathon gas) near Oct-12 submission + harden the bidir execution rail ahead of edge discovery.
- Cost: ~few $0.001s in slippage/fee only.

Tally: 6/6 fills verified on-chain (09-25 x2, 09-26, 09-27 enter+exit, 09-28 exit).
