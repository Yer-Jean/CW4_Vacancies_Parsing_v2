import json
import os

from settings import SEARCH_RESULTS_FILE


class JSONSaver:

    __search_result_file = SEARCH_RESULTS_FILE

    def read_json_file(self) -> list:
        with open(self.__search_result_file) as json_file:  # Иначе считываем из файла данные
            if os.stat(self.__search_result_file).st_size == 0:
                data_list = []
            else:
                data_list: list = json.load(json_file)
        return data_list

    def write_to_json_file(self, data):
        with open(self.__search_result_file, "a") as json_file:
            # Проверяем файл на содержимое. Размер = 0 значит пустой
            if os.stat(self.__search_result_file).st_size == 0:
                json.dump(data, json_file)
            else:  # Иначе считываем из файла данные
                with open(self.__search_result_file) as json_file:
                    data_list = json.load(json_file)
                # Добавляем к ним новые
                data_list += data
                # Удаляем из данных дубликаты
                data_list = self.remove_duplicates(data_list, 'url')
                # И записываем всё вместе в файл
                with open(self.__search_result_file, "w") as json_file:
                    json.dump(data_list, json_file)

    def clear_json_file(self):
        """Очищаем файл с данными"""
        with open(self.__search_result_file, "w") as f:
            pass

    @staticmethod
    def remove_duplicates(data: list, key_value: str) -> list:
        """
        Метод удаляет дубликаты из списка словарей, проверяя
        словари по уникальному значению vacancy_id
        :param data: исходный список словарей
        :param key_value: по какому ключу ищем дубликаты
        :return: очищенный от дубликатов списка словарей
        """
        seen = set()
        new_data = []
        for item in data:
            item_id = item[key_value]
            if item_id not in seen:
                seen.add(item_id)
                new_data.append(item)
        return new_data
