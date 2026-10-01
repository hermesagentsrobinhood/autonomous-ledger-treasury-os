#!/usr/bin/env python3
"""
FLEET EXECUTION TOOL — sol_wrap.py  (built by CEO 10-01)
Completes the SOL exit rail: wraps NATIVE SOL (lamports) -> wSOL on the CDP
signing wallet 84Bs6, so the proven wSOL->USDC Jupiter exit leg becomes usable.

WHY THIS EXISTS
  The Jupiter lite-api quotes wSOL(So111...112)->USDC cleanly, but NATIVE SOL
  (mint So111...111 = the lamport balance, not a real SPL mint) is rejected
  with TOKEN_NOT_TRADABLE. 84Bs6 holds its SOL as native lamports. So the ONLY
  mechanical barrier to a full SOL->USDC exit is wrapping those lamports into
  the wSOL associated token account first. This tool builds that wrap
  transaction (creating the wSOL ATA if absent) for CDP signing.
  The actual signature/broadcast happens through the CDP MCP
  (cdp_solana_accounts_send_transaction), never through this script.

Usage (build tx, no send):
  python3 fleet-tools/sol_wrap.py build <lamports>
Usage (verify wSOL ATA balance on 84Bs6):
  python3 fleet-tools/sol_wrap.py check
"""
import json, sys, base64, urllib.request

from solders.pubkey import Pubkey
from solders.hash import Hash
from solders.instruction import Instruction, AccountMeta
from solders.message import Message
from solders.transaction import Transaction
from solders.system_program import ID as SYS_PROGRAM, transfer as sys_transfer
from solders.system_program import TransferParams
from solders.system_program import create_account as sys_create
from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID
from spl.token.instructions import get_associated_token_address
from spl.token.instructions import create_associated_token_account

WALLET = Pubkey.from_string("84Bs6Gdbrg5XoSuUYVBtMzT1u8bT7svgufwzqLWMF5dP")
WSOL = Pubkey.from_string("So11111111111111111111111111111111111111112")
LAMPORTS_PER_SOL = 1_000_000_000
RPC = "https://api.mainnet-beta.solana.com"

def _rpc(method, params):
    payload = json.dumps({"jsonrpc":"2.0","id":1,"method":method,"params":params}).encode()
    req = urllib.request.Request(RPC, data=payload, headers={"Content-Type":"application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def ata_exists(ata):
    d = _rpc("getTokenAccountBalance", [str(ata)])
    return "result" in d

def wrap_message(lamports: int, recent_blockhash):
    wsol_ata = get_associated_token_address(WALLET, WSOL)
    ixs = []
    if not ata_exists(wsol_ata):
        ixs.append(create_associated_token_account(WALLET, WALLET, WSOL))
    # Transfer native lamports into the wSOL ATA -> token program wraps them.
    ixs.append(sys_transfer(TransferParams(
        from_pubkey=WALLET, to_pubkey=wsol_ata, lamports=lamports)))
    # syncNative so the wSOL token account reflects the wrapped balance.
    ixs.append(Instruction(program_id=TOKEN_PROGRAM_ID,
        accounts=[AccountMeta(wsol_ata, False, True)],
        data=b"\x11"))
    msg = Message.new_with_blockhash(ixs, payer=WALLET, blockhash=recent_blockhash)
    return msg, wsol_ata

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    op = sys.argv[1]
    if op == "check":
        wsol_ata = get_associated_token_address(WALLET, WSOL)
        print("WSOL ATA:", str(wsol_ata))
        d = _rpc("getTokenAccountBalance", [str(wsol_ata)])
        if "error" in d or "result" not in d:
            print("ATA does not exist yet -> no wSOL held (must create on wrap)")
        else:
            bal = d["result"]["value"]
            print(f"wSOL balance: {bal['uiAmountString']} SOL (raw {bal['amount']})")
        sys.exit(0)
    if op == "build":
        lamports = int(sys.argv[2])
        recent = _rpc("getLatestBlockhash", [])["result"]["value"]["blockhash"]
        msg, wsol_ata = wrap_message(lamports, Hash.from_string(recent))
        tx = Transaction.new_unsigned(msg)
        b64 = base64.b64encode(bytes(tx)).decode()
        print("BLOCKHASH:", recent)
        print("WSOL_ATA:", str(wsol_ata))
        print("LAMPORTS:", lamports, f"({lamports/LAMPORTS_PER_SOL:.4f} SOL)")
        print("TRANSACTION_BASE64:", b64)
        print("# Send: cdp_solana_accounts_send_transaction(network='solana', useCdpSponsor=true, transaction=b64)")
        sys.exit(0)
    print(__doc__); sys.exit(1)

if __name__ == "__main__":
    main()
