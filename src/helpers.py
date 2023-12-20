
"""
You will find here intermediary/helper functions that are used in the main script
"""

import pandas as pd
import numpy as np

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

def temp_pres_filter(df, dict):
    """
    Filters a df based on columns and related constant values set in a dictionnary
    :param df: input DataFrame
    :param dict: dictionnary with column names as keys
    :return: filtered DataFrame
    """
    df.reset_index(inplace=True, drop=True)
    for name in dict.keys():
        df = df[df[name].between(dict[name]["temp_min"], dict[name]["temp_max"])]
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


def gc_interpolate(lat1, lng1, lat2, lng2, n):
    """ Great circle interpolation
    
    @param lat1, lng1: latitude, longitude of the point 1, in demical degrees
    @param lat2, lng2: latitude, longitude of the point 2, in demical degrees
    @param n: number of points to be interpolated 
    
    @return points: points to be interpolated
    """
    
    # demical degrees to radians
    lat1 = np.deg2rad(lat1)
    lng1 = np.deg2rad(lng1)
    lat2 = np.deg2rad(lat2)
    lng2 = np.deg2rad(lng2)
    
    a = np.square(np.sin((lat2 - lat1) / 2)) + np.cos(lat1) * np.cos(lat2) * np.square(np.sin((lng2 - lng1) / 2))
    d = 2 * np.arcsin(np.sqrt(a))
    
    points = []
    for i in range(1, n + 1):
        f = 1.0 / (n + 1)
        A = np.sin((1 - f) * d) / np.sin(d)
        B = np.sin(f * d) / np.sin(d)
        x = A * np.cos(lat1) * np.cos(lng1) + B * np.cos(lat2) * np.cos(lng2)
        y = A * np.cos(lat1) * np.sin(lng1) + B * np.cos(lat2) * np.sin(lng2)
        z = A * np.sin(lat1) + B * np.sin(lat2)
        lat3 = np.arctan2(z, np.sqrt(x * x + y * y))
        lng3 = np.arctan2(y, x)
        
        points.append([np.round(np.rad2deg(lat3), 6), np.round(np.rad2deg(lng3), 6)])
        
    return points

