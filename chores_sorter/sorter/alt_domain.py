import os
import random
from math import floor, ceil
from operator import attrgetter

# ABSOLUTE PATH TO THE CHORES FILE
here = os.path.dirname(os.path.abspath(__file__))
chores_file = os.path.join(here, 'chores.txt')

# ABSOLUTE PATH TO THE TEST CHORES FILE
test_chores_file = os.path.join(here, '../tests/test_chores.txt')


class Resident:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age
        self.__tarefas_individuais = list()
        self.__numero_tarefas = 0

    def __str__(self):
        return self.__name

    def is_crianca(self):
        if self.age < 10:
            return True

    def is_crianca_grande(self):
        if 14 > self.age >= 10:
            return True

    def is_adulto(self):
        if self.age >= 15:
            return True

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

    def __init__(self, chores: dict):
        self.__chores = chores

    def _lista_tarefas(self):
        return list(self.__chores.values())

    def _total_tarefas(self):
        lista_valores = 0
        for dificuldade in self._lista_tarefas():
            lista_valores += len(dificuldade)

        return lista_valores

    def tarefa_aleatoria(self):
        dificuldade = random.choice(self._lista_tarefas())
        tarefa = random.choice(dificuldade)
        return self._lista_tarefas()[dificuldade].pop(tarefa)

    def tarefa_facil_aleatoria(self):
        dificuldade = self.__chores['LIGHT']
        tarefa = random.choice(dificuldade)
        return self.__chores[dificuldade].pop(tarefa)

    def tarefa_media_aleatoria(self):
        dificuldade = self.__chores['MID']
        tarefa = random.choice(dificuldade)
        return self.__chores[dificuldade].pop(tarefa)

    @property
    def chores(self):
        return self.__chores

    @property
    def total_tarefas(self):
        return self._total_tarefas()


class Sorter:

    def __init__(self, tarefas: Chores, *residents: Resident):
        self.residentes = residents
        self.tarefas = tarefas

    def distribui_tarefas(self):


    def _calcula_numero_tarefas(self):
        if self._criancas():
            for crianca in self._criancas():
                crianca.numero_tarefas = floor(self.tarefas.total_tarefas / self._numero_residentes())
        if self._criancas_grandes():
            for crianca_grande in self._criancas_grandes():
                crianca_grande.numero_tarefas = floor(self.tarefas.total_tarefas / self._numero_residentes())
        if self._adultos():
            for adulto in self._adultos():
                adulto.numero_tarefas = ceil(self.tarefas.total_tarefas / self._numero_residentes())

    def _distribui_tarefas_faceis(self):
        while len(self.tarefas.chores['LIGHT']) > 0:
            if self._criancas():
                for crianca in sorted(self._criancas(), key=attrgetter('age'), reverse=True):
                    if self.resident_is_valid(crianca):
                        tarefa = self.tarefas.tarefa_facil_aleatoria()
                        crianca.tarefas_individuais.append(tarefa)
            elif self._criancas_grandes():
                for crianca_grande in sorted(self._criancas_grandes(), key=attrgetter('age'), reverse=True):
                    if self.resident_is_valid(crianca_grande):
                        tarefa = self.tarefas.tarefa_facil_aleatoria()
                        crianca_grande.tarefas_individuais.append(tarefa)

        # REVISAR LOGICA DE DISTRIBUICAO. SE TIVER CRIANÇAS MAS JA NAO ESTAO DISPONIVEIS


    def _numero_residentes(self):
        return len(self.residentes)

    def _adultos(self):
        adultos = list()
        for residente in self.residentes:
            if residente.is_adulto():
                adultos.append(residente)

        return adultos

    def _criancas_grandes(self):
        criancas_grandes = list()
        for residente in self.residentes:
            if residente.is_crianca_grande():
                criancas_grandes.append(residente)

        return criancas_grandes

    def _criancas(self):
        criancas = list()
        for residente in self.residentes:
            if residente.is_crianca():
                criancas.append(residente)

        return criancas

    def _residente_aleatorio(self):
        if len(self.residentes) == 1:
            return self.residentes[0]
        else:
            return random.choice(self.residentes)

    def _adulto_aleatorio(self):
        return random.choice(self._adultos())

    def _crianca_grande_aleatoria(self):
        return random.choice(self._criancas_grandes())

    def _crianca_aleatoria(self):
        return random.choice(self._criancas())

    @staticmethod
    def resident_is_valid(resident: Resident):
        if len(resident.tarefas_individuais) < resident.numero_tarefas:
            return True
        else:
            return False

    @property
    def numero_residentes(self):
        return self._numero_residentes
