import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# reads temperature data from csv file
def temperature_data_load():
    dft = pd.read_csv(os.path.abspath("course-project-group-21/backend/GlobalLandTemperaturesByMajorCity.csv"))
    return dft

# reads carbon emissions data from csv file
def carbon_emissions_data_load():
    dfc = pd.read_csv(os.path.abspath("course-project-group-21/backend/AtmosphericCarbonDioxide.csv"))
    return dfc

# data processing and cleaning for temperature dataset
def temperature_data_processing():
    dft = temperature_data_load()
    dft = dft.dropna()
    dft['Year'] = dft['dt'].apply(to_year)                     # creates new year column in temperature dataframe
    dft = dft[(dft["Year"] >= 1958) & (dft["Year"] <= 2013)]   # select a subset of data between 1958 and 2013
    dft = dft[dft["Country"] == "United States"]               # select data from the United States only
    dft = find_avg_temperature(dft)                            # calculates average temperature for each year
    dft = dft.drop(columns=["index", "dt", "AverageTemperatureUncertainty", "City", "Country", "Latitude", "Longitude"])  # drop irrelevant columns
    dft = dft.set_index("Year")                                # set index to be year
    return dft

# data processing and cleaning for carbon emissions dataset
def carbon_emissions_data_processing():
    dfc = carbon_emissions_data_load()
    dfc = dfc.dropna()
    dfc = dfc[(dfc["Year"] >= 1958) & (dfc["Year"] <= 2013)]   # select a subset of data between 1958 and 2013
    dfc = find_avg_carbon_emissions(dfc)                       # calculates average carbon emissions for each year
    dfc = dfc.drop(columns=["index", "Month", "Decimal Date", "Seasonally Adjusted CO2 (ppm)", "Carbon Dioxide Fit (ppm)",
     "Seasonally Adjusted CO2 Fit (ppm)"])                     # drop irrelevant columns
    dfc = dfc.set_index("Year")
    return dfc

# returns only year from datetime column, called in temperature_data_processing()
def to_year(date):
    for i in [date]:
        first = i.split('-')[0]
    return int(first)

# returns new dataframe with average temperature for each year
def find_avg_temperature(df):
    df_avg_temp = pd.DataFrame()
    years = df["Year"].unique()     # finds all unique years in dataframe
    for year in years:              
        df_avg = df[df["Year"] == year]["AverageTemperature"].mean()   # calculates average temperature for specific year
        df_new = (df[df["Year"] == year]).head(1)                      
        df_new["AverageTemperature"] = df_avg                          # stores calculated average temperature in column
        df_avg_temp = df_avg_temp.append(df_new)                       # appends to outputted dataframe
    df_avg_temp = df_avg_temp.reset_index()
    return df_avg_temp

# returns new dataframe with average carbon emissions for each year
def find_avg_carbon_emissions(df):
    df_avg_carbon_emissions = pd.DataFrame()
    years = df["Year"].unique()
    for year in years:
        df_avg = df[df["Year"] == year]['Carbon Dioxide (ppm)'].mean()
        df_new = (df[df["Year"] == year]).head(1)
        df_new["Carbon Dioxide (ppm)"] = df_avg
        df_avg_carbon_emissions = df_avg_carbon_emissions.append(df_new)
    df_avg_carbon_emissions = df_avg_carbon_emissions.reset_index()
    return df_avg_carbon_emissions

# scatter plot visualizing relationship between carbon dioxide and temperature
def temperature_carbon_visualization():
    dft = temperature_data_processing()
    dfc = carbon_emissions_data_processing()
    merge = dft.join(dfc)
    merge.plot(x ='Carbon Dioxide (ppm)', y ='AverageTemperature', kind ='scatter')