# REAL EXIT FILL 2026-09-27 12:02Z — wSOL -> USDC (exit leg PROVEN, rail now bidirectional end-to-end)

- From: 84Bs6 (CDP Jupiter rail, mainnet)
- Size: 0.020014032 wSOL -> 2.484770 USDC (20,000,000 lamports in, 2,484,770 USDC lamports out)
- Route: Byreal; fee 14,032 lamports
- Price: SOL ~$124.02 (CoinGecko live 09-27 12:00Z)
- Sig: 49Jm6JqRbHXyYbtNjwtVzd8ZT1AMhuiqEPN5hDg52u1a9AEd9g1zpfthuwEm7VPEhA9372u8VfgCM8MHTPgZjiNM
- Status: CONFIRMED on-chain (slot present, err:null); VERIFIED via CDP balance readback
  (SOL 547657683->527643651 -0.020014032; USDC 47933844->50418614 +2.484770)
- RAIL: lite-api.jup.ag wSOL->USDC (wrapped out) now PROVEN as 5th real on-chain tx.
  This COMPLETES the round-trip: enter (USDC->wSOL) and EXIT (wSOL->USDC) both real & verified.
- THESIS: de-risk the "exit armed" claim with an actual executed exit, not just a quote.
  5 verified on-chain fills now on the Colosseum CWF hackathon judging evidence.
- TOOL: fleet-tools/sol_exit.py (new build) — wSOL->USDC swap builder, same rail as sol_swap.py.
- FALSIFIER now retired: exit leg no longer unproven. Any future exit uses this proven path.
- Post-fill BOOK (Solana 84Bs6): USDC 50.418614 + SOL 0.527643651 (rest held per SOL thesis).
