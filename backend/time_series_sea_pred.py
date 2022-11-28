# RNN Reference: https://sailajakarra.medium.com/lstm-for-time-series-predictions-cc68cc11ce4f
# The correlation part and model part refers to https://www.kaggle.com/code/nitinsss/time-series-prediction-with-keras-for-beginners
# Data source: https://datahub.io/core/sea-level-rise#readme
# GMSL here represents the cumulative changes(mm) in sea level for the world’s oceans since 1901, 
# based on a combination of long-term tide gauge measurements and recent satellite measurements. 
# It shows average absolute sea level change, which refers to the height of the ocean surface, 
# regardless of whether nearby land is rising or falling. The 0 sea level is the level at 06/15/1990.
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import keras
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.layers import LSTM
from keras.models import Sequential, Model
from keras.layers import Dense, Input, Dropout
import matplotlib.pyplot as plt
from statsmodels.tsa import stattools


dataframe_sea_level = pd.read_csv("./sea.csv",index_col='Time',parse_dates=True)

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


toconcat = pd.DataFrame()
for i in prev_list :
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
model.summary()

## split data
train_size = 0.8
test_size = 0.1
valid_size = 0.1
whole_data = feature_added.reset_index(drop=True).to_numpy()
test_part= whole_data[ int(np.floor(len(whole_data)*(train_size+valid_size))) : ]
else_part = whole_data[ : int(np.floor(len(whole_data)*(train_size+valid_size)))]
train_part = else_part[ : int(np.floor(len(else_part)*(1-valid_size))) ]
valid_part = else_part[ int(np.floor(len(else_part)*(1-valid_size))) : ]
train_input, train_res = train_part[:, 1:], train_part[:, 0]
valid_input, valid_res = valid_part[:, 1:], valid_part[:, 0]
test_inpud, test_res = test_part[:, 1:], test_part[:, 0]


## normalized data
Target_scaler = MinMaxScaler()
Feature_scaler = MinMaxScaler()

X_train_scaled = Feature_scaler.fit_transform(train_input)
X_valid_scaled = Feature_scaler.fit_transform(valid_input)
X_test_scaled = Feature_scaler.fit_transform(test_inpud)

y_train_scaled = Target_scaler.fit_transform(train_res.reshape(-1,1))
y_valid_scaled = Target_scaler.fit_transform(valid_res.reshape(-1,1))
y_test_scaled = Target_scaler.fit_transform(test_res.reshape(-1,1))

## train model
model.fit(x=X_train_scaled, y=y_train_scaled, batch_size=10, epochs=30, verbose=1, validation_data=(X_valid_scaled, y_valid_scaled), shuffle=True)
output = model.predict(X_test_scaled)
rescaled_output = Target_scaler.inverse_transform(output)
y_test_rescaled =  Target_scaler.inverse_transform(y_test_scaled)
level_fact = pd.DataFrame(y_test_rescaled, columns=['Actual sea level'])

level_pred = pd.DataFrame(rescaled_output, columns=['Predicted sea level'])
plt.figure(figsize=(10, 5))
plt.plot(level_fact, color='r')
plt.plot(level_pred, color='b')

plt.legend(['Actual','Predicted'], loc='best', prop={'size': 14})
plt.title('sea level prediction vs actual', weight='bold', fontsize=16)
plt.ylabel('GMSL(mm)', weight='bold', fontsize=14)
plt.xlabel('Days after', weight='bold', fontsize=14)
plt.xticks(weight='bold')
plt.yticks(weight='bold')
plt.grid(color = 'y', linewidth='0.5')
plt.show()