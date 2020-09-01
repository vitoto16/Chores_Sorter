from alt_domain import Resident, Chores, Sorter


chores = {'HARD': ['Varrer', 'Passar pano', 'Tirar poeira', 'Organizar Comodos'],
            'MID': ['Organizar Guarda Roupas', 'Lavar Louca', 'Limpar Fogao',
                    'Levantar Moveis', 'Limpar Box', 'Lavar Roupas'],
            'LIGHT': ['Trocar roupa de cama', 'Limpar Patente', 'Abrir Janelas', 'Levar Lixo', 'Limpar Fraldas']
            }

vittor = Resident('Vittor', 22)
rafaela = Resident('Rafaela', 20)
dante = Resident('Dante', 0)
dani = Resident('Dani', 21)
fran = Resident('Fran', 26)
valentina = Resident('Valentina', 1)
zezinho = Resident('Zezinho', 11)

tarefas = Chores(chores)

sorteio = Sorter(tarefas, vittor, rafaela, dante, zezinho)

sorteio.distribui_tarefas()
