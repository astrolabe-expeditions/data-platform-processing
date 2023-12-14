
"""
You will find here intermediary/helper functions that are used in the main script
"""

import pandas as pd

def drop_invalid_datetime(df):
    """
    Trim values for columns "Date" and "Time"
    :param df: input DataFrame
    :return: df without rows where either date or time is in invalid format
    """
    # a. trim values in columns 'Date' and 'Time'
    df["Date"] = df["Date"].str.strip()
    df["Time"] = df["Time"].str.strip()
    # b. Apply mask
    df["Date"] = pd.to_datetime(df['Date'], format='%y/%m/%d', errors='coerce').dt.date
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time
    # c. Drop columns that are not in good formats
    df = df.dropna(subset=['Date'])
    df = df.dropna(subset=['Time'])

    return df

def to_numeric(df, col_list):
    """
    :param df: df to trasnform
    :param col_list: names of the columns for which we want to change the types to numeric
    :return: df with selected columns to numeric
    """
    for col in col_list:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df


def process_columns(df, temp_min_value, temp_max_value, temp_ext_min_value, temp_ext_max_value, pres_min_value, pres_max_value, ec_min_value, ec_max_value):
    """
    :param df: input df
    :param min_value: min value to filter data
    :param max_value: max value to filter data
    :return: dictionnary with min and max values; list of temp columns; list of pressure columns; list of EC columns
    """
    # Dictionary to store values for columns starting with 'Temp' or 'Pres'
    dict_temp_pres_ec = {}

    # Lists for columns starting with 'Temp', 'EC', and 'Pres'
    temp_columns = []
    ec_columns = []
    pres_columns = []

    for col in df.columns:
        if col.startswith('Temp') or col.startswith('Pres') or col.startswith('EC'):
            # Create a sub-dictionary for each column and set min and max values
            dict_temp_pres_ec[col] = {}
            if col.startswith('Temp'):
                if "ext" in col.lower():
                    dict_temp_pres_ec[col]['min'] = temp_ext_min_value
                    dict_temp_pres_ec[col]['max'] = temp_ext_max_value
                else:
                    dict_temp_pres_ec[col]['min'] = temp_min_value
                    dict_temp_pres_ec[col]['max'] = temp_max_value
                    temp_columns.append(col)
            elif col.startswith('Pres'):
                dict_temp_pres_ec[col]['min'] = pres_min_value
                dict_temp_pres_ec[col]['max'] = pres_max_value
                pres_columns.append(col)
            else:
                dict_temp_pres_ec[col]['min'] = ec_min_value
                dict_temp_pres_ec[col]['max'] = ec_max_value
                ec_columns.append(col)

    return dict_temp_pres_ec, temp_columns, ec_columns, pres_columns


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    df.columns = df.columns.str.strip()
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

def drop_null_columns(data): 
    """
    Drop columns with Nan data to avoid to drop the whole Dataset if there are empty columns
    """
    isnull = data.isnull().values.all(axis=0)
    names_columns_to_drop = []
    for i in range(len(isnull)):
        if isnull[i] == True : 
            names_columns_to_drop.append(data.columns[i])
    for k in names_columns_to_drop : 
        data.drop([k], axis=1, inplace=True)

def temp_pres_ec_filter(df, dict):
    """
    Filters a df based on columns and related constant values set in a dictionnary
    :param df: input DataFrame
    :param dict: dictionnary with column names as keys
    :return: filtered DataFrame
    """
    df.reset_index(inplace=True, drop=True)
    for name in dict.keys():
        df = df[df[name].between(dict[name]["min"], dict[name]["max"])]
    return df

def salinity_calculator(temperature, conductivity, coeffs):
    """
    Calculates the salinity
    :param temperature: temperature value
    :param conductivity: conductivity value
    :param coeffs: constant coefficients dictionnary
    :return: salinity
    """
    R_p = 1. # pour les mesures à faible profondeur
    r_t = sum([coeffs['C'][i] * temperature**i for i in range(5)])
    R_t = conductivity / (42.914 * r_t)

    return (sum([coeffs['A'][i] * R_t**(int(i)/2.) for i in range(6)])
                + (((temperature - 15)/(1 + coeffs["K"] * (temperature - 15)))
                    * (sum([coeffs['B'][i] * R_t**(int(i)/2.) for i in range(6)]))))

def concat_temp(df):
    """
    Concatenates temperatures value to create a list of list of all temperatures value.
    :param df:input df with all columns
    :return: array like [[temp_sea_1(row_1), temp_sea_2(row_1),...,temp_sea_n(row_1)],..., [temp_sea_1(row_m), temp_sea_2(row_m),...,temp_sea_n(row_m)]
    """

    df_temp_columns = df[[col for col in df.columns if col.lower().startswith('temp')]]
    array = df_temp_columns.values().tolist()
    return array

