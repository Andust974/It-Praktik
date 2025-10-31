from __future__ import annotations

import os
import re
import socket
import urllib.request
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl

router = APIRouter(prefix='/web', tags=['web'])

DEFAULT_ALLOW = {'raw.githubusercontent.com', 'example.com'}
MAX_BYTES_DEFAULT = 1_048_576

class FetchReq(BaseModel):
    url: HttpUrl
    method: str = 'GET'

@router.post('/fetch')
def fetch(req: FetchReq):
    method = req.method.upper()
    if method not in ('GET','HEAD'):
        # блокируем небезопасные методы
        raise HTTPException(status_code=405, detail='Only GET/HEAD allowed')
    host = urllib.request.urlparse.urlparse(str(req.url)).hostname or ''
    allow_env = os.getenv('ITP_WEB_ALLOW', '')
    allow = {h.strip() for h in allow_env.split(',') if h.strip()} or DEFAULT_ALLOW
    if host not in allow:
        raise HTTPException(status_code=403, detail=f'Host not allowed: {host}')
    max_bytes = int(os.getenv('ITP_WEB_MAX_BYTES', str(MAX_BYTES_DEFAULT)))
    req_obj = urllib.request.Request(str(req.url), method=method, headers={'User-Agent':'ITP/1.0'})
    try:
        with urllib.request.urlopen(req_obj, timeout=10) as resp:
            data = resp.read(max_bytes)
            truncated = False
            if len(data) == max_bytes:
                # Пробуем понять, есть ли ещё данные
                try:
                    more = resp.read(1)
                    if more:
                        truncated = True
                except Exception:
                    pass
            content_type = resp.headers.get('Content-Type','')
            text: Optional[str] = None
            if content_type.startswith('text/') or 'json' in content_type:
                try:
                    text = data.decode('utf-8', errors='ignore')
                except Exception:
                    text = None
            return {
                'url': str(req.url),
                'status': resp.status,
                'headers': {k:v for k,v in resp.headers.items()},
                'bytes': len(data),
                'truncated': truncated,
                'content_type': content_type,
                'text': text
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=502, detail=f'Fetch error: {e}')
