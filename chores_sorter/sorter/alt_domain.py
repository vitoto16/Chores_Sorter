import random
from math import floor, ceil
from operator import attrgetter


class Resident:

    def __init__(self, name, age):
        self.__name = name
        self.__age = age
        self.__tarefas_individuais = list()
        self.__numero_tarefas = 0

    def __str__(self):
        return self.__name

    def is_crianca(self):
        if self.__age < 10:
            return True

    def is_crianca_grande(self):
        if 14 > self.__age >= 10:
            return True

    def is_adulto(self):
        if self.__age >= 15:
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
        tarefa = random.choice(range(len(dificuldade)))
        return dificuldade.pop(tarefa)

    def tarefa_media_aleatoria(self):
        dificuldade = self.__chores['MID']
        tarefa = random.choice(range(len(dificuldade)))
        return dificuldade.pop(tarefa)

    def tarefa_dificil_aleatoria(self):
        dificuldade = self.__chores['HARD']
        tarefa = random.choice(range(len(dificuldade)))
        return dificuldade.pop(tarefa)

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
        self._calcula_numero_tarefas()

        self._distribui_tarefas_faceis()
        self._distribui_tarefas_medias()
        self._distribui_tarefas_dificeis()

    def _calcula_numero_tarefas(self):
        for residente in self.residentes:
            if residente.is_crianca():
                residente.numero_tarefas = floor(self.tarefas.total_tarefas / self._numero_residentes())
            if residente.is_crianca_grande():
                residente.numero_tarefas = floor(self.tarefas.total_tarefas / self._numero_residentes())
            if residente.is_adulto():
                residente.numero_tarefas = ceil(self.tarefas.total_tarefas / self._numero_residentes())

    def _distribui_tarefas_faceis(self):
        while len(self.tarefas.chores['LIGHT']) > 0 and self._crianca_disponivel():
            for residente in sorted(self.residentes, key=attrgetter('age'), reverse=True):
                if residente.is_crianca() and self.resident_is_valid(residente):
                    tarefa = self.tarefas.tarefa_facil_aleatoria()
                    residente.tarefas_individuais.append(tarefa)
                    print(residente, residente.tarefas_individuais)
        while len(self.tarefas.chores['LIGHT']) > 0 and self._crianca_grande_disponivel():
            for residente in sorted(self.residentes, key=attrgetter('name'), reverse=True):
                if residente.is_crianca_grande() and self.resident_is_valid(residente):
                    tarefa = self.tarefas.tarefa_facil_aleatoria()
                    residente.tarefas_individuais.append(tarefa)
                    print(residente, residente.tarefas_individuais)
        while len(self.tarefas.chores['LIGHT']) > 0:
            for residente in sorted(self.residentes, key=attrgetter('name'), reverse=True):
                if residente.is_adulto():
                    tarefa = self.tarefas.tarefa_facil_aleatoria()
                    residente.tarefas_individuais.append(tarefa)
                    print(residente, residente.tarefas_individuais)

    def _distribui_tarefas_medias(self):
        while len(self.tarefas.chores['MID']) > 0 and self._crianca_grande_disponivel():
            for residente in sorted(self.residentes, key=attrgetter('name'), reverse=True):
                if residente.is_crianca_grande() and len(self.tarefas.chores['MID']):
                    tarefa = self.tarefas.tarefa_media_aleatoria()
                    residente.tarefas_individuais.append(tarefa)
                    print(residente, residente.tarefas_individuais)
        while len(self.tarefas.chores['MID']) > 0:
            for residente in sorted(self.residentes, key=attrgetter('name'), reverse=True):
                if residente.is_adulto() and len(self.tarefas.chores['MID']):
                    tarefa = self.tarefas.tarefa_media_aleatoria()
                    residente.tarefas_individuais.append(tarefa)
                    print(residente, residente.tarefas_individuais)

    def _distribui_tarefas_dificeis(self):
        while len(self.tarefas.chores['HARD']) > 0:
            for residente in sorted(self.residentes, key=attrgetter('name'), reverse=True):
                if residente.is_adulto() and len(self.tarefas.chores['HARD']):
                    tarefa = self.tarefas.tarefa_dificil_aleatoria()
                    residente.tarefas_individuais.append(tarefa)
                    print(residente, residente.tarefas_individuais)

    def _numero_residentes(self):
        return len(self.residentes)

    # def _criancas(self):
    #     criancas = list()
    #     for residente in self.residentes:
    #         if residente.is_crianca():
    #             criancas.append(residente)
    #
    #     return criancas
    #
    # def _crianca_grande(self):
    #     criancas_grandes = list()
    #     for residente in self.residentes:
    #         if residente.is_crianca_grande():
    #             criancas_grandes.append(residente)
    #
    #     return criancas_grandes
    #
    # def _adultos(self):
    #     criancas = list()
    #     for residente in self.residentes():
    #         if residente.is_crianca():
    #             criancas.append(criancas)
    #
    #     return criancas

    def _crianca_disponivel(self):
        for residente in sorted(self.residentes, key=attrgetter('age'), reverse=True):
            if residente.is_crianca() and self.resident_is_valid(residente):
                return residente

        return False

    def _crianca_grande_disponivel(self):
        for residente in sorted(self.residentes, key=attrgetter('age'), reverse=True):
            if residente.is_crianca_grande() and self.resident_is_valid(residente):
                return residente

        return False

    @staticmethod
    def resident_is_valid(resident: Resident):
        if len(resident.tarefas_individuais) < resident.numero_tarefas:
            return True
        else:
            return False

    @property
    def numero_residentes(self):
        return self._numero_residentes
