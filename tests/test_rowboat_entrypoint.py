import importlib

import pytest

try:
    import flask  # noqa: F401
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False


@pytest.mark.skipif(not HAS_FLASK, reason="flask not installed")
def test_rowboat_get_app():
    rowboat = importlib.import_module("rowboat")
    app = rowboat.get_app()
    assert app is not None
