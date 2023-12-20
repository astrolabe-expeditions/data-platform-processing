import pandas as pd
import numpy as np
pd.options.mode.chained_assignment = None  # default='warn'
from tools import treatments_tools as treat
from constants import coeffs_salinite, temp_min_value, temp_max_value, temp_ext_min_value, temp_ext_max_value, pres_min_value, pres_max_value, ec_min_value, ec_max_value


def run(data):
    """
    Main function to execute.
    return: DataFrame with adequate data treatment done
    """
    ### 1/ Read data => trim column names and drop empty columns
    data = treat.trim_all_columns(data)

    ### 2/ We replace all empty strings by NaN
    data.replace('',np.nan,regex = True, inplace=True)

    ### 3/ We drop the empty columns
    treat.drop_null_columns(data)

    ### 4/ Drop empty rows and duplicate rows
    data.dropna(inplace=True)
    data.drop_duplicates(inplace = True)

    ### 5/ Drop columns where dates and/or times do not match the format
    data = treat.drop_invalid_datetime(data)

    ### 6/ filter temp, pres and ec in dataframe and lists of columns for temp, ec, pressure
    data, temp_col_names, ec_col_names, pres_col_names =\
                treat.process_columns(data,
                                temp_min_value,
                                temp_max_value,
                                temp_ext_min_value,
                                temp_ext_max_value,
                                pres_min_value,
                                pres_max_value,
                                ec_min_value,
                                ec_max_value)

    ### 7/ Calculation of EC and temperatures means
    temp_mean = data[temp_col_names].mean(axis=1)
    ec_mean = data[ec_col_names].mean(axis=1)
    sal_mean = treat.salinity_calculator(temp_mean, ec_mean / 1000, coeffs_salinite)

    ### 8/ Creation of Datetime column (for later vizualisation purposes)
    data['Datetime'] = pd.to_datetime(data['Date'].astype(str) + ' ' + data['Time'].astype(str), format='%Y-%m-%d %H:%M:%S')

    ### 9/ Add calculated value to our data
    data['Temp_mean'] = temp_mean
    data['Ec_mean'] = ec_mean
    data['Salinity'] = sal_mean

    ### 10/ Merge temp, ec, and depth columns into one column
    data = treat.to_unique_col(data)

    treat.rename_columns(data)

    return data

