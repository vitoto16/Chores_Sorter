import pytest

from chores_sorter.sorter.domain import Chores, Sorter, Resident
from chores_sorter.sorter.exceptions import CriancaMuitoNova


@pytest.fixture
def lista_de_tarefas():
    return {'HARD': ['Varrer', 'Passar pano', 'Tirar poeira', 'Organizar Comodos'],
            'MID': ['Organizar Guarda Roupas', 'Lavar Louca', 'Limpar Fogao',
                    'Levantar Moveis', 'Limpar Box', 'Lavar Roupas'],
            'LIGHT': ['Trocar roupa de cama', 'Limpar Patente', 'Abrir Janelas',
                      'Levar Lixo', 'Limpar Fraldas', 'Guardar Brinquedos']
            }


def test_deve_designar_todas_as_tarefas_para_o_residente_quando_existe_apenas_um_residente_adulto(lista_de_tarefas):
    vittor = Resident('Vittor', 22)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, vittor)

    sorter.distribui_tarefas()

    assert len(vittor.tarefas_individuais) == 16


def test_deve_designar_apenas_tarefas_medias_ou_faceis_para_residentes_criancas_grandes(lista_de_tarefas):
    zezinho = Resident('Zezinho', 11)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, zezinho)

    sorter.distribui_tarefas()

    assert len(zezinho.tarefas_individuais) == 12


def test_deve_designar_apenas_tarefas_faceis_para_residentes_criancas(lista_de_tarefas):
    dante = Resident('Dante', 5)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, dante)

    sorter.distribui_tarefas()

    assert len(dante.tarefas_individuais) == 6


def test_deve_designar_apenas_o_limite_de_tarefas_para_residentes_criancas_quando_existem_mais_de_um_residente(lista_de_tarefas):
    vittor = Resident('Vittor', 22)
    rafaela = Resident('Rafaela', 20)
    dante = Resident('Dante', 5)
    zezinho = Resident('Zezinho', 11)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, dante, zezinho, vittor, rafaela)

    sorter.distribui_tarefas()

    assert len(dante.tarefas_individuais) == 4 and len(zezinho.tarefas_individuais) == 4


def test_deve_designar_mesmo_numero_de_tarefas_a_cada_residente_crianca_quando_divisivel_pelo_numero_de_residentes(lista_de_tarefas):
    dante = Resident('Dante', 5)
    valentina = Resident('Valentina', 5)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, valentina, dante)

    sorter.distribui_tarefas()

    assert len(dante.tarefas_individuais) == 3 and len(valentina.tarefas_individuais) == 3


def test_deve_designar_mesmo_numero_de_tarefas_a_cada_residente_crianca_grande_quando_divisivel_pelo_numero_de_residentes(lista_de_tarefas):
    zezinho = Resident('Zezinho', 11)
    branca = Resident('Branca', 12)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, zezinho, branca)

    sorter.distribui_tarefas()

    assert len(branca.tarefas_individuais) == 6 and len(zezinho.tarefas_individuais) == 6


def test_deve_designar_o_mesmo_numero_de_tarefas_a_adultos_quando_divisivel_pelo_restante_das_criancas(lista_de_tarefas):
    vittor = Resident('Vittor', 22)
    rafaela = Resident('Rafaela', 20)
    dante = Resident('Dante', 5)
    zezinho = Resident('Zezinho', 11)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, dante, zezinho, vittor, rafaela)

    sorter.distribui_tarefas()

    assert len(vittor.tarefas_individuais) == 4 and len(rafaela.tarefas_individuais) == 4


def test_deve_designar_mais_tarefas_a_residentes_mais_velhos_quando_nao_divisivel_pelo_numero_de_residentes_adultos(lista_de_tarefas):
    vittor = Resident('Vittor', 22)
    rafaela = Resident('Rafaela', 20)
    kamilla = Resident('Kamilla', 38)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, vittor, rafaela, kamilla)

    sorter.distribui_tarefas()

    assert len(kamilla.tarefas_individuais) == 6


def test_deve_designar_mais_tarefas_a_residentes_mais_velhos_quando_nao_divisivel_pelo_numero_de_residentes_criancas_grandes(lista_de_tarefas):
    zezinho = Resident('Zezinho', 11)
    branca = Resident('Branca', 14)
    lobinha = Resident('Lobinha', 10)
    ceni = Resident('Ceni', 12)
    pitty = Resident('Pitty', 10)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, zezinho, branca, lobinha, ceni, pitty)

    sorter.distribui_tarefas()

    assert len(branca.tarefas_individuais) == 3 and len(ceni.tarefas_individuais) == 3


def test_deve_designar_mais_tarefas_a_residentes_mais_velhos_quando_nao_divisivel_pelo_numero_de_residentes_criancas(lista_de_tarefas):
    dante = Resident('Dante', 5)
    valentina = Resident('Valentina', 5)
    joao_francisco = Resident('Joao Francisco', 7)
    enrico = Resident('Enrico', 8)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, dante, valentina, joao_francisco, enrico)

    sorter.distribui_tarefas()

    assert len(enrico.tarefas_individuais) == 2 and len(joao_francisco.tarefas_individuais) == 2


def test_deve_designar_tarefas_apenas_aos_mais_velhos_quando_houverem_mais_criancas_que_tarefas(lista_de_tarefas):
    dante = Resident('Dante', 5)
    valentina = Resident('Valentina', 6)
    joao_francisco = Resident('Joao Francisco', 7)
    enrico = Resident('Enrico', 8)
    lucas = Resident('Lucas', 6)
    lorenzo = Resident('Lorenzo', 6)
    bernardo = Resident('Bernardo', 6)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, dante, valentina, joao_francisco, enrico, lucas, lorenzo, bernardo)

    sorter.distribui_tarefas()

    assert len(dante.tarefas_individuais) == 0


def test_deve_designar_tarefas_apenas_aos_mais_velhos_quando_houverem_mais_criancas_grandes_que_tarefas(lista_de_tarefas):
    dante = Resident('Dante', 10)
    valentina = Resident('Valentina', 11)
    joao_francisco = Resident('Joao Francisco', 12)
    enrico = Resident('Enrico', 13)
    lucas = Resident('Lucas', 11)
    lorenzo = Resident('Lorenzo', 11)
    bernardo = Resident('Bernardo', 11)
    joao = Resident('Joao', 12)
    jorge = Resident('Jorge', 14)
    jaime = Resident('Jaime', 12)
    vittor = Resident('vittor', 13)
    titus = Resident('titus', 12)
    leeeel = Resident('leeeel', 11)

    tarefas = Chores(lista_de_tarefas)

    sorter = Sorter(tarefas, dante, valentina, joao_francisco, enrico, lucas, lorenzo, bernardo, joao, jorge,
                    jaime, vittor, titus, leeeel)

    sorter.distribui_tarefas()

    assert len(dante.tarefas_individuais) == 0


def test_nao_deve_permitir_criancas_menores_que_cinco_anos():
    with pytest.raises(CriancaMuitoNova):
        dante = Resident('Dante', 0)
