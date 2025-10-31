from __future__ import annotations

import json
import os
from typing import Dict, List, Optional

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

_bearer = HTTPBearer(auto_error=False)

class RBAC:
    def __init__(self):
        raw = os.getenv('ITP_TOKENS', '{}')
        try:
            self.tokens: Dict[str, List[str]] = json.loads(raw)
        except Exception:
            self.tokens = {}

    def scopes_for(self, token: str) -> List[str]:
        return self.tokens.get(token, [])

rbac = RBAC()

# Dependency factory

def require_scopes(*scopes: str):
    async def _check(creds: Optional[HTTPAuthorizationCredentials] = Depends(_bearer)):
        if not scopes:
            return True
        if creds is None or not creds.scheme.lower() == 'bearer':
            raise HTTPException(status_code=401, detail='Missing bearer token')
        token = creds.credentials
        have = set(rbac.scopes_for(token))
        need = set(scopes)
        if not need.issubset(have):
            raise HTTPException(status_code=403, detail='Insufficient scopes')
        return True
    return _check
