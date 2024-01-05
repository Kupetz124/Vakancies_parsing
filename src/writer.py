import json
import os


class Writer:
    """
    Класс для записи данных в json файл.
    """

    def __init__(self, data, path: str):
        self.__data = data
        self.__path = path

    def write_to_json(self) -> None:
        """
        Перезаписывает данные в json файл.
        :return: None
        """
        if self.__data:
            with open(self.__path, mode="w", encoding="utf-8") as file:
                json.dump(self.__data, file, ensure_ascii=False, indent=4)
                print(f"Записано в файл {len(self.__data)} вакансий!")
        else:
            print("Данных для записи нет!")

    def add_to_json(self) -> None:
        """
        Добавляет данные в json файл
        :return:
        """
        if self.__data:
            try:
                with open(self.__path, encoding="utf-8", mode="r") as file:
                    all_data = json.load(file)
                    if all_data:
                        if self.__data:
                            for item in self.__data:
                                all_data.append(item)

            except (json.JSONDecodeError, ValueError, FileNotFoundError):
                all_data = self.__data

            try:
                with open(self.__path, mode="w", encoding="utf-8") as file:
                    json.dump(all_data, file, indent=4, ensure_ascii=False)
                    print(f"Добавлено в файл {len(self.__data)} вакансий!")

            except json.JSONDecodeError:
                print("Проверь данные!")
        else:
            print("Данных для записи нет!")

    def clear_json(self) -> None:
        """
        Очищает json файл.
        :return:
        """
        if os.path.exists(self.__path):
            os.remove(self.__path)
            print("Файл удален!")
        else:
            print("Такой файл ещё не был создан!")
