from models.menu import Menu


def main() -> None:
    print('\nЭта программа получает список вакансий с двух сайтов:'
          'HeadHunter.ru и SuperJob.ru'
          'После прохождения этапов работы выдаются ТОП-вакансии'
          'с максимальными оплатами\n')
    menu = Menu()
    menu()


if __name__ == '__main__':
    main()
