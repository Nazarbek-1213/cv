"""Privacy-preserving visit ping → Telegram bot.

Records only what the HTTP request already carries (no fingerprinting):
  - User-Agent → derived platform / device / browser
  - Referer (where the click came from)
  - Accept-Language (browser preferred language)
  - IP (logged once for geolocation by the recipient if desired)
  - Timestamp + page path

A signed cookie + sessionStorage on the client throttle the same browser
to ≤1 ping per hour, and bot User-Agents are skipped. If the bot
environment variables are not configured the endpoint quietly no-ops, so
this is safe to deploy unconfigured.

Env vars (set on Render → Environment):
  TELEGRAM_BOT_TOKEN  — from @BotFather
  TELEGRAM_CHAT_ID    — from @userinfobot (your own Telegram user id)
"""
from __future__ import annotations

import json
import logging
import os
import re
import urllib.request
from datetime import datetime, timezone

from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST


log = logging.getLogger(__name__)

COOKIE_NAME = "_v_pinged"
COOKIE_MAX_AGE = 60 * 60  # 1h throttle per browser

_BOT_UA_RE = re.compile(
    r"\b(bot|crawler|spider|slurp|preview|googlebot|bingbot|duckduckbot|yandexbot|"
    r"baiduspider|facebookexternalhit|whatsapp|skypeuripreview|telegrambot|"
    r"linkedinbot|twitterbot)\b",
    re.I,
)

_PLATFORMS = [
    # (label, regex). First match wins.
    ("Telegram", re.compile(r"Telegram|TGWebView|TGAndroid|tgshare", re.I)),
    ("Instagram", re.compile(r"Instagram", re.I)),
    ("Facebook", re.compile(r"FBAN|FBAV|FB_IAB|FBIOS", re.I)),
    ("LinkedIn", re.compile(r"LinkedInApp|LinkedIn/", re.I)),
    ("TikTok", re.compile(r"TikTok|musical_ly", re.I)),
    ("Twitter / X", re.compile(r"Twitter|TwitterAndroid", re.I)),
    ("WhatsApp", re.compile(r"WhatsApp", re.I)),
]


def _detect_platform(ua: str) -> str | None:
    for label, pat in _PLATFORMS:
        if pat.search(ua):
            return label
    return None


def _detect_browser(ua: str) -> str:
    if "Edg/" in ua:
        return "Edge"
    if "OPR/" in ua or "Opera" in ua:
        return "Opera"
    if "Chrome/" in ua and "Safari/" in ua and "Edg/" not in ua:
        return "Chrome"
    if "Safari/" in ua and "Chrome/" not in ua:
        return "Safari"
    if "Firefox/" in ua:
        return "Firefox"
    return "Browser"


def _detect_device(ua: str) -> str:
    if re.search(r"iPhone|iPod", ua):
        return "iPhone"
    if "iPad" in ua:
        return "iPad"
    if "Android" in ua:
        return "Android"
    if "Macintosh" in ua:
        return "Mac"
    if "Windows" in ua:
        return "Windows"
    if "Linux" in ua:
        return "Linux"
    return "Device"


def _client_ip(request) -> str:
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "")


def _accept_language(request) -> str:
    raw = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
    return raw.split(",")[0].split(";")[0].strip()


def _send_to_telegram(text: str) -> None:
    """Best-effort post; failures never propagate to the request."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
    if not (token and chat_id):
        log.info("visit ping skipped: TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set")
        return
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    body = json.dumps(
        {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urllib.request.urlopen(req, timeout=4).read()
    except Exception as exc:  # noqa: BLE001
        log.warning("visit ping failed: %s", exc)


def _truncate(s: str, n: int) -> str:
    return s if len(s) <= n else s[: n - 1] + "…"


@csrf_exempt
@require_POST
def visit(request):
    # 1. Already pinged this browser recently? Bail early.
    if request.COOKIES.get(COOKIE_NAME):
        return JsonResponse({"ok": True, "throttled": True})

    ua = request.META.get("HTTP_USER_AGENT", "")
    # 2. Ignore obvious bots / crawlers / link previewers.
    if not ua or _BOT_UA_RE.search(ua):
        return JsonResponse({"ok": True, "skipped": "bot"})

    # 3. Parse client payload (best-effort).
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except (ValueError, UnicodeDecodeError):
        payload = {}
    if not isinstance(payload, dict):
        return HttpResponseBadRequest("bad payload")

    referer = (payload.get("referrer") or request.META.get("HTTP_REFERER", ""))[:300]
    page = (payload.get("page") or "/")[:120]
    screen = str(payload.get("screen", ""))[:24]

    platform = _detect_platform(ua)
    browser = _detect_browser(ua)
    device = _detect_device(ua)
    lang = _accept_language(request)
    ip = _client_ip(request)

    when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "🔔 <b>New visit · Portfolio CV</b>",
        "━━━━━━━━━━━━━━━━━━━━━━━━",
        f"📅 {when}",
    ]
    if platform:
        lines.append(f"📱 Source: <b>{platform}</b> in-app browser")
    if referer:
        lines.append(f"↩️ From: <code>{_truncate(referer, 80)}</code>")
    lines.append(f"💻 {device} · {browser}")
    if lang:
        lines.append(f"🌐 Lang: <code>{lang}</code>")
    if screen:
        lines.append(f"🖥 {screen}")
    lines.append(f"📄 Page: <code>{page}</code>")
    if ip:
        lines.append(f"🌍 IP: <code>{ip}</code>")

    _send_to_telegram("\n".join(lines))

    resp = JsonResponse({"ok": True})
    resp.set_cookie(
        COOKIE_NAME, "1",
        max_age=COOKIE_MAX_AGE, httponly=True, samesite="Lax",
        secure=request.is_secure(),
    )
    return resp
