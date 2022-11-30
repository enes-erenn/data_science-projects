###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

# Read in dataset
import pandas as pd
apps_with_duplicates = pd.read_csv("datasets/play_store.csv")

# Drop duplicates from apps_with_duplicates
apps = apps_with_duplicates.drop_duplicates()

# Print the total number of apps
""" print("Total number of apps in the dataset = ", apps.count()) """

# Have a look at a random sample of 5 rows
""" 
print(apps.head())
print(apps["Price"].head())
print(apps["Installs"].head()) 
"""

###########################################
# 2) Data cleaning
###########################################

# List of characters to remove
chars_to_remove = ["+",",","$"]
# List of column names to clean
cols_to_clean = ["Installs","Price"]

# Loop for each column in cols_to_clean
for col in cols_to_clean:
    # Loop for each char in chars_to_remove
    for char in chars_to_remove:
        # Replace the character with an empty string
        apps[col] = apps[col].apply(lambda x: x.replace(char, ""))
        
apps["Installs"] = apps["Installs"].apply(lambda x: 0 if x == "Free" else x)
apps["Price"] = apps["Price"].apply(lambda x : 0 if x == "Everyone" else x)
apps["Type"] = apps["Type"].apply(lambda x : "Free" if x == 0 else x)

# Print a summary of the apps dataframe
""" print(apps.info()) """

###########################################
# 3) Correcting data types
###########################################

import numpy as np
# Convert Installs to float data type
apps["Installs"] = apps["Installs"].astype("float")
apps["Price"] = apps["Price"].astype("float")

# Checking dtypes of the apps dataframe
print(apps.info()) 

###########################################
# 4) Exploring the dataset
###########################################

import matplotlib.pyplot as plt
fig,ax= plt.subplots()

# Print the total number of unique categories
num_categories = len(apps["Category"].unique())
""" print("Number of categories = ", num_categories) """

# Count the number of apps in each "Category". 
num_apps_in_category = apps["Category"].value_counts()
""" print("Number of categories = ", num_apps_in_category) """

# Sort num_apps_in_category in descending order based on the count of apps in each category
sorted_num_apps_in_category = num_apps_in_category.sort_values(ascending = False)
""" print(sorted_num_apps_in_category) """

# Getting the first view with bar plot
plt.bar(num_apps_in_category.index, num_apps_in_category)
ax.set_xticklabels(num_apps_in_category.index,rotation=90)
""" plt.show() """

###########################################
# 5) Distribution of app ratings
###########################################

# Average rating of apps
avg_app_rating = apps["Rating"].mean()
""" print("Average app rating = ", avg_app_rating) """

bins = np.arange(1,5.1, 0.1)
""" print(bins) """

plt.hist(apps["Rating"], bins=bins)
plt.axvline(avg_app_rating, color="k", linestyle="dashed", linewidth=1)
""" plt.show() """

###########################################
# 6) Size and price of an app

# Does the size of an app affect its rating?
# Do users really care about system-heavy apps or do they prefer light-weighted apps?
# Does the price of an app affect its rating?
# Do users always prefer free apps over paid apps?
###########################################

import seaborn as sns
sns.set_style("darkgrid")

# Select rows where both "Rating" and "Size" values are present (ie. the two values are not null)
apps_with_size_and_rating_present = apps[apps["Rating"].notnull() & apps["Size"].notnull()]

# Subset for categories with at least 250 apps
large_categories = apps_with_size_and_rating_present.groupby("Category").filter(lambda x: len(x) >= 250)

# Plot size vs. rating
plt1 = sns.jointplot(x = large_categories["Size"], y = large_categories["Rating"])

# Select apps whose "Type" is "Paid"
paid_apps = apps_with_size_and_rating_present[apps_with_size_and_rating_present["Type"] == "Paid"]
# Plot price vs. rating
plt2 = sns.jointplot(x = paid_apps["Price"], y = paid_apps["Rating"])
""" plt.show() """

###########################################
# 7) Relation between app category and app price
###########################################

import matplotlib.pyplot as plt
fig, ax = plt.subplots()
fig.set_size_inches(15, 8)

# Select a few popular app categories
popular_app_cats = apps[apps.Category.isin(["GAME", "FAMILY", "PHOTOGRAPHY",
                                            "MEDICAL", "TOOLS", "FINANCE",
                                            "LIFESTYLE","BUSINESS"])]

# Examine the price trend by plotting Price vs Category
ax = sns.stripplot(x = popular_app_cats["Price"], y = popular_app_cats["Category"], jitter=True, linewidth=1)
ax.set_title("App pricing trend across categories")

# Apps whose Price is greater than 200
apps_above_200 = apps[apps["Price"] > 200]
apps_above_200[["Category", "App", "Price"]]
""" plt.show() """

###########################################
# 8) Filter out "junk" apps
###########################################

# Select apps priced below $100
apps_under_100 = popular_app_cats[popular_app_cats["Price"] < 100]

fig, ax = plt.subplots()
fig.set_size_inches(15, 8)

# Examine price vs category with the authentic apps (apps_under_100)
ax = sns.stripplot(x = "Price" ,y = "Category", data = apps_under_100 ,jitter = True, linewidth = 1)
ax.set_title("App pricing trend across categories after filtering for junk apps")
""" plt.show() """

###########################################
# 9) Popularity of paid apps vs free apps
###########################################
print(apps["Installs"])
sns.catplot(kind="box", data=apps, x="Type", y="Installs")
plt.yscale("log")

###########################################
# 10) Sentiment analysis of user reviews
###########################################

# Load user_reviews.csv
reviews_df = pd.read_csv("datasets/user_reviews.csv")

# Join the two dataframes
merged_df = apps.merge(reviews_df)

# Drop NA values from Sentiment and Review columns
merged_df = merged_df.dropna(subset = ['Sentiment', 'Review'])

sns.set_style('ticks')
fig, ax = plt.subplots()
fig.set_size_inches(11, 8)

# User review sentiment polarity for paid vs. free apps
ax = sns.boxplot(x = "Type", y = "Sentiment_Polarity", data = merged_df)
ax.set_title('Sentiment Polarity Distribution')
plt.show()