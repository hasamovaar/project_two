from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_main_page():
    """Проверяет, что главная страница работает"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Переводчик" in response.text  # Теперь проверяем новый заголовок
    assert "textarea" in response.text  # Проверяем наличие поля ввода

def test_translation():
    """Тестируем перевод текста (теперь проверяем HTML-ответ)"""
    test_cases = [
        ("mouse in room", "мышь в комнате")
    ]
    
    for english, expected_russian in test_cases:
        response = client.get(f"/translate/?text={english}")
        assert response.status_code == 200
        
        # Теперь ищем перевод в HTML, а не в JSON
        assert expected_russian in response.text, \
            f'Для "{english}" ожидали "{expected_russian}", получили "{response.text}"'