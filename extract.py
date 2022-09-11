from json import load
from abc import ABC, abstractmethod
from typing import Union


class Extractor(ABC):
    def __init__(self, path_doc: str, cfg=None) -> None:
        self.__cfg: Union[dict, None] = cfg

        with open(path_doc, 'r', encoding='UTF-8') as file:
            self.__json_file: list = load(file)

    @staticmethod
    def __format_tuple(raw_tuple: tuple[int]) -> tuple[int]:
        if len(raw_tuple) == 2:
            raw_tuple += (1,)
        elif len(raw_tuple) == 1:
            raw_tuple: tuple[int, None, int] = (-raw_tuple[0], None, 1)

        return raw_tuple

    @abstractmethod
    def extract_events(self, range_events: tuple[int]):
        self.__formatted_tuple: tuple[int] = self.__format_tuple(range_events)

    @property
    def json_file(self) -> list:
        return self.__json_file

    @property
    def cfg(self) -> Union[dict, None]:
        return self.__cfg

    @property
    def formatted_tuple(self) -> tuple[int]:
        return self.__formatted_tuple


class ExtractorFromSite(Extractor):
    def extract_events(self, range_events: tuple[int]) -> list[dict]:
        super().extract_events(range_events)
        return self.json_file[self.formatted_tuple[0]:self.formatted_tuple[1]:self.formatted_tuple[2]]


class ExtractorFromPublic(Extractor):
    def extract_events(self, range_events: tuple[int]) -> list[str]:
        super().extract_events(range_events)

        post_list: list[str] = []
        for public in self.cfg['public']:
            for post in self.json_file[public]:
                post_list.append(post['text'])

        return post_list


# Тест!
extractor_from_site = ExtractorFromSite('data/Event_List_10_09_2022_17_38_.json')
cfg = {'public': ("afisha.almet",)}
extractor_from_public = ExtractorFromPublic('data/Posts_List_10_09_2022_18_55_.json', cfg)
a = extractor_from_site.extract_events((5,))
b = extractor_from_public.extract_events((5,))
print(b)