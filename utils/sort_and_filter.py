from models.vacancy import Vacancy


def sort_processing(vacancies: list, num_top_vacancies: int) -> list:
    """Метод сортирует список вакансий по убыванию оплаты.
    Вакансии, сортируются по полю salary_from (от ХХХ RUB).
    Если это поле в данной вакансии пустое, то берется поле salary_to (до ХХХ RUB)
    Если оба поля пустые, то данная вакансия опускается ниже в сортировке.
    Сортировка происходит по магическим методам класса Vacancy"""
    sorted_vacancies: list = sorted(vacancies, reverse=True)[:num_top_vacancies]
    return sorted_vacancies


def filter_processing() -> list:
    """Метод фильтрует список всех ранее сохраненных вакансий по ключевым словам
    в списке filter_keywords и возвращает отфильтрованный список вакансий"""
    filtered_vacancies: list = []
    # Запрашиваем ключевые слова для фильтра
    filter_phrase: str = input("\nВведите строку фильтра (одно или несколько слов через пробел): ").strip()
    filter_keywords: list = filter_phrase.split()
    # Берем все вакансии
    non_filtered_vacancies: list = Vacancy.get_all_vacancies()
    for vacancy in non_filtered_vacancies:
        if check_vacancy_for_filter(vacancy, filter_keywords):
            filtered_vacancies.append(vacancy)
    # Печатаем статистику по отфильтрованным вакансиям
    print(f'\nПо фильтру "{filter_phrase}"')
    if filtered_vacancies:
        num_of_vacancies = len(filtered_vacancies)
        print(f'найдено вакансий: {num_of_vacancies}')
    else:
        print(f'ничего не найдено.\nИзмените параметры фильтра')
    return filtered_vacancies  # Возвращаем список вакансий, отфильтрованный по ключевым словам


def check_vacancy_for_filter(vacancy: Vacancy, filter_keywords: list) -> bool:
    """Метод ищет совпадение ключевых слов в списке filter_keywords со значениями всех
    строковых атрибутов экземпляров класса вакансий и возвращает True, если совпадение
    найдено, иначе False."""
    for filter_keyword in filter_keywords:  # Проверяем ключевые слова из запроса фильтра
        for key in vacancy.__slots__:  # По всем атрибутам экземпляра класса вакансии
            value = getattr(vacancy, key)  # Получаем значение атрибута
            if type(value) == str:  # Если значение атрибута - строка, то сравниваем ее
                if filter_keyword.lower() in value.lower():  # с ключевым словом и возвращаем True
                    return True
    return False
