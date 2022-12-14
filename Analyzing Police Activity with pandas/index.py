###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

# Import the pandas library as pd
import pandas as pd

# Read 'police.csv' into a DataFrame named ri
ri = pd.read_csv("datasets/police.csv")

# Examine the head of the DataFrame
print(ri.head())

# Count the number of missing values in each column
print(ri.isnull().sum())

###########################################
# 2) Dropping columns and rows
###########################################

# Examine the shape of the DataFrame
print(ri.shape)  # (91741, 15)

# Drop the 'county_name' column
ri.drop(["county_name"], axis="columns", inplace=True)

# Examine the shape of the DataFrame (again)
print(ri.shape)  # (91741, 13)

# Count the number of missing values in each column
print(ri.isnull().sum())

# Drop all rows that are missing 'driver_gender'
ri.dropna(subset=["driver_gender"], inplace=True)

# Count the number of missing values in each column (again)
print(ri.isnull().sum())

# Examine the shape of the DataFrame
print(ri.shape)

###########################################
# 3) Correcting data types
###########################################

# Examine the head of the 'is_arrested' column
print("'is_arrested' datatype was: ", ri.is_arrested.dtype)

# Change the data type of 'is_arrested' to 'bool'
ri["is_arrested"] = ri.is_arrested.astype("bool")

# Check the data type of 'is_arrested'
print("'is_arrested' new datatype is: ", ri.is_arrested.dtype)

# Concatenate 'stop_date' and 'stop_time' (separated by a space)
combined = ri.stop_date.str.cat(ri.stop_time, sep=" ")

# Convert 'combined' to datetime format
ri["stop_datetime"] = pd.to_datetime(combined)

# Examine the data types of the DataFrame
print(ri.dtypes)

# Set 'stop_datetime' as the index
ri.set_index("stop_datetime", inplace=True)

# Examine the index
print(ri.index)

# Examine the columns
print(ri.columns)

###########################################
# 4) Examining traffic violations
###########################################

# Count the unique values in 'violation'
print("Count of 'violation':", ri.violation.value_counts())

# Express the counts as proportions
print("Proportion of 'violation':", ri.violation.value_counts(normalize=True))

# Speeding 0.560, More than half of all violations are for speeding,

# Create a DataFrame of female drivers
female = ri[ri.driver_gender == "F"]

# Create a DataFrame of male drivers
male = ri[ri.driver_gender == "M"]

# Compute the violations by female drivers (as proportions)
print("Violations by female drivers:", female.violation.value_counts(normalize=True))

# Compute the violations by male drivers (as proportions)
print("Violations by male drivers:", male.violation.value_counts(normalize=True))

# About two-thirds of female traffic stops are for speeding,
# whereas stops of males are more balanced among the six categories.
# This doesn't mean that females speed more often than males, however,
# since we didn't take into account the number of stops or drivers.

###########################################
# 5) Comparing speeding outcomes by gender
###########################################

# Create a DataFrame of female drivers stopped for speeding
female_and_speeding = ri[(ri.driver_gender == "F") & (ri.violation == "Speeding")]

# Create a DataFrame of male drivers stopped for speeding
male_and_speeding = ri[(ri.driver_gender == "M") & (ri.violation == "Speeding")]

# Compute the stop outcomes for female drivers (as proportions)
print(
    "Stop Outcomes for female drivers who were stopped for speeding:",
    female_and_speeding.stop_outcome.value_counts(normalize=True),
)

# Compute the stop outcomes for male drivers (as proportions)
print(
    "Stop Outcomes for male drivers who were stopped for speeding:",
    male_and_speeding.stop_outcome.value_counts(normalize=True),
)

#  The numbers are similar for males and females: about 95% of stops for speeding result in a ticket.

###########################################
# 6) Calculating the search rate
###########################################

# Check the data type of 'search_conducted'
print("data type of 'search_conducted':", ri.search_conducted.dtype)

# Calculate the search rate by counting the values
print(
    "search rate by counting the values:",
    ri.search_conducted.value_counts(normalize=True),
)

# Calculate the search rate by taking the mean
print("search rate by taking the mean:", ri.search_conducted.mean())  #  3.8%

# Calculate the search rate for both groups simultaneously
print(
    "search rate for both groups simultaneously:",
    ri.groupby("driver_gender").search_conducted.mean(),
)

