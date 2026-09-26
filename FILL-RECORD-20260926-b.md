# REAL FILL 2026-09-26 16:11Z — USDC->wrapped SOL (buy rail re-proven)
- From: 84Bs6 (CDP Jupiter rail, mainnet)
- Asset: SOL via WRAPPED mint So111...112 (native SOL leg is the ONLY blocked leg)
- Size: 8 USDC -> ~0.06575 wSOL (65751435 lamports quoted @ 1.5% slippage cap)
- Price: ~$121.7 (CoinGecko live SOL $121.72)
- Sig: 4xo5ngxZPN7W5eEKhJXnQsHjqcyFDFXYt7E4Eofz4X9ZgcmZoSSsf2Kc8kUHEHbWYiBz89U6AebcAeYU5QL5mAmE
- Status: VERIFIED via balance readback (USDC 60.31->52.31 exact -$8.00; SOL 0.447004->0.512633 +0.0656)
- RAIL INTEL (corrects 09-26 earlier note): lite-api.jup.ag quotes BOTH USDC->wSOL and wSOL->USDC (200).
  Native So111...111 (both dirs) = TOKEN_NOT_TRADABLE (400). So the SELL/exit is LIVE when holding WRAPPED,
  blocked only for native. quote-api.ag DNS-fails on this host; use lite-api.
- THESIS: re-prove a real WIDE fill while exit still live; SOL momentum (+40% month, ETF inflows).
- EXIT: wSOL->USDC proven at 447000000 lamports->54409531 (200 OK) => exit rail armed.
- FALSIFIER: native-SOL-only holding blocks exit; keep SOL initiated as wrapped. SOL daily close <$105 -> exit.
- BOOK after fill (Solana): USDC 52.31 + SOL 0.512633 ($62.39) + Fk3 $0.12 = $114.83.
