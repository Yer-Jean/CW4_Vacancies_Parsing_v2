from models.exceptions import APIDataException
from models.vacancy import Vacancy
from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI

class SearchVacancies:
    total_vacancies: int = 0
    # filter_keyword: str = ''
    # filter_keywords: list = []
    # filtered_vacancies: list = []
    # selected_vacancies: list = []

    @classmethod
    def get_query_results(cls, class_names: list, query: str) -> bool:
        """Обрабатывает запросы на HeadHunter и SuperJob.
        :param class_names: Список названий классов API.
        :param query: Поисковый запрос.
        :return: Возвращает True, если вакансии найдены."""

        num_of_vacancies: int = 0
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
                # удаляем последние 3 символа от имени класса
                print(f'найдено вакансий на {class_name.replace("API", "")}: {num_of_vacancies}')
                for vacancy in finding_vacancies:
                    Vacancy(**vacancy)
            else:
                print(f'на {class_name.replace("API", "")} ничего не найдено.\nИзмените параметры запроса')

        print(f'------------------\nВсего вакансий: {cls.total_vacancies}\n')
        return bool(vacancies)