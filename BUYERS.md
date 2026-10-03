# Where a buyer pays

The RPC probe in this repo stays free. These are the live ways to pay the treasury `0xbAd41cF0f0d5442f9A53630F8081BFd257DA019b` on Base (chain id 8453). Checked 2026-10-03.

## Unlock the premium ping (0.05 USDC)

1. `GET https://x402-ping.palmbeachpete.workers.dev/premium`
2. The worker answers **HTTP 402**. The body and the `PAYMENT-REQUIRED` header (base64 JSON) both say: scheme `exact`, network `eip155:8453`, amount `50000` (0.05 USDC), asset `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, `payTo` the treasury above.
3. Pay that authorization, then retry the same URL with the `X-PAYMENT` or `PAYMENT-SIGNATURE` header.

Free discovery, no payment:

| URL | What it is |
|---|---|
| https://x402-ping.palmbeachpete.workers.dev/openapi.json | Free JSON. Names `/premium` as the paid route. |
| https://x402-ping.palmbeachpete.workers.dev/.well-known/x402 | Service manifest. Resource is `/premium` at 0.05 USDC. |
| https://x402-ping.palmbeachpete.workers.dev/ | Same free discovery document as `/openapi.json`. |

## Directory listing

Registered 2026-10-03 with one `POST https://agent402.tools/api/index/register` and body `{"origin":"https://x402-ping.palmbeachpete.workers.dev"}`. No account. The crawler read `/.well-known/x402` and probed `GET /premium`.

Public record: https://agent402.tools/api/index?seller=x402-ping.palmbeachpete.workers.dev

That record shows `displayName` `x402-ping`, one tool (`GET /premium`, `$0.05`, `eip155:8453`), `payTo` the treasury, `routable: true`, `health: 1`, `lastVerifiedAt` `2026-10-03T01:37:10.760Z`.

The same record sets `routerDispatchEligible` to false with reason `settlement_required` ("below the settlement floor"). A buyer can still pay `/premium` directly. Agent402's router will not send the call until the origin has settlement history above that floor.

## Other ways to pay the same treasury

| Path | What it is |
|---|---|
| https://shieldz.cash/tip/tip-d2599a4d16a6f4b0 | Tip jar. Any amount. |
| https://shieldz.cash/unlock/NDS0MgohhA3PmPaBvmD0 | Cash-kit unlock. |

Nothing here paywalls `rpc_probe.py` or `rpcs.json`.
