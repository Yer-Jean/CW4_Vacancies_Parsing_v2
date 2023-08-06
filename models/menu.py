from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI
from models.exceptions import FileDataException, GetRemoteDataException
from models.vacancy import Vacancy
from utils.sort_and_filter import sort_processing, filter_processing
from models.json_saver import JSONSaver
from settings import MENU, SEARCH_RESULTS_FILE


class Menu:

    __menu = MENU
    json_saver = JSONSaver()

    def __call__(self, *args, **kwargs):
        while True:
            # Выводим начальное меню
            choice: str = self.menu_interaction(self.__menu['main'])
            match choice:
                case '1':  # Ввести запрос
                    # query: str = 'django'
                    query: str = input("\nВведите поисковый запрос: ").strip()
                case '2':  # Обработать сохраненные вакансии
                    self.menu_sort_filter()
                    continue
                case '3':  # Удалить сохраненные вакансии
                    try:
                        self.json_saver.clear_json_file()
                    except FileDataException as err:
                        print(err.message)
                    vacancies = []
                    print('\nСохраненные вакансии удалены')
                    continue
                case '0':  # Выход из программы
                    return

            # Выводим меню выбора источника данных
            print('\nВыберите источник')
            choice: str = self.menu_interaction(self.__menu['get_API_data'])
            match choice:
                case '1':  # Поиск по запросу на HeadHunter
                    hh_api = HeadHunterAPI()
                    vacancies = hh_api.get_vacancies(query)
                case '2':  # Поиск по запросу на SuperJob
                    sj_api = SuperJobAPI()
                    vacancies = sj_api.get_vacancies(query)
                case '3':  # Поиск по запросу и на HeadHunter, и на SuperJob
                    hh_api = HeadHunterAPI()
                    vacancies = hh_api.get_vacancies(query)
                    sj_api = SuperJobAPI()
                    vacancies = vacancies + sj_api.get_vacancies(query)
                case '4':  # Новый запрос
                    vacancies = []
                    continue
                case '0':  # Выход из программы
                    return
            # Выводим статистику найденных по запросу вакансий
            if vacancies:
                print(f'По запросу {query} найдено вакансий: {len(vacancies)}')
            else:
                print(f'По запросу {query} ничего не найдено.\nИзмените параметры запроса')
                continue

            # Сохраняем полученные вакансии в файл
            try:
                self.json_saver.write_to_json_file(vacancies)
            except (FileDataException, GetRemoteDataException) as err:
                print(err.message)

            print(f'\nРезультаты сохранены В файл {SEARCH_RESULTS_FILE}\n')

    def menu_sort_filter(self):
        while True:
            try:  # Считываем из файла все вакансии
                vacancies = self.json_saver.read_json_file()
                if len(vacancies) == 0:
                    print('В файле нет ранее сохраненных вакансий')
                    continue
            except (FileDataException, GetRemoteDataException) as err:
                print(err.message)
                continue

            # Создаем экземпляры класса для работы с вакансиями
            for vacancy in vacancies:
                Vacancy(**vacancy)

            print(f'\nРанее сохранены в файл {len(vacancies)} вакансий')
            # Выводим меню для обработки вакансий: фильтр и сортировка
            choice: str = self.menu_interaction(self.__menu['sort_filter'])
            match choice:
                case '1':  # Вывести на экран все вакансии
                    for vacancy in Vacancy.get_all_vacancies():
                        print(vacancy)
                case '2':  # Добавить фильтр и сортировать
                    while True:  # Получаем число ТОП вакансий для вывода на экран
                        num = input('\nВведите количество ТОП по оплате вакансий: ')
                        if num.isdigit():
                            num_top_vacancies = int(num)
                            break
                        else:
                            print('Некорректный ввод. Введите целое число')
                    # Фильтруем список вакансий
                    filtered_vacancies = filter_processing()
                    # Сортируем список вакансий по оплате
                    sorted_vacancies = sort_processing(filtered_vacancies, num_top_vacancies)
                    # sorted_vacancies = Vacancy.sort_processing(filtered_vacancies, num_top_vacancies)
                    # Выводим ТОП вакансии по оплате
                    print(f'\nВыводим ТОП-{num_top_vacancies} вакансий:')
                    for vacancy in sorted_vacancies:
                        print(vacancy)
                    break
                case '4':  # Новый запрос
                    break
                case '0':  # Выход из программы
                    return

    @staticmethod
    def menu_interaction(menu: dict) -> str:
        """Печатает доступные опции меню выбора в консоль.
        :param menu: Пункты меню.
        :return: Выбранная опция меню.
        """
        print('\n')
        print('\n'.join([f"({key}) {value}" for key, value in menu.items()]))

        while True:
            choice: str = input('\nВыберите пункт меню: ')
            if choice not in menu:
                print("\nНеправильный выбор. Выберите один из доступных вариантов.")
                continue
            return choice
