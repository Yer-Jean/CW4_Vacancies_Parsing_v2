from api_models.site_api import SiteAPI
from api_models.get_remote_data_mixin import GetRemoteData
from models.exceptions import GetRemoteDataException, APIDataException
from settings import SJ_API_KEY, SJ_API_URL, RESULTS_PER_PAGE
from utils.validate_data_key import validate_key


class SuperJobAPI(SiteAPI, GetRemoteData):
    __sj_api_url = SJ_API_URL
    __sj_api_key = SJ_API_KEY

    def get_vacancies(self, search_string) -> list[dict] | None:
        """Метод возвращает список вакансий по заданному запросу search_string,
        используя SuperJob API. Возвращает список словарей с данными о вакансиях"""
        vacancies = []
        current_page = 0
        __headers = {'X-Api-App-Id': SJ_API_KEY}
        request_params = {'keys': search_string,
                          'count': RESULTS_PER_PAGE,
                          'page': current_page}
        start = True

        while True:
            try:  # Получаем данные о вакансиях используя SuperJob API
                data = self.get_remote_data(url=self.__sj_api_url,
                                            headers=__headers,
                                            params=request_params)
            except GetRemoteDataException as err:  # Если произошли ошибки, то возвращаем None
                print(err.message)
                print('попробуйте немного позже или измените параметры запроса')
                return None

            if start:
                num_of_vacancies = data['total']  # Получаем общее количество найденных вакансий
                if num_of_vacancies == 0:  # Если не найдена ни одна вакансия, то возвращаем None
                    return None
                start = False

            # Из полученного ответа забираем только список вакансий
            vacancies_data = data['objects']

            try:  # Создаем новый список с данными о вакансиях, нормализуя названия ключей
                for i in range(len(vacancies_data)):  # Цикл по вакансиям на странице
                    vacancies += [{
                        'vacancy_id': vacancies_data[i]['id'],
                        'name': vacancies_data[i]['profession'],
                        'employer': vacancies_data[i]['firm_name'],
                        'city': vacancies_data[i]['town']['title'],
                        'employment': validate_key(vacancies_data[i], 'str', 'type_of_work', 'title'),
                        'schedule': validate_key(vacancies_data[i], 'str', 'place_of_work', 'title'),
                        'salary_from': vacancies_data[i]['payment_from'],
                        'salary_to': vacancies_data[i]['payment_to'],
                        'currency': vacancies_data[i]['currency'],
                        'experience': validate_key(vacancies_data[i], 'str', 'experience', 'title'),
                        'requirement': vacancies_data[i]['vacancyRichText'],
                        'url': vacancies_data[i]['link'],
                        'source': 'superjob.ru',
                    }]
            except KeyError:
                raise APIDataException('произошла ошибка при обработке данных вакансий')

            current_page += 1  # Переходим к следующей странице результатов
            request_params.update({'page': current_page})
            if not data['more']:   # Страницы результатов заканчиваются, когда параметр more = False
                return vacancies   # Возвращаем список с данными о вакансиях
