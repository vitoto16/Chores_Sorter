import os
import random
import itertools
from collections import deque

here = os.path.dirname(os.path.abspath(__file__))
chores_file = os.path.join(here, 'chores.txt')


class Resident:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age
        self.__tarefas_individuais = list()
        self.__numero_tarefas = 0

    def __str__(self):
        return self.__name

    @property
    def name(self):
        return self.__name

    @property
    def age(self):
        return self.__age

    @property
    def tarefas_individuais(self):
        return self.__tarefas_individuais

    @property
    def numero_tarefas(self):
        return self.__numero_tarefas

    @numero_tarefas.setter
    def numero_tarefas(self, numero_tarefas):
        self.__numero_tarefas = numero_tarefas


class Chores:

    def __init__(self):
        self.all_chores = dict()
        self.palavras = deque()
        with open(chores_file) as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                self.palavras.append(linha)
        self._monta_dicionario()

    def _monta_dicionario(self):
        for palavra in self.palavras:
            palavra = palavra.strip()

            if palavra == 'HARD':
                self.all_chores[palavra] = list(itertools.islice(self.palavras,
                                                                 self.palavras.index('HARD') + 1,
                                                                 self.palavras.index('MID')))
            elif palavra == 'MID':
                self.all_chores[palavra] = list(itertools.islice(self.palavras,
                                                                 self.palavras.index('MID') + 1,
                                                                 self.palavras.index('LIGHT')))
            elif palavra == 'LIGHT':
                self.all_chores[palavra] = list(itertools.islice(self.palavras,
                                                                 self.palavras.index('LIGHT') + 1,
                                                                 self.palavras.maxlen))


class Sorteio:

    def __init__(self, tarefas: Chores, *residents: Resident):
        self.residentes = residents
        self.tarefas = tarefas

    def distribui_tarefas(self):
        self._calcula_numero_tarefas()

        for dificuldade in self._lista_tarefas():
            while len(dificuldade) > 0:
                residente = self._residente_aleatorio()
                if len(residente.tarefas_individuais) < residente.numero_tarefas:
                    tarefa = dificuldade.pop(random.randint(0, len(dificuldade) - 1))
                    residente.tarefas_individuais.append(tarefa)
                else:
                    continue
                print(residente, residente.tarefas_individuais)
                print(len(residente.tarefas_individuais), residente.numero_tarefas)

                """for residente in self.residentes:
                        if len(dificuldade) != 0 and len(residente.tarefas_individuais)<=residente.numero_tarefas:
                            tarefa = dificuldade.pop(random.randint(0, len(dificuldade) - 1))
                            residente.tarefas_individuais.append(tarefa)"""


        for residente in self.residentes:
            print(residente.name)
            print(residente.tarefas_individuais)

    def _lista_tarefas(self):
        return list(self.tarefas.all_chores.values())

    def _calcula_numero_tarefas(self):
        if len(self._total_tarefas()) % self._numero_residentes() == 0:
            for residente in self.residentes:
                residente.numero_tarefas=len(self._total_tarefas())/self._numero_residentes()

    def _total_tarefas(self):
        lista_valores = list()
        for dificuldade in self._lista_tarefas():
            lista_valores += dificuldade

        return lista_valores

    def _numero_residentes(self):
        return len(self.residentes)

    def _residente_aleatorio(self):
        if len(self.residentes) == 1:
            return self.residentes[0]
        else:
            return self.residentes[random.randint(0, self.numero_residentes() - 1)]

    @property
    def numero_residentes(self):
        return self._numero_residentes

    @property
    def total_tarefas(self):
        return self._total_tarefas
