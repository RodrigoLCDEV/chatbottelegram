import collections
import datetime


class Comprementar:

    def __init__(self):
        self._MESSAGEM_1: str = 'Bom dia'
        self._MESSAGEM_2: str = 'Boa tarde'
        self._MESSAGEM_3: str = 'Boa noite'
        self._data_atual = datetime.datetime.now().hour

    def pessoa(self):
        if self._data_atual < 12:
            return self._MESSAGEM_1
        elif 12 <= self._data_atual < 18:
            return self._MESSAGEM_2
        else:
            return self._MESSAGEM_3
