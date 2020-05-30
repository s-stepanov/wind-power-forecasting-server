from torch import nn
from torch import load
from torch import tensor
import random

class WindPredictionNet(nn.Module):
    def __init__(self, n_hidden_neurons):
        super(WindPredictionNet, self).__init__()
        self.fc1 = nn.Linear(2, n_hidden_neurons)
        self.ac1 = nn.Sigmoid()
        self.fc2 = nn.Linear(n_hidden_neurons, 1) 
    
    def forward(self, x):
        x = self.fc1(x)
        x = self.ac1(x)
        x = self.fc2(x)
        return x


def predict(prediction_data):
  model = WindPredictionNet(200)
  model.load_state_dict(load('prediction_model.pt'))
  model.eval()

  features = []
  dates = []

  for row in prediction_data:
    features.append([row['wind_speed'], row['wind_direction']])
    dates.append(row['time'])

  result_tensor = model.forward(tensor(features)).tolist()
  result = []

  for i in range(0, len(result_tensor)):
    result.append({
      'date': dates[i],
      'power': result_tensor[i]
    })

  return result

