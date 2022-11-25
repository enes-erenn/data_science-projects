###########################################
# 1) Loading data into a dictionary
###########################################

# Create the years and durations lists
years = [2011,2012,2013,2014,2015,2016,2017,2018,2019,2020]
durations = [103, 101, 99, 100, 100, 95, 95, 96, 93, 90,]

# Create a dictionary with the two lists
movie_dict = {"years": years, "durations": durations}

# Print the dictionary
print(movie_dict)

###########################################
# 2) Creating a DataFrame from a dictionary
###########################################

# Import pandas
import pandas as pd

# Create a DataFrame from the dictionary
df = pd.DataFrame(movie_dict)

# Print the DataFrame
print(df)

###########################################
# 3) A visual inspection of our data
###########################################

# Given that the data is continuous and a single variable , a line plot would be a good choice, 
# with the dates represented along the x-axis and the average length in minutes along the y-axis. 
# This will allow us to easily spot any trends in movie durations. 
# There are many ways to visualize data in Python, 
# but matploblib.pyplot is one of the most common packages to do so.

# Import matplotlib
import matplotlib.pyplot as plt
plt.figure()

# Draw a line plot of years and durations
plt.plot(years, durations)

# Create a title
plt.title("Netflix Movie Durations 2011-2020")

# Show the plot
plt.show()

###########################################
# 4) Loading data from the csv file
###########################################

# What does this trend look like over a longer period of time?
# Is this explainable by something like the genre of entertainment?

# To answer these, Read in the CSV as a DataFrame
netflix_df = pd.read_csv("dataset/netflix.csv")

# Print the first five rows of the DataFrame
print(netflix_df.head())

###########################################
# 5) Filtering for movies!
###########################################

# Subset the DataFrame for type "Movie"
netflix_df_movies_only = netflix_df[netflix_df["type"] == "Movie"]

# Select only the columns of interest
netflix_movies_col_subset = netflix_df_movies_only[["title", "country", "genre", "release_year", "duration"]]

# Print the first five rows of the new DataFrame
print(netflix_movies_col_subset.head())

###########################################
# 6) Creating a scatter plot
###########################################

# Create a figure and increase the figure size
fig = plt.figure(figsize=(12,8))

# Create a scatter plot of duration versus year
plt.scatter(netflix_movies_col_subset["release_year"],netflix_movies_col_subset["duration"])

# Create a title
plt.title("Movie Duration by Year of Release")

# Show the plot
plt.show()

###########################################
# 7) Digging deeper
###########################################

#Upon further inspection, something else is going on. 
# Some of these films are under an hour long! Let's filter our DataFrame for movies with a duration under 60 minutes and look at the genres. 
# This might give us some insight into what is dragging down the average.

# Filter for durations shorter than 60 minutes
short_movies = netflix_movies_col_subset[netflix_movies_col_subset["duration"] < 60]

# Print the first 20 rows of short_movies
short_movies.iloc[0:20, :]

###########################################
# 8) Marking non-feature films
###########################################

# We could eliminate these rows from our DataFrame and plot the values again. 
# But another interesting way to explore the effect of these genres on our data would be to plot them, but mark them with a different color.

# Define an empty list
colors = []

# Iterate over rows of netflix_movies_col_subset
for key, value in netflix_movies_col_subset["genre"].items() :
    if value == "Children" :
        colors.append("red")
    elif value == "Documentaries" :
       colors.append("blue")
    elif value == "Stand-Up" :
        colors.append("green")
    else:
        colors.append("black")
        
# Inspect the first 10 values in your list        
print(colors[0:10])

###########################################
# 9) Plotting with color!
###########################################

# Set the figure style and initalize a new figure
plt.style.use('fivethirtyeight')
fig = plt.figure(figsize=(12,8))

# Create a scatter plot of duration versus release_year
plt.scatter(netflix_movies_col_subset["release_year"], netflix_movies_col_subset["duration"])

# Create a title and axis labels
plt.xlabel("Release year")
plt.ylabel("Duration (min)")
plt.title("Movie duration by year of release")

# Show the plot
plt.show()

###########################################
# 10) Conclusion
###########################################

# Well, as we suspected, non-typical genres such as children's movies and documentaries are all clustered around the bottom half of the plot. 
# But we can't know for certain until we perform additional analyses.

# Are we certain that movies are getting shorter?
are_movies_getting_shorter = "no"
