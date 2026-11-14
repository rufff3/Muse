#!/usr/bin/env python3
"""Autonomous AIProve bounty agent."""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from typing import Any, Optional
from urllib.parse import urljoin

requests = None
Account = None
encode_defunct = None

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)
TIMEOUT = 30
RETRY_COUNT = 2
RETRY_DELAY = 2

TARGET_BOUNTIES = {"forecast-btc-7d", "forecast-nvda-3d"}


def log(message: str) -> None:
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", file=sys.stderr, flush=True)


def compact(value: Any, limit: int = 500) -> str:
    if isinstance(value, str):
        text = value
    else:
        try:
            text = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        except Exception:
            text = str(value)
    return text[:limit]


def ensure_dependencies() -> bool:
    global requests, Account, encode_defunct

    try:
        import requests as requests_module
        from eth_account import Account as account_class
        from eth_account.messages import encode_defunct as encode_message

        requests = requests_module
        Account = account_class
        encode_defunct = encode_message
        return True
    except ImportError:
        log("dependensi belum tersedia, menjalankan pip install")
        try:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    "--quiet",
                    "requests",
                    "eth_account",
                ],
                check=True,
            )
            import requests as requests_module
            from eth_account import Account as account_class
            from eth_account.messages import encode_defunct as encode_message

            requests = requests_module
            Account = account_class
            encode_defunct = encode_message
            return True
        except Exception as exc:
            log(f"gagal memasang dependensi: {compact(str(exc))}")
            return False


def request(
    method: str,
    url: str,
    *,
    token: Optional[str] = None,
    params: Optional[dict[str, Any]] = None,
    payload: Optional[dict[str, Any]] = None,
) -> Any:
    headers = {"User-Agent": USER_AGENT}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    last_exception: Optional[Exception] = None

    for attempt in range(RETRY_COUNT + 1):
        try:
            response = requests.request(
                method,
                url,
                headers=headers,
                params=params,
                json=payload,
                timeout=TIMEOUT,
            )

            if response.status_code >= 500 or response.status_code == 429:
                if attempt < RETRY_COUNT:
                    time.sleep(RETRY_DELAY)
                    continue

            return response
        except requests.RequestException as exc:
            last_exception = exc
            if attempt < RETRY_COUNT:
                time.sleep(RETRY_DELAY)
                continue
            raise

    if last_exception:
        raise last_exception
    raise RuntimeError("request gagal tanpa response")


def response_data(response: Any) -> Any:
    try:
        return response.json()
    except ValueError:
        return response.text


def fetch_skill(base_url: str, errors: list[str]) -> None:
    try:
        response = request("GET", urljoin(base_url + "/", "skill.md"))
        excerpt = response.text[:500].replace("\n", "\\n")
        log(f"skill.md dibaca: {excerpt}")
        if not 200 <= response.status_code < 300:
            errors.append(f"skill.md HTTP {response.status_code}")
    except Exception as exc:
        errors.append(f"skill.md gagal: {compact(str(exc))}")
        log("skill.md gagal dibaca")


def make_keypair() -> Any:
    account = Account.create()
    log(f"keypair baru dibuat, address={account.address}")
    return account


def authenticate(base_url: str, account: Any, errors: list[str]) -> Optional[str]:
    try:
        challenge_response = request(
            "GET",
            urljoin(base_url + "/", "api/auth/challenge"),
            params={"address": account.address},
        )
        if not 200 <= challenge_response.status_code < 300:
            errors.append(f"challenge HTTP {challenge_response.status_code}")
            return None

        challenge_data = response_data(challenge_response)
        challenge = challenge_data.get("challenge") if isinstance(challenge_data, dict) else None
        if not isinstance(challenge, str):
            errors.append("challenge bukan string")
            return None

        signed = account.sign_message(encode_defunct(text=challenge))
        signature = signed.signature.hex()
        if not signature.startswith("0x"):
            signature = "0x" + signature

        verify_response = request(
            "POST",
            urljoin(base_url + "/", "api/auth/verify"),
            payload={"address": account.address, "signature": signature},
        )
        if not 200 <= verify_response.status_code < 300:
            errors.append(f"auth verify HTTP {verify_response.status_code}")
            return None

        verify_data = response_data(verify_response)
        token = verify_data.get("token") if isinstance(verify_data, dict) else None
        if not isinstance(token, str) or not token:
            errors.append("token auth tidak ditemukan")
            return None

        log("autentikasi berhasil")
        return token
    except Exception as exc:
        errors.append(f"autentikasi gagal: {compact(str(exc))}")
        log("autentikasi gagal")
        return None


