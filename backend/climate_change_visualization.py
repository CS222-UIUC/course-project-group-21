import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import seasonal_decompose
import seaborn as sns
import os

def climate_change_visualization():
    # read csv file into dataframe

    df = pd.read_csv(os.path.abspath("course-project-group-21/backend/GlobalLandTemperaturesByState.csv"))

    # removes rows with null values
    df = df.dropna(how = 'any', axis = 0)

    # renames columns as more readable and user-friendly
    df.rename(columns={'dt': 'Date', 'AverageTemperature':'Average Temperature', 'AverageTemperatureUncertainty':'Avg Temperature Confidence Interval'}, inplace=True)

    # converts string datatime to python datatime object 
    df['Date'] = pd.to_datetime(df['Date'])
    # sets date column as index of dataframe
    df.set_index('Date', inplace=True)

    # create new year column
    df['Year'] = df.index.year

    # select temperature data from 1980 to 2013
    df = df.loc['1980' : '2013']

    # group by country, find average land temperature of each country over time and sort in increasing order
    # df[['Country', 'Average Temperature']].groupby(['Country']).mean().sort_values('Average Temperature')

    plt.figure(figsize=(10,5))
    sns.lineplot(x = "Year", y = "Average Temperature", data=df)
    plt.show()