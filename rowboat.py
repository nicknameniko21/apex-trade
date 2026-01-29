#!/usr/bin/env python3
"""
Rowboat entry point for launching the CTO system and UI.
"""

import logging
import os

from cto_self_sustaining_startup import run_startup
from ui_server import app, initialize_swarm

logger = logging.getLogger(__name__)
DEFAULT_PORT = 5000
DEFAULT_HOST = "127.0.0.1"
ROWBOAT_HOST = "0.0.0.0"


def get_app():
    """Expose the Flask app for testing."""
    return app


def resolve_host(port_value):
    host = os.environ.get("HOST")
    if host:
        return host
    if os.environ.get("ROWBOAT_STARTUP") == "1":
        return ROWBOAT_HOST
    if port_value is not None:
        return ROWBOAT_HOST
    return DEFAULT_HOST


def main():
    os.environ.setdefault("ROWBOAT_STARTUP", "1")
    run_startup()
    initialize_swarm()
    port_value = os.environ.get("PORT")
    if port_value is None:
        port = DEFAULT_PORT
    else:
        try:
            port = int(port_value)
        except ValueError:
            logger.warning("Invalid PORT value %r, defaulting to %s", port_value, DEFAULT_PORT)
            port = DEFAULT_PORT
    host = resolve_host(port_value)
    if host == "0.0.0.0":
        logger.warning(
            "HOST is set to 0.0.0.0, exposing the service on all interfaces; "
            "set HOST to restrict external access."
        )
    logger.info("Starting Rowboat UI on http://%s:%s", host, port)
    logger.warning(
        "Flask development server in use; configure a production WSGI server for deployments."
    )
    app.run(debug=False, host=host, port=port)


if __name__ == "__main__":
    main()
