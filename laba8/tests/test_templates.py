import pytest
from jinja2 import Environment, FileSystemLoader
import os


class TestTemplates:
    """тестирование шаблонов Jinja2"""

    def setup_method(self):
        """настройка Jinja2 окружения"""
        # путь к папке templates
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates')
        self.env = Environment(
            loader=FileSystemLoader(template_path),
            autoescape=True
        )

    def test_template_variables_passed_correctly(self):
        """проверка корректной передачи переменных"""
        template = self.env.get_template("index.html")

        # тестовые данные
        context = {
            "myapp": "CurrenciesListApp",
            "author_name": "Полина Прозорова",
            "group": "P3120"
        }

        # рендерим шаблон
        html = template.render(**context)

        # проверка отображения данных
        assert "CurrenciesListApp" in html
        assert "Полина Прозорова" in html
        assert "P3120" in html

    def test_loop_rendering_in_users_template(self):
        """проверка рендеринга циклов в users.html"""
        template = self.env.get_template("users.html")

        # тестовые пользователи
        users = [
            {"id": 1, "name": "Иван"},
            {"id": 2, "name": "Мария"},
            {"id": 3, "name": "Алексей"}
        ]

        context = {
            "myapp": "TestApp",
            "author_name": "Test",
            "group": "Test",
            "users": users
        }

        html = template.render(**context)

        # проверка отображения пользователей
        assert "Иван" in html
        assert "Мария" in html
        assert "Алексей" in html
        assert "Пользователи" in html or "users" in html.lower()

    def test_conditional_rendering_in_users_template(self):
        """проверка рендеринга условий в users.html"""
        template = self.env.get_template("users.html")

        # current_user (наличие дополнительной информации)
        context_with_user = {
            "myapp": "Test",
            "author_name": "Test",
            "group": "Test",
            "users": [],
            "current_user": {"id": 1, "name": "Текущий пользователь"},
            "user_currencies": [{"char_code": "USD", "value": 92.5}]
        }

        html_with_user = template.render(**context_with_user)

        # без current_user
        context_without_user = {
            "myapp": "Test",
            "author_name": "Test",
            "group": "Test",
            "users": [],
            "current_user": None,
            "user_currencies": []
        }

        html_without_user = template.render(**context_without_user)

        # шаблоны должны отличаться
        assert html_with_user != html_without_user

    def test_currencies_template_rendering(self):
        """проверка currencies.html"""
        template = self.env.get_template("currencies.html")

        currencies = [
            {"id": 1, "char_code": "USD", "name": "Доллар", "value": 92.5, "nominal": 1},
            {"id": 2, "char_code": "EUR", "name": "Евро", "value": 99.8, "nominal": 1}
        ]

        context = {
            "myapp": "Test",
            "author_name": "Test",
            "group": "Test",
            "currencies": currencies
        }

        html = template.render(**context)

        # проверяем отображение валют
        assert "USD" in html
        assert "EUR" in html
        assert "Доллар" in html or "доллар" in html.lower()
        assert "92.5" in html or "92,5" in html


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
