import pandas as pd


class Vacancies:
    """Класс для выбора и сортировки вакансий."""

    def __init__(self, data: list[dict]) -> None:
        try:
            self.df = pd.DataFrame(data)
            self.df.index = range(1, len(self.df) + 1)
        except ValueError:
            self.df = pd.DataFrame()

    def sort_vacancies(self) -> pd.DataFrame:
        """
        Сортирует вакансии по размеру зарплаты.
        :return: Отсортированный список вакансий.
        """
        try:
            df = self.df.sort_values("Зарплата от", ascending=False)
            df.index = range(1, len(df) + 1)
            return df
        except KeyError:
            return pd.DataFrame()

    def get_top_vacancies(self) -> pd.DataFrame:
        """
        Возвращает топ-5 вакансий по размеру зарплаты.
        :return: топ-5 вакансий по размеру зарплаты.
        """
        try:
            df = self.sort_vacancies()
            return df.head()
        except AttributeError:
            return pd.DataFrame()

    def filter_by_salary(self, lower_value: int) -> pd.DataFrame:
        try:
            df = self.df[self.df["Зарплата от"] >= lower_value]

            df.index = range(1, len(df) + 1)
            return df
        except KeyError:
            return pd.DataFrame()

    def filter_by_schedule(self, row: str) -> pd.DataFrame:
        """
        Фильтрует вакансии по графику работы.
        :param row: Искомый график работы
        :return: DataFrame c с вакансиями с нужным графиком работы.
        """
        try:
            df = self.df[self.df["График работы"].str.contains(row, case=False)]
            df.index = range(1, len(df) + 1)
            return df
        except KeyError:
            return pd.DataFrame()

    def filter_by_firm_name(self, row: str) -> pd.DataFrame:
        """
        Фильтрует вакансии по графику работы.
        :param row: Искомый график работы
        :return: DataFrame c с вакансиями с нужным графиком работы.
        """
        try:
            df = self.df[self.df["Предприятие"].str.contains(row, case=False)]
            df.index = range(1, len(df) + 1)
            return df
        except KeyError:
            return pd.DataFrame()
