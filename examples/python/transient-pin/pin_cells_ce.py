import openmc
from materials_ce import materials
from surfaces import surfaces

###############################################################################
#                 Exporting to OpenMC geometry.xml File
###############################################################################

cells = {}
universes = {}

cells['Fuel'] = openmc.Cell(name='Fuel')
cells['Fuel'].region = -surfaces['Fuel OR'] & +surfaces['Pin z-min'] & -surfaces['Pin z-max']
cells['Fuel'].fill = materials['UO2']

cells['Gap'] = openmc.Cell(name='Gap')
cells['Gap'].region = +surfaces['Fuel OR'] & -surfaces['Clad IR'] & +surfaces['Pin z-min'] & -surfaces['Pin z-max']
cells['Gap'].fill = materials['Void']


cells['Clad'] = openmc.Cell(name='Clad')
cells['Clad'].region = +surfaces['Clad IR'] & -surfaces['Clad OR'] & +surfaces['Pin z-min'] & -surfaces['Pin z-max']
cells['Clad'].fill = materials['Zr Clad']

cells['Moderator'] = openmc.Cell(name='Moderator')
cells['Moderator'].region = +surfaces['Clad OR'] & -surfaces['Pin x-max'] & +surfaces['Pin x-min'] & -surfaces['Pin y-max'] & +surfaces['Pin y-min'] & +surfaces['Pin z-min'] & -surfaces['Pin z-max']
cells['Moderator'].fill = materials['Moderator']


universes['Root'] = openmc.Universe(name='Root')
universes['Root'].add_cell(cells['Fuel'])
universes['Root'].add_cell(cells['Gap'])
universes['Root'].add_cell(cells['Clad'])
universes['Root'].add_cell(cells['Moderator'])
