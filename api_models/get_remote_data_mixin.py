import json
import requests

from models.exceptions import GetRemoteDataException, APIDataException
from models.vacancy import Vacancy


class GetRemoteData:

    total_vacancies: int = 0

    @classmethod
    def get_query_results(cls, class_names: list, query: str) -> bool:
        """Обрабатывает запросы на HeadHunter и SuperJob.
        :param class_names: Список названий классов API.
        :param query: Поисковый запрос.
        :return: Возвращает True, если вакансии найдены."""

        num_of_vacancies: int = 0
        finding_vacancies: list | None = None
        vacancies: list = []
        print(f'\nПо запросу "{query}"')

        for class_name in class_names:
            class_api = globals()[class_name]()  # Создаем экземпляр класса из списка class_name
        try:
            finding_vacancies: list | None = class_api.get_vacancies(query)
        except APIDataException as err:
            print(err.message)

        if finding_vacancies:
            num_of_vacancies = len(finding_vacancies)
            vacancies += finding_vacancies
            # cls.total_vacancies += num_of_vacancies
            # удаляем аббревиатуру из имени класса
            print(f'найдено вакансий на {class_name.replace("API", "")}: {num_of_vacancies}')
            for vacancy in finding_vacancies:
                Vacancy(**vacancy)
        else:
            print(f'на {class_name.replace("API", "")} ничего не найдено.\nИзмените параметры запроса')  # конец цикла for

        print(f'------------------\nВсего вакансий: {cls.total_vacancies}\n')
        return bool(vacancies)

    @staticmethod
    def get_remote_data(**kwargs) -> dict | None:
        """Метод получает ответ сайта по API в формате JSON.
        В случае успеха возвращает словарь с данными.
        В случае ошибки возвращает None, при этом обрабатываются
        как сетевые(web) исключения, так и ошибки ответа сайта.
        Кроме того, проверяется корректность JSON-формата.
        Все исключения обрабатываются в классе GetRemoteDataException
        """
        try:
            response = requests.get(**kwargs)
        except requests.exceptions.ConnectionError:
            raise GetRemoteDataException('\nНе найден сайт или ошибка сети')
        except requests.exceptions.HTTPError:
            raise GetRemoteDataException('\nНекорректный HTTP ответ')
        except requests.exceptions.Timeout:
            raise GetRemoteDataException('\nВышло время ожидания ответа')
        except requests.exceptions.TooManyRedirects:
            raise GetRemoteDataException('\nПревышено максимальное значение перенаправлений')

        if response.status_code != 200:  # Все ответы сайта, кроме - 200, являются ошибочными
            raise GetRemoteDataException(f'\nОшибка {response.status_code} - {response.reason}')

        # Пытаемся декодировать JSON
        try:
            data: dict = response.json()
        except json.decoder.JSONDecodeError:
            raise GetRemoteDataException('\nОшибка в формате данных')

        # Возвращаем словарь с данными, если не возникло каких-либо ошибок
        return data
