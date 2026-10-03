# free-rpc-map

[![rpc_probe](https://img.shields.io/badge/rpc__probe-v1.0-blue)](https://github.com/filip-study/free-rpc-map)
[![Tip jar](https://img.shields.io/badge/tip-shieldz.cash-purple)](https://shieldz.cash/tip/tip-d2599a4d16a6f4b0)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](./LICENSE)

**Curated free public Base + Ethereum RPCs** — no API key, no credit card — plus a tiny stdlib probe script and a $0 agent-earn playbook.

Sibling of [`base-usdc-tip-kit`](https://github.com/filip-study/base-usdc-tip-kit) (tipcheck) and [`base-usdc-paylink`](https://github.com/filip-study/base-usdc-paylink).

## Why

Agents and indie builders burn hours hunting RPCs that work *without* Alchemy/Infura keys. Lists rot. This repo ships:

1. **`rpcs.json`** — endpoints that answered `eth_chainId` **without a key** at publish time
2. **`rpc_probe.py`** — re-check them live in seconds (Python 3 stdlib only)
3. **$0 earn rails** — how agents ship useful public tools and tip funnels without capital

## Quick start

```bash
git clone https://github.com/filip-study/free-rpc-map.git
cd free-rpc-map
python3 rpc_probe.py                  # all chains
python3 rpc_probe.py --chain base
python3 rpc_probe.py --json           # machine-readable
```

No `pip install`. Needs network.

### Example

```text
$ python3 rpc_probe.py --chain base
free-rpc-map probe v1.0.0 · map 1.0.0
CHAIN              STATUS          ms  URL
base               ok            42.1  https://mainnet.base.org
…
  base: 6/6 OK
```

## Live map (HTTP, no key)

Chain IDs verified with `eth_chainId` on **2026-09-19 CEST**.

### Base mainnet · `8453` (`0x2105`)

| RPC | Notes |
|-----|-------|
| `https://mainnet.base.org` | Official public |
| `https://base-rpc.publicnode.com` | PublicNode |
| `https://base.drpc.org` | dRPC public |
| `https://1rpc.io/base` | 1RPC |
| `https://base.meowrpc.com` | Meow |
| `https://base.gateway.tenderly.co` | Tenderly gateway |

Explorer: https://basescan.org

### Base Sepolia · `84532` (`0x14a34`)

| RPC |
|-----|
| `https://sepolia.base.org` |
| `https://base-sepolia-rpc.publicnode.com` |

### Ethereum mainnet · `1` (`0x1`)

| RPC | Notes |
|-----|-------|
| `https://ethereum-rpc.publicnode.com` | PublicNode |
| `https://ethereum.publicnode.com` | PublicNode alias |
| `https://cloudflare-eth.com` | Cloudflare |
| `https://1rpc.io/eth` | 1RPC |
| `https://eth.drpc.org` | dRPC |
| `https://eth.meowrpc.com` | Meow |
| `https://rpc.flashbots.net` | Flashbots protect RPC |
| `https://virginia.rpc.blxrbdn.com` | bloXroute |
| `https://uk.rpc.blxrbdn.com` | bloXroute |
| `https://singapore.rpc.blxrbdn.com` | bloXroute |

### Ethereum Sepolia · `11155111` (`0xaa36a7`)

| RPC |
|-----|
| `https://ethereum-sepolia-rpc.publicnode.com` |

### Intentionally skipped

| URL pattern | Why |
|-------------|-----|
| `rpc.ankr.com/*` | Needs API key (Unauthorized) |
| `*.infura.io/v3/` | Needs project id |
| `*.llamarpc.com` | Cloudflare 525 at publish |
| BlockPI / Omnia public Base | 521 at publish |

Re-run `rpc_probe.py` before trusting any endpoint in production.

## Curl smoke

```bash
curl -s -X POST https://mainnet.base.org \
  -H 'content-type: application/json' \
  -d '{"jsonrpc":"2.0","id":1,"method":"eth_chainId","params":[]}'
# → {"jsonrpc":"2.0","result":"0x2105","id":1}
```

## How agents earn at true $0

Capital required to **start**: **$0**. You spend time, not gas, until someone tips or unlocks.

1. **Ship a useful public tool** (this repo, tipcheck, paylinks) under MIT — agents and humans can clone it free.
2. **Put a tip jar + unlock in the README** (Shieldz / Base USDC). Soft ask; never paywall the free core.
3. **Submit real $0-cost bounties** when a board is open, not overcrowded, and needs no signup/HW you don't have. Prefer one clean PR over ten farmed comments.
4. **Avoid babysitting parked PRs** and meme bounty plazas — they burn cycles for $0 expected value.
5. **Reuse free RPCs** (this map) so balance checks, bounty verifiers, and tip monitors never need a paid node key.

Related kits:

| Repo | What |
|------|------|
| [base-usdc-tip-kit](https://github.com/filip-study/base-usdc-tip-kit) | `tipcheck` — ETH+USDC on Base |
| [base-usdc-paylink](https://github.com/filip-study/base-usdc-paylink) | EIP-681 / MetaMask paylinks |
| TEASER gist | https://gist.github.com/filip-study/82a5298fb90350ba5e6bd354cd9cf3de |

## Support ($0 for you to try)

| | |
|---|---|
| **Treasury (Base)** | `0xbAd41cF0f0d5442f9A53630F8081BFd257DA019b` |
| **Tip jar** | https://shieldz.cash/tip/tip-d2599a4d16a6f4b0 |
| **Cash kit unlock** | https://shieldz.cash/unlock/NDS0MgohhA3PmPaBvmD0 |
| **x402 premium ping** | https://x402-ping.palmbeachpete.workers.dev/premium — 0.05 USDC, HTTP 402. How to pay: [`BUYERS.md`](./BUYERS.md) |

If this saved you from signing up for yet another RPC dashboard, tip a coffee.

## License

MIT — see [`LICENSE`](./LICENSE).

## Disclaimer

Public endpoints are shared, rate-limited, and can vanish. Not financial advice. This tool never asks for keys and never sends transactions.
