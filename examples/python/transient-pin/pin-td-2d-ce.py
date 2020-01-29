#input file for fresh fuel pin to hold steady state

import math
import pickle
import matplotlib
from copy import deepcopy

import numpy as np
import os

import openmc
import openmc.mgxs
import openmc.plotter
import openmc.kinetics as kinetics

from geometry_2d_ce import materials, surfaces, universes, cells, geometry


case = '3.4'
omega = 0.8

# Adjust the cells to have the desired moderator densities
if case == '3.0':
    omega = 1.0
elif case == '3.1':
    omega = 0.95
elif case == '3.2':
    omega = 0.90
elif case == '3.3':
    omega = 0.85
elif case == '3.4':
    omega = 0.8

# Create pin cell mesh
full_pin_cell_mesh = openmc.RegularMesh()
full_pin_cell_mesh.type = 'regular'
full_pin_cell_mesh.dimension = [10,10,30]
full_pin_cell_mesh.lower_left = [-0.62992,-0.62992,-182.88]
full_pin_cell_mesh.upper_right =[0.62992,0.62992,182.88]

materials_file = openmc.Materials(geometry.get_all_materials().values())
name = 'Moderator'
d = materials[name].density
density = np.array([[0., 1., 2.],[d,omega*d,d]])
materials[name].set_density('g/cm3',density)

# OpenMC simulation parameters
batches = 200
inactive = 100
particles = 1000

settings_file = openmc.Settings()
settings_file.batches = batches
settings_file.inactive = inactive
settings_file.particles = particles
settings_file.output = {'tallies': False}

# Create an initial uniform spatial source distribution over fissionable zones
lower_left = [-0.62992, -0.62992, -182.88]
upper_right = [0.62992, 0.62992, 182.88]
uniform_dist = openmc.stats.Box(lower_left, upper_right, only_fissionable=True)
settings_file.source = openmc.source.Source(space=uniform_dist)

sourcepoint = dict()
sourcepoint['batches'] = [batches]
sourcepoint['separate'] = True
sourcepoint['write'] = True
settings_file.sourcepoint = sourcepoint

entropy_mesh = openmc.RegularMesh()
entropy_mesh.type = 'regular'
entropy_mesh.dimension = [4,4,1]
entropy_mesh.lower_left = lower_left
entropy_mesh.upper_right = upper_right
settings_file.entropy_mesh = entropy_mesh

# plot = openmc.Plot()
# plot.width = [1.0, 1.0]
# plot.origin = [0., 0., 0.]
# plot.color_by = 'material'
# plot.filename = 'fuel-pin'
# plot.basis = 'yz'
# plots = openmc.Plots([plot])
# plots.export_to_xml()

# Instantiate an EnergyGroups object for the diffuion coefficients
fine_groups = openmc.mgxs.EnergyGroups()
fine_groups.group_edges = [0., 0.13, 0.63, 4.1, 55.6, 9.2e3, 1.36e6, 1.0e7]

# Instantiate an EnergyGroups object for the transient solve
energy_groups = openmc.mgxs.EnergyGroups()
energy_groups.group_edges = [0., 0.13, 0.63, 4.1, 55.6, 9.2e3, 1.36e6, 1.0e7]
two_groups = openmc.mgxs.EnergyGroups()
two_groups.group_edges = [0., 0.63, 1.0e7]
# Instantiate an EnergyGroups object for one group data
one_group = openmc.mgxs.EnergyGroups()
one_group.group_edges = [fine_groups.group_edges[0], fine_groups.group_edges[-1]]

t_outer = np.arange(0., 2.5, 5.e-1)
#dt_inner = [1.e-2]# for j in range(len(t_outer))]

# Instantiate a clock object
clock = openmc.kinetics.Clock(start=0., end=2., dt_inner=1.e-2, t_outer=t_outer)

#print(int(round(dt_outer / dt_inner)))


#Instantiate a kinetics solver object
solver = openmc.kinetics.Solver(directory='PIN_TD_2D_CE')
solver.num_delayed_groups           = 6
solver.amplitude_mesh               = full_pin_cell_mesh
solver.shape_mesh                   = full_pin_cell_mesh
solver.tally_mesh                   = full_pin_cell_mesh
solver.one_group                    = one_group
solver.energy_groups                = energy_groups
solver.fine_groups                  = fine_groups
solver.tally_groups                 = energy_groups
solver.geometry                     = geometry
solver.settings_file                = settings_file
solver.materials_file               = materials_file
solver.inner_tolerance              = np.inf
solver.outer_tolerance              = np.inf
solver.method                       = 'OMEGA'
solver.multi_group                  = False
solver.clock                        = clock
solver.mpi_procs                    = 1
solver.threads                      = 64
solver.core_volume                  = np.pi*0.39218**2*365.7
solver.constant_seed                = False
solver.seed                         = 1
solver.min_outer_iters              = 2 #new line
solver.use_pcmfd                    = False
solver.use_agd                      = False
solver.condense_dif_coef            = True
solver.chi_delayed_by_delayed_group = True
solver.chi_delayed_by_mesh          = False
solver.use_pregenerated_sps         = False
solver.run_on_cluster               = False
solver.log_file_name                = 'log_file.h5'

solver.solve()
