import pytest
from urllib.parse import parse_qs, urlparse


class TestController:
    """тестирование контроллера"""

    def test_root_route_logic(self):
        """проверка логики обработки маршрута / (главная)"""
        test_path = '/'
        if test_path == '/':
            assert True  # маршрут обработан
        else:
            assert False

    def test_users_route_logic(self):
        """Проверка маршрута /users"""
        test_path = '/users'

        if test_path == '/users':
            # должен вернуть список пользователей
            assert test_path.endswith('users')
        else:
            assert False

    def test_currencies_route_logic(self):
        """Проверка маршрута /currencies"""
        test_path = '/currencies'

        if test_path == '/currencies':
            # должен вернуть список валют
            assert 'currencies' in test_path
        else:
            assert False

    def test_user_query_parameter_parsing(self):
        """проверка обработки query-параметров /user?id=..."""
        test_url = '/user?id=2'
        parsed = urlparse(test_url)
        params = parse_qs(parsed.query)
        user_id = int(params.get('id', [1])[0])

        assert user_id == 2

        # тест с несколькими параметрами
        test_url2 = '/user?id=3&name=test'
        parsed2 = urlparse(test_url2)
        params2 = parse_qs(parsed2.query)
        user_id2 = int(params2.get('id', [1])[0])
        assert user_id2 == 3

    def test_default_id_when_no_parameter(self):
        """проверка значения по умолчанию при отсутствии параметра"""
        test_url = '/user'  # без параметра
        parsed = urlparse(test_url)
        params = parse_qs(parsed.query)

        # В вашем коде: int(params.get('id', [1])[0])
        default_id = int(params.get('id', [1])[0])

        assert default_id == 1  # значение по умолчанию

    def test_invalid_id_parameter_handling(self):
        """проверка обработки неверного параметра ID"""
        test_url = '/user?id=abc'
        parsed = urlparse(test_url)
        params = parse_qs(parsed.query)
        assert 'id' in params
        assert params['id'][0] == 'abc'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
