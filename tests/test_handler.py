import json
import types
import socket as real_socket
from handler import check_host


class DummySocket:
    def __init__(self, connect_result: int):
        self._connect_result = connect_result
        self.timeout = None

    def settimeout(self, timeout):
        self.timeout = timeout

    def connect_ex(self, addr):
        return self._connect_result

    def close(self):
        return None


def _with_stubbed_socket(monkeypatch, result_code: int):
    # Patch socket.socket to return our dummy implementation
    monkeypatch.setattr(
        real_socket, "socket", lambda *args, **kwargs: DummySocket(connect_result=result_code)
    )


def test_missing_host_returns_400():
    event = {"body": json.dumps({})}
    result = check_host(event, None)
    assert result["statusCode"] == 400


def test_active_when_port_open(monkeypatch):
    _with_stubbed_socket(monkeypatch, 0)
    event = {"body": json.dumps({"host": "example.com", "port": 80})}
    result = check_host(event, None)
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["status"] == "active"
    assert body["host"] == "example.com"
    assert body["port"] == 80


def test_inactive_when_port_closed(monkeypatch):
    _with_stubbed_socket(monkeypatch, 111)
    event = {"body": json.dumps({"host": "example.com", "port": 81})}
    result = check_host(event, None)
    body = json.loads(result["body"])
    assert result["statusCode"] == 200
    assert body["status"] == "inactive"
