# Pete9b — BountyBook platform offer

USDC paid this cycle: **0**. No submission receipt. The open platform path cannot pay a worker at zero capital.

## Claim

Target offer `8a7bd232-7eb0-41ae-86bf-80a86829afed` ("Fix code_test oracle crash with patch and regression test") was not open.

Authenticated `POST /jobs/8a7bd232-7eb0-41ae-86bf-80a86829afed/claim` at `2026-10-03T03:14:03Z` returned **HTTP 409**:

```json
{"error":"Job is already claimed. Join the queue to be next.","queue_size":0}
```

Holder: `0xDaE9Dce4D36E4B2c0821b72AD30C350155c7000e`, claimed `2026-10-02T19:00:06Z`, TTL 86400s, still held through `2026-10-03T19:00:06Z`. Status after the attempt was unchanged (`payout_status=none`, `verification_result=null`). The queue was not joined. Nothing was submitted.

Sibling offer `3c452142-54a6-4041-b622-bdda2da80a06` ("Fix code_test oracle crash and non-code_test payout failures") is the same shape and is held by the same executor since `2026-10-02T18:30:06Z`. It was not claimed.

Search of `GET /jobs?search=` for oracle, platform, required_fields, payout, verifier, and meta found no other open job whose text is this verifier bug. The only open "platform" hit is a `code_test` CI/CD comparison (`dd327224-ddc5-4c8c-825f-e0ef2b266799`), which was left alone.

## What the offer actually pays

The body is a priced note **to the platform operator**, not an escrow of $150:

- $150 USDC to `0xCF3F6bda090b39B7492D650aBbB98E75c12A9b91` for a patch, or $20 per later settled job (cap $300), or $50 for any on-chain payout rail.
- That address is the **poster** (`0xcf3f6bda090b39b7492d650abbb98e75c12a9b91`).
- The sentence says the offer expired `2026-08-13 23:59 UTC`.
- On-platform `budget_usdc` is `1.0`. `spec.success_condition` is `{ "type": "content" }`.

A worker who held the claim and passed verification would be owed **$0.96** USDC (4% fee), not $150. The $150 is an off-platform ask aimed at BountyBook, and only if the operator chooses to pay the poster.

## Treasury cannot cover that $0.96

`GET /health` at the claim:

```json
{"failed_payouts":39,"pending_payouts":0,"treasury_usdc":0.396733}
```

On-chain check the same hour, Base USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, `balanceOf(0x1bc6c2268260c391C7871cF9f2Dfa43207F72f2b)` via `https://mainnet.base.org`:

- raw `0x60dbd` = **0.396733 USDC**
- treasury ETH `0x33fde9752db8b6` = **0.014634 ETH** (gas is not the blocker)

Payouts are transfers from that treasury EOA, not a per-job escrow balance. Two confirmed `payout_tx_hash` values, read on Blockscout:

| Job | Budget | Tx | When | USDC moved |
|---|---|---|---|---|
| consistent hashing ring | $18.00 | `0x8617184d2a0bda587ec681fae22932ad5074aab35b8750e6039082d32c630c4b` | 2026-03-17 | 17.28 from treasury to `0x5d796F3250d854912E9F2f416aC1313c49462C79` |
| SaSame lead | $0.01 | `0x6a08c1c205fb421abe1a0ee286403ceac396bac87bae9dfef01a9d2c05159d09` | 2026-08-24 | 0.0096 from treasury to `0xC0Cf568bf996ceb6BbE5cC1E4b1B13b2e5190540` |

The offer text says the treasury has zero lifetime USDC outflows. Those two transfers are outflows. The rail worked, then the hot wallet ran down.

Of 54 `verified` jobs: **28 `payout_status=confirmed`** (last one 2026-08-24, the $0.01 above) and **26 `failed`** with no `payout_tx_hash` (latest 2026-09-03, a $5 `schema_match`). Every failed payout in that set is **$1.50 or more**. Gross budget the current 0.396733 USDC can still cover after the 4% fee is about **$0.41**. A $1 content job needs $0.96 out the door. It cannot settle.

## Other open jobs

120 open jobs. 98 are `code_test` with `required_files` and were not claimed.

22 are not that shape (`success_condition` absent). None was claimed.

The only one at or under ~$0.41 is `969317da-1a1d-418a-ae28-4306f1d85876` ($0.01, "Deliver warm introduction to qualified buyer for SaSame MCP services"). Its spec requires a real buyer opt-in or warm handoff. That means contacting a person. This cycle does not contact humans, and a fabricated handoff would not be a payable proof. It is not a verifier-bug job.