# Male drivers are searched more than twice as often as female drivers.

# Calculate the search rate for each combination of gender and violation
print(
    "search rate for each combination of gender and violation:",
    ri.groupby(["driver_gender", "violation"]).search_conducted.mean(),
)

# For all types of violations, the search rate is higher for males than for females, disproving our hypothesis

###########################################
# 7) Does gender affect who is frisked during a search?
###########################################

# Count the 'search_type' values
print(ri.search_type.value_counts())

# Check if 'search_type' contains the string 'Protective Frisk'
ri["frisk"] = ri.search_type.str.contains("Protective Frisk", na=False)

# Check the data type of 'frisk'
print(ri.frisk.dtype)

# Take the sum of 'frisk'
print(ri.frisk.sum())

#  It looks like there were 303 drivers who were frisked.

# Create a DataFrame of stops in which a search was conducted
searched = ri[ri.search_conducted == True]

# Calculate the overall frisk rate by taking the mean of 'frisk'
print(searched.frisk.mean())

# Calculate the frisk rate for each gender
print(searched.groupby("driver_gender").frisk.mean())

# The frisk rate is higher for males than for females,
# though we can't conclude that this difference is caused by the driver's gender.

###########################################
# 8) Does time of day affect arrest rate?
###########################################

# Calculate the overall arrest rate
print(ri.is_arrested.mean())

# Save the hourly arrest rate
hourly_arrest_rate = ri.groupby(ri.index.hour).is_arrested.mean()

# Calculate the hourly arrest rate
print("hourly arrest rate:", hourly_arrest_rate)

# Import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

# Create a line plot of 'hourly_arrest_rate'
hourly_arrest_rate.plot()

# Add the xlabel, ylabel, and title
plt.xlabel("Hour")
plt.ylabel("Arrest Rate")
plt.title("Arrest Rate by Time of Day")

# Display the plot
plt.show()

# The arrest rate has a significant spike overnight, and then dips in the early morning hours.

###########################################
# 9) Are drug-related stops on the rise?
###########################################

# Calculate the annual rate of drug-related stops
print(ri.drugs_related_stop.resample("A").mean())

# Save the annual rate of drug-related stops
annual_drug_rate = ri.drugs_related_stop.resample("A").mean()

# Create a line plot of 'annual_drug_rate'
annual_drug_rate.plot()

# Display the plot
plt.show()

# The rate of drug-related stops nearly doubled over the course of 10 years.

###########################################
# 10) Hypothesis: The rate of drug-related stops increased significantly between 2005 and 2015 and the rate of vehicle searches was also increasing.
###########################################

# Calculate and save the annual search rate
annual_search_rate = ri.search_conducted.resample("A").mean()

# Concatenate 'annual_drug_rate' and 'annual_search_rate'
annual = pd.concat([annual_drug_rate, annual_search_rate], axis="columns")

# Create subplots from 'annual'
annual.plot(subplots=True)

# Display the subplots
plt.show()

# The rate of drug-related stops increased even though the search rate decreased, disproving our hypothesis.

###########################################
# 11) What violations are caught in each district?
###########################################

""" # Create a frequency table of districts and violations
print(pd.crosstab(ri.district, ri.violation))

# Save the frequency table as 'all_zones'
all_zones = pd.crosstab(ri.district, ri.violation)

# Select rows 'Zone K1' through 'Zone K3'
print(all_zones.loc["Zone K1":"Zone K3"])

# Save the smaller table as 'k_zones'
k_zones = all_zones.loc["Zone K1":"Zone K3"]

# Create a bar plot of 'k_zones'
k_zones.plot(kind="bar", stacked=True)

# Display the plot
plt.show() """

# The vast majority of traffic stops in Zone K1 are for speeding,
# and Zones K2 and K3 are remarkably similar to one another in terms of violations.

###########################################
# 12) How long might you be stopped for a violation?
###########################################

# Print the unique values in 'stop_duration'
print(ri.stop_duration.unique())

# Create a dictionary that maps strings to integers
mapping = {"0-15 Min": 8, "16-30 Min": 23, "30+ Min": 45}

# Convert the 'stop_duration' strings to integers using the 'mapping'
ri["stop_minutes"] = ri.stop_duration.map(mapping)

# Print the unique values in 'stop_minutes'
print(ri["stop_minutes"].unique())

