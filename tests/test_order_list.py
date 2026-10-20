import allure
from helpers import get_orders


@allure.story("Список заказов")
class TestOrderList:

    @allure.title("Получение списка заказов")
    def test_get_order_list_success(self):
        response = get_orders()
        
        assert response.status_code == 200
        response_json = response.json()
        assert "orders" in response_json
        assert isinstance(response_json["orders"], list)