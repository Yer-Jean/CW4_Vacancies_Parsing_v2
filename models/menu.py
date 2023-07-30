from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI
from models.vacancy import Vacancy
from models.json_saver import JSONSaver
from settings import MENU, SEARCH_RESULTS_FILE


class Menu:

    __menu = MENU

    def __call__(self, *args, **kwargs):
        json_saver = JSONSaver()
        # Выводим первое меню
        while True:
            # ----------- Выводим начальное меню -----------
            choice: str = self.menu_interaction(self.__menu['level_0'])
            match choice:
                case '1':  # Ввести запрос
                    # query: str = 'django'
                    query: str = input("\nВведите поисковый запрос: ").strip()
                case '2':  # Обработать сохраненные вакансии
                    # Считываем из файла все вакансии
                    vacancies = json_saver.read_json_file()
                    print(len(vacancies))
                    for vacancy in vacancies:
                        Vacancy(**vacancy)
                case '3':  # Удалить сохраненные вакансии
                    json_saver.clear_json_file()
                    vacancies = []
                    continue
                case '0':  # Выход из программы
                    return

            # ----------- Выводим меню 1 уровня -----------
            print('\nВыберите источник')
            choice: str = self.menu_interaction(self.__menu['level_1'])
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

            if vacancies:
                print(f'По запросу {query} найдено вакансий: {len(vacancies)}')
            else:
                print(f'По запросу {query} ничего не найдено.\nИзмените параметры запроса')
                continue

            # Сохраняем полученные вакансии в файл
            json_saver.write_to_json_file(vacancies)

            print(f'\nРезультаты сохранены В файл {SEARCH_RESULTS_FILE}\n')  # Вывести на экран?')
            # if self.menu_interaction(self.__menu['Yes_No']) == 'y':
            #     for vacancy in vacancies:  #Vacancy.get_all_vacancies():
            #         print(vacancy)

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
