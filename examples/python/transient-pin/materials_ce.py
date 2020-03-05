import openmc
import copy

materials = {}

###############################################################################
#                Create the continuous energy materials
###############################################################################


# Instantiate some Materials and register the appropriate Nuclides
materials['UO2'] = openmc.Material(name='UO2')
materials['UO2'].set_density('sum')
materials['UO2'].add_nuclide('U235', 8.6500E-4 , 'ao') 
materials['UO2'].add_nuclide('U238', 2.2250E-2 , 'ao') 
materials['UO2'].add_element('O'   , 4.62200E-2, 'ao')

materials['Moderator'] = openmc.Material(name='Moderator')
materials['Moderator'].set_density('g/cm3', 0.7406) #'sum')
#materials['Moderator'].temperature = 566
materials['Moderator'].add_element('H', 2*3.3500E-2, 'ao')
materials['Moderator'].add_element('O',   3.3500E-2, 'ao')
materials['Moderator'].add_element('B',   2.7800E-5, 'ao')
materials['Moderator'].add_s_alpha_beta('c_H_in_H2O')

materials['Zr Clad'] = openmc.Material(name='Zr Clad')
materials['Zr Clad'].set_density('sum')
materials['Zr Clad'].add_element('Zr', 4.3000E-2, 'ao')

materials['Void'] = openmc.Material(name='Void')
materials['Void'].set_density('sum')
materials['Void'].add_element('He', 1.e-10, 'ao')
