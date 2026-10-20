import random
import string
import allure
import requests
from urls import Urls


def generate_random_string(length=10):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


@allure.step("Отправка запроса на создание курьера")
def create_courier(data):
    return requests.post(Urls.CREATE_COURIER_URL, json=data)


@allure.step("Отправка запроса на логин курьера")
def login_courier(data):
    return requests.post(Urls.LOGIN_COURIER_URL, json=data)


@allure.step("Отправка запроса на удаление курьера по ID: {courier_id}")
def delete_courier(courier_id):
    return requests.delete(f"{Urls.CREATE_COURIER_URL}/{courier_id}")


@allure.step("Отправка запроса на создание заказа")
def create_order(data):
    return requests.post(Urls.ORDER_URL, json=data)


@allure.step("Отправка запроса на получение списка заказов")
def get_orders():
    return requests.get(Urls.ORDER_URL)


@allure.step("Отправка запроса на отмену заказа по треку: {track}")
def cancel_order(track):
    return requests.put(f"{Urls.ORDER_URL}/cancel", params={"track": track})