# Курсовая работа №4
### Курс "Объектно-ориентированное программирование"


## Парсер вакансий
В результате работы программы пользователь по запросу получает ТОП-N вакансий с максимальной оплатой с двух сайтов по поиску работы:
- HeadHunter.ru
- SuperJob.ru

## Логика работы программы
### Программа неявно разделена на две части:

1. Получение по запросу вакансий и запись их в JSON-файл.

Этот файл накапливает все запросы полученные программой, создавая базу данных подходящих вакансий. Однако у пользователя есть возможность очистить файл при необходимости
2. Обработка вакансий, хранящихся в этом файле.

Обработка включает фильтрацию всех вакансий по ключевым словам и затем сортировку и вывод ТОП-N вакансий по размеру оплаты.

### Взаимодействие с пользователем производится в диалоговом режиме:
- ввод текста запроса, ввод ключевых слов
- выбор возможных действия на данном этапе работы программы