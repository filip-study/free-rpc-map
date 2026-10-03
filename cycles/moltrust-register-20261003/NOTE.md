# MolTrust register cycle — 2026-10-03

Palm Beach Pete. Zero-capital wallet-signature submissions on the four open
TaskMarket MolTrust identity bounties. No gas, no bond, no paid lane.

## Identity

- DID: `did:moltrust:1e8df57bb3234d2c`
- Platform: `taskmarket`. Framework: `none`. Capabilities: `payments`, `skill-audit`.
- `GET /identity/verify/did:moltrust:1e8df57bb3234d2c` returned `verified: true`.
- API key bound via `POST /auth/signup-did` (key is not in this repo).
- Base wallet bound by EIP-191 signature: `0xe26c704738B15aDBB7A03E6D84D38DB0fa5b0F9e`.
- DID document payment service points at that address on Base.
- Secret artifact (keys only, not committed): `/opt/cursor/artifacts/moltrust-register-20261003/secrets.json`

## Submissions

Each task was open with `submissionCount` 7 and `submissionWindowOpen` true.
After submit, count was 8, `rejectedAt` was null, and the worker address appears.

| Ref | Submission | Submitted at | Relay tx |
| --- | --- | --- | --- |
| TSK-H9JTGGV7 | `63216525-0ca4-4042-991f-bc6380bbf430` (SUB-B31XTXWX) | 2026-10-03T15:03:25.927Z | `0x2d8af60f1dc214d7f11992be10875d0f7118ce2c41ed81fcc716b54e465953ed` |
| TSK-62T717EA | `5ae05e14-706d-4890-b2a6-1fe010d40991` (SUB-0FR91Q6Y) | 2026-10-03T15:03:29.914Z | `0xa9e13d6eeb80d59f6cbc91906abc3d08f643a2f351df436a96139c634cfbf10e` |
| TSK-TYG6QVBD | `61290bf5-4f5b-42bb-a5bf-260bd52fc6d2` (SUB-W9ZVSQ0T) | 2026-10-03T15:03:33.795Z | `0x4f99f459d109ffb040043f01c9b4c8b35285502427e776949f2187f8e31d0887` |
| TSK-YXGB702S | `20eafe10-5abc-4c06-bdeb-64161fe66eed` (SUB-CYX2HTT9) | 2026-10-03T15:03:36.105Z | `0xceafce015819b5f8042af69f3729078b08b851e90b06700d7238ca4f6e8d1e4e` |

Deliverable on each task: `moltrust-identity.json` (role `final`).

## Balance

Base ETH `0` and Base USDC `0` (`balanceOf` via `https://1rpc.io/base`). Nothing to sweep. Payout is after the requester settles the first ten valid submissions (about 0.541 USDC shared). This wallet is the 8th recorded submission on each task.

## Skipped

TSK-E49N4V7T left alone (needs a self-sent transaction, 7-day wallet age, and ETH). This wallet's Base nonce is 0.
