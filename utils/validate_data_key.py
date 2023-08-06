import re

from typing import Any


def clean_and_cut_requirement(text: str) -> str:
    """Метод удаляет из строки text HTML-теги и специальные символы и возвращает
    результат в виде очищенной строки максимальной длиной 115 символов."""
    # result_string: str = re.sub(r'\s', ' ', re.sub(r'<.*?>', '', text))
    result_string: str = re.sub(r'<.*?>', '', text)  # Удаляем из строки HTML-теги
    return f'{result_string[:115]}...' if len(result_string) > 115 else result_string


def validate_key(data: list, value_type: str, key: str, sub_key: str) -> Any:
    """
    В принимаемом словаре data проверяется наличие значений по
    ключу key. Если значение не пустое, то проверяется наличие значений
    по подключу sub_key. Если таких значений нет, то возвращаем пустое
    значение в соответствии с типом ожидаемых данных value_type,
    если есть, то - значение находящееся по ключу subkey.

    (За отсутствием необходимости, в данной задаче не рассматриваем
    бОльшую вложенность словарей: data[key][sub_key1][sub_key2]...итд)

    :param data: словарь с данными
    :param value_type: тип возвращаемого значения
    :param key: ключ
    :param sub_key: подключ
    :return: значение, полученное по цепочке ключей
    """
    value: Any = None

    if data[key] is not None and data[key][sub_key] is not None:
        value = data[key][sub_key]
    else:
        match value_type:
            case 'int':
                value = 0
            case 'float':
                value = 0.0
            case 'str':
                value = ''
            case 'bool':
                value = False
            case 'list':
                value = []
            case 'dict':
                value = {}
            case 'tuple':
                value = ()
    return value
