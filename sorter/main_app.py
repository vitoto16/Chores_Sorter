from domain import Resident, Chores, Sorteio


vittor = Resident('Vittor', 22)
rafaela = Resident('Rafaela', 20)
dante = Resident('Dante', 0)
dani = Resident('Dani', 21)
fran = Resident('Fran', 26)
valentina = Resident('Valentina', 1)

tarefas = Chores()
tarefas.le_arquivo()

sorteio = Sorteio(tarefas, vittor, rafaela, dante, dani, fran, valentina)

sorteio.distribui_tarefas()
