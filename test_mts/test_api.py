import pytest
import allure
from .config import Config

pytestmark = pytest.mark.all


@allure.feature("API-тесты. Интернет-магазин МТС")
class TestAPICart:

    @allure.story("Позитивные проверки")
    @allure.title("Добавление товара в корзину")
    @allure.description("Тест проверяет добавление товара в корзину через API")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.api
    def test_add_product_to_cart(self, cart_client):
        with allure.step("Добавить товар"):
            response = cart_client.add_product(Config.VALID_PRODUCT_ID)
        with allure.step("Получение содержимого корзины"):
            cart_response = cart_client.get_cart()
        with allure.step("Проверить статус ответа"):
            assert cart_response.status_code == 200, (
                f"Ожидаемый результат: статус 200, "
                f"Фактический результат: {response.status_code}")
        with allure.step("Проверить, что количество товаров больше 0"):
            cart_body = cart_response.json()
            items = cart_body.get("items", [])
            assert len(items) > 0
        with allure.step("Проверить, что id товара в корзине"
                         " соответствует добавленному товару"):
            assert items[0]["id"] == 947328, (
                f"Ожидаемый результат: id = 947328,"
                f"Фактический результат: {items[0]['id']}")

    @allure.story("Позитивные проверки")
    @allure.title("Получение списка товаров в корзине")
    @allure.description("Тест получает список товаров в корзине")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_get_cart_items(self, cart_client):
        with allure.step("Добавить товар"):
            response = cart_client.add_product(Config.VALID_PRODUCT_ID)
        with allure.step("Получение содержимого корзины"):
            cart_response = cart_client.get_cart()
        with allure.step("Проверить статус ответа"):
            assert cart_response.status_code == 200, (
                f"Ожидаемый результат: статус 200, "
                f"Фактический результат: {response.status_code}")

        with allure.step("Проверить, что количество товаров больше 0"):
            cart_body = cart_response.json()
            items = cart_body.get("items", [])
            assert len(items) > 0, (
                f"Ожидаемый результат: количество товаров = 1"
                f"Фактический результат: {len(items)}")

    @allure.story("Позитивные проверки")
    @allure.title("Редактирование количества товара в корзине")
    @allure.description("Тест изменяет количество товара в корзине")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_update_cart_item_quantity(self, cart_client):
        with allure.step("Добавить товар в корзину"):
            response = cart_client.add_product(Config.VALID_PRODUCT_ID)
        with allure.step("Проверить, что количество равно 1"):
            items_before = response.json().get("personalCart", {}).get(
                "items", [])
            assert items_before[0]["quantity"] == 1
        with allure.step("Изменить количество товара на 2"):
            response_edit = cart_client.update_cart_item(
                Config.VALID_PRODUCT_ID, 2)
            with allure.step("Проверить статус ответа"):
                assert response_edit.status_code == 200
        with allure.step("Проверить, что количество изменилось"):
            items_after = response_edit.json().get("items", [])
            assert items_after[0]["quantity"] == 2, (
                f"Ожидаемый результат: количество = 2, "
                f"Фактический результат: {items_after}")

    @allure.story("Позитивные проверки")
    @allure.title("Удаление товара из корзины")
    @allure.description("Тест выполняет удаление товара из корзины")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.api
    def test_delete_product_from_cart(self, cart_client):
        with allure.step("Добавить товар в корзину"):
            response = cart_client.add_product(Config.VALID_PRODUCT_ID)
            with allure.step("Получить ID позиции в корзине"):
                item_id = (
                    response.json()["personalCart"]["items"][0]["cartItemId"])
                allure.attach(str(item_id),
                              "cartItemId", allure.attachment_type.TEXT)
        with allure.step("Удалить товар из корзины"):
            response = cart_client.delete_cart_item(item_id)
            with allure.step("Проверить статус ответа"):
                assert response.status_code == 200
        with allure.step("Проверить, что корзина пуста"):
            items = cart_client.get_cart().json().get("items", [])
            assert len(items) == 0

    @allure.story("Негативные проверки")
    @allure.title("Добавление несуществующего товара в корзину")
    @allure.description("Тест проверяет наличие сообщения об ошибке"
                        " при добавлении несуществующего товара")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_add_invalid_product_to_cart(self, cart_client):
        with allure.step("Добавить несуществующий товар в корзину"):
            response = cart_client.add_product(Config.INVALID_PRODUCT_ID)
        with allure.step("Проверить статус ответа"):
            assert response.status_code == 400, (
                f"Ожидаемый результат: статус 400, "
                f"Фактический результат: {response.status_code}")
        with allure.step("Проверить сообщение об ошибке"):
            response_body = response.json()
            assert response_body["error"]["title"] == "не удалось добавить"
