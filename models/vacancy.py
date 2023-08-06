from utils.validate_data_key import clean_and_cut_requirement


class Vacancy:

    __all_vacancies: list = []

    __slots__ = ('vacancy_id',
                 'name',
                 'employer',
                 'city',
                 'employment',
                 'schedule',
                 'salary_from',
                 'salary_to',
                 'salary',
                 'currency',
                 'experience',
                 'requirement',
                 'url',
                 'source')

    def __init__(self, vacancy_id: str, name: str, employer: str, city: str, employment: str, schedule: str,
                 salary_from: int, salary_to: int, currency: str, experience: str, requirement: str, url: str,
                 source: str):
        self.vacancy_id: str = vacancy_id
        self.name: str = name
        self.employer: str = employer
        self.city: str = city
        self.employment: str = employment if employment != 'Не имеет значения' else ''
        self.schedule: str = schedule if schedule != 'Не имеет значения' else ''
        self.salary_from: int = salary_from
        self.salary_to: int = salary_to
        self.currency: str = currency
        self.experience: str = experience
        self.requirement: str = clean_and_cut_requirement(requirement)
        self.url: str = url
        self.source: str = source

        self.__all_vacancies.append(self)
        # Атрибут, которому присваивается значение нижней границы оплаты, если она указана, иначе - верхней границы
        self.salary: int = self.salary_from if self.salary_to == 0 else self.salary_to

    def __str__(self):
        salary: str = {
            self.salary_from == 0 and self.salary_to == 0: 'по договоренности',
            self.salary_from > 0 and self.salary_to == 0: f'от {self.salary_from:,} {self.currency}',
            self.salary_from == 0 and self.salary_to > 0: f'до {self.salary_to:,} {self.currency}',
            self.salary_from > 0 and self.salary_to > 0: f'{self.salary_from:,} - {self.salary_to:,} {self.currency}'
        }[True]
        return f'\nВакансия: {self.name}\nРаботодатель: {self.employer}\nГород {self.city}' \
               f'\nОплата {salary}\nНеобходимый опыт: {self.experience}' \
               f'\nЗанятость и график: {self.employment} {self.schedule}' \
               f'\nОтрывок из требований по вакансии: {self.requirement}' \
               f'\nПолный текст вакансии по ссылке {self.url}\nИсточник - {self.source}'

    def __eq__(self, other):
        s = self.verify_data(other)
        return self.salary == s

    def __ne__(self, other):
        s = self.verify_data(other)
        return self.salary != s

    def __lt__(self, other):
        s = self.verify_data(other)
        return self.salary < s

    def __le__(self, other):
        s = self.verify_data(other)
        return self.salary <= s

    def __gt__(self, other):
        s = self.verify_data(other)
        return self.salary > s

    def __ge__(self, other):
        s = self.verify_data(other)
        return self.salary >= s

    @classmethod
    def verify_data(cls, other):
        if not isinstance(other, int | Vacancy):
            raise TypeError('Ошибка в сравнении данных.')
        return other if isinstance(other, int) else other.salary

    @classmethod
    def get_all_vacancies(cls):
        """Метод возвращает все экземпляры классов вакансий из списка"""
        return cls.__all_vacancies

    @classmethod
    def clear_all_vacancies(cls):
        """Метод удаляет все экземпляры классов вакансий из списка"""
        cls.__all_vacancies.clear()
