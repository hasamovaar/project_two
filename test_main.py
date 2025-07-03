from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_main_page():
    """Проверяет, что главная страница работает"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Введите текст на английском" in response.text

def test_translation():
    """Тестируем конкретные примеры переводов"""
    test_cases = [
        ("mouse in room", "мышь в комнате")
    ]
    
    for english, expected_russian in test_cases:
        response = client.get(f"/translate/?text={english}")
        assert response.status_code == 200
        
        result = response.json()
        actual_translation = result["translation"]
        
        # Проверяем что перевод содержит ожидаемую фразу
        # (используем in, так как перевод может быть немного другим)
        assert expected_russian in actual_translation, \
            f'Для "{english}" ожидали "{expected_russian}", получили "{actual_translation}"'