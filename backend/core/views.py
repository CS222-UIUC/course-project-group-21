from django.shortcuts import render
#from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User


## Used data provided by meteostat https://dev.meteostat.net/.
from tkinter.filedialog import asksaveasfile
import numpy as np
from datetime import datetime
from meteostat import Point,Hourly, Daily, Monthly, Stations

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


from sklearn.preprocessing import MinMaxScaler
import keras
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.layers import LSTM
from keras.models import Sequential, Model
from keras.layers import Dense, Input, Dropout
import matplotlib.pyplot as plt
from statsmodels.tsa import stattools



##########################################################################################
#                               TEMPERATURE GRAPH (tianfan)
##########################################################################################

def temp_graph():
    time_period = [1980,1,1,2020,12,31]
    loc = [49.2497, -123.1193]
    features = ['tavg', 'tmin', 'tmax']
    freq = 'monthly'
    # input validity check
    assert(len(time_period)==6)
    assert(len(loc)>=2)
    
    # Set time period
    start = datetime(time_period[0], time_period[1], time_period[2])
    end = datetime(time_period[3], time_period[4], time_period[5])
    
    # Create Point for particular location
    if (len(loc) == 3):
        location = Point(loc[0], loc[1], loc[2])
    else:
        location = Point(loc[0], loc[1])
        
    # Get data freq
    match freq:
        case 'hourly':
            data = Hourly(location, start, end)
        case 'daily':
            data = Daily(location, start, end)
        case 'monthly':
            data = Monthly(location, start, end)
        case other:
            raise TypeError("invalid freq")
    
    data = data.fetch()
    selected = data[features]
    return selected
    #s_axes = selected.plot()
    #dict_data = selected.to_dict()

class TempGraph(APIView):
    def get(self, request):
        the_temp_graph = temp_graph()
        return Response({
            "selected": the_temp_graph.to_json()
        })







##########################################################################################
#                               CARBON GRAPH (aashi)
##########################################################################################


# reads temperature data from csv file
def temperature_data_load():
    dft = pd.read_csv(os.path.abspath("./core/GlobalLandTemperaturesByMajorCity.csv"))
    return dft

# reads carbon emissions data from csv file
def carbon_emissions_data_load():
    dfc = pd.read_csv(os.path.abspath("./core/AtmosphericCarbonDioxide.csv"))
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
    return merge

    # merge.plot(x ='Carbon Dioxide (ppm)', y ='AverageTemperature', kind ='scatter')

class CarbonGraph(APIView):
    def get(self, request):
        carbon_vis = temperature_carbon_visualization()
        return Response({
            "dataframe": carbon_vis.to_json()
        })









##########################################################################################
#                               SEA LEVEL GRAPH (tianfan)
##########################################################################################


# RNN Reference: https://sailajakarra.medium.com/lstm-for-time-series-predictions-cc68cc11ce4f
# The correlation part and model part refers to https://www.kaggle.com/code/nitinsss/time-series-prediction-with-keras-for-beginners
# Data source: https://datahub.io/core/sea-level-rise#readme
# GMSL here represents the cumulative changes(mm) in sea level for the world’s oceans since 1901, 
# based on a combination of long-term tide gauge measurements and recent satellite measurements. 
# It shows average absolute sea level change, which refers to the height of the ocean surface, 
# regardless of whether nearby land is rising or falling. The 0 sea level is the level at 06/15/1990.
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# import keras
# from keras.preprocessing.sequence import TimeseriesGenerator
# from keras.layers import LSTM
# from keras.models import Sequential, Model
# from keras.layers import Dense, Input, Dropout
# import matplotlib.pyplot as plt
# from statsmodels.tsa import stattools

