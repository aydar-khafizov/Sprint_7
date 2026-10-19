import pytest
import requests
from urls import Urls
from helpers import generate_random_string


@pytest.fixture
def courier():
    """Фикстура создаёт уникального курьера и удаляет его после теста."""
    # 1. Генерируем уникальные данные для нового курьера
    courier_data = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(6)
    }

    # 2. Создаём курьера
    response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)

    # 3. Отдаём данные и ответ тесту (всё, что до yield - это setup)
    yield courier_data, response

    # 4. Всё, что после yield - это teardown (уборка после теста)
    # Авторизуемся, чтобы получить id созданного курьера
    login_response = requests.post(Urls.LOGIN_COURIER_URL, json={
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
    
    # Если авторизация прошла успешно (код 200) и в ответе есть id - удаляем курьера
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        requests.delete(f"{Urls.CREATE_COURIER_URL}/{courier_id}")