import os
import random
import itertools
from collections import deque
from math import floor, ceil

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

    def __init__(self):
        self.all_chores = dict()
        self.palavras = deque()

    # READS CHORES FILE AND MAKES A DICTIONARY OUT OF THE CONTENT
    def le_arquivo(self):
        with open(chores_file) as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                self.palavras.append(linha)
        self._monta_dicionario()

    # READ TEST CHORES FILE AND MAKES A DICTIONARY OUT OF THE CONTENT
    def _le_arquivo_teste(self):
        with open(test_chores_file) as arquivo:
            for linha in arquivo:
                linha = linha.strip()
                self.palavras.append(linha)
        self._monta_dicionario()

    # BUILDS A DICTIONARY WITH DIFFICULTIES AS KEYS AND CHORES AS VALUES
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

    # SORTS CHORES BETWEEN RESIDENTS PASSED AS ARGS
    def distribui_tarefas(self):
        self._calcula_numero_tarefas()

        for dificuldade in self._lista_tarefas():
            while len(dificuldade) > 0:
                if dificuldade == self.tarefas.all_chores['HARD']:
                    residente = self._adulto_aleatorio()
                    if len(residente.tarefas_individuais) < residente.numero_tarefas:
                        tarefa = dificuldade.pop(random.randint(0, len(dificuldade) - 1))
                        residente.tarefas_individuais.append(tarefa)
                    elif self._residente_incompleto(residente):
                        tarefa = dificuldade.pop(random.randint(0, len(dificuldade) - 1))
                        self._residente_incompleto(residente).tarefas_individuais.append(tarefa)
                    else:
                        continue
                elif dificuldade == self.tarefas.all_chores['MID']:
                    if self._criancas_grandes():
                        choices = [self._adulto_aleatorio(), self._crianca_grande_aleatoria()]
                        residente = random.choice(choices)
                    else:
                        residente = self._adulto_aleatorio()
                else:
                    if self._criancas() and self._criancas_grandes():
                        choices = [self._crianca_aleatoria(), self._crianca_grande_aleatoria()]
                        residente = random.choice(choices)
                    elif self._criancas():
                        residente = self._crianca_aleatoria()
                    elif self._criancas_grandes():
                        residente = self._crianca_grande_aleatoria()
                    else:
                        residente = self._adulto_aleatorio()
                        tarefa = dificuldade.pop(random.randint(0, len(dificuldade) - 1))
                        residente.tarefas_individuais.append(tarefa)

                if residente.is_crianca_grande() or residente.is_crianca():
                    if len(residente.tarefas_individuais) < residente.numero_tarefas:
                        tarefa = dificuldade.pop(random.randint(0, len(dificuldade) - 1))
                        residente.tarefas_individuais.append(tarefa)
                    elif self._residente_incompleto(residente):
                        tarefa = dificuldade.pop(random.randint(0, len(dificuldade) - 1))
                        self._residente_incompleto(residente).tarefas_individuais.append(tarefa)
                    else:
                        continue

                print(residente, residente.tarefas_individuais)
                print(len(residente.tarefas_individuais), residente.numero_tarefas)

        for residente in self.residentes:
            print(residente.name)
            print(residente.tarefas_individuais)

    def _lista_tarefas(self):
        return list(self.tarefas.all_chores.values())

    def _calcula_numero_tarefas(self):
        if self._total_tarefas() % self._numero_residentes() == 0:
            for residente in self.residentes:
                residente.numero_tarefas = self._total_tarefas() / self._numero_residentes()
        else:
            if self._criancas():
                for crianca in self._criancas():
                    crianca.numero_tarefas = floor(self._total_tarefas() / self._numero_residentes())
            if self._criancas_grandes():
                for crianca_grande in self._criancas_grandes():
                    crianca_grande.numero_tarefas = floor(self._total_tarefas() / self._numero_residentes())
            if self._adultos():
                for adulto in self._adultos():
                    adulto.numero_tarefas = ceil(self._total_tarefas() / self._numero_residentes())

    def _total_tarefas(self):
        lista_valores = 0
        for dificuldade in self._lista_tarefas():
            lista_valores += len(dificuldade)

        return lista_valores

    def _tarefa_aleatoria(self):
        dificuldade = random.randint(0, len(self._lista_tarefas()) - 1)
        tarefa = random.randint(0, len(self._lista_tarefas()[dificuldade]) - 1)
        return self._lista_tarefas()[dificuldade].pop(tarefa)

    def _numero_residentes(self):
        return len(self.residentes)

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

    def _criancas(self):
        criancas = list()
        for residente in self.residentes:
            if residente.is_crianca():
                criancas.append(residente)

        return criancas

    def _criancas_grandes(self):
        criancas_grandes = list()
        for residente in self.residentes:
            if residente.is_crianca_grande():
                criancas_grandes.append(residente)

        return criancas_grandes

    def _adultos(self):
        adultos = list()
        for residente in self.residentes:
            if residente.is_adulto():
                adultos.append(residente)

        return adultos

    def _residente_incompleto(self, resident: Resident):
        if resident.is_adulto():
            for adulto in self._adultos():
                if len(adulto.tarefas_individuais) < adulto.numero_tarefas:
                    return adulto
        if resident.is_crianca_grande():
            for crianca_grande in self._criancas_grandes():
                if len(crianca_grande.tarefas_individuais) < crianca_grande.numero_tarefas:
                    return crianca_grande
        if resident.is_crianca():
            for crianca in self._criancas():
                if len(crianca.tarefas_individuais) < crianca.numero_tarefas:
                    return crianca

        return False


    @property
    def numero_residentes(self):
        return self._numero_residentes

    @property
    def total_tarefas(self):
        return self._total_tarefas
