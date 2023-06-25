from __future__ import annotations
import json
import os.path
import pprint
import datetime
from operator import itemgetter
import requests


class SuperJobParser:
    URL = "https://api.superjob.ru/2.0/vacancies/?"

    def __init__(self):
        self.__vacancies_list = []

    def __get_request(self, vacancy_for_search: str, preferred_city: str, pages_for_parse=1) -> list:
        header = {
            'X-Api-App-Id': 'v3.r.137637317.47d9a78b5821d68e1dacd961631c70b83525ca13.9c1f97fb07f002057ba6a3651d89f5d60baae416'
        }

        params = {'keywords': vacancy_for_search.title(),
                  'town': preferred_city,
                  'count': 100,
                  'page': pages_for_parse,
                  'more': True}

        return requests.get(self.URL, headers=header, params=params).json()['objects']

    def parse(self, vacancy_for_search: str, preferred_city: str, pages_for_parse=10) -> None:
        current_page = 0

        for i in range(pages_for_parse):
            current_page += 1
            print(f"Парсинг страницы {i + 1}", end=': ')
            values = self.__get_request(vacancy_for_search, preferred_city, i)
            print(f"Найдено {len(values)} вакансий")
            self.__vacancies_list.extend(values)

    @property
    def get_vacancies(self) -> list:
        return self.__vacancies_list


class SuperJobVacancyInterface:

    def __init__(self, file_title: str):
        self.__file_title = f"{file_title.title().strip()}.json"

    def create_json(self, data: list):

        if not os.path.isfile(self.__file_title):
            self.__write_json(data)

        else:
            while True:
                answer = input(f"Файл {self.__file_title} уже создан, перезаписать?"
                               f"\n(yes\\no): ").lower().strip()
                if answer == 'yes':
                    self.__write_json(data)
                    print('Информация перезаписана')
                    return
                elif answer == 'no':
                    print("не перезаписано")
                    return
                else:
                    print("Некорректный ввод. Введите 'yes' или 'no'.")

    def show_vacancies(self) -> str:
        result_info = []

        for i in self.__from_json:
            salary_from = 'Начальная плата не указана' if i['payment_from'] == 0 else i['payment_from']
            salary_to = 'Максимальный порог не указан' if i['payment_to'] == 0 else i['payment_to']

            result_info.append(f"ID вакансии: {i['id']}. "
                               f"Наименование: {i['profession']}. "
                               f"Заработная плата({i['currency']}): {salary_from} - {salary_to}. "
                               f"Ссылка: {i['link']}.")

        return '\n'.join(result_info)

    def get_information_by_id(self, id: str | int) -> str:
        result = []

        try:
            for i in self.__from_json:
                date_pub = i['date_published']
                pre_date = datetime.datetime.fromtimestamp(date_pub)
                final_date = pre_date.strftime('%Y-%m-%d %H:%M:%S')

                if i['id'] == int(id):
                    address_info = 'адрес не указан' if i.get('address') is None else i.get('address')

                    salary_from = 'начальная плата не указана' if i['payment_from'] == 0 else i['payment_from']
                    salary_to = 'максимальный порог не указан' if i['payment_to'] == 0 else i['payment_to']

                    result.append(f"Дата размещения: {final_date}. \n"
                                  f"ID Вакансии: {i['id']}.\n"
                                  f"Наименование: {i['profession']}. \n"
                                  f"Заработная плата({i['currency']}): от {salary_from} до {salary_to}. \n"
                                  f"Адрес: {address_info}. \n"
                                  f"Требования: {i.get('candidat')}. \n"
                                  f"Описание: {i.get('work')}. \n"
                                  f"Ссылка: {i['link']}.\n")

                    return ''.join(result)

            return 'Вакансии по такому ID не найдено'

        except ValueError:
            return 'Вакансии по такому ID не найдено'

    def top_ten(self):
        leaders_list = []

        for i in self.__from_json:
            salary_avg = (i['payment_from'] + i['payment_to']) / 2

            if i['payment_from'] == 0 or i['payment_to'] == 0 or i['currency'] != 'rub':
                continue

            else:
                leaders_list.append({"ID вакансии": i['id'],
                                     "Наименование": i['profession'],
                                     "Средняя заработная плата": salary_avg,
                                     "Ссылка": {i['link']}})
        sorted_data = sorted(leaders_list, key=itemgetter("Средняя заработная плата"), reverse=True)
        pprint.pprint(sorted_data[:10], width=110)

    def __write_json(self, data: list):
        with open(self.__file_title, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    @property
    def __from_json(self):
        with open(self.__file_title, encoding='utf-8') as file:
            vacancies = json.load(file)
            return vacancies
