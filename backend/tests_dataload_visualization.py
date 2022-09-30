import pytest
# from .data_collection import data_load, data_visualize
import data_collection


def test_data_load():
    test_mon = data_collection.data_load([1980,1,1,2020,12,31],[49.2497, -123.1193],['tavg', 'tmin', 'tmax'], 'monthly')
    ##not sure what is a good way to test this
    test_day = data_collection.data_load([1980,1,1,2020,12,31],[49.2497, -123.1193],['tavg', 'tmin', 'tmax'], 'daily')
    assert(1)

def test_data_vis():
    test = data_collection.data_load([1980,1,1,2020,12,31],[49.2497, -123.1193],['tavg', 'tmin', 'tmax'], 'monthly')
    data_collection.data_visualize(test)
    assert(1)