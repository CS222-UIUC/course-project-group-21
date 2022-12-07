import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import TensorDataset, DataLoader
from poutyne.framework import Experiment
dataframe_CO2 = pd.read_csv("./CO2_monthly.csv")
dataframe_CH4 = pd.read_csv("./CH4_monthly.csv")
dataframe_N2O = pd.read_csv("./N2O_monthly.csv")
dataframe_glacier =pd.read_csv("./glaciers_csv.csv")
dataframe_temp = pd.read_csv("./sea-surface-temp.csv")
dataframe_oceanheat = pd.read_csv("./ocean-heat.csv")
dataframe_sea_level = pd.read_csv("./epa-sea-level_csv.csv")

co2 = dataframe_CO2['average'][52:425:12].to_numpy()
ch4 = dataframe_CH4['average'][2:375:12].to_numpy()
glacier = dataframe_glacier['Mean cumulative mass balance'][38:].to_numpy()
temp = dataframe_temp['Annual anomaly'][103:135].to_numpy()
heat = dataframe_oceanheat['CSIRO'][28:60].to_numpy()
sea_level = dataframe_sea_level['CSIRO Adjusted Sea Level'][103:].to_numpy()

X_input = torch.from_numpy(np.column_stack((co2,ch4,glacier,temp,heat)))
X_input = X_input.to(torch.float32)
Y_input = torch.from_numpy(sea_level)
Y_input = Y_input.to(torch.float32)
dataset = TensorDataset(X_input,Y_input)
dataloader = DataLoader(dataset)
class rnnmodel(nn.Module):
    def __init__(self, input_dim, hidden_dim, num_layers, output_dim):
        super(rnnmodel, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        
        # RNN
        self.rnn = nn.GRU(input_dim, hidden_dim, num_layers, batch_first=True, bidirectional = False)
        self.drop = nn.Dropout(p = 0.5)
        self.lin= nn.Linear(hidden_dim, output_dim)
    def forward(self, data):
        x = self.rnn(data)[0]
        d = self.drop(x)
        output = self.lin(d)
        return output
input_dim = 5
output_dim = 1
hidden_dim = 100
num_layers = 10
rnn = rnnmodel(input_dim, hidden_dim, num_layers, output_dim)

lr = 0.01
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(rnn.parameters(), lr=lr)
print(X_input.shape)
for ep in range(30):
    optimizer.zero_grad()
    output = rnn(X_input)
    loss = criterion(output, Y_input)
    loss.backward()
    optimizer.step()
pred = torch.from_numpy(np.array([[340, 1626,-10,0.066, -3.686433333]])).to(torch.float32)
out = rnn(pred)
print(out)