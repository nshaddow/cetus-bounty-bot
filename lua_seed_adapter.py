# lua_seed_adapter.py

import hashlib
import datetime

def seed_from_worldstate(ws: dict) -> int:
    """
    If we later get the actual Lua seed logic, we plug it in here.
    """
    if ws and "timestamp" in ws:
        base = str(ws["timestamp"])
    else:
        base = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H")

    h = hashlib.sha256(base.encode()).hexdigest()
    return int(h[:8], 16)