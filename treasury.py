#!/usr/bin/env python3
"""
Autonomous Ledger — a small onchain treasury reader for Solana + EVM chains.

Given one or more wallet addresses, it fetches SPL token / native balances and
marks them to USD via the CoinGecko price API, reporting a single
USDC-equivalent total. Pure stdlib + requests-less (urllib only). No keys.

This is the core of the fleet's own daily treasury reconciliation, released
as the hackathon MVP: a verifiable, dependency-light onchain finance tool.

Usage:
    python3 treasury.py <wallet> [wallet...]
    python3 treasury.py --sol <SOL address> --evm base 0x... --evm ethereum 0x...
"""
import json
import sys
import urllib.request

SOL_RPC = "https://api.mainnet-beta.solana.com"
USDC_MINT = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
WRAPPED_SOL = "So11111111111111111111111111111111111111111"
# Monad EVM network (Monad Metropolis hackathon track: Onchain Finance & Trading)
MONAD_RPC = "https://rpc.monad.xyz"                 # QuickNode-backed, ~25 rps
MONAD_USDC = "0x754704Bc059F8C67012fEd69BC8A327a5aafb603"  # Circle-native USDC on Monad
MONAD_CHAINID = 143
# CoinGecko ids for native tokens
NATIVE_IDS = {"SOL": "solana", "ETH": "ethereum", "MON": "monad"}
# SPL mints we recognize as USD-stable (illustrative; extend as needed)
USD_STABLES = {USDC_MINT: "USDC"}
KNOWN_SPL = {
    USDC_MINT: "USDC",
    WRAPPED_SOL: "SOL",
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC",
}


def rpc(url, method, params=None):
    body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": method, "params": params or []}).encode()
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=20))


