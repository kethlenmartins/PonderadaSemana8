import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress

def draw_plot():
    # Read data from file
    df = pd.read_csv("epa-sea-level.csv")

    plt.figure(figsize=(10, 6))
    plt.scatter(df["Year"], df["CSIRO Adjusted Sea Level"])

    slope, intercept, r_value, p_value, std_err = linregress(df["Year"], df["CSIRO Adjusted Sea Level"])
    years_extended = pd.Series([i for i in range(1880, 2051)])
    line_of_best_fit = intercept + slope * years_extended
    plt.plot(years_extended, line_of_best_fit, label='Best Fit Line (1880-2050)', color='red')

    df_2000 = df[df["Year"] >= 2000]
    slope_2000, intercept_2000, r_value_2000, p_value_2000, std_err_2000 = linregress(df_2000["Year"], df_2000["CSIRO Adjusted Sea Level"])
    years_extended_2000 = pd.Series([i for i in range(2000, 2051)])
    line_of_best_fit_2000 = intercept_2000 + slope_2000 * years_extended_2000
    plt.plot(years_extended_2000, line_of_best_fit_2000, label='Best Fit Line (2000-2050)', color='green')

    plt.xlabel("Year")
    plt.ylabel("Sea Level (inches)")
    plt.title("Rise in Sea Level")

    # Save plot and return data for testing (do not modify)
    plt.savefig('sea_level_plot.png')
    return plt.gca()