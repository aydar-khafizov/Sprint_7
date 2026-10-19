import allure
import pytest
import requests
from urls import Urls
from data.data import order_black, order_gray, order_both, order_no_color


@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize(
        "order_data", 
        [order_black, order_gray, order_both, order_no_color],
        ids=["BLACK", "GREY", "BLACK_AND_GREY", "NO_COLOR"]
    )
    def test_create_order_success(self, order_data):
        # 1. Создаем заказ
        response = requests.post(Urls.ORDER_URL, json=order_data)
        
        # 2. Проверяем код ответа и наличие track
        assert response.status_code == 201
        response_json = response.json()
        assert "track" in response_json
        
        # 3. Очистка: отменяем заказ, чтобы не засорять базу
        track = response_json["track"]
        requests.put(f"{Urls.ORDER_URL}/cancel", params={"track": track})