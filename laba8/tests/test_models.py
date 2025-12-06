import pytest
from laba8.models import Author, User, Currency, UserCurrency, App


class TestModels:
    """тестирование моделей - проверка геттеров, сеттеров и исключений"""

    def test_author_getters_setters(self):
        """проверка геттеров и сеттеров author"""
        author = Author("Полина", "P3120")
        # геттеры
        assert author.name == "Полина"
        assert author.group == "P3120"
        # сеттеры
        author.name = "Новое имя"
        author.group = "P3121"
        assert author.name == "Новое имя"
        assert author.group == "P3121"

    def test_author_exceptions(self):
        """проверка выброса исключений author при некорректных значениях"""
        author = Author("Тест", "Группа")
        with pytest.raises(ValueError):
            author.name = ""  # пустое имя
        with pytest.raises(ValueError):
            author.group = "A"  # слишком короткая группа

    def test_user_getters_setters(self):
        """проверка геттеров и сеттеров user"""
        user = User(1, "Иван")
        assert user.id == 1
        assert user.name == "Иван"
        user.id = 2
        user.name = "Петр"
        assert user.id == 2
        assert user.name == "Петр"

    def test_user_exceptions(self):
        """проверка исключений user"""
        user = User(1, "Тест")
        with pytest.raises(ValueError):
            user.id = -1  # отрицательный ID
        with pytest.raises(ValueError):
            user.id = "строка"  # не число
        with pytest.raises(ValueError):
            user.name = "Я"  # слишком короткое имя

    def test_currency_getters_setters(self):
        """проверка геттеров и сеттеров currency"""
        currency = Currency(1, "840", "USD", "Доллар", 92.5, 1)
        assert currency.id == 1
        assert currency.char_code == "USD"
        assert currency.value == 92.5
        currency.value = 95.0
        assert currency.value == 95.0

    def test_currency_exceptions(self):
        """проверка исключений currency"""
        currency = Currency(1, "840", "USD", "Доллар", 92.5, 1)
        with pytest.raises(ValueError):
            currency.value = -10.0  # отрицательный курс
        with pytest.raises(ValueError):
            currency.char_code = "US"  # неправильная длина
