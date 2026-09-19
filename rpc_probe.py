#!/usr/bin/env python3
"""rpc_probe — smoke-test free public Base/ETH RPCs (stdlib only, $0).

Reads rpcs.json next to this script (or --file), POSTs eth_chainId to each
HTTP endpoint, prints a live status table. Exit 0 if at least one OK per
requested chain (or overall if --chain all).
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

VERSION = "1.0.0"
HERE = Path(__file__).resolve().parent
DEFAULT_FILE = HERE / "rpcs.json"
UA = "free-rpc-map/1.0 (+https://github.com/filip-study/free-rpc-map)"


def load_map(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def eth_chain_id(url: str, timeout: float) -> tuple[str | None, str | None, float]:
    body = json.dumps(
        {"jsonrpc": "2.0", "id": 1, "method": "eth_chainId", "params": []}
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        ms = (time.perf_counter() - t0) * 1000
        if "error" in payload:
            err = payload["error"]
            if isinstance(err, dict):
                return None, str(err.get("message", err)), ms
            return None, str(err), ms
        return str(payload.get("result")), None, ms
    except Exception as e:  # noqa: BLE001 — surface any transport failure
        ms = (time.perf_counter() - t0) * 1000
        return None, f"{type(e).__name__}: {e}", ms


def main() -> int:
    p = argparse.ArgumentParser(
        description="Probe free public Base/ETH RPCs ($0, no API key).",
        epilog=(
            "Tip jar: https://shieldz.cash/tip/tip-d2599a4d16a6f4b0 · "
            "Unlock: https://shieldz.cash/unlock/NDS0MgohhA3PmPaBvmD0 · "
            "Treasury: 0xbAd41cF0f0d5442f9A53630F8081BFd257DA019b"
        ),
    )
    p.add_argument("--file", type=Path, default=DEFAULT_FILE, help="rpcs.json path")
    p.add_argument(
        "--chain",
        default="all",
        help="Chain key from rpcs.json (base, ethereum, …) or 'all'",
    )
    p.add_argument("--timeout", type=float, default=8.0)
    p.add_argument("--json", action="store_true", help="Machine-readable output")
    p.add_argument("--version", action="version", version=f"rpc_probe {VERSION}")
    args = p.parse_args()

    data = load_map(args.file)
    chains = data.get("chains") or {}
    if args.chain != "all" and args.chain not in chains:
        print(f"Unknown chain {args.chain!r}. Keys: {', '.join(chains)}", file=sys.stderr)
        return 2

    selected = (
        {args.chain: chains[args.chain]} if args.chain != "all" else chains
    )

    rows: list[dict] = []
    ok_by_chain: dict[str, int] = {k: 0 for k in selected}

    for name, meta in selected.items():
        expected = str(meta.get("hex") or "").lower()
        for url in meta.get("http") or []:
            got, err, ms = eth_chain_id(url, args.timeout)
            status = "ok"
            if err:
                status = "fail"
            elif expected and got and got.lower() != expected:
                status = "mismatch"
                err = f"expected {expected}, got {got}"
            if status == "ok":
                ok_by_chain[name] += 1
            rows.append(
                {
                    "chain": name,
                    "url": url,
                    "status": status,
                    "chainId": got,
                    "ms": round(ms, 1),
                    "error": err,
                }
            )

    if args.json:
        print(
            json.dumps(
                {
                    "version": VERSION,
                    "map_version": data.get("version"),
                    "ok_by_chain": ok_by_chain,
                    "results": rows,
                },
                indent=2,
            )
        )
    else:
        print(f"free-rpc-map probe v{VERSION} · map {data.get('version')}")
        print(f"{'CHAIN':<18} {'STATUS':<10} {'ms':>7}  URL")
        for r in rows:
            print(
                f"{r['chain']:<18} {r['status']:<10} {r['ms']:>7.1f}  {r['url']}"
                + (f"  ({r['error']})" if r["error"] and r["status"] != "ok" else "")
            )
        print()
        for name, n in ok_by_chain.items():
            total = len(selected[name].get("http") or [])
            print(f"  {name}: {n}/{total} OK")

    # Success if every selected chain has ≥1 OK
    if all(ok_by_chain[c] > 0 for c in selected):
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
