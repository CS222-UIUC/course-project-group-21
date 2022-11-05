import pytest
import pandas as pd
import temperature_carbon_regression_model


def test_temperature_data_load():
    df1 = temperature_carbon_regression_model.temperature_data_load()
    df2 = pd.read_csv(os.path.abspath("course-project-group-21/backend/GlobalLandTemperaturesByState.csv"))
    assert df1.equals(df2)

def test_carbon_emissions_data_load():
    df1 = temperature_carbon_regression_model.carbon_emissions_data_load()
    df2 = pd.read_csv(os.path.abspath("course-project-group-21/backend/AtmosphericCarbonDioxide.csv"))
    assert df1.equals(df2)

def test_to_year():
    assert temperature_carbon_regression_model.to_year("1855-09-01") == 1855
    assert temperature_carbon_regression_model.to_year("1953-10-01") == 1953
    assert temperature_carbon_regression_model.to_year("2003-01-01") == 2003

def test_find_avg_temperature():
    data = [[2001, 10], [2002, 20], [2003, 30]]
    df1 = pd.DataFrame(data, columns=['Year', 'AverageTemperature'])
    df2 = temperature_carbon_regression_model.find_avg_temperature(df1)
    assert df1.equals(df2)
    
def test_find_avg_carbon_emissions():
    data = [[2001, 5], [2002, 7], [2003, 9]]
    df1 = pd.DataFrame(data, columns=['Year', 'Carbon Dioxide (ppm)'])
    df2 = temperature_carbon_regression_model.find_avg_carbon_emissions(df1)
    assert df1.equals(df2)


def test_temperature_data_processing():
    dft = temperature_carbon_regression_model.temperature_data_processing()
    assert dft.notnull()
    assert "AverageTemperature" in dft.columns

def test_carbon_emissions_data_processing():
    dfc = temperature_carbon_regression_model.carbon_emissions_data_processing()
    assert dfc.notnull()
    assert "Carbon Dioxide (ppm)" in dfc.columns
    