def list_bounties(base_url: str, errors: list[str]) -> Optional[list[dict[str, Any]]]:
    try:
        response = request(
            "GET",
            urljoin(base_url + "/", "api/bounties"),
            params={"status": "open"},
        )
        if not 200 <= response.status_code < 300:
            errors.append(f"list bounty HTTP {response.status_code}")
            return None

        data = response_data(response)
        if isinstance(data, list):
            bounties = data
        elif isinstance(data, dict) and isinstance(data.get("bounties"), list):
            bounties = data["bounties"]
        else:
            errors.append("format list bounty tidak valid")
            return None

        log(f"{len(bounties)} bounty open ditemukan")
        return [item for item in bounties if isinstance(item, dict)]
    except Exception as exc:
        errors.append(f"list bounty gagal: {compact(str(exc))}")
        return None


def enter_bounty(
    base_url: str,
    slug: str,
    handle: str,
    token: str,
) -> tuple[bool, str]:
    try:
        response = request(
            "POST",
            urljoin(base_url + "/", f"api/bounties/{slug}/enter"),
            token=token,
            payload={"handle": handle},
        )
        if 200 <= response.status_code < 300:
            log(f"enter sukses: {slug}")
            return True, ""
        return False, f"HTTP {response.status_code}: {compact(response_data(response))}"
    except Exception as exc:
        return False, compact(str(exc))


def submit_prediction(
    base_url: str,
    slug: str,
    prediction: dict[str, Any],
    handle: str,
    token: str,
) -> tuple[int, Any]:
    response = request(
        "POST",
        urljoin(base_url + "/", f"api/bounties/{slug}/submit"),
        token=token,
        payload={"prediction": prediction, "handle": handle},
    )
    return response.status_code, response_data(response)


def numeric_values(values: Any) -> list[float]:
    result = []
    if not isinstance(values, list):
        return result
    for value in values:
        try:
            number = float(value)
            if number == number:
                result.append(number)
        except (TypeError, ValueError):
            continue
    return result


def btc_signal(errors: list[str]) -> Optional[dict[str, Any]]:
    coingecko_url = (
        "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
    )
    try:
        response = request(
            "GET",
            coingecko_url,
            params={"vs_currency": "usd", "days": "14"},
        )
        if 200 <= response.status_code < 300:
            data = response_data(response)
            prices = data.get("prices", []) if isinstance(data, dict) else []
            points = [
                (float(point[0]), float(point[1]))
                for point in prices
                if isinstance(point, list) and len(point) >= 2
            ]
            if len(points) >= 2:
                latest_timestamp, latest_price = points[-1]
                target_timestamp = latest_timestamp - 7 * 24 * 60 * 60 * 1000
                old_timestamp, old_price = min(
                    points,
                    key=lambda point: abs(point[0] - target_timestamp),
                )
                if old_price > 0:
                    return build_btc_prediction(latest_price, old_price)
        log("CoinGecko BTC gagal, memakai Binance")
    except Exception:
        log("CoinGecko BTC gagal, memakai Binance")

    try:
        response = request(
            "GET",
            "https://api.binance.com/api/v3/klines",
            params={"symbol": "BTCUSDT", "interval": "1d", "limit": "8"},
        )
        if 200 <= response.status_code < 300:
            data = response_data(response)
            closes = numeric_values(
                [row[4] for row in data if isinstance(row, list) and len(row) > 4]
            )
            if len(closes) >= 2 and closes[0] > 0:
                return build_btc_prediction(closes[-1], closes[0])
    except Exception:
        pass

    errors.append("BTC signal gagal dari CoinGecko dan Binance")
    log("BTC signal gagal, bounty dilewati")
    return None


def build_btc_prediction(latest_price: float, old_price: float) -> dict[str, Any]:
    momentum = (latest_price - old_price) / old_price
    answer = "yes" if momentum > 0 else "no"
    confidence = max(0.55, min(0.85, 0.55 + abs(momentum) * 3))
    return {
        "answer": answer,
        "confidence": round(confidence, 2),
    }


def nvda_signal(errors: list[str]) -> Optional[dict[str, Any]]:
    yahoo_url = "https://query1.finance.yahoo.com/v8/finance/chart/NVDA"

    try:
        response = request(
            "GET",
            yahoo_url,
            params={"range": "10d", "interval": "1d"},
        )
        if 200 <= response.status_code < 300:
            data = response_data(response)
            result = data.get("chart", {}).get("result", []) if isinstance(data, dict) else []
            if result:
                closes = numeric_values(
                    result[0].get("indicators", {})
                    .get("quote", [{}])[0]
                    .get("close", [])
                )
                if len(closes) >= 2:
                    recent = closes[-6:]
                    returns = [
                        (recent[index] - recent[index - 1]) / recent[index - 1]
                        for index in range(1, len(recent))
                        if recent[index - 1] > 0
                    ]
                    average_return = sum(returns) / len(returns) if returns else 0.0
                    prediction = closes[-1] * (1 + average_return * 3)
                    return {"answer": round(prediction, 2)}
        log("Yahoo NVDA gagal, memakai Stooq")
    except Exception:
        log("Yahoo NVDA gagal, memakai Stooq")

    try:
        response = request(
            "GET",
            "https://stooq.com/q/l/",
            params={"s": "nvda.us", "f": "l", "e": "csv"},
        )
        if 200 <= response.status_code < 300:
            rows = list(csv.reader(response.text.splitlines()))
            if len(rows) >= 2:
                for value in reversed(rows[1]):
                    try:
                        price = float(value.strip())
                        if price == price:
                            return {"answer": round(price, 2)}
                    except ValueError:
                        continue
    except Exception:
        pass

    errors.append("NVDA signal gagal dari Yahoo dan Stooq")
    log("NVDA signal gagal, bounty dilewati")
    return None


