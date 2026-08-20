from src.memory.mem0_service import Mem0Service


def test_mem0_disabled_by_default(monkeypatch):
    monkeypatch.delenv("MEM0_ENABLED", raising=False)
    service = Mem0Service()
    assert service.available is False
    assert service.search("What is my preference?") == []
    assert service.add_turn("hello", "hi") is False
