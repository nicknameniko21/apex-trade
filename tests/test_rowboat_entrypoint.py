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


def test_rowboat_resolve_host_defaults(monkeypatch):
    rowboat = importlib.import_module("rowboat")
    monkeypatch.delenv("HOST", raising=False)
    monkeypatch.delenv("PORT", raising=False)
    monkeypatch.delenv("ROWBOAT_STARTUP", raising=False)
    assert rowboat.resolve_host(None) == "127.0.0.1"


def test_rowboat_resolve_host_rowboat(monkeypatch):
    rowboat = importlib.import_module("rowboat")
    monkeypatch.delenv("HOST", raising=False)
    monkeypatch.setenv("ROWBOAT_STARTUP", "1")
    assert rowboat.resolve_host(None) == "0.0.0.0"
