import pytest
from urls import Urls
from helpers import (
    generate_random_string, 
    create_courier, 
    login_courier, 
    delete_courier,
    cancel_order
)


@pytest.fixture
def courier():
    """Фикстура создаёт уникального курьера ДО теста и удаляет его ПОСЛЕ."""
    courier_data = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(6)
    }

    # Создаём курьера (запрос обернут в allure.step внутри helpers)
    response = create_courier(courier_data)

    # Отдаём данные и ответ тесту
    yield courier_data, response

    # Уборка после теста
    login_response = login_courier({
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
    
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)


@pytest.fixture
def courier_data_for_creation():
    """
    Фикстура генерирует данные для курьера, НЕ создавая его.
    После теста проверяет, был ли он создан, и если да — удаляет.
    """
    courier_data = {
        "login": generate_random_string(),
        "password": generate_random_string(),
        "firstName": generate_random_string(6)
    }
    
    yield courier_data  # Отдаём тесту только словарь с данными
    
    # Уборка после теста (сработает, если тест успешно создал курьера)
    login_response = login_courier({
        "login": courier_data["login"],
        "password": courier_data["password"]
    })
    
    if login_response.status_code == 200 and "id" in login_response.json():
        courier_id = login_response.json()["id"]
        delete_courier(courier_id)


@pytest.fixture
def order_tracker():
    """
    Фикстура для отслеживания созданных заказов.
    Возвращает пустой список, в который тест добавляет track.
    После теста отменяет все заказы из этого списка.
    """
    created_orders = []
    
    yield created_orders  # Отдаем пустой список тесту
    
    # Уборка после теста: отменяем все заказы, которые были созданы
    for track in created_orders:
        cancel_order(track)