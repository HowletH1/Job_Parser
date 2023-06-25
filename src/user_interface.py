def user_interaction(api_instance, api_interface, search_city=None):
    class_instance = api_instance()

    commands = {1: "Показать информацию о всех вакансиях",
                2: "Получить информацию о вакансии по id",
                3: "Показать топ 10 вакансий по средней зп",
                4: "Выход"}

    view_commands = '\n'.join([f"{key}: {value}" for key, value in commands.items()])

    while True:

        search_vacancy = input('Вакансия, по которой произвести поиск: ').title().strip()
        while not search_vacancy.replace(' ', '').isalpha():
            search_vacancy = input('Название вакансии должно быть строкового типа: ').title().strip()

        pages_count = input('Количество страниц с которых необходимо парсить.\n'
                            'Значение 10 является максимальным: ').strip()
        print()
        while not pages_count.isdigit() or int(pages_count) > 10:
            pages_count = input('Некорректное значение: ').strip()

        if search_city is None:
            class_instance.parse(search_vacancy, int(pages_count))
        else:
            class_instance.parse(search_vacancy, search_city, int(pages_count))
        result = class_instance.get_vacancies

        filename = input("Введите название файла, для записи полученной информации в формате JSON: ").strip()
        while filename == '':
            filename = input("Название файла не может быть пустым: ").strip()

        api_interface = api_interface(filename)
        api_interface.create_json(result)

        print("\nТеперь вам доступны следующие команды для отображения полученной информации:")
        print(view_commands)
        print("Чтобы вызвать команду, введите ее номер.\n"
              "Также с помощью команды 'Помощь' можно получить список доступных к вызову команд.")

        user_command = input("\nОжидание команды: ").title().strip()

        while user_command != '4':

            if user_command == 'Помощь':
                print(view_commands)

            if user_command == '1':
                print(api_interface.show_vacancies())

            if user_command == '2':
                search_id = input("Введите id вакансии.\n"
                                  "Чтобы узнать id вакансии, воспользуйтесь командой 1\n"
                                  "Ожидание ввода id: ").strip()

                print(api_interface.get_information_by_id(search_id))

            if user_command == "3":
                print('Ниже информация о топ 10 вакансиях по зп.\n'
                      'лист состоит из вакансий, в которых зарплата указана в руб\n')
                api_interface.top_ten()

            elif user_command not in ('1', '2', '3', 'Помощь'):
                print('Команда не найдена')

            user_command = input("\nОжидание номера команды: ").title().strip()

        print(f"Завершено, файл {filename.title()}.json находится в основной директории проекта.\n")
        exit(0)
