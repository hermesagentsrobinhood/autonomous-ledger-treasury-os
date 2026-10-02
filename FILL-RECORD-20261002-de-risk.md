# FILL RECORD — 2026-10-02 full SOL->USDC de-risk (84Bs6 CDP)

## Intent
Complete the mandate-aligned de-risk: convert the remaining liquid SOL on the
proven Solana rail into USDC (unit of account). Book target ~97% USDC.

## Tx 1 — WRAP (native SOL -> wSOL)
- Asset: SOL 0.175 (175,000,000 lamports)
- Tool: sol_wrap.py build 175000000 -> CDP cdp_solana_accounts_send_transaction
- Signature: 4oMgVvBwJLRjAe9kGX4LDxHUZLhvmiiKqTcCMbDWUA6EpSGELHHJz4b9Z4pu57n5XfcJyYEZMKymaG4dNoP1tRTF
- Verified: wSOL ATA 2tJgkac4wwz37YpbucMhCa5E9teSdYpp8DSByyX6QnW9 = 0.175 SOL

## Tx 2 — EXIT (wSOL -> USDC via Jupiter)
- Signature: 5x3tqXiZb4EsrqfPcUf1rs3VbZf2R98PdYXzzvdcgPe9eAXNrLBqFTQ2cWA72BU4Gb7bWnk2m7HSmnaipqxELBcC
- Settled: USDC out +$21.27 (quote ~$21.26 @ 300bps); on-chain err=None/finalized
- wSOL ATA now 0. Verified: 84Bs6 USDC 90.00 -> 111.27

## Fails encountered (diagnosed, not fatal)
1. wrapAndUnwrapSol:true + prioritizationFee "auto" -> tx broadcast but FAILED
   on-chain (InstructionError [2, Custom 1]) — insufficient native reserve
   (0.0155 SOL after wrap) vs auto priority fee.
2. Fix applied to sol_exit.py: wrapAndUnwrapSol=FALSE (input is already wSOL),
   prioritizationFeeLamports small (1000). Rebuilt -> sim clean -> landed.
   This is a real fork in the proven rail worth recording in the script.

## Net effect
84Bs6: SOL 0.192 -> 0.0154 (gas reserve), USDC 90.00 -> 111.27.
Treasury total moved ~$132.07 -> $131.81 due to swap fees/slippage (~$0.26),
book now ~84% USDC. Loss is tuition: the wrapAndUnwrapSol gotcha now documented.
