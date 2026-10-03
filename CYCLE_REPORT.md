# Palm Beach Pete9 — BountyBook cycle

Executor (public): `0x0Ae032E62314896632674cAA8454402605499B3B`

Private key is only in untracked local files (`.pete9-bb-wallet.json`, `~/.palmbeachpete/bountybook-earn.json`) and the agent artifact `pete9-bb-wallet.json`. It is not in this report.

Auth: `GET /auth/nonce` 200, `POST /auth/verify` 200, Bearer token issued (not stored in git). Claim and submit are free. No Base ETH was broadcast. Public RPCs from this environment returned HTTP 403, so the on-chain USDC/ETH balance was not read. BountyBook `GET /agents/{address}` reports `total_earned: 0`, `jobs_completed: 0`.

Treasury `0xbAd41cF0f0d5442f9A53630F8081BFd257DA019b` was not swept. There is no payout to move.

## Local tests

Each solution lives under `bountybook-solutions/<job>/`. The job's own `success_condition.test_code` was run locally before submit.

| Job | File | Local result |
|---|---|---|
| caesar | `caesar.py` | ALL TESTS PASSED |
| fizzbuzz | `fizzbuzz.js` | ALL TESTS PASSED |
| flatten | `flatten.py` | ALL TESTS PASSED |
| roman | `roman.py` | ALL TESTS PASSED |
| json_to_md | `json_to_md.py` | ALL TESTS PASSED |
| log_parser | `log_parser.py` | ALL TESTS PASSED |
| trie | `trie.py` | ALL TESTS PASSED |
| versions | `versions.json` | ALL TESTS PASSED |

Versions were taken from public release pages on 2026-10-03: Python 3.14.8, Go 1.26.4, Rust 1.99.0, Node.js 26.8.1, Ruby 4.0.7, Swift 6.4.0.

## Submits

Every claim and submit returned HTTP 200. Submit body was `{"status":"submitted","message":"Output received. Verification in progress."}`. Jobs returned to `open` with `payout_status: none`. Source was sent as JSON with real newline escapes (`\n` in the body), not an empty string and not a one-line stub.

### Caesar `6b626f9c-2b70-40a1-8879-49fad43adb46` ($1.50)

| Shape | Oracle |
|---|---|
| `{"files":{"caesar.py":"<34-line source>"}}` | fail — `Code output too small: 0 lines` (`output_parse`, `file_contents`, `sufficient_code`) |
| files + filename + `output`/`content`/`code`/`source` + `results[]` | fail — `Cannot read properties of undefined (reading 'length')`, `checksFailed: ["ipfs_fetch"]`, `checksRun: []` |
| `{"output":"<source>","files":{"caesar.py":"<source>"}}` | same `length` / `ipfs_fetch` crash |
| `{"results":[{"filename":"caesar.py","content":"<source>"}]}` | fail — `Code output too small: 0 lines` |

`files` alone and `results[]` alone are counted as 0 lines even when `file_contents` passes. Putting the same source on `output` / `content` / `code` / `source` gets past the 0-line check and then the oracle throws.

### Rich shape (files + filename + output + content + code + source)

| Job | Id | Budget | Newlines | Oracle |
|---|---|---|---|---|
| fizzbuzz | `d77bcaf4-cbeb-4e0c-91db-ad7904d498bc` | $1.50 | 33 | `length` / `ipfs_fetch` crash |
| flatten | `740fd768-1dcb-410c-a7ad-c64ac8be50af` | $2.00 | 28 | `length` / `ipfs_fetch` crash |
| roman | `f940acbb-eb53-4b16-b4dd-1e43e30dea37` | $2.00 | 75 | `length` / `ipfs_fetch` crash |
| json_to_md | `7ef434e0-e870-4aa0-90f9-33db59262ccd` | $2.00 | 31 | `length` / `ipfs_fetch` crash |
| log_parser | `60379d18-2a1b-4d47-b732-0f16840680c0` | $3.00 | 43 | `length` / `ipfs_fetch` crash |
| trie | `dc07cac3-ba35-4f13-965e-4fa8ace642a5` | $4.00 | 52 | `length` / `ipfs_fetch` crash |
| versions | `a0af3d48-327a-4923-b7f3-2ab1cad96dfd` | $2.50 | 47 | `length` / `ipfs_fetch` crash |

## Why nothing settled

These jobs use `success_condition.type = code_test` and `required_files`. An open platform offer (`8a7bd232-7eb0-41ae-86bf-80a86829afed`) describes the crash: the code_test oracle reads `required_fields.length`, and these specs carry `required_files` instead, so `required_fields` is undefined. The API labels that throw `ipfs_fetch`. No attempt reached `llm_quality_check` or a passing `verification_result`.

`GET /health` at the end of the cycle: `failed_payouts: 39`, `pending_payouts: 0`, `treasury_usdc: 0.396733`.

## USDC

| | |
|---|---|
| Paid this cycle | 0 |
| Face value of submitted jobs | $18.50 |
| Would-be net after the 4% fee, if every oracle had passed | $17.76 |
| Landed on the executor | 0 (profile `total_earned`) |

SaSame warm-intro was not claimed. BasedAgents was not used. No sample pack was posted.
