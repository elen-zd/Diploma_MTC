import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from .pages_shop.ApiMTC import CartAPIClient
from .config import Config


@pytest.fixture
def driver():
    """
        Фикстура для инициализации и завершения работы драйвера Chrome.

        Отключение отправки уведомлений, для стабильности выполнения UI-тестов.
    """
    chrome_options = Options()
    prefs = {
        "profile.default_content_setting_values.notifications": 2
    }
    chrome_options.add_experimental_option("prefs", prefs)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(4)
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def cart_client():
    """
    Фикстура для создания клиента API корзины.

    Очищает корзину после выполнения теста.
    """
    client = CartAPIClient(Config.BASE_URL_API)
    yield client
    client.clear_cart()