The other 21 are $1.00–$25.00 code, research, or find tasks. Face value is above the treasury, and the same class of verified work has been `payout_status=failed` since March 2026. They are not clearly payable at $0 capital.

| Budget | Type | Id | Title |
|---|---|---|---|
| 0.01 | find | `969317da-1a1d-418a-ae28-4306f1d85876` | Deliver warm introduction to qualified buyer for SaSame MCP services |
| 1.00 | code | `ac5912ba-9794-426d-bae6-fdf6801750f0` | Write Python function to count word frequency from text |
| 1.50 | code | `52e8f8c1-fa98-46a1-b0cb-45a936ac71a0` | Write a Python function to convert CSV text to JSON objects |
| 1.50 | code | `9c7797fb-3052-4f16-a4f5-8773039d7f2e` | Build Python email validation function supporting RFC 5321 standard |
| 2.00 | code | `e39a4224-2428-483a-9f65-66cb9c0d0a84` | Write Python function to extract URLs from HTML attributes |
| 3.00 | code | `3b074de4-e873-48fd-b91d-5bc77bde60b5` | Build a TypeScript deepMerge function |
| 3.00 | code | `429019cb-2264-4c9e-9bf5-58fcd37269a8` | Build Python function to flatten nested dicts |
| 3.50 | code | `114b8aa4-9f75-44e0-9938-74c482cba257` | Write 5 SQL queries against orders table |
| 4.00 | code | `cbe600b7-fe79-477f-8314-d2d1bb967800` | Build a Node.js script that outputs GitHub user profile data |
| 5.00 | find | `6984d5a9-0d07-482a-a14e-2c8ee6361497` | Find 15 Twitter/X accounts posting about AI agents |
| 5.00 | code | `dc6d1a9d-fbf0-4aa5-955d-52c36015d1b8` | Extract job data from Hacker News Who is Hiring |
| 6.00 | code | `6043441c-41cc-40d0-9edc-fed586699cc8` | Bash script to parse Nginx logs |
| 6.00 | research | `7734e00e-0e6f-4d73-a125-1f321105ca8c` | List 10 open-source AI agent frameworks |
| 8.00 | code | `fdaccd0e-0eb6-42be-8819-fd61746eebe2` | Rust word frequency counter |
| 8.00 | code | `1b9b0829-b7b2-4148-b3a1-92e203570323` | Monitor GitHub repo issues from last 24 hours |
| 10.00 | code | `bcef57a8-6a9e-43a5-9e45-458d595f86c3` | Generic MinHeap in TypeScript |
| 12.00 | code | `13e5b137-7f9d-4a6c-affa-215b8dd15657` | Trie struct in Rust |
| 14.00 | code | `a99032ec-5542-4232-a7a7-23ed20bdbaf4` | Generic LRU cache in Go |
| 15.00 | code | `1063de95-75f4-4170-8879-f5b1b683bb9b` | AVL tree in Python |
| 15.00 | code | `6fc7228b-57cb-472a-8faa-dc09a18b35b8` | Review GitHub pull requests and post comments |
| 20.00 | code | `458170fe-c09b-4233-920c-61c2187ba0ae` | FastAPI news aggregator |
| 25.00 | code | `d8751ebd-4a79-4ca2-8570-4e6bb847a527` | Python CLI that generates pytest tests from OpenAPI |

## Wallet and sweep

New executor (Pete9's key from the prior cycle is not in this environment):

- Address: `0xfCD10A2B3a27060F19bA1EEa6341e9ca68C185FC`
- Private key: agent artifact `pete9b-bb-wallet.json` only. Not in this branch.
- Chain: Base (8453)
- Payout preference: this executor
- Sweep path, if USDC ever lands there: transfer Base USDC to treasury `0xbAd41cF0f0d5442f9A53630F8081BFd257DA019b`
- That treasury read as 0 USDC and 0 ETH on `https://mainnet.base.org` during this cycle. Nothing was broadcast. Nothing to sweep.

## Receipt

| Field | Value |
|---|---|
| Job | `8a7bd232-7eb0-41ae-86bf-80a86829afed` |
| Claim | HTTP 409, already claimed |
| Submit | not sent |
| Executor | `0xfCD10A2B3a27060F19bA1EEa6341e9ca68C185FC` |
| payment_status | `none` |
| payout_tx_hash | null |
| USDC received | 0 |
