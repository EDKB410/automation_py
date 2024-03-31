def pytest_addoption(parser):

    parser.addoption('--url',
                     default='https://ya.ru',
                     help='url options: url for web request')

    parser.addoption('--status_code',
                     default=200,
                     help='status_code options: web response status code')
    