def sea_level_data(future_year, future_month):
    dataframe_sea_level = pd.read_csv("./core/sea.csv",index_col='Time',parse_dates=True)

    # cor = stattools.acf(dataframe_sea_level,  nlags=100, qstat=True, fft=True,alpha = 0.05)[0]

    # # plt.figure(figsize=(10, 5))
    # # plt.plot(pd.Series(cor), color='r', linewidth=2)
    # # plt.title('Autocorrelation of months')
    # # plt.xlabel('Length')
    # # plt.ylabel('Correlation')

    ## We choose the cor >= 90%. From the graph, it is about 35.
    prev_len = 35
    sea_level = dataframe_sea_level
    prev_list = np.arange(35)
    attribute = 'GMSL'
    start = prev_list[-1] 
    end = len(sea_level)
    sea_level['datetime'] = sea_level.index
    cut_sea_level = sea_level[start:end]
    cut_sea_level.reset_index(inplace=True, drop=True)
    # print(cut_sea_level)

    # print("got here 1")

    toconcat = pd.DataFrame()
    for i in prev_list:
        prev_level = pd.DataFrame(sea_level[attribute].iloc[(start - i) : (end - i)])
        prev_level.reset_index(drop=True, inplace=True)
        toconcat = pd.concat([toconcat, prev_level], axis=1)
    feature_added = pd.concat([cut_sea_level, toconcat], axis=1)
    feature_added.set_index(['datetime'], drop=True, inplace=True)
    
    # print("got here 2")

    ## define layers for NN
    input_layer = Input(shape=(35), dtype='float32')
    # lstm_layer = LSTM(50, activation='relu')(input_layer)
    dense1 = Dense(60, activation='linear')(input_layer)
    dense2 = Dense(60, activation='linear')(dense1)
    dropout_layer = Dropout(0.2)(dense2)
    output_layer = Dense(1, activation='linear')(dropout_layer)
    model = Model(inputs=input_layer, outputs=output_layer)
    model.compile(loss='mean_squared_error', optimizer='adam')
    # model.summary()

    # print("got here 3")

    ## split data
    train_size = 0.8
    test_size = 0.1
    valid_size = 0.1
    whole_data = feature_added.reset_index(drop=True).to_numpy()
    test_part= whole_data[int(np.floor(len(whole_data)*(train_size+valid_size))) :]
    else_part = whole_data[ : int(np.floor(len(whole_data)*(train_size+valid_size)))]
    train_part = else_part[ : int(np.floor(len(else_part)*(1-valid_size))) ]
    valid_part = else_part[ int(np.floor(len(else_part)*(1-valid_size))) : ]
    train_input, train_res = train_part[:, 1:], train_part[:, 0]
    valid_input, valid_res = valid_part[:, 1:], valid_part[:, 0]
    test_input, test_res = test_part[:, 1:], test_part[:, 0]




    ## train model
    model.fit(x=train_input, y=train_res, batch_size=10, epochs=30, verbose=0, validation_data=(valid_input, valid_res), shuffle=True)
    model.save('./core/time_series_sea_model')

    # print("got here 4")

    # this loads the model
    model = keras.models.load_model('./core/time_series_sea_model')
    output = model.predict(test_input)
    level_fact = pd.DataFrame(test_res, columns=['Actual sea level'])

    level_pred = pd.DataFrame(output, columns=['Predicted sea level'])

    # print("got here 5")


    #future_sea_level_prediction(future_month):
    #assert(future_month > 0)

    cur_year = 2014
    cur_month = 1

    converted_future_month = (future_year - cur_year) * 12 + (future_month - cur_month)


    
    output = []
    cur_batch = test_input[-1:]
    for i in range(converted_future_month):
        pred = model.predict(cur_batch,verbose = 0)[0,0]
        output.append(pred)
        updated_part = np.append(cur_batch[0,1:],pred)
        cur_batch[0,:] = updated_part
    level_pred = pd.DataFrame(output, columns=['Actual sea level'])

    return [level_fact, level_pred]


class SeaLevelGraph(APIView):
    def post(self, request):
        future_year = request.data['year']
        future_month = request.data['month']

        sea_level_pred = sea_level_data(future_year, future_month)
        # print("got here 6")
        return Response({
            "actual": sea_level_pred[0].to_json(),
            "predicted": sea_level_pred[1].to_json(),
        })




