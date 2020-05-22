import openmc

###############################################################################
#                       Create the OpenMC Surfaces
###############################################################################

surfaces = {}

# Instantiate ZCylinder surfaces
surfaces['Fuel OR'] = openmc.ZCylinder(x0=0, y0=0, r=0.39218, name='Fuel OR')
surfaces['Clad IR'] = openmc.ZCylinder(x0=0, y0=0, r=0.40005, name='Clad IR')
surfaces['Clad OR'] = openmc.ZCylinder(x0=0, y0=0, r=0.4572, name='Clad OR')

# Instantiate the axial surfaces
surfaces['Axial Midplane'] = openmc.ZPlane(z0=0.0, name='Axial Midplane')
surfaces['Pin x-min'] = openmc.XPlane(x0=-0.62992, name='Pin x-min')
surfaces['Pin x-max'] = openmc.XPlane(x0= 0.62992, name='Pin x-max')
surfaces['Pin y-min'] = openmc.YPlane(y0=-0.62992, name='Pin y-min')
surfaces['Pin y-max'] = openmc.YPlane(y0= 0.62992, name='Pin y-max')
surfaces['Pin z-min'] = openmc.ZPlane(z0=-182.88, name='Pin z-min')
surfaces['Pin z-max'] = openmc.ZPlane(z0= 182.88, name='Pin z-max')
# surfaces['Lower Reflector z-min'] = openmc.ZPlane(z0=-198.12, name='Lower Reflector z-min')
# surfaces['Upper Reflector z-max'] = openmc.ZPlane(z0= 198.12, name='Upper Reflector z-max')

# Set the boundary conditions
surfaces['Pin x-min'].boundary_type = 'reflective'
surfaces['Pin x-max'].boundary_type = 'reflective'
surfaces['Pin y-min'].boundary_type = 'reflective'
surfaces['Pin y-max'].boundary_type = 'reflective'
surfaces['Pin z-min'].boundary_type = 'vacuum'
surfaces['Pin z-max'].boundary_type = 'vacuum'
# surfaces['Lower Reflector z-min'].boundary_type = 'vacuum'
# surfaces['Upper Reflector z-max'].boundary_type = 'vacuum'
