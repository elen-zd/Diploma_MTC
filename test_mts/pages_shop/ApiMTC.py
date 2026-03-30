import allure
import requests


class CartAPIClient:
    """
    Класс для работы с API корзины интернет-магазина МТС.
    Содержит методы для выполнения операций с корзиной через API.
    """

    def __init__(self, api_url) -> None:
        """
        Конструктор класса.

        Инициализирует базовый URL API и заголовки для HTTP-запросов.

        :param api_url: str — базовый URL API.
        :return: None — метод ничего не возвращает.
        :rtype: None
        """
        self.api_url = api_url
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    @allure.step("Добавить товар {product_id} в корзину")
    def add_product(self, product_id: int) -> requests.Response:
        """
        Добавление товара в корзину через API.

        Выполняет POST запрос на endpoint /cart/add
        с указанием ID товара.

        :param product_id: int — идентификатор товара.
        :return: Response — объект ответа requests.
        :rtype: requests.Response
        """
        url = f"{self.api_url}/cart/add"
        body = {"id": product_id}
        response = self.session.post(url, headers=self.headers, json=body)
        return response

    @allure.step("Получить содержимое корзины")
    def get_cart(self) -> requests.Response:
        """
        Получение содержимого корзины через API.

        Выполняет GET запрос на endpoint /cart,
        для получения списка товаров в корзине.

        :return: Response — объект ответа requests.
        :rtype: requests.Response.
        """
        url = f"{self.api_url}/cart"
        response = self.session.get(url, headers=self.headers)
        return response

    @allure.step("Редактировать количество товара {product_id} до {quantity}")
    def update_cart_item(self, product_id: int,
                         quantity: int) -> requests.Response:
        """
        Изменение количества товара в корзине.

        Выполняет PATCH-запрос на endpoint /baskets/current/items
        для изменения количества товара по его id

        :param product_id: int — идентификатор товара.
        :param quantity: Int — новое количество.
        :return: Response — объект ответа requests.
        :rtype: requests.Response.
        """
        url = f"{self.api_url}/baskets/current/items"
        body = {
            "products": [
                {
                    "id": product_id,
                    "quantity": quantity
                }
            ]
        }
        response = self.session.patch(url, headers=self.headers, json=body)
        return response

    @allure.step("Удалить товар {basket_item_id} из корзины")
    def delete_cart_item(self, basket_item_id: int) -> requests.Response:
        """
        Удаление товара из корзины.

        Выполняет DELETE запрос на endpoint /baskets/current/items/{id},
        для удаления товара по id товара в корзине.

        :param basket_item_id: int — идентификатор товара в корзине.
        :return: Response — объект ответа requests.
        :rtype: requests.Response
        """
        url = f"{self.api_url}/baskets/current/items/{basket_item_id}"
        response = self.session.delete(url, headers=self.headers)
        return response

    @allure.step("Очистить корзину")
    def clear_cart(self) -> None:
        """
        Полная очистка корзины.

        Получает текущую корзину через GET запрос,
        извлекает список товаров и последовательно удаляет
        каждый товар из корзины.

        :return: None — метод ничего не возвращает.
        :rtype: None
        """
        cart_response = self.get_cart()
        cart_body = cart_response.json()
        items = cart_body.get("items", [])

        for item in items:
            cart_item_id = item.get("id")
            if cart_item_id:
                self.delete_cart_item(cart_item_id)

    def get_product_quantity(self, product_id: int) -> int:
        """
        Получение количества товара в корзине по id товара.

        Выполняет GET запрос для получения списка товаров в корзине,
        находит товар по ID и возвращает его количество.

        :param product_id: int — идентификатор товара.
        :return: int — количество товара (0 если товар не найден).
        :rtype: int
        """
        cart_response = self.get_cart()
        cart_body = cart_response.json()
        items = cart_body.get("items", [])
        for item in items:
            if str(item.get("id")) == str(product_id):
                return item.get("quantity", 0)
        return 0
