import allure
import pytest
from helpers import create_order
from data.data import order_black, order_gray, order_both, order_no_color


@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с разными вариантами цвета")
    @pytest.mark.parametrize(
        "order_data", 
        [order_black, order_gray, order_both, order_no_color],
        ids=["BLACK", "GREY", "BLACK_AND_GREY", "NO_COLOR"]
    )
    def test_create_order_success(self, order_data, order_tracker):
        response = create_order(order_data)
        
        assert response.status_code == 201
        response_json = response.json()
        assert "track" in response_json
        
        # Передаем track в фикстуру для последующей отмены
        order_tracker.append(response_json["track"])