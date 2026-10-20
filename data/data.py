# Базовый шаблон заказа
base_order = {
    "firstName": "Иван",
    "lastName": "Петров",
    "address": "г. Москва, ул. Тверская, д. 1",
    "metroStation": 1,
    "phone": "+7 999 123 45 67",
    "rentTime": 5,
    "deliveryDate": "2026-10-20",
    "comment": "Комментарий к заказу"
}

# 1. Заказ с одним цветом BLACK
order_black = {**base_order, "color": ["BLACK"]}

# 2. Заказ с одним цветом GREY
order_gray = {**base_order, "color": ["GREY"]}

# 3. Заказ с обоими цветами
order_both = {**base_order, "color": ["BLACK", "GREY"]}

# 4. Заказ без указания цвета
order_no_color = {**base_order}


# Классы с константами для сообщений об ошибках
class CourierErrors:
    DUPLICATE_LOGIN = "Этот логин уже используется. Попробуйте другой."
    MISSING_FIELDS = "Недостаточно данных для создания учетной записи"


class LoginErrors:
    USER_NOT_FOUND = "Учетная запись не найдена"
    LOGIN_DATA_MISSING = "Недостаточно данных для входа"