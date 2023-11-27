import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
from helpers import to_numeric, temp_pres_filter, salinity_calculator, drop_invalid_datetime, trim_all_columns, drop_null_columns
from constants import dict_temp_pres, temp_col_names, ec_col_names, coeffs_salinite


def run():
    """
    Main function to execute.
    return: DataFrame with adequate data treatment done
    """
    ### 1/ Read data => trim column names and drop empty columns
    data = pd.read_csv(r'C:\Users\kamel\Desktop\IMT Atlantique\A2\Commande Entreprise\Datasets\Données\2021-10-capablanca.csv', delimiter=';')
    data.columns = data.columns.str.strip()
    data = trim_all_columns(data)
    ## we replace all empty strings by NaN and drop the empty columns
    data.replace('',np.nan,regex = True, inplace=True)
    drop_null_columns(data)

    ### 2/ Drop empty rows and duplicate rows
    data.dropna(inplace=True)
    data.drop_duplicates(inplace = True)

    ### 3/ Drop columns where dates and/or times do not match the format
    data = drop_invalid_datetime(data)

    ### 4/ Set adequate format for relevant columns:
    data = to_numeric(data, ec_col_names)
    data = to_numeric(data, temp_col_names)

    ### 5/ Reset index, drop NaN values
    data.reset_index(inplace=True, drop=True)
    data.dropna(inplace=True)

    ### 6/ Filter on temperature
    data = temp_pres_filter(data, dict_temp_pres)

    ### 7/ Calculation of EC and temperatures means
    temp_mean = data[temp_col_names].mean(axis=1)
    ec_mean = data[ec_col_names].mean(axis=1)
    sal_mean = salinity_calculator(temp_mean, ec_mean / 1000, coeffs_salinite)

    ### 8/ Creation of Datetime column (for later vizualisation purposes)
    data['Datetime'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'].astype(str), format='%Y-%m-%d %H:%M:%S')

    ### 9/ Add calculated value to our data
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
