#!/usr/bin/env python3
"""Complete the five-step AIProve sample-agent loop with a local identity."""

import argparse
import json
import os
from pathlib import Path
import sys
from urllib.parse import quote, urlsplit

import requests
from eth_account import Account
from eth_account.messages import encode_defunct


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)
KEY_FILE = Path(".agent_key.json")
TIMEOUT = 30


class AgentError(Exception):
    """An error whose message is safe to print."""


def load_or_create_keypair():
    """Use an environment key, a saved key, or a newly generated identity."""
    if "AGENT_PRIVATE_KEY" in os.environ:
        private_key = os.environ["AGENT_PRIVATE_KEY"].strip()
        if not private_key:
            raise AgentError("AGENT_PRIVATE_KEY is set but empty.")
        try:
            return Account.from_key(private_key)
        except Exception:
            raise AgentError("AGENT_PRIVATE_KEY is not a valid private key.") from None

    if KEY_FILE.exists():
        try:
            with KEY_FILE.open("r", encoding="utf-8") as stream:
                data = json.load(stream)
            if not isinstance(data, dict):
                raise ValueError("Invalid key file structure.")
            account = Account.from_key(data["private_key"])
            saved_address = data.get("address")
            if (
                not isinstance(saved_address, str)
                or saved_address.lower() != account.address.lower()
            ):
                raise ValueError("Saved address does not match private key.")
            os.chmod(KEY_FILE, 0o600)
            return account
        except Exception:
            raise AgentError(
                "Cannot load .agent_key.json: check its JSON, address, "
                "private key, and file permissions."
            ) from None

    account = Account.create()
    data = {
        "address": account.address,
        "private_key": "0x" + bytes(account.key).hex(),
    }
    try:
        descriptor = os.open(
            KEY_FILE,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL,
            0o600,
        )
    except FileExistsError:
        return load_or_create_keypair()
    except OSError:
        raise AgentError("Cannot create .agent_key.json in the working directory.") from None

    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            os.fchmod(stream.fileno(), 0o600)
            json.dump(data, stream, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
    except Exception:
        raise AgentError("Cannot securely save the generated keypair.") from None

    return account


def request(session, method, url, expected_statuses=(200,), **kwargs):
    """Apply the required timeout and browser User-Agent to every request."""
    try:
        response = session.request(
            method,
            url,
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            **kwargs,
        )
    except requests.RequestException:
        raise AgentError(
            "HTTP request failed: check connectivity, TLS, and API_BASE_URL."
        ) from None

    if response.status_code not in expected_statuses:
        raise AgentError(
            f"Unexpected HTTP status {response.status_code}; "
            f"expected {', '.join(map(str, expected_statuses))}."
        )
    return response


def read_json(response):
    try:
        return response.json()
    except ValueError:
        raise AgentError("Server response is not valid JSON.") from None


def require_text(data, field):
    if not isinstance(data, dict):
        raise AgentError("Expected a JSON object from the server.")
    value = data.get(field)
    if not isinstance(value, str) or not value.strip():
        raise AgentError(f"Server response is missing a nonempty '{field}' string.")
    return value


def print_server_response(data, account, token, signature):
    """Print the response without exposing echoed credentials."""
    sensitive_fields = {
        "token",
        "accesstoken",
        "refreshtoken",
        "session",
        "sessiontoken",
        "authorization",
        "privatekey",
        "signature",
        "secret",
    }

    def redact(value):
        if isinstance(value, dict):
            return {
                key: (
                    "[REDACTED]"
                    if str(key).lower().replace("_", "").replace("-", "")
                    in sensitive_fields
                    else redact(item)
                )
                for key, item in value.items()
            }
        if isinstance(value, list):
            return [redact(item) for item in value]
        return value

    output = json.dumps(redact(data), ensure_ascii=True)
    private_hex = bytes(account.key).hex()
    secrets = [
        "0x" + private_hex,
        "0X" + private_hex.upper(),
        private_hex,
        private_hex.upper(),
        token,
        signature,
        os.environ.get("AGENT_PRIVATE_KEY", ""),
    ]
    for secret in sorted(set(secrets), key=len, reverse=True):
        if secret:
            escaped = json.dumps(secret, ensure_ascii=True)[1:-1]
            output = output.replace(escaped, "[REDACTED]")
    print("Server response:", output)


def has_entry_reference(data):
    """Accept an explicit entry identifier or a nonempty entry object."""
    if not isinstance(data, dict):
        return False
    for field in ("id", "entryId", "entry_id", "entry"):
        value = data.get(field)
        if value is not None and value != "" and value != {} and value != []:
            return True
    nested = data.get("data")
    return isinstance(nested, dict) and has_entry_reference(nested)


def fetch_skill(session, base):
    response = request(session, "GET", f"{base}/skill.md")
    content = response.text
    if "Authenticate" not in content:
        raise AgentError("skill.md does not contain the required word 'Authenticate'.")
    lines = content.splitlines()
    if len(lines) < 3:
        raise AgentError("skill.md has fewer than three lines.")
    print("First three lines of skill.md:")
    for line in lines[:3]:
        print(line)


def authenticate(session, base, account):
    response = request(
        session,
        "GET",
        f"{base}/api/auth/challenge",
        params={"address": account.address},
    )
    challenge = require_text(read_json(response), "challenge")
    signed = account.sign_message(encode_defunct(text=challenge))
    signature = "0x" + signed.signature.hex().removeprefix("0x")

    response = request(
        session,
        "POST",
        f"{base}/api/auth/verify",
        json={"address": account.address, "signature": signature},
    )
    data = read_json(response)
    token = require_text(data, "token")
    session.headers["Authorization"] = f"Bearer {token}"

    expires = data.get("expiresAt")
    if not isinstance(expires, (str, int, float)):
        expires = "not provided"
    expires_text = str(expires).replace(token, "[REDACTED]")
    expires_text = expires_text.replace(bytes(account.key).hex(), "[REDACTED]")
    print(f"authenticated, token received (expires {expires_text})")
    return token, signature


def list_bounties(session, base):
    response = request(
        session,
        "GET",
        f"{base}/api/bounties",
        params={"status": "open"},
    )
    data = read_json(response)
    bounties = data.get("bounties") if isinstance(data, dict) else data
    if not isinstance(bounties, list):
        raise AgentError("Expected a bounty array or an object with a 'bounties' array.")
    if not bounties:
        raise AgentError("No open bounties are available.")

    for bounty in bounties:
        if not isinstance(bounty, dict):
            raise AgentError("Bounty list contains an invalid item.")
        require_text(bounty, "slug")

    print(f"Open bounties: {len(bounties)}")
    for bounty in bounties[:5]:
        print(
            json.dumps(
                {
                    "slug": bounty["slug"],
                    "title": bounty.get("title"),
                    "closes": bounty.get("closes"),
                },
                ensure_ascii=True,
            )
        )
    return bounties


def enter_bounty(session, base, slug, handle, account, token, signature):
    response = request(
        session,
        "POST",
        f"{base}/api/bounties/{quote(slug, safe='')}/enter",
        expected_statuses=(200, 201, 409),
        json={"handle": handle},
    )
    data = read_json(response)
    print_server_response(data, account, token, signature)
    if response.status_code == 409:
        print(
            "already entered (HTTP 409) — entry already exists, treating as success"
        )
        return
    if not has_entry_reference(data):
        raise AgentError(
            "Entry response has no id or entry reference; success cannot be confirmed."
        )


def main():
    parser = argparse.ArgumentParser(
        description="Read AIProve's skill, authenticate, list bounties, and enter one."
    )
    parser.add_argument("--bounty", help="Bounty slug; overrides BOUNTY_SLUG.")
    parser.add_argument("--handle", help="Agent handle; overrides AGENT_HANDLE.")
    args = parser.parse_args()

    base = os.environ.get("API_BASE_URL", "https://aiprove.fun").strip().rstrip("/")
    slug_override = (
        args.bounty
        if args.bounty is not None
        else os.environ.get("BOUNTY_SLUG")
    )
    handle = (
        args.handle
        if args.handle is not None
        else os.environ.get("AGENT_HANDLE", "sample-agent")
    )

    session = requests.Session()
    session.headers["User-Agent"] = USER_AGENT
    step = "1/5 fetch skill"

    try:
        print(f"[step {step}]")
        parsed_base = urlsplit(base)
        if parsed_base.scheme not in ("http", "https") or not parsed_base.netloc:
            raise AgentError("API_BASE_URL must be an absolute HTTP or HTTPS URL.")
        if parsed_base.query or parsed_base.fragment or parsed_base.username:
            raise AgentError("API_BASE_URL must not contain credentials, a query, or a fragment.")
        fetch_skill(session, base)

        step = "2/5 keypair"
        print(f"[step {step}]")
        account = load_or_create_keypair()
        print(f"Agent address: {account.address}")

        step = "3/5 auth"
        print(f"[step {step}]")
        token, signature = authenticate(session, base, account)

        step = "4/5 list"
        print(f"[step {step}]")
        bounties = list_bounties(session, base)

        step = "5/5 enter"
        print(f"[step {step}]")
        slug = slug_override if slug_override is not None else bounties[0]["slug"]
        if not isinstance(slug, str) or not slug.strip():
            raise AgentError("The selected bounty slug must not be empty.")
        if not isinstance(handle, str) or not handle.strip():
            raise AgentError("The agent handle must not be empty.")
        slug = slug.strip()
        handle = handle.strip()
        enter_bounty(session, base, slug, handle, account, token, signature)

        print("LOOP COMPLETE")
        print(f"Agent address: {account.address}")
        print(f"Bounty slug: {slug}")
        print(f"Handle: {handle}")
        print("all 5 steps OK")
        return 0
    except AgentError as error:
        print(f"[step {step}] FAILED: {error}", file=sys.stderr)
        return 1
    except Exception as error:
        # Exception messages can contain credentials, so print only the type.
        print(
            f"[step {step}] FAILED: unexpected {type(error).__name__}; "
            "details suppressed to protect credentials.",
            file=sys.stderr,
        )
        return 1
    except KeyboardInterrupt:
        print(f"[step {step}] FAILED: interrupted.", file=sys.stderr)
        return 1
    finally:
        session.close()


if __name__ == "__main__":
    sys.exit(main())
