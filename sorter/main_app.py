from domain import Resident, Chores, Sorteio

vittor = Resident('Vittor', 22)
rafaela = Resident('Rafaela', 20)
dante = Resident('Dante', 0)

tarefas = Chores()

sorteio = Sorteio(tarefas, vittor, rafaela, dante)

sorteio.distribui_tarefas()
