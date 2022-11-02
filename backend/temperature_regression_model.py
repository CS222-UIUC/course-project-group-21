import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# reads temperature data from csv file
def temperature_data_load():
    df = pd.read_csv(os.path.abspath("course-project-group-21/backend/GlobalLandTemperaturesByState.csv"))
    return df

# reads carbon emissions data from csv file
def carbon_emissions_data_load():
    cd = pd.read_csv(os.path.abspath("course-project-group-21/backend/AtmosphericCarbonDioxide.csv"))
    return cd

# returns only year from date time column
def to_year(date):
    for i in [date]:
        first = i.split('-')[0]
        return int(first)

# returns new dataframe with column Average Temperature
# TO DO: def find_avg_temperature(df):
