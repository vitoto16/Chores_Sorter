import pytest

from sorter.domain import Chores, Sorteio, Resident

@pytest.fixture
def vittor():
    return Resident('Vittor', 22)

@pytest.fixture
def tarefas():
    return Chores()

def test_deve_designar_todas_as_tarefas_para_o_residente_quando_existe_apenas_um_residente(vittor, tarefas):
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

    sorteio = Sorteio(tarefas, vittor, rafa, dante)

    total_tarefas = len(sorteio.total_tarefas())

    sorteio.distribui_tarefas()

    divisao_exata = (total_tarefas%sorteio.numero_residentes() == 0)

    if divisao_exata:
        for residente in sorteio.residentes:
            assert residente.numero_tarefas == total_tarefas/sorteio.numero_residentes()
