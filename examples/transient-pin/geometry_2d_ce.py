import openmc
from pin_cells_ce import materials, surfaces, universes, cells

pin = universes['Root'] 

geometry = openmc.Geometry(pin)
