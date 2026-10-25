#!/usr/bin/env python3
"""Ping IndexNow (Bing, Yandex, Seznam...) with all sitemap URLs after a prod deploy.
Run after a prod deploy: python3 scripts/indexnow_ping.py"""
import json, re, urllib.request, pathlib

KEY = (pathlib.Path(__file__).parent / "indexnow_key.txt").read_text().strip()
HOST = "beatplan.io"

sitemap = urllib.request.urlopen(f"https://{HOST}/sitemap.xml", timeout=30).read().decode()
urls = re.findall(r"<loc>([^<]+)</loc>", sitemap)

body = json.dumps({
    "host": HOST,
    "key": KEY,
    "keyLocation": f"https://{HOST}/{KEY}.txt",
    "urlList": urls,
}).encode()
req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                             headers={"Content-Type": "application/json; charset=utf-8"})
with urllib.request.urlopen(req, timeout=30) as r:
    print(f"IndexNow: HTTP {r.status} for {len(urls)} URLs")
