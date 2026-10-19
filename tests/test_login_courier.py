import allure
import pytest
import requests
from urls import Urls
from helpers import generate_random_string


class Data:
    USER_NOT_FOUND = "Учетная запись не найдена"
    LOGIN_DATA_MISSING = "Недостаточно данных для входа"


@allure.story("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешная авторизация курьера")
    def test_login_success(self, courier):

        courier_data, _ = courier
        
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": courier_data["password"]
        })
        
        assert response.status_code == 200
        # Проверяем, что в ответе есть id
        assert "id" in response.json()

    @allure.title("Ошибка при неверном логине")
    def test_login_wrong_login(self, courier):
        courier_data, _ = courier
        
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": generate_random_string(),
            "password": courier_data["password"]
        })
        
        assert response.status_code == 404
        assert response.json()["message"] == Data.USER_NOT_FOUND

    @allure.title("Ошибка при неверном пароле")
    def test_login_wrong_password(self, courier):
        courier_data, _ = courier
        
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": generate_random_string()
        })
        
        assert response.status_code == 404
        assert response.json()["message"] == Data.USER_NOT_FOUND

    @allure.title("Ошибка авторизации под несуществующим пользователем")
    def test_login_non_existent_user(self):
        # Пытаемся войти с абсолютно случайными данными
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": generate_random_string(),
            "password": generate_random_string()
        })
        
        assert response.status_code == 404
        assert response.json()["message"] == Data.USER_NOT_FOUND

    @allure.title("Ошибка при отсутствии логина")
    def test_login_no_login(self, courier):
        courier_data, _ = courier
        
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": "",
            "password": courier_data["password"]
        })
        
        assert response.status_code == 400
        assert response.json()["message"] == Data.LOGIN_DATA_MISSING

    @allure.title("Ошибка при отсутствии пароля")
    def test_login_no_password(self, courier):
        courier_data, _ = courier
        
        response = requests.post(Urls.LOGIN_COURIER_URL, json={
            "login": courier_data["login"],
            "password": "" 
        })
        
        assert response.status_code == 400
        assert response.json()["message"] == Data.LOGIN_DATA_MISSING