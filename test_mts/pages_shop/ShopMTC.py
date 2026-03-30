from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import allure
from ..config import Config


class Shop:
    """
    Класс для работы с UI интернет-магазина МТС.
    Содержит методы для выполнения операций на страницах магазина.
    """
    def __init__(self, driver: WebDriver) -> None:
        """
        Конструктор класса Shop.

        Инициализирует драйвер и объект ожидания для работы с элементами.

        :param driver: WebDriver — объект драйвера Selenium.
        :return: None — метод ничего не возвращает.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.EXPLICIT_WAIT)

    @allure.step("Открыть главную страницу")
    def main_page(self) -> None:
        """
        Открытие главной страницы интернет-магазина МТС.

        Выполняет переход на главную страницу, закрывает модальное окно
        выбора региона и устанавливает куки для согласия на cookies.

        :return: None — метод ничего не возвращает.
        """
        self.driver.get(Config.BASE_URL)
        region_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        Config.SELECTORS["region_button"]))
        )
        region_button.click()

        self.driver.add_cookie({'name': 'COOKIES_MASSAGE_APPLY',
                                'value': 'true'})
        self.driver.refresh()

    @allure.step("Выполнить поиск: {query}")
    def field_search(self, query: str) -> None:
        """
        Выполнение поиска товара по поисковому запросу.

        Находит поле поиска, кликает по нему.
        Ожидает появления модального окна со строкой поиска.
        Кликает по стоке поиска в модальном окне.
        Очищает строку поиска.
        Вводит запрос и нажимает Enter.

        :param query: str — поисковый запрос.
        :return: None — метод ничего не возвращает.
        """
        search_input = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        Config.SELECTORS["search_input"]))
        )
        search_input.click()
        search_popup = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            Config.SELECTORS["search_popup"]))
        )
        search_popup.clear()
        search_popup.send_keys(query)
        search_popup.send_keys(Keys.ENTER)

    @allure.step("Отображение результатов поиска с валидным запросом")
    def check_search_results_displayed(self) -> bool:
        """
        Проверка отображения результатов поиска.

        Ожидает появления карточки товара на странице результатов поиска.

        :return: bool — True если результаты отображаются.
        """
        results = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            Config.SELECTORS["product_card"]))
        )
        return results.is_displayed()

    @allure.step("Отображение результатов поиска с невалидным запросом")
    def check_no_results_message_displayed(self) -> bool:
        """
        Проверка отображения сообщения об отсутствии результатов.

        Ожидает появления сообщения "Ничего не нашлось" на странице.

        :return: bool — True если сообщение отображается.
        """
        no_results = self.wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            Config.SELECTORS["no_results"]))
        )
        return no_results.is_displayed()

    @allure.step("Добавление товара в корзину")
    def add_first_product_to_cart(self) -> None:
        """
        Добавление товара из результатов поиска в корзину.

        Находит карточку товара и нажимает кнопку добавления в корзину.

        :return: None — метод ничего не возвращает.
        """
        add_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        Config.SELECTORS["add_to_cart"]))
        )
        add_button.click()

    @allure.step("Закрыть окно 'Товар в корзине' после добавления товара")
    def close_modal_page(self) -> None:
        """
        Закрытие модального окна после добавления товара.

        Ожидает появления модального окна.
        Находит и нажимает кнопку закрытия.

        :return: None — метод ничего не возвращает.
        """
        self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            Config.SELECTORS["modal_page"]))
        )
        close_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        Config.SELECTORS["close_modal_page"]))
        )
        close_button.click()

    @allure.step("Перейти в корзину")
    def open_cart(self) -> None:
        """
        Открытие страницы корзины.

        Находит и нажимает на иконку корзины.

        :return: None — метод ничего не возвращает.
        """
        cart_icon = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                        Config.SELECTORS["cart_icon"]))
        )
        cart_icon.click()

    @allure.step("Наличие товара в корзине")
    def check_cart_has_items(self) -> bool:
        """
        Проверка наличия товаров в корзине.

        Находит все элементы товаров в корзине и проверяет их количество.

        :return: bool — True если есть товары.
        """
        cart_items = self.wait.until(
            EC.presence_of_all_elements_located((
                By.CSS_SELECTOR, Config.SELECTORS["cart_item"]))
        )
        return len(cart_items) > 0

    @allure.step("Перейти в категорию Смартфоны")
    def go_to_smartphones_category(self) -> None:
        """
        Переход в категорию "Смартфоны".

        Находит и нажимает на ссылку категории смартфонов.

        :return: None — метод ничего не возвращает.
        """
        category = self.wait.until(
            EC.element_to_be_clickable((
                By.CSS_SELECTOR, Config.SELECTORS["category_smartfony"]))
        )
        category.click()

    @allure.step("Проверить URL страницы")
    def check_url(self, text: str) -> bool:
        """
        Проверка содержания текста в текущем URL.

        Ожидает, что URL содержит указанный текст,
         и возвращает результат проверки.

        :param text: str — текст, который должен содержаться в URL.
        :return: bool — True если текст найден.
        """
        self.wait.until(EC.url_contains(text))
        return text in self.driver.current_url