def get_token_accounts(wallet):
    """Return {mint: amount(float)} for a Solana address's token accounts + native SOL."""
    out = {}
    try:
        res = rpc(SOL_RPC, "getTokenAccountsByOwner", [
            wallet,
            {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
            {"encoding": "jsonParsed"},
        ])
        for acc in res.get("result", {}).get("value", []):
            info = acc["account"]["data"]["parsed"]["info"]
            mint = info["mint"]
            amt = float(info["tokenAmount"]["uiAmountString"] or 0)
            out[mint] = out.get(mint, 0.0) + amt
    except Exception as e:
        print(f"  [token accounts error: {e}]", file=sys.stderr)
    try:
        lamports = rpc(SOL_RPC, "getBalance", [wallet])["result"]["value"]
        out[WRAPPED_SOL] = out.get(WRAPPED_SOL, 0.0) + lamports / 1e9
    except Exception as e:
        print(f"  [balance error: {e}]", file=sys.stderr)
    return out


BALANCE_OF = "0x70a08231"  # balanceOf(address) selector
DECIMALS = "0x313ce567"    # decimals() selector


def evm_call(to, data):
    """eth_call on Monad; returns raw 0x-hex result or raises."""
    res = rpc(MONAD_RPC, "eth_call", [{"to": to, "data": data}, "latest"])
    if "error" in res:
        raise RuntimeError(f"eth_call error: {res['error']}")
    return res.get("result", "0x0")


def hex_to_uint(hexstr):
    return int(hexstr, 16)


def evm_balance(network, address):
    """Read USDC (ERC20) + native MON balances for an address on Monad mainnet.

    Returns {kind: (amount_float, symbol)}.
    """
    out = {}
    addr = address[2:].lower().rjust(64, "0")
    # USDC balanceOf
    try:
        usdc_raw = evm_call(MONAD_USDC, BALANCE_OF + addr)
        usdc_amt = hex_to_uint(usdc_raw) / 1e6
        out["USDC"] = (usdc_amt, "USDC")
    except Exception as e:
        print(f"  [monad usdc error: {e}]", file=sys.stderr)
    # native MON
    try:
        mon_full = rpc(MONAD_RPC, "eth_getBalance", [address, "latest"])
        mon_amt = hex_to_uint(mon_full.get("result", "0x0")) / 1e18
        out["MON"] = (mon_amt, "MON")
    except Exception as e:
        print(f"  [monad balance error: {e}]", file=sys.stderr)
    return out


JUP_PRICE = "https://api.jup.ag/price/v2"

def price_usd(symbols):
    """symbols: list of COINGECKO ids -> {id: usd}. Uses cache-friendly simple/price."""
    ids = ",".join(sorted(set(symbols)))
    if not ids:
        return {}
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AutonomousLedger/0.1"})
        return json.load(urllib.request.urlopen(req, timeout=20))
    except Exception as e:
        print(f"  [price error: {e}]", file=sys.stderr)
        return {}


def jupiter_price_usd(mints):
    """Batch price arbitrary SPL mints via Jupiter Price API v2 (read-only, no key).

    Returns {mint: usd}. A mint absent from the response has NO live route on
    Jupiter and is treated as illiquid (excluded) — the honest-accounting core.
    """
    ids = ",".join(sorted(set(mints)))
    if not ids:
        return {}
    try:
        req = urllib.request.Request(
            f"{JUP_PRICE}?ids={ids}",
            headers={"User-Agent": "AutonomousLedger/0.1"},
        )
        data = json.load(urllib.request.urlopen(req, timeout=20))
        out = {}
        for mint, p in (data.get("data") or {}).items():
            price = float(p.get("price") or 0)
            if price > 0:
                out[mint] = price
        return out
    except Exception as e:
        print(f"  [jupiter price error: {e}]", file=sys.stderr)
        return {}


def main():
    sol_wallets = []
    evm = {}  # network -> (address, amount_usd_override) not used; keep simple
    for a in sys.argv[1:]:
        if a.startswith("0x"):
            evm[a] = None
        else:
            sol_wallets.append(a)

    prices = price_usd(["solana", "ethereum", "monad"])
    sol_price = (prices.get("solana") or {}).get("usd") or 0
    mon_price = (prices.get("monad") or {}).get("usd") or 0

    rows = []
    grand_total = 0.0

    all_accts = {}
    for w in sol_wallets:
        all_accts[w] = get_token_accounts(w)

    # Batch-price any SPL mint we don't already know, via Jupiter (route-to-USDC).
    unknown = set()
    for accts in all_accts.values():
        for mint in accts:
            if mint not in KNOWN_SPL and mint not in (WRAPPED_SOL,):
                unknown.add(mint)
    jup_prices = jupiter_price_usd(unknown)

    for w, accts in all_accts.items():
        sol_amt = accts.pop(WRAPPED_SOL, 0.0)
        sol_usd = sol_amt * sol_price
        rows.append((w, "SOL(native)", sol_amt, sol_usd))
        grand_total += sol_usd
        for mint, amt in accts.items():
            if mint == USDC_MINT:
                usd = amt
                label = "USDC"
            elif mint in KNOWN_SPL:
                usd = amt * sol_price if KNOWN_SPL[mint] == "SOL" else 0.0
                label = KNOWN_SPL[mint]
            else:
                p = jup_prices.get(mint, 0.0)
                usd = amt * p
                label = f"SPL {mint[:4]}.. (Jup)"
            rows.append((w, label, amt, usd))
            grand_total += usd

    # Monad EVM wallets
    for w in evm:
        bals = evm_balance("monad", w)
        for kind, (amt, sym) in bals.items():
            if kind == "USDC":
                usd = amt
            elif kind == "MON":
                usd = amt * mon_price
            else:
                usd = 0.0
            rows.append((w, f"{sym}(Monad)", amt, usd))
            grand_total += usd

    print("=" * 64)
    print("AUTONOMOUS LEDGER — treasury snapshot")
    print("=" * 64)
    for w, label, amt, usd in rows:
        print(f"  {label:16} {amt:>18,.6f}   ${usd:>12,.2f}   {w[:12]}...")
    print("-" * 64)
    print(f"  USDC-equivalent total:  ${grand_total:,.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
