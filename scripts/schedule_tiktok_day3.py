#!/usr/bin/env python3
"""Schedule day-3 Video_50..Video_46 to TikTok via Taisly (1/day, reverse order).

Usage:
  export TAISLY_API_KEY=taisly_...
  python3 scripts/schedule_tiktok_day3.py --start 2026-09-10 --time 10:00 --caption ""

Requires outbound HTTPS to app.taisly.com (not available inside the Arena sandbox).
Prefer the GitHub Action: .github/workflows/schedule-tiktok.yml
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

BASE = "https://app.taisly.com/api/private"
IST = timezone(timedelta(hours=5, minutes=30))
ROOT = Path(__file__).resolve().parents[1]


def api(key: str, method: str, path: str, form_fields=None, files=None):
    url = BASE + path
    if form_fields is not None or files is not None:
        cmd = [
            "curl",
            "-sS",
            "-X",
            method,
            url,
            "-H",
            f"Authorization: Bearer {key}",
            "-w",
            "\n__HTTP_STATUS__:%{http_code}",
        ]
        for k, v in (form_fields or {}).items():
            cmd += ["-F", f"{k}={v}"]
        for k, p in (files or {}).items():
            cmd += ["-F", f"{k}=@{p}"]
        out = subprocess.check_output(cmd, text=True)
        body, _, status_part = out.rpartition("\n__HTTP_STATUS__:")
        status = int(status_part.strip()) if status_part else 0
        try:
            parsed = json.loads(body) if body.strip() else {}
        except json.JSONDecodeError:
            parsed = {"raw": body}
        return status, parsed

    headers = {
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
        "User-Agent": "arena-taisly-scheduler/1.0",
    }
    req = Request(url, headers=headers, method=method)
    try:
        with urlopen(req, timeout=120) as resp:
            raw = resp.read().decode()
            return resp.status, json.loads(raw) if raw else {}
    except HTTPError as e:
        raw = e.read().decode()
        try:
            parsed = json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return e.code, parsed
    except URLError as e:
        return 0, {"error": str(e)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", default="2026-09-10", help="First day YYYY-MM-DD (IST)")
    parser.add_argument("--time", default="10:00", help="Daily HH:MM IST")
    parser.add_argument("--caption", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--key", default=os.environ.get("TAISLY_API_KEY", ""))
    args = parser.parse_args()
    key = args.key.strip()
    if not key:
        print("Set TAISLY_API_KEY or pass --key", file=sys.stderr)
        return 1

    print("=== auth / platforms ===")
    status, resp = api(key, "GET", "/platform/platforms")
    print("HTTP", status)
    print(json.dumps(resp, indent=2)[:3000])
    if status != 200 or not resp.get("success"):
        return 1

    platforms = resp.get("data") or []
    tiktok = [p for p in platforms if "tiktok" in str(p.get("platform", "")).lower()]
    if not tiktok:
        print("No TikTok connected")
        return 1
    tiktok_id = tiktok[0]["id"]
    print("TikTok id:", tiktok_id, tiktok[0].get("username") or tiktok[0].get("displayName"))

    hour, minute = map(int, args.time.split(":"))
    start = datetime.strptime(args.start, "%Y-%m-%d").replace(
        hour=hour, minute=minute, second=0, microsecond=0, tzinfo=IST
    )
    videos = [ROOT / f"day-3/Video_{n:02d}.mp4" for n in range(50, 45, -1)]
    plan = []
    for i, path in enumerate(videos):
        when = start + timedelta(days=i)
        plan.append((path, when, int(when.timestamp() * 1000)))
        print(f"  {path.name} @ {when.isoformat()} ms={int(when.timestamp()*1000)}")

    if args.dry_run:
        print("dry-run done")
        return 0

    for i, (path, when, ms) in enumerate(plan, 1):
        print(f"\n--- uploading day {i} {path.name} ---")
        st, r = api(
            key,
            "POST",
            "/post",
            form_fields={
                "platforms": json.dumps([tiktok_id]),
                "description": args.caption,
                "previewTime": "0",
                "scheduled": str(ms),
            },
            files={"video": str(path)},
        )
        print("HTTP", st)
        print(json.dumps(r, indent=2)[:2000])
        time.sleep(2)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
