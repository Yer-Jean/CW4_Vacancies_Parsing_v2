from api_models.site_api import SiteAPI
from api_models.get_remote_data_mixin import GetRemoteData
from models.exceptions import GetRemoteDataException, APIDataException
from settings import RESULTS_PER_PAGE, HH_API_URL
from utils.validate_data_key import validate_key


class HeadHunterAPI(SiteAPI, GetRemoteData):

    __hh_api_url = HH_API_URL

    def get_vacancies(self, search_string) -> list[dict] | None:
        """Метод возвращает список вакансий по заданному запросу search_string,
        используя HeadHunter API. Возвращает список словарей с данными о вакансиях"""
        vacancies = []
        current_page = 0
        request_params = {'search_field': 'name',
                          'text': search_string,
                          'per_page': RESULTS_PER_PAGE,
                          'page': current_page}
        num_of_pages = 0
        start = True

        while True:
            try:  # Получаем данные о вакансиях используя HeadHunter API
                data = self.get_remote_data(url=self.__hh_api_url, params=request_params)
            except GetRemoteDataException as err:  # Если произошли ошибки, то возвращаем None
                print(err.message)
                print('\nПопробуйте немного позже или измените параметры запроса')
                return None

            if start:
                num_of_pages = data['pages']  # Получаем количество страниц найденных вакансий
                num_of_vacancies = data['found']  # Получаем общее количество найденных вакансий
                if num_of_vacancies == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                    return None
                start = False

            # Из полученного ответа забираем только список вакансий
            vacancies_data = data['items']

            try:  # Создаем новый список с данными о вакансиях, нормализуя названия ключей
                for i in range(len(vacancies_data)):  # Цикл по вакансиям на странице
                    vacancy = {
                        'vacancy_id': vacancies_data[i]['id'],
                        'name': vacancies_data[i]['name'],
                        'employer': vacancies_data[i]['employer']['name'],
                        'city': vacancies_data[i]['area']['name'],
                        'employment': validate_key(vacancies_data[i], 'str', 'employment', 'name'),
                        'schedule': validate_key(vacancies_data[i], 'str', 'schedule', 'name'),
                        'salary_from': validate_key(vacancies_data[i], 'int', 'salary', 'from'),
                        'salary_to': validate_key(vacancies_data[i], 'int', 'salary', 'to'),
                        'currency': validate_key(vacancies_data[i], 'str', 'salary', 'currency'),
                        'experience': validate_key(vacancies_data[i], 'str', 'experience', 'name'),
                        'requirement': validate_key(vacancies_data[i], 'str', 'snippet', 'requirement'),
                        'url': vacancies_data[i]['alternate_url'],
                        'source': 'hh.ru',
                    }
                    vacancies.append(vacancy)
            except KeyError:
                raise APIDataException('произошла ошибка при обработке данных вакансий')

            current_page += 1  # Переходим к следующей странице результатов
            request_params.update({'page': current_page})
            if current_page == num_of_pages + 1:  # Когда достигли последней страницы с вакансиями:
                return vacancies                  # возвращаем их список
