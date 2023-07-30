from abc import ABC, abstractmethod


class SiteAPI(ABC):

    @abstractmethod
    def get_vacancies(self, search_string):
        pass
