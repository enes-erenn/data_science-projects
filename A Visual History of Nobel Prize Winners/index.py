###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

# Loading in required libraries
import pandas as pd

# Reading in the Nobel Prize data
nobel = pd.read_csv("datasets/nobel.csv")

# Taking a look at the first several winners
nobel.head(6)

###########################################
# 2) The Most Nobel winner countries
###########################################

# Display the number of prizes won by the top 10 nationalities.
print(nobel["birth_country"].value_counts().head(10))

###########################################
# 3) USA dominance
###########################################

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Calculating the proportion of USA born winners per decade
nobel["usa_born_winner"] = nobel["birth_country"] == "United States of America"
nobel["decade"] = (np.floor(nobel["year"] / 10) * 10).astype(int) 
prop_usa_winners = nobel.groupby("decade", as_index=False)["usa_born_winner"].mean()

# Display the proportions of USA born winners per decade
print(prop_usa_winners)

# Setting the plotting theme
sns.set()

# Plotting USA born winners 
ax = sns.lineplot(x="decade", y="usa_born_winner", data=prop_usa_winners)
plt.show()

###########################################
# 4) Female Nobel Prize winners
###########################################

# Calculating the proportion of female laureates per decade
nobel["female_winner"] = nobel["sex"] == "Female"
prop_female_winners = nobel.groupby(["decade","category"], as_index=False)["female_winner"].mean()

# Plotting USA born winners 
ax = sns.relplot(x="decade", y="female_winner", kind="line", row="category", data=prop_female_winners, hue="category")
plt.show()

###########################################
# 5) The first woman to win the Nobel Prize
###########################################

# Picking out the first woman to win a Nobel Prize
nobel[nobel.sex == "Female"].nsmallest(1, "year")

###########################################
# 6) Repeat laureates
###########################################

# Selecting the laureates that have received 2 or more prizes.
print(nobel.groupby("full_name").filter(lambda name: len(name) >=2))

###########################################
# 7) How old are the Nobel Winners
###########################################

# Converting birth_date from String to datetime
nobel['birth_date'] = pd.to_datetime(nobel["birth_date"])

# Calculating the age of Nobel Prize winners
nobel['age']  = nobel['year'] - nobel['birth_date'].dt.year

# Plotting the age of Nobel Prize winners
sns.lmplot(x="year" ,y="age", data=nobel,lowess=True, 
           aspect=2, line_kws={'color' : 'black'})
plt.show()

###########################################
# 8) Age differences between prize categories
###########################################

# Same plot as above, but separate plots for each type of Nobel Prize
sns.lmplot(x="year" , y="age", row="category", data=nobel)
plt.show()

###########################################
# 9) Oldest and youngest winners
###########################################

# The oldest winner of a Nobel Prize as of 2016
nobel.nlargest(1 , "age")

# The youngest winner of a Nobel Prize as of 2016
nobel.nsmallest(1 , "age")
