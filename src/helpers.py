
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


def process_columns(df, temp_min_value, temp_max_value, temp_ext_min_value, temp_ext_max_value, pres_min_value, pres_max_value, ec_min_value, ec_max_value):
    """
    :param df: input df
    :param min_value: min value to filter data
    :param max_value: max value to filter data
    :return: processed dataframe; list of temp columns; list of pressure columns; list of EC columns
    """

    # Lists for columns starting with 'Temp', 'EC', and 'Pres'
    temp_columns = []
    ec_columns = []
    pres_columns = []

    for col in df.columns:
        # find relevant columns
        if col.startswith('Temp') or col.startswith('Pres') or col.startswith('EC'):
            # set adequate format 
            df[col] = pd.to_numeric(col, errors = 'coerce')
            # filter columns based on col dimension
            if col.startswith('Temp'):
                if "ext" in col.lower():
                    df = df[temp_pres_ec_filter(col,temp_ext_min_value,temp_ext_max_value)]
                else:
                    df = df[temp_pres_ec_filter(col,temp_min_value,temp_max_value)]
                    temp_columns.append(col)
            elif col.startswith('Pres'):
                df = df[temp_pres_ec_filter(col, pres_min_value, pres_max_value)]
                pres_columns.append(col)
            else:
                df = df[temp_pres_ec_filter(col, ec_min_value,ec_max_value)]
                ec_columns.append(col)
            # drop null values and reset index
            df.dropna(inplace = True)
            df.reset_index(inplace = True, drop = True)
    return df, temp_columns, ec_columns, pres_columns


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

def temp_pres_ec_filter(col, mini, maxi):
    """
    Filters a column based on min and max values
    :param col: input column
    :param mini: float value minimum accepted
    :param maxi: float value maximum accepted
    :return: filtered column
    """
    col = col.between(mini, maxi)
    return col

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

def to_unique_col(df):
    """
    Concatenates temp, ec, depth values to create a single columns made of list
    temp_sea column will look like:
         [[temp_sea_1(row_1), temp_sea_2(row_1),...,temp_sea_n(row_1)],..., [temp_sea_1(row_m), temp_sea_2(row_m),...,temp_sea_n(row_m)]
    :param df:input df with all columns
    :return: new df
    """
    # Identify columns
    temp_cols = [col for col in df.columns if col.lower().startswith('temp')]
    ec_cols = [col for col in df.columns if col.lower().startswith('ec')]
    depth_cols = [col for col in df.columns if col.lower().startswith('depth')]

    # Concatenate values into lists
    if depth_cols:
        df["depth"] = df[depth_cols].values.tolist()
        df.drop(columns=depth_cols, inplace=True)
    else:
        df["depth"] = [[] for _ in range(len(df))]

    if temp_cols:
        df["temp_sea"] = df[temp_cols].values.tolist()
        df.drop(columns=temp_cols, inplace=True)
    else:
        df["temp_sea"] = [[] for _ in range(len(df))]

    if ec_cols:
        df["ec_sea"] = df[ec_cols].values.tolist()
        df.drop(columns=ec_cols, inplace=True)
    else:
        df["ec_sea"] = [[] for _ in range(len(df))]

    return df

