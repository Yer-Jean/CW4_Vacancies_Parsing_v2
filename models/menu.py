from models import search_vacancies
from models.search_vacancies import SearchVacancies
from models.vacancy import Vacancy
from settings import MENU


class Menu:

    __menu = MENU

    def __call__(self, *args, **kwargs):
        start_search = True
        # start_filter = True
        # Создаем класс содержащий методы поиска и фильтрации по вакансиям
        find_vacancies = SearchVacancies()
        # Выводим первое меню
        while True:
            if start_search:
                # ----------- Выводим начальное меню -----------
                choice: str = self.menu_interaction(self.__menu['level_0'])
                match choice:
                    case '1':  # Ввести запрос
                        # query: str = 'django'
                        query: str = input("\nВведите поисковый запрос: ").strip()
                        start_search = False
                    case '0':  # Выход из программы
                        return

            # ----------- Выводим меню 1 уровня -----------
            print('\nВыберите источник')
            choice: str = self.menu_interaction(self.__menu['level_1'])
            match choice:
                case '1':  # Поиск по запросу на HeadHunter
                    if not find_vacancies.get_query_results(class_names=['HeadHunterAPI'], query=query):
                        start_search = True
                        continue
                case '2':  # Поиск по запросу на SuperJob
                    if not find_vacancies.get_query_results(class_names=['SuperJobAPI'], query=query):
                        start_search = True
                        continue
                case '3':  # Поиск по запросу и на HeadHunter, и на SuperJob
                    if not find_vacancies.get_query_results(class_names=['HeadHunterAPI', 'SuperJobAPI'],
                                                              query=query):
                        start_search = True
                        continue
                # case '4':  # Новый запрос
                #     Vacancy.clear_all_vacancies()  # Перед новым запросом удаляем предыдущие результаты
                #     SearchFilter.total_vacancies = 0  # и обнуляем счетчик
                #     start_search = True
                #     continue
                case '0':  # Выход из программы
                    return

            print('Результаты сохранены в файл\nВывести на экран?')
            if self.menu_interaction(self.__menu['Yes_No']) == 'y':
                for vacancy in Vacancy.get_all_vacancies():
                    print(vacancy)

    @staticmethod
    def menu_interaction(menu: dict) -> str:
        """Печатает доступные опции меню выбора в консоль.
        :param menu: Пункты меню.
        :return: Выбранная опция меню.
        """
        print('\n'.join([f"({key}) {value}" for key, value in menu.items()]))

        while True:
            choice: str = input('\nВыберите пункт меню: ')
            if choice not in menu:
                print("\nНеправильный выбор. Выберите один из доступных вариантов.")
                continue
            return choice
