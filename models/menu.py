from api_models.hh_api import HeadHunterAPI
from api_models.sj_api import SuperJobAPI
from models import search_vacancies
# from models.search_vacancies import SearchVacancies
from models.vacancy import Vacancy
from settings import MENU


class Menu:

    __menu = MENU

    def __call__(self, *args, **kwargs):
        # start_search = True
        vacancies = []
        # start_filter = True

        # Выводим первое меню
        while True:
            # ----------- Выводим начальное меню -----------
            choice: str = self.menu_interaction(self.__menu['level_0'])
            match choice:
                case '1':  # Ввести запрос
                    # query: str = 'django'
                    query: str = input("\nВведите поисковый запрос: ").strip()
                case '3':  # Новый запрос
                    Vacancy.clear_all_vacancies()
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
                    # Vacancy.clear_all_vacancies()  # Перед новым запросом удаляем предыдущие результаты
                #     SearchFilter.total_vacancies = 0  # и обнуляем счетчик
                #     start_search = True
                    continue
                case '0':  # Выход из программы
                    return

            if vacancies:
                print(f'По запросу {query} найдено вакансий: {len(vacancies)}')
            else:
                print(f'По запросу {query} ничего не найдено.\nИзмените параметры запроса')
                continue

            for vacancy in vacancies:
                Vacancy(**vacancy)

            print('Результаты сохранены в файл\nВывести на экран?')
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
