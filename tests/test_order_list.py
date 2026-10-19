import allure
import requests
from urls import Urls


@allure.story("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_order_list_success(self):
        # Отправляем GET-запрос на ручку заказов
        response = requests.get(Urls.ORDER_URL)
        
        # Проверяем код ответа
        assert response.status_code == 200
        
        # Проверяем, что в теле ответа есть ключ "orders" и это список
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)