import project

def test_get_username(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "Mark")
    assert project.get_username() == "Mark"

    monkeypatch.setattr('builtins.input', lambda _: "Astanatol")
    assert project.get_username() == "Astanatol"

def test_get_site(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: "aswanatawa")
    assert project.get_site("site") == "aswanatawa"

    monkeypatch.setattr('builtins.input', lambda _: "monter556")
    assert project.get_site("login") == "monter556"

def test_get_opt(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda _: 2)
    assert project.get_opt(3) == 2
