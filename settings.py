HH_API_URL = 'https://api.hh.ru/vacancies'
SJ_API_URL = 'https://api.superjob.ru/2.0/vacancies/'
SJ_API_KEY = 'v3.r.137695416.0a834cab09168649ce71b4bb9afc6a5879e3e64d.7c882995003416062bf7505f66a50213e7bc5183'
SEARCH_RESULTS_FILE = 'search_results.json'
RESULTS_PER_PAGE = 2

MENU = {
    'titles': (
        'Что будем искать',
        'На каких ресурсах искать',
        'Что делать дальше',
        'Фильтр'
    ),
    'level_0': {
        '1': 'Ввести запрос',
        '2': 'Обработать сохраненные вакансии',
        '3': 'Удалить сохраненные вакансии\n----------------------',
        '0': 'Выход из программы'
    },
    'level_1': {
        '1': 'HeadHunter',
        '2': 'SuperJob',
        '3': 'HeadHunter и SuperJob',
        '4': 'Новый запрос\n----------------------',
        '0': 'Выход из программы'
    },
    'Yes_No': {
        'y': 'Да',
        'n': 'Нет'
    }
}