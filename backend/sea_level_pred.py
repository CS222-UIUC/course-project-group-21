# Citation: https://www.epa.gov/climate-indicators/climate-change-indicators-sea-surface-temperature
# https://datahub.io/core/glacier-mass-balance#resource-glacier-mass-balance_zip
# https://www.star.nesdis.noaa.gov/socd/lsa/SeaLevelRise/LSA_SLR_timeseries.php

from re import X
import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn import linear_model
from sklearn import svm
from sklearn.linear_model import Ridge
## build model with inputs of glacier melting, sea-surface temp, ocean heat, GHG gases to predict global sea-level. 
## One could find much more data(like flodding, land subsidence) if focusing on US,and make some more precise models. See https://www.epa.gov/climate-indicators/oceans for more details.
## Note that as the dataset is pretty small, we prefer simple models to avoid overfitting


## data_loading
dataframe_CO2 = pd.read_csv("./CO2_monthly.csv")
dataframe_CH4 = pd.read_csv("./CH4_monthly.csv")
dataframe_N2O = pd.read_csv("./N2O_monthly.csv")
dataframe_glacier =pd.read_csv("./glaciers_csv.csv")
dataframe_temp = pd.read_csv("./sea-surface-temp.csv")
dataframe_oceanheat = pd.read_csv("./ocean-heat.csv")
dataframe_sea_level = pd.read_csv("./epa-sea-level_csv.csv")

## multi-polynomial-regression model: we can only build this with data from 1983-2014 because of insufficient data
co2 = dataframe_CO2['average'][52:425:12].to_numpy()
ch4 = dataframe_CH4['average'][2:375:12].to_numpy()
glacier = dataframe_glacier['Mean cumulative mass balance'][38:].to_numpy()
temp = dataframe_temp['Annual anomaly'][103:135].to_numpy()
heat = dataframe_oceanheat['CSIRO'][28:60].to_numpy()
sea_level = dataframe_sea_level['CSIRO Adjusted Sea Level'][103:].to_numpy()

## poly reg
X_input = np.column_stack((co2,ch4,glacier,temp,heat))
## By some testing, it turns out that even deg = 2 would result in large overfit. So we choose deg = 1 here.
poly = PolynomialFeatures(degree=1)
X = poly.fit_transform(X_input)
poly_reg_model = linear_model.LinearRegression()
poly_reg_model.fit(X, sea_level)

## svm regression model
svm_model = svm.SVR()
svm_model.fit(X_input, sea_level)

## TODO: ridge or lasso, but I think it may not help.

## define prediction fnc with poly_reg_model. Inputs are optional with default value of latest collected value
def pol_pred(CO2=415.58, CH4= 1906.11, GLA = -28.652, TEMP = 0.84, HEAT = 15.88066667):
    poly = PolynomialFeatures(degree=1)
    pred = poly.fit_transform([[CO2,CH4,GLA, TEMP, HEAT]])
    return poly_reg_model.predict(pred)

## prediction fnc with svm-regression. 
def svm_pred(CO2=415.58, CH4= 1906.11, GLA = -28.652, TEMP = 0.84, HEAT = 15.88066667):
    return svm_model.predict([[CO2,CH4,GLA, TEMP, HEAT]])


## TODO: it turns out we may need a larger dataset to train a better model. Monthly data is one option, but need to find corresponding datasets at first.
