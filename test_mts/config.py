class Config:
    """
        Класс базовые URL и тестовые данные для UI и API тестов.
    """

    BASE_URL = "https://shop.mts.ru/"
    BASE_URL_API = "https://shop.mts.ru/api/v1"

    IMPLICIT_WAIT = 4
    EXPLICIT_WAIT = 10

    SEARCH_QUERIES = {
        "valid": "Samsung",
        "valid_2": "iPhone",
        "invalid": "asdfghjkl123456789",
        "empty": ""
    }

    VALID_PRODUCT_ID = 947328
    # ID несуществующего товара (можно использовать заведомо неверный)
    INVALID_PRODUCT_ID = 999999

    SELECTORS = {
        "region_button": "button[class*='confirm-region__close']",
        "search_input": "input[name='q']",
        "search_popup": "#search-popup-field",
        "product_card": "[data-testid='product-card'], .product-card",
        "no_results": "//*[contains(text(), 'Ничего не нашлось')]",
        "add_to_cart": "button[data-v-40c326dc]",
        "modal_page": "div.mtsds-modal-page--open",
        "close_modal_page": "button[aria-label='Закрыть']",
        "cart_icon": ".cart-button",
        "cart_item": "[class*='basket-structure__list'],"
                     " [class*='basket-structure__list-item']",
        "category_smartfony": "a[href*='smartfony']"
    }
