from abc import ABC


class AbstractClass(ABC):

    def __get_request(self, search_vacancy: str, page: int) -> list:
        pass

    def parse(self, keyword, pages) -> None:
        pass
