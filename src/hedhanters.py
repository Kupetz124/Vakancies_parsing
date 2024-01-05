import requests

from src.abstract_class import Parser


class ParserHH(Parser):
    """
    Класс для получения вакансий по API с 'HeadHunter.ru'
    """

    def __init__(self, city: str, vacancy: str) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__vacancy = vacancy

        self.__city_id = self.__get_city_id(city)

        self.__response = self.get_vacancies
        self.dict = self.get_dict()
        self.count_vacancies = len(self.dict)

    def __str__(self):
        return f"Получено {self.count_vacancies} вакансий c 'HeadHunter.ru'."

    @staticmethod
    def __get_city_id(city: str) -> str:
        """
        Извлекает id города по названию из словаря hh.ru
        :param city: название города
        :return: id города для API
        """
        res_cities = requests.get("https://api.hh.ru/areas").json()

        city_id = None

        for item in res_cities:
            for line in item["areas"]:
                if line["name"].lower() == city.lower():
                    city_id = line["id"]
            if city_id is None:  # Если у зоны есть внутренние зоны
                for row in item["areas"]:
                    for items in row["areas"]:
                        if items["name"].lower() == city.lower():
                            city_id = items["id"]
        return city_id

    @property
    def get_vacancies(self) -> dict:
        """
        Получает данные по запрошенной вакансии из API запроса
        :return: список словарей с вакансиями.
        """
        try:
            # параметры для гет-запроса
            params_dict = {
                "text": self.__vacancy,
                "per_page": 100,
                "area": self.__city_id,
                "only_with_salary": True,
                "vacancy_search_fields": [{"id": "name", "name": "в названии вакансии"}],
            }

            # гет-запрос
            return requests.get(self.__url, params=params_dict).json()
        except requests.exceptions.RequestException:
            print("Ошибка! Проверьте параметры гет-запроса к 'HeadHunter.ru'.")
            return {}

    def get_dict(self) -> list[dict]:
        """
        Создаёт словари с данными по вакансиям из json, полученного по API запросу.
        :return: Список словарей с вакансиями
        """
        try:
            # рассчитываем число страниц с вакансиями
            if int(self.__response["found"]) % 100 == 0:
                count_page = int(self.__response["found"]) // 100
            else:
                count_page = int(self.__response["found"]) // 100 + 1

            # ограничиваем максимальное количество вакансий <= 2000 (сайт больше не выдаёт)
            if count_page > 20:
                count_page = 20

            vacancies_list = []

            # цикл для перебора страниц с найденными вакансиями
            for item in range(count_page):
                params_dict = {
                    "text": self.__vacancy,
                    "per_page": 100,
                    "area": self.__city_id,
                    "only_with_salary": True,
                    "page": item,
                    "vacancy_search_fields": [{"id": "name", "name": "в названии вакансии"}],
                }
                response = requests.get(self.__url, params=params_dict).json()
                # цикл для формирования словарей с данными
                for row in response["items"]:
                    if row["salary"]:
                        if row["salary"]["from"]:
                            res_dict = dict()
                            res_dict["Вакансия"] = row["name"]
                            res_dict["Зарплата от"] = row["salary"]["from"]
                            res_dict["Предприятие"] = row["employer"]["name"]
                            res_dict["График работы"] = row["schedule"]["name"]
                            res_dict["Город"] = row["area"]["name"]
                            res_dict["Ссылка на вакансию"] = row["alternate_url"]

                            vacancies_list.append(res_dict)

            return vacancies_list
        except (requests.exceptions.RequestException, KeyError):
            print("Ошибка! Проверьте параметры гет-запроса к 'HeadHunter.ru'.\n")
            return []
