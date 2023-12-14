import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
from helpers import to_numeric, temp_pres_ec_filter, salinity_calculator, drop_invalid_datetime, trim_all_columns, drop_null_columns, process_columns
from constants import coeffs_salinite, temp_min_value, temp_max_value, temp_ext_min_value, temp_ext_max_value, pres_min_value, pres_max_value, ec_min_value, ec_max_value


def run():
    """
    Main function to execute.
    return: DataFrame with adequate data treatment done
    """
    ### 1/ Read data => trim column names and drop empty columns
    data = pd.read_csv(r'C:\Users\THEO\Desktop\Projet Commande Entrerprise\combine.csv', delimiter=';')
    data = trim_all_columns(data)

    ### 2/ We replace all empty strings by NaN
    data.replace('',np.nan,regex = True, inplace=True)

    ### 3/ We drop the empty columns
    drop_null_columns(data)

    ### 4/ Drop empty rows and duplicate rows
    data.dropna(inplace=True)
    data.drop_duplicates(inplace = True)

    ### 5/ Drop columns where dates and/or times do not match the format
    data = drop_invalid_datetime(data)

    ### 6/ Create dictionnary with temp and pres boundaries, and lists of columns for temp, ec, pressure
    dict_temp_pres_ec, temp_col_names, ec_col_names, pres_col_names =\
                process_columns(data,
                                temp_min_value,
                                temp_max_value,
                                temp_ext_min_value,
                                temp_ext_max_value,
                                pres_min_value,
                                pres_max_value,
                                ec_min_value,
                                ec_max_value)


    ### 7/ Set adequate format for relevant columns:
    data = to_numeric(data, ec_col_names)
    data = to_numeric(data, temp_col_names)
    data = to_numeric(data, pres_col_names)

    ### 8/ Reset index, drop NaN values
    data.reset_index(inplace=True, drop=True)
    data.dropna(inplace=True)

    ### 9/ Filter on temperature
    data = temp_pres_ec_filter(data, dict_temp_pres_ec)

    ### 10/ Calculation of EC and temperatures means
    temp_mean = data[temp_col_names].mean(axis=1)
    ec_mean = data[ec_col_names].mean(axis=1)
    sal_mean = salinity_calculator(temp_mean, ec_mean / 1000, coeffs_salinite)

    ### 11/ Creation of Datetime column (for later vizualisation purposes)
    data['Datetime'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'].astype(str), format='%Y-%m-%d %H:%M:%S')

    ### 12/ Add calculated value to our data
    data['Temp_mean'] = temp_mean
    data['Ec_mean'] = ec_mean
    data['Salinity'] = sal_mean

    data.to_csv('data_traitees_test_capablanca.csv', index=False,  sep = ';')

    ###################################################################################

    # Vizualisation trials
    """
    NB: I was in the train with no WiFi so I used matplotlib
    Other libraries might be more suitable to add a better font (world map for example)
    """

    import matplotlib.pyplot as plt

    plt.scatter(data.Lat, data.Lng, c=data.Temp_mean, cmap='coolwarm')
    plt.colorbar(label='Temperature')
    plt.title("Temperature map")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    plt.scatter(data.Lat, data.Lng, c=data.Salinity, cmap='coolwarm')
    plt.colorbar(label='Salinity')
    plt.title("Salinity map")
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

    


if __name__ == "__main__":
    run()
