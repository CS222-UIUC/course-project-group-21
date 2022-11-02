import pytest
import temperature_regression_model

def test_to_year():
    assert temperature_regression_model.to_year("1855-09-01") == 1855
    assert temperature_regression_model.to_year("1953-10-01") == 1953
    assert temperature_regression_model.to_year("2003-01-01") == 2003
