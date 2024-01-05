import os

import pandas as pd

from src.hedhanters import ParserHH
from src.reader import Reader
from src.superjobs import ParserSJ
from src.vacancies import Vacancies
from src.writer import Writer

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

# Получение пути к текущему исполняемому файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
base_dir = current_dir[: -(len(current_dir.split("\\")[-1]) + 1)]

# Создание относительного пути к нужным файлам от текущего файла
LOADED_VACANCIES = os.path.join(base_dir, "data", "downloaded_data", "loaded_vacancies.json")
FAVORITES_VACANCIES = os.path.join(base_dir, "data", "favorites_vacancies.json")


def main():
    print("Привет!")
    while True:
        # выбираем, с какими вакансиями будем работать.
        while True:
            user_answer = input(
                "\nВыбери действие:\n"
                "\n1 - Перейти к уже загруженным вакансиям."
                "\n2 - Перейти к поиску вакансий на интернет-ресурсах."
                "\n0 - Выйти из программы.\n"
            )
            if user_answer == "0":
                print("Программа завершена. До свидания!")
                return

            elif user_answer == "1":
                break

            elif user_answer == "2":
                # Поиск вакансий в интернете.
                while True:
                    vacancy = input("\nНапиши нужную вакансию:\n")
                    city = input("\nНапиши нужный город:\n")

                    # список действий с поиском вакансий
                    answer = input(
                        "\nВыбери действие:\n"
                        "\n1 - Искать вакансии на 'HeadHunter.ru'."
                        "\n2 - Искать вакансии на 'SuperJob.ru'."
                        "\n3 - Искать вакансии на 'HeadHunter.ru' и 'SuperJob.ru'."
                        "\n4 - Вернуться в предыдущее меню."
                        "\n0 - Выйти из программы.\n"
                    )

                    # ищем вакансии на 'HeadHunter.ru'
                    if answer == "1":
                        print("Идёт поиск вакансий на 'HeadHunter.ru'....\n")
                        data_hh = ParserHH(city, vacancy)
                        print(data_hh)
                        # записываем найденные вакансии в файл
                        writer = Writer(data_hh.dict, LOADED_VACANCIES)
                        writer.write_to_json()
                        break

                    # ищем вакансии на 'SuperJob.ru'
                    elif answer == "2":
                        print("Идёт поиск вакансий на 'SuperJob.ru'....\n")
                        data_sj = ParserSJ(city, vacancy)
                        print(data_sj)
                        # записываем найденные вакансии в файл
                        writer = Writer(data_sj.dict, LOADED_VACANCIES)
                        writer.write_to_json()
                        break

                    #  ищем вакансии на 'HeadHunter.ru' и 'SuperJob.ru'.
                    elif answer == "3":
                        print("Идёт поиск вакансий на 'HeadHunter.ru' и 'SuperJob.ru'....\n")
                        data_hh = ParserHH(city, vacancy)
                        data_sj = ParserSJ(city, vacancy)

                        print(data_hh)
                        print(data_sj)

                        # записываем найденные вакансии в файл
                        writer = Writer(data_hh.dict, LOADED_VACANCIES)
                        writer.write_to_json()

                        writer = Writer(data_sj.dict, LOADED_VACANCIES)
                        writer.add_to_json()

                        # считаем, сколько всего вакансий записалось в файл.
                        counter = len(Reader(LOADED_VACANCIES).data)
                        print(f'\nВсего в файле "loaded_vacancies.json  {counter} вакансий!')

                        break
                    # выходим из цикла и переходим в следующее меню.
                    elif answer == "4":
                        break

                    # завершаем программу
                    elif answer == "0":
                        print("Программа завершена. До свидания!")
                        return

                    # если команды пользователя в списке нет
                    else:
                        print("Такой команды нет! Выбери другую команду!")

            # если команды пользователя в списке нет
            else:
                print("Такой команды нет! Выбери другую команду!")

        # Выбор и сортировка, фильтрация вакансий:
        vacancies = Reader(LOADED_VACANCIES).data
        while True:
            # список действий с сортировкой и фильтрацией вакансий.
            answer = input(
                "\nВыбери действие:\n"
                "\n1 - Выбрать все загруженные вакансии."
                "\n2 - Отсортировать вакансии по размеру зарплаты."
                "\n3 - Выбрать топ-5  вакансий по размеру зарплаты."
                "\n4 - Выбрать вакансии по минимальному значению зарплаты."
                "\n5 - Выбрать вакансии по названию предприятия."
                "\n6 - Выбрать вакансии по графику работы."
                "\n7 - Удалить все найденные вакансии."
                "\n8 - Перейти в следующее меню."
                "\n0 - Выйти из программы.\n"
            )
            # завершаем программу
            if answer == "0":
                print("Программа завершена. До свидания!")
                return

            # выбираем и выводим в консоль все найденные вакансии
            elif answer == "1":
                reader = Reader(LOADED_VACANCIES)
                vacancies = reader.df

                if not vacancies.empty:
                    print(vacancies)
                    continue
                else:
                    print("Данные удалены или повреждены!")
                continue

            # сортируем вакансии по размеру зарплаты
            elif answer == "2":
                selected_vacancies = Vacancies(vacancies)
                vacancies = selected_vacancies.sort_vacancies()

                if not vacancies.empty:
                    print(vacancies)
                    continue
                else:
                    print("Данные удалены или повреждены!")
                continue

            # выбираем и выводим в консоль топ-5 вакансий по размеру зарплаты
            elif answer == "3":
                selected_vacancies = Vacancies(vacancies)
                vacancies = selected_vacancies.get_top_vacancies()

                if not vacancies.empty:
                    print(vacancies)
                    continue
                else:
                    print("Данные удалены или повреждены!")
                continue

            # выбираем и выводим в консоль вакансии с зарплатой от заданного пользователем значения.
            elif answer == "4":
                selected_vacancies = Vacancies(vacancies)
                if not selected_vacancies.df.empty:
                    answer = int(input("Напиши от какого значения зарплаты тебя интересуют вакансии:\n"))
                    vacancies = selected_vacancies.filter_by_salary(answer)
                    print(vacancies)
                    continue
                else:
                    print("Данные удалены или повреждены!")
                continue

            # выбираем и выводим в консоль вакансии с зарплатой от заданной пользователем компании.
            elif answer == "5":
                selected_vacancies = Vacancies(vacancies)
                if not selected_vacancies.df.empty:
                    answer = input("Напиши какая компания тебя интересует:\n")
                    vacancies = selected_vacancies.filter_by_firm_name(answer)
                    print(vacancies)
                    continue
                else:
                    print("Данные удалены или повреждены!")
                continue

            # выбираем и выводим в консоль вакансии с зарплатой от заданного пользователем графика работы.
            elif answer == "6":
                selected_vacancies = Vacancies(vacancies)
                if not selected_vacancies.df.empty:
                    answer = input("Напиши какой график работы тебя интересует:\n")
                    vacancies = selected_vacancies.filter_by_schedule(answer)
                    print(vacancies)
                    continue
                else:
                    print("Данные удалены или повреждены!")
                continue

            # удаляем все найденные вакансии
            elif answer == "7":
                writer = Writer(vacancies, LOADED_VACANCIES)
                writer.clear_json()
                vacancies = []

            # переходим в следующее меню
            elif answer == "8":
                break

            # если команды пользователя в списке нет
            else:
                print("Такой команды нет! Выбери другую команду!")

        # преобразовываем pd.DataFrame с вакансиями в список словарей.
        if type(vacancies) is pd.DataFrame:
            vacancies = vacancies.to_dict("records")

        # Решаем, добавлять вакансии в избранное, или нет.
        while True:
            # список команд для работы с избранными вакансиями
            answer = input(
                "\nВыбери действие:\n"
                "\n1 - Показать вакансии в 'избранном'."
                "\n2 - Добавить новые вакансии в 'избранное'."
                "\n3 - Удалить всё в 'избранном' и записать туда новые вакансии."
                "\n4 - Удалить файл 'избранное'."
                "\n5 - Перейти в следующее меню."
                "\n0 - Выйти из программы.\n"
            )

            # завершаем программу
            if answer == "0":
                print("Программа завершена. До свидания!")
                return

            # считываем и выводим в консоль вакансии в 'избранном'.
            elif answer == "1":
                reader = Reader(FAVORITES_VACANCIES)

                if not reader.df.empty:
                    print(reader.df)
                    continue
                else:
                    print("Данные удалены или повреждены!")
                continue

            # добавляем вакансии в файл 'избранное'.
            elif answer == "2":
                writer = Writer(vacancies, FAVORITES_VACANCIES)
                writer.add_to_json()
                continue

            # перезаписываем 'избранное' новыми вакансиями.
            elif answer == "3":
                writer = Writer(vacancies, FAVORITES_VACANCIES)
                writer.write_to_json()
                continue

            # очищаем файл с избранным.
            elif answer == "4":
                writer = Writer(vacancies, FAVORITES_VACANCIES)
                writer.clear_json()
                continue

            # переходим в следующее меню
            elif answer == "5":
                break

            # если команды пользователя в списке нет
            else:
                print("Такой команды нет! Выбери другую команду!")


if __name__ == "__main__":
    main()
