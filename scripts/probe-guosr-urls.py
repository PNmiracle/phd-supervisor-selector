#!/usr/bin/env python3
"""Probe all URLs in batch-write-guosr.py: status code, bytes, title."""
import json, re, ssl, sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

sys.path.insert(0, '/Users/leyiqingxue/.workbuddy/skills/phd-supervisor-selector/scripts')
# Import the candidates without executing the Vika write.
import importlib.util
spec = importlib.util.spec_from_file_location(
    'bwg', '/Users/leyiqingxue/.workbuddy/skills/phd-supervisor-selector/scripts/batch-write-guosr.py')
# We only want the CANDIDATES list; exec the file in a namespace with vika stubbed.
import types
ns = types.ModuleType('bwg')
# Stub out the token read and vika function so import does not hit the network.
def fake_vika(*a, **k):
    raise RuntimeError('not used')
ns.vika = fake_vika
spec.loader.exec_module(ns)

ctx = ssl.create_default_context()
CANDIDATES = ns.CANDIDATES

def probe(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'})
    try:
        with urlopen(req, timeout=20, context=ctx) as r:
            body = r.read(200000)
            status = r.status
            final_url = r.geturl()
            ctype = r.headers.get('Content-Type', '')
    except HTTPError as e:
        status = e.code
        body = b''
        final_url = url
        ctype = ''
    except URLError as e:
        status = f'ERR:{type(e).__name__}'
        body = b''
        final_url = url
        ctype = ''
    except Exception as e:
        status = f'ERR:{type(e).__name__}'
        body = b''
        final_url = url
        ctype = ''
    title = ''
    m = re.search(rb'<title[^>]*>(.*?)</title>', body, re.I | re.S)
    if m:
        title = m.group(1).decode('utf-8', 'ignore').strip()[:120]
    return status, len(body), title, final_url, ctype

for c in CANDIDATES:
    print(f"\n=== {c['导师']} ===")
    for field, key in [('主页', '主页'), ('申请', '申请'), ('档案', '档案')]:
        url = c[key]
        status, size, title, final_url, ctype = probe(url)
        flag = 'OK' if status == 200 and size > 1000 and title else 'CHECK'
        if status != 200:
            flag = 'BAD'
        print(f"  [{flag}] {field}: {status} | {size}B | {title or '(no title)'} | {url}")
        if final_url != url:
            print(f"      -> redirect: {final_url}")
