import pytest
from laba8.utils.currencies_api import get_currencies


class TestGetCurrencies:
    """тестирование функции get_currencies"""

    def test_correct_currencies_retrieval(self):
        """проверка корректного получения курсов"""
        result = get_currencies(['USD', 'EUR'])
        assert result == {'USD': '92,50', 'EUR': '99,80'}

    def test_get_mixed_currencies(self):
        """смесь существующих и несуществующих"""
        result = get_currencies(['USD', 'XYZ', 'EUR'])
        assert result == {'USD': '92,50', 'EUR': '99,80'}
        assert 'XYZ' not in result

    def test_nonexistent_currency_returns_empty(self):
        """проверка отсутствия валюты - возвращает пустой словарь"""
        result = get_currencies(['XYZ', 'ABC'])  # несуществующие
        assert result == {}  # пустой словарь

    def test_currency_format(self):
        """проверка формата данных"""
        result = get_currencies(['USD'])
        value = result['USD']
        assert isinstance(value, str)
        assert ',' in value
        # преобразуем в число
        assert float(value.replace(',', '.')) == 92.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
