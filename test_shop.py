"""
Протестируйте классы из модуля homework/models.py
"""
import pytest

from models import Product, Cart


@pytest.fixture
def product():
    return Product("book", 100, "This is a book", 1000)

@pytest.fixture
def product2():
    return Product("notebook", 60, "This is a notebook", 500)

@pytest.fixture
def cart():
    return Cart()


class TestProducts:
    """
    Тестовый класс - это способ группировки ваших тестов по какой-то тематике
    Например, текущий класс группирует тесты на класс Product
    """

    def test_product_check_quantity(self, product):
        # напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity)

    def test_product_buy(self, product):
        #  напишите проверки на метод buy
        assert not product.check_quantity(product.quantity + 1)

    def test_product_buy_more_than_available(self, product):
        #  напишите проверки на метод buy,
        #  которые ожидают ошибку ValueError при попытке купить больше, чем есть в наличии
        with pytest.raises(ValueError):
            product.buy(product.quantity + 1)



class TestCart:
    """
    Напишите тесты на методы класса Cart
        На каждый метод у вас должен получиться отдельный тест
        На некоторые методы у вас может быть несколько тестов.
        Например, негативные тесты, ожидающие ошибку (используйте pytest.raises, чтобы проверить это)
    """
    def test_cart_add_product(self, cart, product, product2): # Добавление товаров
        cart.add_product(product, 3)
        cart.add_product(product2, 4)
        assert cart.products[product] == 3
        assert cart.products[product2] == 4

    def test_cart_add_same_product(self, cart, product): # Увеличение кол0ва товара, если он уже есть в корзине
        cart.add_product(product, 10)
        cart.add_product(product, 3)

        assert cart.products[product] == 13

    def test_cart_remove_product_all(self, cart, product): # Удаление товара
        cart.add_product(product, 15)
        cart.remove_product(product)

        assert product not in cart.products

    def test_cart_remove_one_product(self, cart, product, product2): # Удаление только одного товара из двух
        cart.add_product(product, 50)
        cart.add_product(product2, 30)
        cart.remove_product(product, 50)

        assert cart.products[product] == 0
        assert cart.products[product2] == 30

    def test_cart_remove_product_more_than_cart(self, cart, product): # Удаление товара больше, чем есть в корзине
        cart.add_product(product, 4)
        cart.remove_product(product, 10)

        assert product not in cart.products

    def test_cart_get_total_price(self, cart, product, product2): # Общая стоимость
        cart.add_product(product, 5)
        cart.add_product(product2, 13)

        assert cart.get_total_price() == 1280

    def test_cart_clear(self, cart, product, product2): # Очистка корзины
        cart.add_product(product, 3)
        cart.add_product(product2, 2)
        cart.clear()

        assert not cart.products

    def test_cart_buy_success(self, cart, product): # Успешная покупка
        cart.add_product(product, 10)
        cart.buy()

        assert product.quantity == 990

    def test_cart_buy_not_enough_stock(self, cart, product): # Нет на складе
        cart.add_product(product, 2000)

        with pytest.raises(ValueError):
            cart.buy()

    def test_cart_buy_one_not_enough_stock(self, cart, product, product2): # Нет только одного на складе
        cart.add_product(product, 500)
        cart.add_product(product2, 600)

        with pytest.raises(ValueError):
            cart.buy()

        assert cart.products[product] == 500
        assert cart.products[product2] == 600