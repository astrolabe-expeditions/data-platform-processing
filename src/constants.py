
"""
Notes: you will find here different constants and parameters used in the code.
You can dircetly modify, add, and delete columns if necessary.
The same can be applied to set constant values to filter temperatures, pressure, or salinity coefficients
"""

# min and max value for filters
temp_min_value = -20
temp_max_value = 100
temp_ext_min_value = -20
temp_ext_max_value = 100
pres_min_value = 70
pres_max_value = 2000
ec_min_value = -100000
ec_max_value = 100000

# dictionnary containing salinity coefficients
coeffs_salinite = {'A': [0.0080, -0.1692, 25.3851, 14.0941, -7.0261, 2.7081],
                   'B': [0.0005, -0.0056, -0.0066, -0.0375, 0.0636, -0.0144],
                   'C': [0.6766097, 0.0200564, 0.000110426, -6.9698E-07, 1.0031E-09],
                   'K': 0.0162}
