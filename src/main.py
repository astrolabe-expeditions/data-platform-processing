import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
from helpers import to_numeric, temp_pres_filter, salinity_calculator, drop_invalid_datetime, trim_all_columns, drop_null_columns, gc_interpolate
from constants import dict_temp_pres, temp_col_names, ec_col_names, coeffs_salinite


def run():
    """
    Main function to execute.
    return: DataFrame with adequate data treatment done
    """
    ### 1/ Read data => trim column names and drop empty columns
    data = pd.read_csv(r'C:\Users\kamel\Desktop\IMT Atlantique\A2\Commande Entreprise\combine2.csv', delimiter=';')
    data = trim_all_columns(data)
    ## we replace all empty strings by NaN
    data.replace('',np.nan,regex = True, inplace=True)
    ## we drop the empty columns
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

    ### 7/ Filter on coordinates
    idx1 = 0
    idx2 = 0
    display_idxs = []
    interpolate_idxs = []
    for i in range(0, len(data)):
        if i <= idx2: 
            continue

        print(data['Lat'][i])
        print(data['Lng'][i])

        if data['Lat'][i] == 0 or data['Lng'][i] == 0:
            idx1 = i
            idx2 = i
            while idx1 != 0 and (data['Lat'][idx1] == 0 or data['Lng'][idx1] == 0):
                idx1 -= 1

            while idx2 != len(data) - 1 and (data['Lat'][idx2] == 0 or data['Lng'][idx2] == 0):
                idx2 += 1
            
            interpolate_idxs.append([idx1, idx2])
            display_idxs = display_idxs + list(range(idx1, idx2 + 1))

    # interpolation

    for [idx1, idx2] in interpolate_idxs:
        points = gc_interpolate(data['Lat'][idx1], data['Lng'][idx1], data['Lat'][idx2], data['Lng'][idx2], idx2 - idx1 - 1)
        for i, point in enumerate(points):
            data.at[idx1 + i + 1, 'Lat'] = point[0]
            data.at[idx1 + i + 1, 'Lng'] = point[1]


    ### 8/ Calculation of EC and temperatures means
    temp_mean = data[temp_col_names].mean(axis=1)
    ec_mean = data[ec_col_names].mean(axis=1)
    sal_mean = salinity_calculator(temp_mean, ec_mean / 1000, coeffs_salinite)

    ### 9/ Creation of Datetime column (for later vizualisation purposes)
    data['Datetime'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'].astype(str), format='%Y-%m-%d %H:%M:%S')

    ### 10/ Add calculated value to our data
    data['Temp_mean'] = temp_mean
    data['Ec_mean'] = ec_mean
    data['Salinity'] = sal_mean

    data.to_csv('data_traitees_test3.csv', index=False,  sep = ';')

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