def run(dry_run: bool = False) -> int:
    base_url = os.environ.get("API_BASE_URL", "https://aiprove.fun").rstrip("/")
    errors: list[str] = []
    entered: list[str] = []
    entered_failed: dict[str, str] = {}
    predictions_submitted: list[dict[str, Any]] = []
    skipped: list[str] = []

    if not ensure_dependencies():
        summary = {
            "address": None,
            "handle": None,
            "entered": [],
            "entered_failed": {},
            "predictions_submitted": [],
            "skipped": [],
            "errors": errors,
        }
        print(json.dumps(summary, ensure_ascii=False))
        try:
            with open("run_log.json", "w", encoding="utf-8") as file:
                json.dump(summary, file, ensure_ascii=False, indent=2)
        except OSError:
            pass
        return 1

    fetch_skill(base_url, errors)
    account = make_keypair()
    address = account.address
    default_handle = f"auto-{address[2:8].lower()}"
    handle = os.environ.get("AGENT_HANDLE", default_handle)

    try:
        health = request("GET", urljoin(base_url + "/", "api/health"))
        if not 200 <= health.status_code < 300:
            errors.append(f"health HTTP {health.status_code}")
            log(f"health tidak sehat: HTTP {health.status_code}")
        else:
            log("health API OK")
    except Exception as exc:
        errors.append(f"health gagal: {compact(str(exc))}")
        log("health API gagal")

    bounties = list_bounties(base_url, errors)
    if bounties is None:
        summary = {
            "address": address,
            "handle": handle,
            "entered": [],
            "entered_failed": {},
            "predictions_submitted": [],
            "skipped": [],
            "errors": errors,
        }
        print(json.dumps(summary, ensure_ascii=False))
        with open("run_log.json", "w", encoding="utf-8") as file:
            json.dump(summary, file, ensure_ascii=False, indent=2)
        return 1

    token: Optional[str] = None
    if not dry_run:
        token = authenticate(base_url, account, errors)
        if token is None:
            summary = {
                "address": address,
                "handle": handle,
                "entered": [],
                "entered_failed": {},
                "predictions_submitted": [],
                "skipped": [],
                "errors": errors,
            }
            print(json.dumps(summary, ensure_ascii=False))
            with open("run_log.json", "w", encoding="utf-8") as file:
                json.dump(summary, file, ensure_ascii=False, indent=2)
            return 1
    else:
        log("dry-run aktif, semua write call dilewati")

    for bounty in bounties:
        slug = bounty.get("slug")
        if not isinstance(slug, str) or not slug:
            errors.append("bounty tanpa slug dilewati")
            continue

        if dry_run:
            continue

        assert token is not None
        success, reason = enter_bounty(base_url, slug, handle, token)
        if success:
            entered.append(slug)
        else:
            entered_failed[slug] = reason
            log(f"enter gagal: {slug} ({reason[:180]})")

    if not dry_run:
        assert token is not None
        for bounty in bounties:
            slug = bounty.get("slug")
            if not isinstance(slug, str):
                continue

            if slug == "forecast-btc-7d":
                prediction = btc_signal(errors)
            elif slug == "forecast-nvda-3d":
                prediction = nvda_signal(errors)
            else:
                prediction = None
                skipped.append(f"{slug}: needs human/external work")
                log(f"skipped {slug}: needs human/external work")

            if prediction is None:
                continue

            try:
                status, response = submit_prediction(
                    base_url,
                    slug,
                    prediction,
                    handle,
                    token,
                )
                predictions_submitted.append(
                    {
                        "slug": slug,
                        "prediction": prediction,
                        "http_status": status,
                        "response": compact(response),
                    }
                )
                log(f"submit {slug}: HTTP {status}")
            except Exception as exc:
                errors.append(f"submit {slug} gagal: {compact(str(exc))}")
                log(f"submit {slug} gagal")

    summary = {
        "address": address,
        "handle": handle,
        "entered": entered,
        "entered_failed": entered_failed,
        "predictions_submitted": predictions_submitted,
        "skipped": skipped,
        "errors": errors,
    }

    try:
        with open("run_log.json", "w", encoding="utf-8") as file:
            json.dump(summary, file, ensure_ascii=False, indent=2)
    except OSError as exc:
        errors.append(f"gagal menulis run_log.json: {compact(str(exc))}")

    print(json.dumps(summary, ensure_ascii=False))
    return 0 if dry_run or entered else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous AIProve bounty agent")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="baca skill, health, dan daftar bounty tanpa write call",
    )
    args = parser.parse_args()
    return run(dry_run=args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
