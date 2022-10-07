## data reference:
## Ed Dlugokencky and Pieter Tans, NOAA/GML (gml.noaa.gov/ccgg/trends/)
## Lan, X., K.W. Thoning, and E.J. Dlugokencky (2022): Trends in globally-averaged CH4, N2O, and SF6 determined from NOAA Global Monitoring Laboratory measurements. 
## Version 2022-10, https://doi.org/10.15138/P8XG-AA10

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
## editions in text files so it can read as csv
dataframe_CH4 = pd.read_csv("C:/Users/xutia/course-project-group-21-main/course-project-group-21-main/backend/CH4_monthly.txt", sep = ',')

# storing this dataframe in a csv file
dataframe_CH4.to_csv('C:/Users/xutia/course-project-group-21-main/course-project-group-21-main/backend/CH4_monthly.csv', 
                  index = None)

dataframe_N2O = pd.read_csv("C:/Users/xutia/course-project-group-21-main/course-project-group-21-main/backend/N2O_monthly.txt", sep = ',')
dataframe_N2O.to_csv('C:/Users/xutia/course-project-group-21-main/course-project-group-21-main/backend/N2O_monthly.csv', 
                  index = None)

dataframe_CO2 = pd.read_csv("C:/Users/xutia/course-project-group-21-main/course-project-group-21-main/backend/CO2_monthly.csv")

## in the datasets, there're values of -9.99 indicating uncalculated uncertainty. Usually unc isn't used, but let's do it anyway.
## Here we just use the average value of other rows to fill in
dataframe_CH4['average_unc'].loc[dataframe_CH4['average_unc'] == -9.99] = dataframe_CH4['average_unc'].loc[dataframe_CH4['average_unc'] != -9.99].mean()
dataframe_CH4['trend_unc'].loc[dataframe_CH4['trend_unc'] == -9.99] = dataframe_CH4['trend_unc'].loc[dataframe_CH4['trend_unc'] != -9.99].mean()
dataframe_N2O['average_unc'].loc[dataframe_N2O['average_unc'] == -9.99] = dataframe_N2O['average_unc'].loc[dataframe_N2O['average_unc'] != -9.99].mean()
dataframe_N2O['trend_unc'].loc[dataframe_N2O['trend_unc'] == -9.99] = dataframe_N2O['trend_unc'].loc[dataframe_N2O['trend_unc'] != -9.99].mean()

## make plot combining these three datasets
fig = plt.figure()
color = iter(cm.rainbow(np.linspace(0, 1, 6)))
labels = iter(np.array(['CH4_average','CH4_trend','N2O_average','N2O_trend','CO2_average','CO2_trend']))
for frame in [dataframe_CH4, dataframe_N2O, dataframe_CO2]:
    np_year = np.array(frame['decimal'])
    np_average = np.array(frame['average'])
    np_trend = np.array(frame['trend'])
    plt.plot(np_year, np_average, c = next(color), label = next(labels))
    plt.plot(np_year, np_trend, c = next(color), label = next(labels))
plt.xlabel('year')
plt.ylabel('mole fraction(ppm)')
plt.legend(loc='best')
plt.show()

## Todo: since their scales differ, we can also show each of them
## we can see from the plots that there is upward trend in all three green house gases.

## We then combine the data about the rise of sea level
sea_level = pd.read_csv("C:/Users/xutia/course-project-group-21-main/course-project-group-21-main/backend/epa-sea-level_csv.csv")
## here we could focus on the sea level starting from 1979(the start date of GHG dataset)
sea_level = sea_level[99:]

## relation between CO2 and sea level
fig = plt.figure()
plt.plot(dataframe_CO2['average'][4:413:12], sea_level['CSIRO Adjusted Sea Level'][:-1])
plt.xlabel('CO2')
plt.ylabel('sea level')
plt.legend(loc='best')
plt.show()

## we can also check the correlation
print(np.corrcoef(dataframe_CO2['average'][4:413:12],sea_level['CSIRO Adjusted Sea Level'][:-1]))
## the result here is 0.9725, which implies they are highly correlated