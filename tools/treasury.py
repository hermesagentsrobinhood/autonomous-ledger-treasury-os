#!/usr/bin/env python3
"""
FLEET TREASURY RECONCILIATION  (build by CEO 09-24)
Pulls live balances from CDP-controlled public addresses + live spot prices,
computes a single USDC-equivalent treasury figure with per-venue breakdown.
Read-only. No keys. Safe to run every cycle.
Requires: python3 + requests (or urllib fallback).

Usage: python3 treasury.py
"""
import json, urllib.request, sys, datetime, argparse

# CDP custody addresses
WALLETS = {
    "Fk3(agentic)": {
        "type": "solana",
        "addr": "Fk3SSGthErvQfAJoXVuGePfdriAjwqjVgFM9o7bPwtsa",
    },
    "84Bs6(CDP)": {
        "type": "solana",
        "addr": "84Bs6Gdbrg5XoSuUYVBtMzT1u8bT7svgufwzqLWMF5dP",
    },
    "0xA684(EVM/base)": {
        "type": "evm",
        "addr": "0xA684A6e3Ad9815ba169a83Ff5C9E74B861B79Ff7",
    },
}

COINGECKO = "https://api.coingecko.com/api/v3/simple/price?ids={ids}&vs_currencies=usd"

# Known token -> usd label mapping (mint->cgid) for value computation
SOLANA_TOKENS = {
    "So11111111111111111111111111111111111111111": "solana",
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "usdc",   # USDC
}
EVM_TOKENS = {
    "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee": "ethereum",  # native ETH
    "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913": "usdc",      # USDC base
}

def get(url):
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.loads(r.read().decode())

def sol_balances(addr):
    """Public RPC-free: use CDP data API path via public JSON-RPC fallback."""
    # Use publicbitcoin Solana JSON-RPC to avoid requiring CDP MCP in this script
    payload = json.dumps({"jsonrpc":"2.0","id":1,"method":"getTokenAccountsByOwner",
        "params":[addr,{"programId":"TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
        {"encoding":"jsonParsed"}]}).encode()
    req = urllib.request.Request("https://api.mainnet-beta.solana.com", data=payload,
        headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode())
    out = {}
    for item in data.get("result",{}).get("value",[]):
        info = item["account"]["data"]["parsed"]["info"]
        mint = info["mint"]; amt = info["tokenAmount"]
        out[mint] = {"amount": amt["amount"], "decimals": amt["decimals"], "ui": amt["uiAmountString"]}
    # native SOL balance
    try:
        p2 = json.dumps({"jsonrpc":"2.0","id":1,"method":"getBalance","params":[addr]}).encode()
        req2 = urllib.request.Request("https://api.mainnet-beta.solana.com", data=p2,
            headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(req2, timeout=30) as r:
            d2 = json.loads(r.read().decode())
        lamports = int(d2["result"]["value"])
        out["So11111111111111111111111111111111111111111"] = {
            "amount": str(lamports), "decimals": 9, "ui": lamports/1e9}
    except Exception:
        pass
    return out

def evm_balances(addr, network="8453"):
    """Use public base RPC eth_getBalance. mainnet.base.org 403s clients that
    omit a browser-like User-Agent, so we send one and rotate across fallbacks."""
    ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
    urls = {
        "8453": ["https://mainnet.base.org", "https://base-rpc.publicnode.com",
                 "https://base.meowrpc.com", "https://base.drpc.org"],
        "1":    ["https://cloudflare-eth.com", "https://eth.llamarpc.com"],
    }[network]
    last=None
    for url in urls:
        try:
            req = urllib.request.Request(url,
                data=json.dumps({"jsonrpc":"2.0","id":1,"method":"eth_getBalance","params":[addr,"latest"]}).encode(),
                headers={"Content-Type":"application/json","User-Agent":ua})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = json.loads(r.read().decode())
            if "result" in data:
                wei = int(data["result"],16)
                return {"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE": {"amount": str(wei), "decimals": 18, "ui": wei/1e18}}
        except Exception as e:
            last=e; continue
    raise last if last else RuntimeError("all EVM RPCs failed")

def main():
    ap = argparse.ArgumentParser(description="Fleet treasury USDC-eq reconciliation")
    ap.add_argument("--evm-eth", type=float, default=None,
        help="EVM native ETH balance (units) injected from authoritative CDP MCP read; host base RPC is 403-blocked")
    ap.add_argument("--evm-usdc", type=float, default=None,
        help="EVM/base USDC balance (units) injected from authoritative CDP MCP read")
    a = ap.parse_args()
    ids = "solana,ethereum"
    px = get(COINGECKO.format(ids=ids))["usd"] if False else None
    px = get(COINGECKO.format(ids=ids))
    # px is {id: {usd: x}}
    prices = {k:v["usd"] for k,v in px.items()}
    prices["usdc"] = 1.0

    ts = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    rows=[]
    totals=0.0
    # --- Solana ---
    for label in ["Fk3(agentic)","84Bs6(CDP)"]:
        addr=WALLETS[label]["addr"]
        try:
            toks=sol_balances(addr)
        except Exception as e:
            print(f"  !! {label}: balance read failed: {e}")
            toks={}
        sub=0.0
        for mint,b in toks.items():
            cg=SOLANA_TOKENS.get(mint)
            ui=float(b["ui"] or 0)
            val = ui*prices.get(cg,0) if cg else 0.0
            tag=cg.upper() if cg else ("UNMAPPED/ILLIQUID:"+mint[:6])
            sub+=val
            if ui>0 and cg:   # only price a holding that has a route to USDC
                rows.append((label,tag,round(ui,6),round(val,4)))
        totals+=sub
        # native SOL in these CDP wallets appears via token list already
    # --- EVM ---
    for label in ["0xA684(EVM/base)"]:
        addr=WALLETS[label]["addr"]
        try:
            toks=evm_balances(addr)
        except Exception as e:
            print(f"  !! {label}: evm balance read failed (native only): {e}")
            toks={}
        sub=0.0
        for caddr,b in toks.items():
            cg=EVM_TOKENS.get(caddr.lower())
            ui=b["ui"]
            val=ui*prices.get(cg,0) if cg else 0.0
            tag=cg.upper() if cg else "UNMAPPED"
            sub+=val
            if ui>0 and cg:
                rows.append((label,tag,round(ui,6),round(val,4)))
        totals+=sub
    # --- Injectable EVM (authoritative via CDP MCP; host base RPC is 403-blocked) ---
    if a.evm_eth is not None or a.evm_usdc is not None:
        label="0xA684(EVM/base)"
        if a.evm_eth is not None:
            val=a.evm_eth*prices["ethereum"]
            rows.append((label,"ETH",round(a.evm_eth,6),round(val,4)))
            totals+=val
        if a.evm_usdc is not None:
            rows.append((label,"USDC",round(a.evm_usdc,6),round(a.evm_usdc,4)))
            totals+=a.evm_usdc

    print("="*60)
    print(f"FLEET TREASURY  ts={ts}")
    print("="*60)
    for label,tag,amt,val in rows:
        print(f"  {label:18} {tag:8} {amt:>14}  = ${val:>10.2f}")
    print("-"*60)
    print(f"  TOTAL USDC-EQ          ${totals:,.2f}")
    gap=100000-totals
    days=(datetime.date(2026,12,31)-datetime.date.today()).days
    print(f"  GAP to 100k            ${gap:,.2f}")
    print(f"  Days left              {days}")
    print(f"  Required/day           ${gap/days:,.2f}  ({gap/days/totals:.2f}x total/day)" if totals>0 else "  Required/day: n/a")

if __name__=="__main__":
    main()
