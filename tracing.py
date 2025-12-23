# tracing.py
import json
import logging
from datetime import datetime
from functools import wraps

# =========================
# Logging configuration
# =========================

LOGGER_NAME = "meal_agent.trace"

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# =========================
# Trace config
# =========================

TRACE_ENABLED = True

IGNORE_KEYS = {
    "api",  # object không serialize
}

# =========================
# Utils
# =========================

def _safe(obj):
    """Serialize state safely for logging"""
    try:
        return json.loads(json.dumps(obj, default=str))
    except Exception:
        return str(obj)

# =========================
# Decorator
# =========================

def trace_node(node_name: str):
    """
    Trace LangGraph node:
    - log input state
    - log output state
    - isolate observability from business logic
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(state: dict):
            if not TRACE_ENABLED:
                return fn(state)

            before = _safe({
                k: v for k, v in state.items()
                if k not in IGNORE_KEYS
            })

            logger.info("=" * 60)
            logger.info("[NODE ] %s", node_name)
            logger.info("[IN   ] %s", json.dumps(
                before, indent=2, ensure_ascii=False
            ))

            out = fn(state)

            if not isinstance(out, dict):
                logger.error(
                    "[NODE %s] returned non-dict output: %r",
                    node_name,
                    out,
                )
                raise TypeError(
                    f"Node '{node_name}' must return dict, got {type(out)}"
                )

            after = _safe({
                k: v for k, v in out.items()
                if k not in IGNORE_KEYS
            })

            logger.info("[OUT  ] %s", json.dumps(
                after, indent=2, ensure_ascii=False
            ))
            logger.info("=" * 60)

            return out

        return wrapper
    return decorator
