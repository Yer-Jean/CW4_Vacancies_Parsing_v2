from abc import ABC, abstractmethod


class SiteAPI(ABC):
    """Абстрактный класс для работы с сайтами через API."""
    @abstractmethod
    def get_vacancies(self, search_string):
        pass
