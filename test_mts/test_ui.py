import pytest
import allure
from .pages_shop.ShopMTC import Shop
from .config import Config

pytestmark = pytest.mark.all


@allure.feature("UI-тесты. Интернет-магазин МТС")
class TestUIShop:

    @allure.story("Позитивные проверки")
    @allure.title("Поиск существующего товара")
    @allure.description("Тест выполняет поиск на наличие существующего товара")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_search_existing_product(self, driver):
        shop = Shop(driver)
        with allure.step("Открыть главную страницу"):
            shop.main_page()
        with allure.step(f"Выполнить поиск товара '"
                         f"{Config.SEARCH_QUERIES['valid']}'"):
            shop.field_search(Config.SEARCH_QUERIES["valid"])
        with allure.step("Проверить, что результаты поиска отображаются"):
            results_displayed = shop.check_search_results_displayed()
            assert results_displayed is True

    @allure.story("Негативные проверки")
    @allure.title("Поиск несуществующего товара")
    @allure.description("Тест проверяет наличие сообщения,"
                        " при поиске несуществующего товара")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_search_invalid_product(self, driver):
        shop = Shop(driver)
        with allure.step("Открыть главную страницу"):
            shop.main_page()
        with allure.step(f"Выполнить поиск товара '"
                         f"{Config.SEARCH_QUERIES['invalid']}'"):
            shop.field_search(Config.SEARCH_QUERIES["invalid"])
        with allure.step("Проверить, наличия сообщения"
                         " об отсутствии результатов"):
            no_results_displayed = shop.check_no_results_message_displayed()
            assert no_results_displayed is True

    @allure.story("Негативные проверки")
    @allure.title("Поиск с пустым запросом")
    @allure.description("Тест проверяет URL страницы,"
                        " при поиске с пустым запросом")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_search_empty_query(self, driver):
        shop = Shop(driver)
        with allure.step("Открыть главную страницу"):
            shop.main_page()
        with allure.step("Выполнить поиск с пустым запросом"):
            shop.field_search(Config.SEARCH_QUERIES["empty"])
        with allure.step("Проверить, что мы остались на главной странице"):
            assert Config.BASE_URL == driver.current_url

    @allure.story("Позитивные проверки")
    @allure.title("Добавление товара в корзину")
    @allure.description("Тест проверяет добавление товара в корзину через UI")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.ui
    def test_add_to_cart(self, driver):
        shop = Shop(driver)
        with allure.step("Открыть главную страницу"):
            shop.main_page()
        with allure.step(f"Выполнить поиск товара '"
                         f"{Config.SEARCH_QUERIES['valid']}'"):
            shop.field_search(Config.SEARCH_QUERIES["valid"])
        with allure.step("Проверить, что результаты поиска отображаются"):
            results_displayed = shop.check_search_results_displayed()
            assert results_displayed is True
        with allure.step("Добавить товар в корзину"):
            shop.add_first_product_to_cart()
        with allure.step("Закрыть модальное окно 'Товары в корзине'"):
            shop.close_modal_page()
        with allure.step("Открыть корзину"):
            shop.open_cart()
        with allure.step("Проверить, что товар добавился в корзину"):
            has_items = shop.check_cart_has_items()
            assert has_items is True

    @allure.story("Позитивные проверки")
    @allure.title("Переход в категорию Смартфоны")
    @allure.description("Тест проверяет URL страницы,"
                        " при переходе в категорию 'Смартфоны'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_category_navigation(self, driver):
        shop = Shop(driver)
        with allure.step("Открыть главную страницу"):
            shop.main_page()
        with allure.step("Перейти в категорию Смартфоны"):
            shop.go_to_smartphones_category()
        with allure.step("Проверить, что URL содержит 'smartfony'"):
            url_contains = shop.check_url("smartfony")
            assert url_contains, (f"URL должен содержать 'smartfony',"
                                  f" текущий URL: {driver.current_url}")
