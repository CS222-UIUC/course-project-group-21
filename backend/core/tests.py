# from django.test import TestCase

# Create your tests here.


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

def sea_level_data():
    dataframe_sea_level = pd.read_csv("backend/core/sea.csv",index_col='Time',parse_dates=True)

    cor = stattools.acf(dataframe_sea_level,  nlags=100, qstat=True, fft=True,alpha = 0.05)[0]

    plt.figure(figsize=(10, 5))
    plt.plot(pd.Series(cor), color='r', linewidth=2)
    plt.title('Autocorrelation of months')
    plt.xlabel('Length')
    plt.ylabel('Correlation')

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

    toconcat = pd.DataFrame()
    for i in prev_list:
        prev_level = pd.DataFrame(sea_level[attribute].iloc[(start - i) : (end - i)])
        prev_level.reset_index(drop=True, inplace=True)
        toconcat = pd.concat([toconcat, prev_level], axis=1)
    feature_added = pd.concat([cut_sea_level, toconcat], axis=1)
    feature_added.set_index(['datetime'], drop=True, inplace=True)
    
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
    # model.fit(x=train_input, y=train_res, batch_size=10, epochs=30, verbose=0, validation_data=(valid_input, valid_res), shuffle=True)
    # model.save('./time_series_sea_model')

    # this loads the model
    model = keras.models.load_model('backend/core/time_series_sea_model')
    output = model.predict(test_input)
    level_fact = pd.DataFrame(test_res, columns=['Actual sea level'])

    level_pred = pd.DataFrame(output, columns=['Predicted sea level'])

    return [level_fact, level_pred]

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


temp_graph()