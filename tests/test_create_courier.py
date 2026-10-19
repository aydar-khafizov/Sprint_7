import allure
import requests
from urls import Urls
from helpers import generate_random_string


# Класс с константами для сообщений
class Data:
    DUPLICATE_LOGIN = "Этот логин уже используется. Попробуйте другой."
    MISSING_FIELDS = "Недостаточно данных для создания учетной записи"


@allure.story("Создание курьера")
class TestCreateCourier:

    @allure.title("Успешное создание курьера")
    def test_create_courier_success(self):
        courier_data = {
            "login": generate_random_string(),
            "password": generate_random_string(),
            "firstName": generate_random_string(6)
        }
        with allure.step("Создание нового курьера"):
            response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)
            assert response.status_code == 201
            assert response.json() == {"ok": True}
        
        # Очистка: удаляем созданного курьера
        with allure.step("Удаление созданного курьера"):
            login_response = requests.post(Urls.LOGIN_COURIER_URL, json={
                "login": courier_data["login"],
                "password": courier_data["password"]
            })
            if login_response.status_code == 200 and "id" in login_response.json():
                courier_id = login_response.json()["id"]
                requests.delete(f"{Urls.CREATE_COURIER_URL}/{courier_id}")

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_duplicate_courier(self, courier):

        courier_data, _ = courier
        # Создать курьера с теми же данными
        duplicate_response = requests.post(Urls.CREATE_COURIER_URL, json=courier_data)
        assert duplicate_response.status_code == 409
        assert duplicate_response.json()["message"] == Data.DUPLICATE_LOGIN

    @allure.title("Ошибка при создании без логина")
    def test_create_courier_no_login(self):
        data = {"password": generate_random_string(), "firstName": generate_random_string(6)}
        response = requests.post(Urls.CREATE_COURIER_URL, json=data)
        assert response.status_code == 400
        assert response.json()["message"] == Data.MISSING_FIELDS

    @allure.title("Ошибка при создании без пароля")
    def test_create_courier_no_password(self):
        data = {"login": generate_random_string(), "firstName": generate_random_string(6)}
        response = requests.post(Urls.CREATE_COURIER_URL, json=data)
        assert response.status_code == 400
        assert response.json()["message"] == Data.MISSING_FIELDS

    @allure.title("Ошибка при создании с существующим логином")
    def test_create_courier_existing_login(self, courier):
        courier_data, _ = courier
        new_data = {
            "login": courier_data["login"],
            "password": generate_random_string(),
            "firstName": generate_random_string(6)
        }
        response = requests.post(Urls.CREATE_COURIER_URL, json=new_data)
        assert response.status_code == 409
        assert response.json()["message"] == Data.DUPLICATE_LOGIN