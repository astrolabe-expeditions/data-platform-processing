
"""
Notes: you will find here different constants and parameters used in the code.
You can dircetly modify, add, and delete columns if necessary.
The same can be applied to set constant values to filter temperatures, pressure, or salinity coefficients
"""

# names of the columns carrying information on temperatures
temp_col_names = ['Temp_sea(C)',
                  'Temp_sea(C) .1',
                  'Temp_sea(C) .2']

# names of the columns carrying information on conductivity
ec_col_names = ['EC_sea',
                'EC_sea .1',
                'EC_sea .2']

# dictionnary storing minimum and maximum boundaries for temperatures and pressure columns
dict_temp_pres = \
    {'Temp_sea(C)':
         {'temp_min': -20,
          'temp_max': 100},
     'Temp_sea(C) .1':
         {'temp_min': -20,
          'temp_max': 100},
     'Temp_sea(C) .2':
         {'temp_min': -20,
          'temp_max': 100},
     'Temp_int(C)':
         {'temp_min': -150,
          'temp_max': 150},
     'Temp_ext(C)':
         {'temp_min': -150,
          'temp_max': 150},
     'Pression_ext(hpa)':
         {'temp_min': 70,
          'temp_max': 2000},
    }

# dictionnary containing salinity coefficients
coeffs_salinite = {'A': [0.0080, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081],
                   'B': [0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144],
                   'C': [0.6766097, 0.0200564, 0.000110426, -6.9698E-07, 1.0031E-09],
                   'K': 0.0162}