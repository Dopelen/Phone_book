import re
from prettytable import PrettyTable


class Phone_Book:
    """Класс, включающий в себя все функции программы
    (__init__, show_line, add_line, initializing, searching)

    :returns: None

    """

    def __init__(self) -> None:
        """Функция содержащая шаблон таблицы для вывода в консоль, индексы полей таблицы и текущее максимальное значение индекса.
        Вызывается при запуске программы, после установки значений переменных запускает функцию initializing
        
        """

        self.table_sample = PrettyTable()
        self.table_sample.field_names = ["ID", "Фамилия", "Имя", "Отчество", "Компания", "Домашний телефон",
                                         "Мобильный телефон"]
        self.number_of_records = 0
        self.codes = {"ID": 0, "Фамилия": 1, "Имя": 2, "Отчество": 3, "Компания": 4, "Домашний телефон": 5,
                      "Мобильный телефон": 6}
        self.clear_lines = []
        self.splited_list = []
        self.initializing()

    def custom_input(self, prompt: str) -> int:
        """Функция осуществляющая заполнение большинства полей в программе. Допускает ввод только цифр, выдает сообщение об ошибке при обратном.
        Принимает строку с инструкцией к вводу - возвращает число.

        :return: int

        """

        while True:
            user_input = input(prompt)
            if user_input.isdigit():
                return int(user_input)
            else:
                print("Введенный символ не является числом. Повторите попытку")

    def show_line(self, all_lines: list, to_show: int) -> None:
        """Функция, получающая лист с текущим содержанием текстового файла "Data.txt" и число строк к выводу.
        В результате - выводит таблицу с указанным числом строк в вывод.
        Также производит сортировку содержимого таблицы с выводом результата на экран.

        :return: None

         """

        current_table = PrettyTable(align="l")
        current_table.field_names = self.table_sample.field_names
        amount_of_data = len(all_lines)
        if to_show > amount_of_data:
            to_show = amount_of_data
        for line in range(to_show):
            current_table.add_row(all_lines[line])
        print(current_table)
        sort_check = self.custom_input(
            "Чтобы отсортировать таблицу, введите индекс поля, по которому производить сортировку. Чтобы продолжить - введитe:'9'\n")
        if sort_check in range(1, 7):
            current_table.sortby = current_table.field_names[sort_check]
            print(current_table)
        else:
            print("Столбец с данным индексом не найден")
        self.input_options()

    def add_line(self) -> None:
        """Функция открывает файл "Data.txt" на добавление, чтобы внести новые данные в соответствии с вводом пользователя, а
         также увеличивает максимальный существующий индекс в таблице на 1.
         После ввода полей, выводит промежуточный результат с уточнением о необходимости внесения изменений.
         Результатом работы функции является изменение файла "Data.txt" и максимального индекса внутри таблицы.

         :return: None

         """

        test_table = PrettyTable(align="l")
        test_table.field_names = self.table_sample.field_names
        with open("Data.txt", "a") as p_book_a:
            self.number_of_records += 1
            new_line_view = ["ID_" + str(self.number_of_records), input("Введите фамилию "), input(
                "Имя "), input(
                "Отчество "), input("Название компании "), input(
                "Домашний телефон "), input("Мобильный телефон ")]
            new_line_text = "\n" + "\t".join(new_line_view)
            test_table.add_row(new_line_view)
            print("Добавить данную строку в файл?\n", test_table)
            check = self.custom_input("Для подтверждения введите ""1"", для отмены ""0""\n")
            test_table.clear_rows()
            if check == 1:
                p_book_a.write(new_line_text)
        self.initializing()

    def editing(self) -> None:
        """Функция запрашивает от пользователя индекс строки и затем поля, которое необхоимо изменить.
         Затем вводится новое содержание поля.
         Демонстрируется строка после изменения, в табличном формате, и после подтверждения изменения вносятся в файл.

         :returns: None

         """
        
        self.editing_table = PrettyTable(align="l")
        self.editing_table.field_names = self.table_sample.field_names
        str_counter = -1
        Finded = False
        target_for_edit = self.custom_input("Введите числовое значение индекса строки, которую хотите изменить\n")
        with open("Data.txt") as p_book_edit:
            edit_list_from_file = list(p_book_edit)
            for edit_str in edit_list_from_file:
                str_counter += 1
                if re.search(f"\\bID_{target_for_edit}\\b", edit_str) != None:
                    Finded = True
                    edit_list_for_edit = edit_str[:-1].split("\t")
                    self.editing_table.add_row(edit_list_for_edit)
                    print(self.editing_table)
                    edit_helper = self.custom_input(
                        "Введите код поля, которое нуждается в корректировке. ID: 0, Фамилия: 1, Имя: 2, Отчество: 3, Компания: 4, Домашний телефон: 5, Мобильный телефон: 6 \n")
                    if edit_helper not in range(0, 7):
                        print("Указанный индекс не соответствует имеющимся полям")
                        break
                    if edit_helper == 0:
                        edit_check = self.custom_input(
                            "Введите новое числовое значение (ID_ будет добавлено автоматически)\n")
                        if edit_check in self.indexses:
                            print("Ошибка. Данный индекс уже используется")
                            break
                        edit_check = "ID_" + str(edit_check)
                    else:
                        edit_check = input("Введите новое значение\n")
                    edit_list_for_edit[edit_helper] = edit_check
                    edit_list_from_file[str_counter] = "\t".join(edit_list_for_edit) + "\n"
                    with open("Data.txt", "w") as final_edit:
                        final_edit.writelines(edit_list_from_file)
                        self.editing_table.clear_rows()
                        break
            if not Finded:
                print("Искомая строка не найдена")
        self.initializing()

    def initializing(self) -> None:
        """Функция просматривает все строки текстового файла и модифицирует переменную, указывающую на максимальный
        используемый индекс. Предлагает использовать возможные функции или завершить работу программы.
        Вызывается после запуска программы а также каждого изменения текстового файла.

        :returns: None

        """

        with open("Data.txt") as p_book:
            p_book.seek(0)
            list_data = list(p_book)
            self.clear_lines = [elem.strip("\n") for elem in list_data]
            self.splited_list = [elem.split("\t") for elem in self.clear_lines]
            self.indexses = [int(self.splited_list[i][0][3:]) for i in range(len(list_data))]
            self.number_of_records = max(self.indexses)
        self.input_options()

    def input_options(self) -> None:
        """Функция, запускающая методы класса в зависимости от ввода пользователя.

        :returns: None

        """

        code_of_action = self.custom_input(
            "Введите:\n1. Для отображения таблицы\n2. Для поиска внутри таблицы\n3. Для добавления строки в таблицу\n4. Для редактирования строк таблицы\n5. Для выхода\n\n")
        if code_of_action == 1:
            check_lenght = input("Введите число строк для отображения. Для отображения всего файла введите '*'\n")
            if check_lenght == "*":
                to_show = len(self.splited_list)
            elif check_lenght.isdigit():
                to_show = int(check_lenght)
            else:
                print("Введенный символ не является числом. Отмена операции\n")
                self.input_options()
            self.show_line(self.splited_list, to_show)

        elif code_of_action == 2:
            self.searching_table = PrettyTable(align="l")
            self.searching_table.field_names = self.table_sample.field_names
            field_amount = self.custom_input("По скольким полям искать? \n")
            intermediate_result = self.searching()
            if field_amount != 1:
                for field in range(int(field_amount) - 1):
                    intermediate_result = intermediate_result & self.searching()
                self.searching_table.clear_rows()
            if intermediate_result:
                self.searching_answer(intermediate_result)
            self.input_options()

        elif code_of_action == 3:
            self.add_line()

        elif code_of_action == 4:
            self.editing()

        elif code_of_action == 5:
            return

        else:
            print("Неизвестный код, попробуйте ещё\n")
            self.input_options()

    def searching(self) -> set:
        """Функция получает через строку ввода от пользователя индекс поля(str: digit in range(7)), внутри которого будет
        производиться поиск в телефонной книге.
        Затем пользователь вводит строку, в соответствии с которой будет произведен поиск внутри заданного поля
        (с использованием регулярных выражений).
        При нахождении совпадения, строка выводится в консоль, а также, ID строки заносится в множество,
        которое и является возвращаемым значением.
        Множество используется при необходимости поиска по нескольким полям.

        :returns: set

        """
        
        self.searching_table.clear_rows()
        search_targets = self.custom_input(
            "Введите код поля, по которому искать. ID: 0, Фамилия: 1, Имя: 2, Отчество: 3, Компания: 4, Домашний телефон: 5, Мобильный телефон: 6 \n")
        target = input("Что ищем в поле? \n")
        answer = set()
        for line_1 in self.splited_list:
            if re.search(target, line_1[search_targets]) != None:
                answer.add(line_1[0])
                self.searching_table.add_row(line_1)
        print("Найденные поля:\n", self.searching_table)
        if not answer:
            print("Ничего не найдено\n")
        return answer

    def searching_answer(self, ans: set) -> None:
        """Функция конструирует и выводит в консоль таблицу результатов поиска по полученному множеству

        :returns: None

        """
        
        self.searching_table.clear_rows()
        for match in ans:
            for answer_line in self.splited_list:
                if answer_line[0] == match:
                    self.searching_table.add_row(answer_line)
        print("Результат поиска:\n", self.searching_table)


if __name__ == "__main__":
    our_book = Phone_Book()
