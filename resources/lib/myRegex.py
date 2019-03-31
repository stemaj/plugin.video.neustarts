from __future__ import unicode_literals
import io
import re
#from typing import NamedTuple

# class User():
#     name: str

class MyStruct:
    def __init__(self, str1, str2):
        self.film = str1
        self.link = str2
    # bar: int
    # baz: list
    # qux: User

def loadFromFile():
    with io.open('file.txt', 'r', encoding='utf-8') as fo:
        data = fo.read()
    return data.encode('utf-8')

def parseToFilmList(result):
    #filme = re.compile(b"class=\"_2lnW0\" title=\"(.+?)\"").findall(result)
    filme1 = re.compile(b"IN_3r\" data-reactid=\"[0-9]+\"><a href=\"(.+?)\" class=\"_2lnW0\" title=\"(.+?)\"").findall(result)
    filme2 = re.compile(b"video\":{\"id\":(.+?),").findall(result)
    filme = []
    for x in range(0, len(filme2)):
        link = 'http://m.moviepilot.de' + filme1[x][0].decode('utf-8') + '/trailer/' + filme2[x].decode('utf-8')
        my_item = MyStruct(filme1[x][1], link)
        filme.append(my_item)
    return filme


def parseLink(result):
    xxx = re.compile(b"og:video\" content=\"(.+?)\">").findall(result)
    return xxx[0]