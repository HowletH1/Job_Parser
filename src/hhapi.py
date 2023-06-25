from __future__ import annotations
import json
import os
import pprint
from operator import itemgetter
import requests
import datetime

from src.abstract import AbstractClass


class HHAPI(AbstractClass):

    __url = "https://api.hh.ru/vacancies?only_with_salary=true"

    def __init__(self):
        self.__vacancies_list = []

    def __get_request(self, vacancy_for_search: str, pages_for_parse: int) -> list:
        params = {"text": vacancy_for_search,
                  "page": pages_for_parse,
                  "per_page": 100
                  }
        return requests.get(self.__url, params=params).json()['items']

    def parse(self, vacancy_for_search: str, pages_for_parse=10) -> None:
        current_page = 0
        now = datetime.datetime.now()
        current_time = now.strftime(f"%d.%m.%Y Время: %X")

        for i in range(pages_for_parse):
            current_page += 1
            print(f"Парсинг страницы {i + 1}", end=': ')
            values = self.__get_request(vacancy_for_search, i)
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies_list.extend(values)

        print(f"Собрано {len(self.__vacancies_list)} вакансий с {current_page} страниц\n"
              f"Информация собрана {current_time}\n")

    @property
    def get_vacancies(self):
        return self.__vacancies_list


class HHVacancy:
    def __init__(self, keyword: str):
        self.__filename = f"{keyword.title().strip()}.json"

    def create_json(self, data: list) -> str | None:
        if not os.path.isfile(self.__filename):
            self.__write_json(data)

        else:
            while True:
                answer = input(f"Файл с именем {self.__filename} уже создан, перезаписать?"
                               f"\nВаш ответ(yes\\no): ").lower().strip()
                if answer == 'yes':
                    self.__write_json(data)
                    print('Информация в файле была перезаписана')
                    return
                elif answer == 'no':
                    print("Файл не перезаписан")
                    return
                else:
                    print("Некорректный ввод. Введите 'yes' или 'no'.")

    def show_vacancies(self) -> str:
        result_info = []

        for i in self.__from_json:

            salary_from = 'Начальная плата не указана' if not i['salary'].get('from') else i['salary'].get('from')
            salary_to = 'Максимальный порог не указан' if not i['salary'].get('to') else i['salary'].get('to')

            result_info.append(f"ID вакансии: {i['id']}. "
                               f"Наименование: {i['name']}. "
                               f"Заработная плата({i['salary']['currency']}): {salary_from} - {salary_to}. "                               
                               f"Ссылка: {i['alternate_url']}.")

        return '\n'.join(result_info)

    def get_information_by_id(self, id: str | int) -> str:
        result_info = []

        for i in self.__from_json:

            if i['id'] == str(id):
                if i.get('address') is None:
                    address_info = 'адрес не указан'
                else:
                    address_info = f"{i['address']['city']} {i['address']['street']} {i['address']['building']}"

                result_info.append(f"\nВакансия: {i['name']}.\n"
                                   f"Наименование организации {i['employer']['name']}.\n"
                                   f"Адрес: {address_info}.\n"
                                   f"Требования: {i['snippet']['requirement']}.\n"
                                   f"Основные задачи: {i['snippet']['responsibility']}.\n"
                                   f"Заработная плата({i['salary']['currency']}): {i['salary']['from']} - {i['salary']['to']}.\n"
                                   f"Ссылка: {i['alternate_url']}.")

                return ''.join(result_info)
        return 'Вакансии по такому ID не найдено'

    def top_ten(self):
        leaders_list = []

        for i in self.__from_json:
            if i['salary']['from'] is None or i['salary']['to'] is None or i['salary']['currency'] != 'RUR':
                continue

            else:
                salary_avg = (i['salary']['from'] + i['salary']['to']) / 2
                leaders_list.append({"ID вакансии": i['id'],
                                     "Наименование": i['name'],
                                     "Средняя заработная плата": salary_avg,
                                     "Ссылка": {i['alternate_url']}})
        sorted_data = sorted(leaders_list, key=itemgetter("Средняя заработная плата"), reverse=True)
        pprint.pprint(sorted_data[:10], width=110)

    def __write_json(self, data):
        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @property
    def __from_json(self):
        with open(self.__filename, encoding='utf-8') as file:
            vacancies = json.load(file)
            return vacancies
