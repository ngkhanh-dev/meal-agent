# trace.py
import json
import copy
from datetime import datetime

TRACE_ENABLED = True

IGNORE_KEYS = {
    "api",          # object không serialize
}

def _safe(obj):
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return str(obj)

def trace_node(node_name: str):
    def decorator(fn):
        def wrapper(state: dict):
            if not TRACE_ENABLED:
                return fn(state)

            before = _safe({
                k: v for k, v in state.items()
                if k not in IGNORE_KEYS
            })

            print("\n" + "=" * 60)
            print(f"[TRACE] {datetime.now().isoformat()}")
            print(f"[NODE ] {node_name}")
            print(f"[IN   ] {json.dumps(before, indent=2, ensure_ascii=False)}")

            out = fn(state)

            after = _safe({
                k: v for k, v in out.items()
                if k not in IGNORE_KEYS
            })

            print(f"[OUT  ] {json.dumps(after, indent=2, ensure_ascii=False)}")
            print("=" * 60)

            return out
        return wrapper
    return decorator
