###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

import pandas as pd

medals = pd.read_csv("datasets/medals_by_country_2016.csv")
olympic = pd.read_csv('datasets/summer2016.csv')
austin_weather = pd.read_csv("datasets/austin_weather.csv")
seattle_weather= pd.read_csv("datasets/seattle_weather.csv")
climate_change = pd.read_csv('datasets/climate_change.csv', parse_dates=["date"], index_col="date")

# Filtering the data
mens_gymnastics = olympic[(olympic["Sport"] == "Gymnastics") & (olympic["Sex"] == "M")]
mens_rowing = olympic[(olympic["Sport"] == "Rowing") & (olympic["Sex"] == "M")]
seattle_weather = seattle_weather.tail(12)

months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

# Adding a 'MONTH' column
austin_weather["MONTH"] = months
seattle_weather["MONTH"] = months

print(olympic,mens_gymnastics,mens_rowing)

###########################################
# 2) Quantitative comparisons: bar-charts
###########################################

import matplotlib.pyplot as plt

fig, ax = plt.subplots()

# Plot a bar-chart of gold medals as a function of country
ax.bar(medals.index,medals["Gold"])

# Set the x-axis tick labels to the country names
ax.set_xticklabels(medals.index, rotation=90)

# Set the y-axis label
ax.set_ylabel("Number of medals")

plt.show()

###########################################
# 3) Stacked bar chart
###########################################

fig, ax = plt.subplots()

# Add bars for "Gold" with the label "Gold"
ax.bar(medals.index, medals["Gold"], label="Gold")

# Stack bars for "Silver" on top with label "Silver"
ax.bar(medals.index, medals["Silver"], bottom=medals["Gold"], label="Silver")

# Stack bars for "Bronze" on top of that with label "Bronze"
ax.bar(medals.index, medals["Bronze"], bottom=medals["Gold"] + medals["Silver"], label="Bronze")

# Display the legend
ax.legend()

plt.show()

###########################################
# 4) Quantitative comparisons: histograms
###########################################

fig, ax = plt.subplots()
# Plot a histogram of "Weight" for mens_rowing
ax.hist(mens_rowing["Weight"])

# Compare to histogram of "Weight" for mens_gymnastics
ax.hist(mens_gymnastics["Weight"])

# Set the x-axis label to "Weight (kg)"
ax.set_xlabel("Weight (kg)")

# Set the y-axis label to "# of observations"
ax.set_ylabel("# of observations")

plt.show()

###########################################
#5) "Step" histogram
###########################################

fig, ax = plt.subplots()

# Plot a histogram of "Weight" for mens_rowing
ax.hist( mens_rowing["Weight"], histtype="step", bins=5, label="Rowing")

# Compare to histogram of "Weight" for mens_gymnastics
ax.hist( mens_gymnastics["Weight"], histtype="step", bins=5, label="Gymnastics")

ax.set_xlabel("Weight (kg)")
ax.set_ylabel("# of observations")

# Add the legend and show the Figure
ax.legend()
plt.show()

###########################################
#6) Statistical plotting
###########################################

fig, ax = plt.subplots()

# Add a bar for the rowing "Height" column mean/std
ax.bar("Rowing", mens_rowing["Height"].mean(), yerr=mens_rowing["Height"].std())

# Add a bar for the gymnastics "Height" column mean/std
ax.bar("Gymnastics", mens_gymnastics["Height"].mean(), yerr=mens_gymnastics["Height"].std())

# Label the y-axis
ax.set_ylabel("Height (cm)")

plt.show()

###########################################
#7) Adding error-bars to a plot
###########################################

fig, ax = plt.subplots()

# Add Seattle temperature data in each month with error bars
ax.errorbar(seattle_weather["MONTH"],seattle_weather["MLY-TAVG-NORMAL"] , yerr=seattle_weather["MLY-TAVG-STDDEV"])

# Add Austin temperature data in each month with error bars
ax.errorbar(austin_weather["MONTH"],austin_weather["MLY-TAVG-NORMAL"] , yerr=austin_weather["MLY-TAVG-STDDEV"])

# Set the y-axis label
ax.set_ylabel("Temperature (Fahrenheit)")

plt.show()

###########################################
#8) Creating boxplots
###########################################

fig, ax = plt.subplots()

# Add a boxplot for the "Height" column in the DataFrames
ax.boxplot([mens_rowing["Height"],mens_gymnastics["Height"]])

# Add x-axis tick labels:
ax.set_xticklabels(["Rowing", "Gymnastics"])

# Add a y-axis label
ax.set_ylabel("Height (cm)")

plt.show()

###########################################
#9) Quantitative comparisons: scatter plots
###########################################

fig, ax = plt.subplots()

# Add data: "co2" on x-axis, "relative_temp" on y-axis
ax.scatter(climate_change["co2"], climate_change["relative_temp"])

# Set the x-axis label to "CO2 (ppm)"
ax.set_xlabel("CO2 (ppm)")

# Set the y-axis label to "Relative temperature (C)"
ax.set_ylabel("Relative temperature (C)")

plt.show()

###########################################
#10) Encoding time by color
###########################################

fig, ax = plt.subplots()

# Add data: "co2", "relative_temp" as x-y, index as color
ax.scatter(climate_change["co2"], climate_change["relative_temp"], c=climate_change.index)

# Set the x-axis label to "CO2 (ppm)"
ax.set_xlabel("CO2 (ppm)")

# Set the y-axis label to "Relative temperature (C)"
ax.set_ylabel("Relative temperature (C)")

plt.show()