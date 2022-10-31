import csv
import numpy as np


"""
CSV Files To Duplicate:

Format: year,month,decimal,average,average_unc,trend,trend_unc
CH4_monthly.csv
CO2_monthly.csv
N2O_monthly.csv

Format: Year,CSIRO Adjusted Sea Level,Lower Error Bound,Upper Error Bound,NOAA Adjusted Sea Level
epa-sea-level_csv.csv

Format: Year,Mean cumulative mass balance,Number of observations
glaciers_csv.csv

Format: Year,CSIRO,IAP,MRI/JMA,NOAA
ocean-heat.csv

Format: Year,Annual anomaly,Lower 95% confidence interval,Upper 95% confidence interval
sea-surface-temp.csv
"""

# Format
# year,month,decimal,average,average_unc,trend,trend_unc

def generate_file(name):
    return