from chores_sorter.sorter.domain import Resident, Chores, Sorter

chores = {'HARD': ['Varrer', 'Passar pano', 'Tirar poeira', 'Organizar Comodos'],
          'MID': ['Organizar Guarda Roupas', 'Lavar Louca', 'Limpar Fogao',
                  'Levantar Moveis', 'Limpar Box', 'Lavar Roupas'],
          'LIGHT': ['Trocar roupa de cama', 'Limpar Patente', 'Abrir Janelas', 'Levar Lixo', 'Limpar Fraldas']
          }

dante = Resident('Dante', 5)
valentina = Resident('Valentina', 6)
joao_francisco = Resident('Joao Francisco', 7)
enrico = Resident('Enrico', 8)
lucas = Resident('Lucas', 6)
lorenzo = Resident('Lorenzo', 6)
bernardo = Resident('Bernardo', 6)

tarefas = Chores(chores)

sorter = Sorter(tarefas, dante, valentina, joao_francisco, enrico, lucas, lorenzo, bernardo)

sorter.distribui_tarefas()
