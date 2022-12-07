import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from torch.nn.functional import normalize

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
dataframe_CO2 = pd.read_csv("./CO2_monthly.csv")
dataframe_CH4 = pd.read_csv("./CH4_monthly.csv")
dataframe_N2O = pd.read_csv("./N2O_monthly.csv")
dataframe_sea_level = pd.read_csv("./sea.csv")
## need normalize here
co2 = dataframe_CO2['average'][265:420].to_numpy() 
ch4 = dataframe_CH4['average'][211:366].to_numpy()
n2o = dataframe_N2O['average'][1:156].to_numpy()
sea_level = dataframe_sea_level['GMSL'][1201:1356].to_numpy()
X = np.column_stack((co2,ch4,n2o))
# X_input = torch.from_numpy(np.column_stack((co2,ch4,n2o)))
# print("x-shape")
# print(X_input.shape)
# X_input = normalize(X_input, dim=0)
# X_input = X_input.to(torch.float32)
# X_input = torch.nn.functional.normalize(X_input)
# Y_input = torch.from_numpy(sea_level)
# Y_input = Y_input.to(torch.float32)
# print(Y_input.shape)
class rnnmodel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(rnnmodel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # RNN
        self.rnn = nn.RNN(input_dim, hidden_dim, num_layers, batch_first=True, bidirectional = False)
        self.drop = nn.Dropout(p = 0.5)
        self.lin= nn.Linear(hidden_dim, output_dim)
    def forward(self, data):
        x = self.rnn(data)[0]
        d = self.drop(x)
        output = self.lin(d)
        return output
input_dim = 3
output_dim = 1
hidden_dim = 10
num_layers = 10
rnn = rnnmodel(input_dim, hidden_dim, num_layers, output_dim)

# lr = 0.01
# criterion = nn.MSELoss()
# optimizer = torch.optim.SGD(rnn.parameters(), lr=lr)
# print(X_input.shape)
# for ep in range(20):
#     optimizer.zero_grad()
#     output = rnn(X_input)
#     # print(output)
#     loss = criterion(output, Y_input)
#     loss.backward()
#     print(loss.item())
#     optimizer.step()
# pred = torch.from_numpy(np.array([[400, 1810.39, 325.51]])).to(torch.float32)
# torch.save(rnn, "./rnn_sea")
# out = rnn(pred)
# loaded = torch.load("./rnn_sea")
# loaded.eval()

# out = loaded(pred)
# print(out)
# print(Y_input)

# the model built here doesn't perform well. Try something like to example.

num_fea = 3
val_ind = np.random.choice(range(155), 20, replace=False)
total_ind = np.arange(0,155)
train_ind = [i for i in total_ind if i not in val_ind]
x_train = X[train_ind].reshape(135,3,1)
y_train = sea_level[train_ind]
x_val = X[val_ind].reshape(20,3,1)
y_val = sea_level[val_ind]
model = Sequential()
model.add(LSTM(32, activation='relu'))
model.add(Dense(1))
model.compile(optimizer='adam', loss='mse')

model.fit(x_train, y_train, batch_size = 4, epochs = 10, validation_data = (x_val, y_val))
model.save('./keras_model')
print("train complete")
print(model.predict(np.array([[400, 1810.39, 325.51]]).reshape(1,3,1)))
print(model.predict(np.array([[800, 1810.39, 325.51]]).reshape(1,3,1)))
print(model.predict(np.array([[1200, 1810.39, 325.51]]).reshape(1,3,1)))


