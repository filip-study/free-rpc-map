#!/usr/bin/env python3
"""Map a public BasedAgents delivery receipt onto a W3C VC 2.0 document.

The issuer of each credential is this transformer (PalmBeachPete8), not the
agent who delivered the task. The credential attests that a public receipt
and its hash-chain entry were observed. It does not replay the deliverer's
AgentSig request signature as a proof over the credential.

Spec pins (read-only, 2026-10-03):
  BasedAgents SPEC + service.ts @ 91a5bd3809281ed0a5f0a3c6049a562e5da9d918
  VC JSON Schema $id https://www.w3.org/2022/credentials/v2/verifiable-credential-schema.json
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from jsonschema import Draft202012Validator

SPEC_COMMIT = "91a5bd3809281ed0a5f0a3c6049a562e5da9d918"
ISSUER_AGENT_ID = "ag_HpM3PAVi1H7zis4ynukSrkrxzhYz8LnLB5PBGYzZbqFn"
ISSUER_NAME = "PalmBeachPete8"
ISSUER_CHAIN_SEQUENCE = 761
API = "https://api.basedagents.ai"
TASK_IDS = [
    "task_Hv5VtYTtYFkdjnNpgfn4A",
    "task_y8UbY27CZEgFTqvWHGT8V",
    "task_CShbba36IAw8E7itdnfpY",
]
RECEIPT_FIELDS = [
    "receipt_id",
    "task_id",
    "agent_id",
    "submission_type",
    "completed_at",
    "chain_sequence",
    "chain_entry_hash",
    "signature",
    "content_private",
    "agent_public_key",
]
# Fields hashed into profile_hash by writeDeliveryReceipt (service.ts).
# summary / artifact_urls / commit_hash / pr_url / submission_content are
# not returned on the public receipt when content_private is true.
HASHED_PAYLOAD_FIELDS = [
    "receipt_id",
    "task_id",
    "agent_id",
    "summary",
    "artifact_urls",
    "commit_hash",
    "pr_url",
    "submission_type",
    "submission_content",
    "completed_at",
]

HERE = Path(__file__).resolve().parent
SCHEMA_PATH = HERE / "schema" / "verifiable-credential-schema.json"
DEFAULT_KEYPAIR = Path("/home/ubuntu/.palmbeachpete/basedagents-pete8-keypair.json")


def canonical_json(value) -> str:
    """RFC 8785 subset used by BasedAgents canonicalJsonStringify."""
    if value is None:
        return "null"
    if isinstance(value, bool) or isinstance(value, int):
        return json.dumps(value)
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, list):
        return "[" + ",".join(canonical_json(v) for v in value) + "]"
    if isinstance(value, dict):
        keys = sorted(value)
        return "{" + ",".join(json.dumps(k) + ":" + canonical_json(value[k]) for k in keys) + "}"
    return json.dumps(value)


def fetch_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": "PalmBeachPete8/1.0"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return json.load(response)


def chain_entry_hash(entry: dict) -> str:
    """v2 length-prefixed entry hash. public_key is raw key bytes, not hex text."""
    public_key = bytes.fromhex(entry["public_key"])
    parts = [
        entry["previous_hash"].encode(),
        public_key,
        (entry.get("nonce") or "").encode(),
        entry["profile_hash"].encode(),
        entry["timestamp"].encode(),
    ]
    blob = b""
    for part in parts:
        blob += len(part).to_bytes(4, "big") + part
    return hashlib.sha256(blob).hexdigest()


def load_signing_key(path: Path) -> tuple[Ed25519PrivateKey, str]:
    data = json.loads(path.read_text())
    private_hex = data["privateKey"]
    public_hex = data["publicKey"]
    key = Ed25519PrivateKey.from_private_bytes(bytes.fromhex(private_hex))
    derived = key.public_key().public_bytes_raw().hex()
    if derived != public_hex:
        raise SystemExit("keypair public key does not match the private key")
    return key, public_hex


def mapping_rows() -> list[dict]:
    return [
        {
            "receipt_field": "receipt_id",
            "vc_path": "id (fragment) and credentialSubject.delivery.receiptId",
            "notes": "Public receipt identifier. Also the fragment of the credential id.",
        },
        {
            "receipt_field": "task_id",
            "vc_path": "credentialSubject.delivery.taskId",
            "notes": "Task the receipt belongs to. Credential id URL uses the same id.",
        },
        {
            "receipt_field": "agent_id",
            "vc_path": "credentialSubject.id",
            "notes": "Subject of the delivery event. Not the VC issuer.",
        },
        {
            "receipt_field": "submission_type",
            "vc_path": "credentialSubject.delivery.submissionType",
            "notes": "json, link, or pr. Present on the public receipt and inside the hashed payload.",
        },
        {
            "receipt_field": "completed_at",
            "vc_path": "credentialSubject.delivery.completedAt",
            "notes": "When the delivery was written. Not copied to validFrom: this VC is issued later, by a different party.",
        },
        {
            "receipt_field": "chain_sequence",
            "vc_path": "evidence[0].chainSequence",
            "notes": "Index of the task_delivered chain entry.",
        },
        {
            "receipt_field": "chain_entry_hash",
            "vc_path": "evidence[0].chainEntryHash",
            "notes": "Recomputed from the public chain entry with the v2 length-prefixed formula.",
        },
        {
            "receipt_field": "signature",
            "vc_path": "credentialSubject.delivery.requestSignature",
            "notes": "AgentSig over the deliver HTTP request, not over the receipt or the VC. Stored as an opaque string. Not used as proof.proofValue.",
        },
        {
            "receipt_field": "content_private",
            "vc_path": "credentialSubject.delivery.contentPrivate",
            "notes": "When true, summary and submission_content are absent, so profile_hash cannot be opened.",
        },
        {
            "receipt_field": "agent_public_key",
            "vc_path": "evidence[0].delivererPublicKey",
            "notes": "Deliverer's Ed25519 public key. Checked equal to the chain entry public_key. Distinct from the VC issuer key.",
        },
    ]


def build_credential(receipt: dict, chain: dict, issued_at: str, issuer_public_hex: str) -> dict:
    task_id = receipt["task_id"]
    receipt_id = receipt["receipt_id"]
    subject_id = receipt["agent_id"]
    issuer_id = f"https://basedagents.ai/agents/{ISSUER_AGENT_ID}"
    unsigned = {
        "@context": [
            "https://www.w3.org/ns/credentials/v2",
            {
                "BasedAgentsDeliveryReceipt": "https://basedagents.ai/ns#BasedAgentsDeliveryReceipt",
                "BasedAgentsAgent": "https://basedagents.ai/ns#BasedAgentsAgent",
                "BasedAgentsHashChainAnchor": "https://basedagents.ai/ns#BasedAgentsHashChainAnchor",
            },
        ],
        "id": f"{API}/v1/tasks/{task_id}/receipt#{receipt_id}",
        "type": ["VerifiableCredential", "BasedAgentsDeliveryReceipt"],
        "issuer": {"id": issuer_id, "name": ISSUER_NAME},
        "validFrom": issued_at,
        "credentialSubject": {
            "id": f"https://basedagents.ai/agents/{subject_id}",
            "type": "BasedAgentsAgent",
            "delivery": {
                "receiptId": receipt_id,
                "taskId": task_id,
                "submissionType": receipt["submission_type"],
                "completedAt": receipt["completed_at"],
                "contentPrivate": receipt["content_private"],
                "requestSignature": receipt["signature"],
            },
        },
        "evidence": [
            {
                "id": f"{API}/v1/chain/{chain['sequence']}",
                "type": "BasedAgentsHashChainAnchor",
                "entryType": chain.get("entry_type"),
                "chainSequence": chain["sequence"],
                "chainEntryHash": chain["entry_hash"],
                "previousHash": chain["previous_hash"],
                "profileHash": chain["profile_hash"],
                "delivererPublicKey": chain["public_key"],
                "delivererAgentId": chain["agent_id"],
                "anchoredAt": chain["timestamp"],
                "entryHashRecomputed": chain_entry_hash(chain) == chain["entry_hash"],
            }
        ],
    }
    message = canonical_json(unsigned).encode()
    return unsigned, message, issuer_id


def sign_credential(unsigned: dict, message: bytes, key: Ed25519PrivateKey, public_hex: str, issued_at: str, issuer_id: str) -> dict:
    signature = key.sign(message)
    credential = dict(unsigned)
    credential["proof"] = {
        "type": "BasedAgentsObservationProof2026",
        "proofPurpose": "assertionMethod",
        "verificationMethod": [
            {
                "id": f"{issuer_id}#key-1",
                "type": "Ed25519VerificationKey2020",
                "controller": issuer_id,
                "publicKeyHex": public_hex,
                "chainAnchor": f"{API}/v1/chain/{ISSUER_CHAIN_SEQUENCE}",
            }
        ],
        "created": issued_at,
        "proofValue": base64.b64encode(signature).decode(),
        "canonicalization": "basedagents-canonical-json-subset-rfc8785",
    }
    return credential


def verify_proof(credential: dict) -> None:
    proof = credential["proof"]
    method = proof["verificationMethod"][0]
    unsigned = {k: v for k, v in credential.items() if k != "proof"}
    message = canonical_json(unsigned).encode()
    public = Ed25519PublicKey.from_public_bytes(bytes.fromhex(method["publicKeyHex"]))
    public.verify(base64.b64decode(proof["proofValue"]), message)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--keypair", default=os.environ.get("BASEDAGENTS_KEYPAIR_PATH", str(DEFAULT_KEYPAIR)))
    parser.add_argument("--out", default=str(HERE / "out"))
    args = parser.parse_args()

    out = Path(args.out)
    (out / "receipts").mkdir(parents=True, exist_ok=True)
    (out / "chain").mkdir(parents=True, exist_ok=True)
    (out / "examples").mkdir(parents=True, exist_ok=True)

    key, public_hex = load_signing_key(Path(args.keypair))
    issued_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    schema = json.loads(SCHEMA_PATH.read_text())
    validator = Draft202012Validator(schema)

    credentials = []
    checks = []
    for task_id in TASK_IDS:
        receipt = fetch_json(f"{API}/v1/tasks/{task_id}/receipt")["receipt"]
        missing = [field for field in RECEIPT_FIELDS if field not in receipt]
        if missing:
            raise SystemExit(f"{task_id} missing receipt fields: {missing}")
        chain = fetch_json(f"{API}/v1/chain/{receipt['chain_sequence']}")
        recomputed = chain_entry_hash(chain)
        if recomputed != chain["entry_hash"]:
            raise SystemExit(f"entry hash mismatch at {chain['sequence']}")
        if receipt["chain_entry_hash"] != chain["entry_hash"]:
            raise SystemExit(f"receipt chain_entry_hash mismatch for {task_id}")
        if receipt["agent_public_key"] != chain["public_key"]:
            raise SystemExit(f"deliverer key mismatch for {task_id}")
        if receipt["agent_id"] != chain["agent_id"]:
            raise SystemExit(f"deliverer id mismatch for {task_id}")

        (out / "receipts" / f"{receipt['receipt_id']}.json").write_text(json.dumps(receipt, indent=2) + "\n")
        (out / "chain" / f"{chain['sequence']}.json").write_text(json.dumps(chain, indent=2) + "\n")

        unsigned, message, issuer_id = build_credential(receipt, chain, issued_at, public_hex)
        credential = sign_credential(unsigned, message, key, public_hex, issued_at, issuer_id)
        errors = sorted(validator.iter_errors(credential), key=lambda err: list(err.path))
        if errors:
            rendered = "; ".join(f"{'/'.join(map(str, err.path))}: {err.message}" for err in errors)
            raise SystemExit(f"schema failed for {task_id}: {rendered}")
        verify_proof(credential)
        (out / "examples" / f"{receipt['receipt_id']}.vc.json").write_text(json.dumps(credential, indent=2) + "\n")
        credentials.append(credential)
        checks.append(
            {
                "task_id": task_id,
                "receipt_id": receipt["receipt_id"],
                "chain_sequence": chain["sequence"],
                "entry_type": chain.get("entry_type"),
                "entry_hash_recomputed": True,
                "content_private": receipt["content_private"],
                "profile_hash_openable_from_public_receipt": False,
                "schema_valid": True,
                "observation_proof_verified": True,
            }
        )

    report = {
        "issued_at": issued_at,
        "issuer": ISSUER_AGENT_ID,
        "issuer_chain_sequence": ISSUER_CHAIN_SEQUENCE,
        "spec_commit": SPEC_COMMIT,
        "schema_id": schema.get("$id"),
        "credentials": len(credentials),
        "checks": checks,
        "hashed_payload_fields_not_on_public_receipt": [
            field for field in HASHED_PAYLOAD_FIELDS if field not in RECEIPT_FIELDS
        ],
    }
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
