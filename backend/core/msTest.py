


## Used data provided by meteostat https://dev.meteostat.net/.
from tkinter.filedialog import asksaveasfile
import numpy as np
from datetime import datetime
from meteostat import Point,Hourly, Daily, Monthly, Stations

import pandas as pd



def get():
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
    #s_axes = selected.plot()
    #dict_data = selected.to_dict()
    return Response({
        "selected": selected.to_json()
    })

get()
    
