import os

import requests
from dotenv import load_dotenv

from src.abstract_class import Parser

load_dotenv()

API_KEY = os.getenv("API_KEY_SJ")


class ParserSJ(Parser):
    """
    Класс для получения вакансий по API с 'SuperJob.ru'
    """

    def __init__(self, city: str, vacancy: str) -> None:
        self.__url = "https://api.superjob.ru/2.0/vacancies/"

        self.__vacancy = vacancy
        self.__city = city

        self.__response = self.get_vacancies
        self.dict = self.get_dict()
        self.count_vacancies = len(self.dict)

    def __str__(self):
        return f"Получено {self.count_vacancies} вакансий c 'SuperJob.ru'."

    @property
    def get_vacancies(self) -> dict:
        """
        Приводит данные о вакансиях в удобный для чтения и обработки формат
        :return: список словарей с вакансиями.
        """
        try:
            headers = {"X-Api-App-Id": API_KEY}
            params = {
                "srws": 1,
                "keys": self.__vacancy,
                "town": self.__city,
                "not_archive": True,
                "payment_from": 1,
                "count": 100,
            }
            response = requests.get(self.__url, headers=headers, params=params)
            return response.json()

        except requests.exceptions.RequestException:
            print("Ошибка! Проверьте параметры гет-запроса к 'SuperJob.ru'.")
            return {}

    def get_dict(self) -> list[dict]:
        """
        Создаёт словари с данными по вакансиям из json, полученного по API запросу.
        :return: Список словарей с вакансиями
        """
        try:
            # рассчитываем число страниц с вакансиями
            if int(self.__response["total"]) % 100 == 0:
                count_page = int(self.__response["total"]) // 100
            else:
                count_page = int(self.__response["total"]) // 100 + 1

            # ограничиваем максимальное количество вакансий <= 500 (сайт больше не выдаёт.)
            if count_page > 5:
                count_page = 5

            vacancies_list = []

            # цикл для перебора страниц с найденными вакансиями
            for item in range(count_page):
                headers = {"X-Api-App-Id": API_KEY}
                params = {
                    "srws": 1,
                    "keys": self.__vacancy,
                    "town": self.__city,
                    "not_archive": True,
                    "payment_from": 1,
                    "count": 100,
                    "page": item,
                }
                response = requests.get(self.__url, headers=headers, params=params).json()

                # цикл для формирования списка со словарями данных
                for row in response["objects"]:
                    if row["payment_from"]:
                        res_dict = dict()
                        res_dict["Вакансия"] = row["profession"]
                        res_dict["Зарплата от"] = row["payment_from"]
                        res_dict["Предприятие"] = row["firm_name"]
                        res_dict["График работы"] = row["type_of_work"]["title"]
                        res_dict["Город"] = row["town"]["title"]
                        res_dict["Ссылка на вакансию"] = row["link"]

                        vacancies_list.append(res_dict)

            return vacancies_list
        except (requests.exceptions.RequestException, KeyError):
            print("Ошибка! Проверьте параметры гет-запроса к 'SuperJob.ru'.\n")
            return []
