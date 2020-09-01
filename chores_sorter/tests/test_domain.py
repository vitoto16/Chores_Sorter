import pytest

from chores_sorter.sorter.domain import Chores, Sorteio, Resident


@pytest.fixture
def vittor():
    return Resident('Vittor', 22)


@pytest.fixture
def tarefas():
    return Chores()


def test_deve_designar_todas_as_tarefas_para_o_residente_quando_existe_apenas_um_residente_adulto(vittor, tarefas):
    tarefas._le_arquivo_teste()
    lista_valores = list(tarefas.all_chores.values())
    lista_tarefas = list()
    for valor in lista_valores:
        lista_tarefas += valor

    sorteio = Sorteio(tarefas, vittor)
    sorteio.distribui_tarefas()

    assert sorted(vittor.tarefas_individuais) == sorted(lista_tarefas)


def test_deve_designar_mesmo_numero_de_tarefas_a_cada_residente_quando_divisivel_pelo_numero_de_residentes(vittor, tarefas):
    rafa = Resident('Rafa', 20)
    dante = Resident('Dante', 0)

    tarefas._le_arquivo_teste()

    sorteio = Sorteio(tarefas, vittor, rafa, dante)

    total_tarefas = sorteio.total_tarefas()

    sorteio.distribui_tarefas()

    for residente in sorteio.residentes:
        assert residente.numero_tarefas == total_tarefas/sorteio.numero_residentes()


def test_deve_designar_mais_tarefas_a_pessoas_de_maior_idade_quando_tarefas_nao_sao_divisiveis_por_pessoas(vittor, tarefas):
    rafa = Resident('Rafa', 20)
    dante = Resident('Dante', 0)
    dani = Resident('Dani', 21)
    fran = Resident('Fran', 26)
    valentina = Resident('Valentina', 0)

    tarefas._le_arquivo_teste()

    sorteio = Sorteio(tarefas, vittor, rafa, dante, dani, fran, valentina)

    sorteio.distribui_tarefas()

    assert (len(dante.tarefas_individuais) == 2 and len(valentina.tarefas_individuais) == 2)


def test_deve_designar_apenas_tarefas_faceis_a_criancas_pequenas(vittor, tarefas):
    dante = Resident('Dante', 0)

    tarefas_teste = Chores()

    tarefas._le_arquivo_teste()
    tarefas_teste._le_arquivo_teste()

    sorteio = Sorteio(tarefas, vittor, dante)

    sorteio.distribui_tarefas()

    assert dante.tarefas_individuais == tarefas_teste.all_chores['LIGHT']
