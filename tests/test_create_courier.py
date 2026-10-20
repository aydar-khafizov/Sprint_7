import allure
from helpers import generate_random_string, create_courier
from data.data import CourierErrors


@allure.story("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self, courier_data_for_creation):
        response = create_courier(courier_data_for_creation)
        
        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier):
        courier_data, _ = courier
        duplicate_response = create_courier(courier_data)
        
        assert duplicate_response.status_code == 409
        assert duplicate_response.json()["message"] == CourierErrors.DUPLICATE_LOGIN

    @allure.title("Ошибка при создании без логина")
    def test_create_courier_no_login(self):
        data = {"password": generate_random_string(), "firstName": generate_random_string(6)}
        response = create_courier(data)
        
        assert response.status_code == 400
        assert response.json()["message"] == CourierErrors.MISSING_FIELDS

    @allure.title("Ошибка при создании без пароля")
    def test_create_courier_no_password(self):
        data = {"login": generate_random_string(), "firstName": generate_random_string(6)}
        response = create_courier(data)
        
        assert response.status_code == 400
        assert response.json()["message"] == CourierErrors.MISSING_FIELDS

    @allure.title("Ошибка при создании с существующим логином")
    def test_create_courier_existing_login(self, courier):
        courier_data, _ = courier
        new_data = {
            "login": courier_data["login"],
            "password": generate_random_string(),
            "firstName": generate_random_string(6)
        }
        response = create_courier(new_data)
        
        assert response.status_code == 409
        assert response.json()["message"] == CourierErrors.DUPLICATE_LOGIN