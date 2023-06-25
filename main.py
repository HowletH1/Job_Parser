from src.hhapi import HHAPI, HHVacancy
from src.sjapi import SuperJobVacancyInterface, SuperJobParser
from src.user_interface import user_interaction

if __name__ == '__main__':

    print('Программа для парсинга вакансий на площадках Super Job и HeadHunter\n')

    necessary_platform = input('выберете один из доступных сервисов:\n'
                               '1: Super Job\n'
                               '2: Head Hunter\n'
                               'Ожидание ввода: ').strip()
    while necessary_platform not in ('1', '2'):
        necessary_platform = input('Такого сервиса нет: ').strip()

    if necessary_platform == '1':

        print('\nВыбран Super Job для поиска вакансий.\n')

        search_city = input('Введите город, по которому вы хотите произвести поиск: ').title().strip()

        while not search_city.replace(' ', '').isalpha():
            search_city = input('Название должно быть строкового типа и не может быть пустым\n'
                                'Повторите ввод: ')

        print(user_interaction(SuperJobParser, SuperJobVacancyInterface, search_city))

    elif necessary_platform == '2':

        print('\nВыбран Head Hunter для поиска вакансий.\n')

        print(user_interaction(HHAPI, HHVacancy))
