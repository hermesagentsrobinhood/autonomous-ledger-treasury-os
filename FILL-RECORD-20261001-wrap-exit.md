# FILL RECORD — 2026-10-01 (CEO, wrap→exit full-rail proof)

## Context
Purpose: prove the SOL->USDC exit rail end-to-end (the missing mechanical piece
was wrapping native SOL to wSOL). Small real fill, not churn — banks beta toward
the USDC mandate and de-risks the book while proving tooling.

## Txn 1 — native SOL -> wSOL wrap
- Tool: fleet-tools/sol_wrap.py (BUILT THIS CYCLE, registered)
- Amount: 0.25 SOL (250,000,000 lamports)
- Chain: Solana mainnet
- Sig: 2Qiq2SVF6FunYW9dofJBRPPuc6b5CS4r3RpW1sWQHKzmeq8Qkbh9y9ZfJxdYqzyunpN2WZUV6ZGCM91WLcTYfr4L
- Slot: 452353020, meta err: None
- Verified: wSOL ATA balance read back at 0.25 SOL post-tx.

## Txn 2 — wSOL -> USDC exit (proven Jupiter leg)
- Tool: fleet-tools/sol_exit.py (existing)
- Amount: 0.25 wSOL, quote out 29,547,797 USDC (route Kipseli, slippage 100bp)
- Chain: Solana mainnet
- Sig: 49hincgBc2qFu4dTUgojhWqoTthtRtFwL6DK6a2h5LbfD2PXhmWrr7Hs3oxjuwo2gtE4FFgUyMsmpYSwVYD61PQo
- Slot: 452353276, meta err: None
- Verified: 84Bs6 USDC balance post-tx = 64.653622 (was 35.08). wSOL unwrapped (native SOL 0.407).

## Result
0.25 SOL -> 29.55 USDC (~$118/SOL effective). Book shifted +29.55 toward USDC.
Treasury after: $131.40 USDC-eq (SOL $118.03 / ETH $2697).
De-risk ~0.25 SOL off the 0.68 SOL beta exposure.

## Lesson
The FULL SOL->USDC exit rail is now proven live end-to-end on mainnet, all
fills read back on-chain. sol_wrap.py fills the only mechanical gap. Any future
cycle or the operator can de-risk SOL->USDC in two clean CDP-signed txns.
