"""
Основной модуль приложения для отображения курсов валют.

Реализует простой HTTP сервер с маршрутизацией и шаблонизацией Jinja2.

Содержит:
    - инициализацию данных (пользователи, валюты, подписки)
    - HTTP обработчик SimpleHTTPRequestHandler
    - маршрутизацию по пути запроса
    - интеграцию с шаблонами Jinja2
"""
from jinja2 import Environment, PackageLoader, select_autoescape
from models import Author, App, User, Currency, UserCurrency
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from utils.currencies_api import get_currencies

# инициализация jinja2
env = Environment(loader=PackageLoader("laba8"), autoescape=select_autoescape())

# шаблоны
index_template = env.get_template("index.html")
author_template = env.get_template("author.html")
users_template = env.get_template("users.html")
currencies_template = env.get_template("currencies.html")

# данные приложения
author = Author('Прозорова Полина', 'P3120')
app = App("CurrenciesListApp", "1.0", author)

# пользователи и их подписки на валюты
users = [User(1, "Иван"), User(2, "Мария"), User(3, "Алексей")]
subscriptions = [UserCurrency(1, 1, 1), UserCurrency(2, 1, 2), UserCurrency(3, 2, 2)]

# инициализация валют (стартовые значения, обновятся при первом запросе)
currencies = [
    Currency(1, "840", "USD", "Доллар США", 0.0, 1),
    Currency(2, "978", "EUR", "Евро", 0.0, 1),
    Currency(3, "826", "GBP", "Фунт стерлингов", 0.0, 1)
]

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Обработчик HTTP запросов для приложения курсов валют.

        Реализует маршрутизацию и рендеринг шаблонов для следующих маршрутов:
            - /             : главная страница
            - /author       : информация об авторе
            - /users        : список всех пользователей
            - /user?id=<id> : информация о конкретном пользователе
            - /currencies   : список валют с текущими курсами
            - /currencies/update : обновление курсов валют

        Attributes:
            Не имеет публичных атрибутов, наследует BaseHTTPRequestHandler.

        Methods:
            do_GET(): обработчик всех GET запросов.
        """
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == '/':
            html = index_template.render(
                myapp="CurrenciesListApp",
                author_name=author.name,
                group=author.group
            )

        elif path == '/author':
            html = author_template.render(
                myapp="CurrenciesListApp",
                author_name=author.name,
                group=author.group
            )

        elif path == '/users':
            html = users_template.render(
                myapp="CurrenciesListApp",
                author_name=author.name,
                group=author.group,
                users=users
            )

        elif path == '/user':
            user_id = int(params.get('id', [1])[0])

            user = None
            for u in users:
                if u.id == user_id:
                    user = u
                    break
            if not user:
                user = users[0]

            user_currencies = []
            for sub in subscriptions:
                if sub.user_id == user_id:
                    for curr in currencies:
                        if curr.id == sub.currency_id:
                            user_currencies.append(curr)
                            break

            html = users_template.render(
                myapp="CurrenciesListApp",
                author_name=author.name,
                group=author.group,
                users=users,
                current_user=user,
                user_currencies=user_currencies
            )

        elif path == '/currencies':
            html = currencies_template.render(
                myapp="CurrenciesListApp",
                author_name=author.name,
                group=author.group,
                currencies=currencies
            )

        elif path == '/currencies/update':
            # обновление курсов
            currency_list = ['USD', 'EUR', 'GBP']
            data = get_currencies(currency_list)

            for currency in currencies:
                if currency.char_code in data:
                    new_value = float(data[currency.char_code].replace(',', '.'))
                    currency.value = new_value

            # перенаправление обратно
            self.send_response(302)
            self.send_header('Location', '/currencies')
            self.end_headers()
            return

        else:
            html = index_template.render(
                myapp="CurrenciesListApp",
                author_name=author.name,
                group=author.group
            )

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

# запуск
server = HTTPServer(('localhost', 8080), SimpleHTTPRequestHandler)
print('server is running on http://localhost:8080')
server.serve_forever()