# Calculate the mean 'stop_minutes' for each value in 'violation_raw'
print(ri.groupby("violation_raw").stop_minutes.mean())

# Save the resulting Series as 'stop_length'
stop_length = ri.groupby("violation_raw").stop_minutes.mean()

# Sort 'stop_length' by its values and create a horizontal bar plot
stop_length.sort_values().plot(kind="barh")

# Display the plot
plt.show()

###########################################
# 13) Exploring the weather dataset
###########################################

# Read 'weather.csv' into a DataFrame named 'weather'
weather = pd.read_csv("datasets/weather.csv")

# Describe the temperature columns
print(weather[["TMIN", "TAVG", "TMAX"]].describe())

# Create a box plot of the temperature columns
weather.plot(kind="box")

# Display the plot
plt.show()

# Create a 'TDIFF' column that represents temperature difference
weather["TDIFF"] = weather.TMAX - weather.TMIN

# Describe the 'TDIFF' column
print(weather.TDIFF.describe())

# Create a histogram with 20 bins to visualize 'TDIFF'
weather.TDIFF.plot(bins=20, kind="hist")

# Display the plot
plt.show()

###########################################
# 14) Categorizing the weather
###########################################

# Copy 'WT01' through 'WT22' to a new DataFrame
WT = weather.loc[:, "WT01":"WT22"]

# Calculate the sum of each row in 'WT'
weather["bad_conditions"] = WT.sum(axis="columns")

# Replace missing values in 'bad_conditions' with '0'
weather["bad_conditions"] = weather.bad_conditions.fillna(0).astype("int")

# Create a histogram to visualize 'bad_conditions'
weather.bad_conditions.plot(kind="hist")

# Display the plot
plt.show()

# Count the unique values in 'bad_conditions' and sort the index
print(weather.bad_conditions.value_counts().sort_index())

# Create a dictionary that maps integers to strings
mapping = {
    0: "good",
    1: "bad",
    2: "bad",
    3: "bad",
    4: "bad",
    5: "worse",
    6: "worse",
    7: "worse",
    8: "worse",
    9: "worse",
}

# Convert the 'bad_conditions' integers to strings using the 'mapping'
weather["rating"] = weather.bad_conditions.map(mapping)

# Count the unique values in 'rating'
print(weather.rating.value_counts())

# Specify the logical order of the weather ratings
cats = pd.CategoricalDtype(["good", "bad", "worse"], ordered=True)

# Change the data type of 'rating' to category
weather["rating"] = weather.rating.astype(cats)

# Examine the head of 'rating'
print(weather.rating.head())

###########################################
# 15) Merging datasets
###########################################

# Reset the index of 'ri'
ri.reset_index(inplace=True)

# Examine the head of 'ri'
print(ri.head())

# Create a DataFrame from the 'DATE' and 'rating' columns
weather_rating = weather[["DATE", "rating"]]

# Examine the head of 'weather_rating'
print(weather_rating.head())

# Examine the shape of 'ri'
print(ri.shape)

# Merge 'ri' and 'weather_rating' using a left join
ri_weather = pd.merge(
    left=ri, right=weather_rating, left_on="stop_date", right_on="DATE", how="left"
)

# Examine the shape of 'ri_weather'
print(ri_weather.shape)

# Set 'stop_datetime' as the index of 'ri_weather'
ri_weather.set_index("stop_datetime", inplace=True)

###########################################
# 16) Does weather affect the arrest rate?
###########################################

# Calculate the arrest rate for each 'violation' and 'rating'
print(ri_weather.groupby(["violation", "rating"]).is_arrested.mean())

# Save the output of the groupby operation from the last exercise
arrest_rate = ri_weather.groupby(["violation", "rating"]).is_arrested.mean()

# Print the 'arrest_rate' Series
print(arrest_rate)

# Print the arrest rate for moving violations in bad weather
print(arrest_rate.loc["Moving violation", "bad"])

# Print the arrest rates for speeding violations in all three weather conditions
print(arrest_rate.loc["Speeding"])

# Unstack the 'arrest_rate' Series into a DataFrame
print(arrest_rate.unstack())

# Create the same DataFrame using a pivot table
print(ri_weather.pivot_table(index="violation", columns="rating", values="is_arrested"))

# The arrest rate increases as the weather gets worse,
# and that trend persists across many of the violation types.
# This doesn't prove a causal link, but it's quite an interesting result!
