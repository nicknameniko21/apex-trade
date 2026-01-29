"""
Vercel serverless entrypoint for the Flask UI.
Ensures root path is available and initializes the swarm lazily
to avoid cold-start timeouts.
"""

import logging
import sys
from pathlib import Path

# Make repo root importable when Vercel executes from the /api directory
ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from ui_server import app as flask_app, initialize_swarm  # noqa: E402

logger = logging.getLogger(__name__)
_initialized = False


def _ensure_initialized():
    global _initialized
    if _initialized:
        return
    try:
        initialize_swarm()
        _initialized = True
    except Exception as exc:  # pragma: no cover - defensive
        logger.error("Failed to initialize swarm during cold start: %s", exc)
        raise


# Vercel Python runtime looks for a module-level WSGI app
_ensure_initialized()
app = flask_app
