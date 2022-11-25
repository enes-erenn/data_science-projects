#################################################################
# 1) Loading data with pandas
#################################################################
import pandas as pd

# Reading csv files with pandas
pulls_one = pd.read_csv("datasets/pulls_2011-2013.csv")
pulls_two = pd.read_csv("datasets/pulls_2014-2018.csv")
pull_files = pd.read_csv("datasets/pull_files.csv")

# The first two files include the information about the PR (Pull Request) id, user, and the PR date
# The last file includes PR's id and the file name

#################################################################
# 2) Preparing and cleaning the data
#################################################################

# Append pulls_one to pulls_two (Vertical Merge)
pulls = pulls_one.append(pulls_two, ignore_index=True)

# Convert the date for the pulls object
pulls['date'] = pd.to_datetime(pulls['date'], utc=True)
#  2013-12-31T23:10:55Z to 2013-12-31 23:10:55+00:00

#################################################################
# 3) Merging the DataFrames
#################################################################

data = pulls.merge(pull_files, on="pid")
# We added the file name column to the pulls DataFrame, and now all in one

print(data)

#################################################################
# 4) Detecting the project's state
#################################################################

# Create a column that will store the year
data['year'] = data["date"].dt.year

print(data)

# Group by the month and year and count the pull requests
counts = data.groupby(["year"])["pid"].count()
print(counts)

# Plot the results
import matplotlib.pyplot as plt

counts.plot(kind='bar', figsize = (12,4))
plt.xlabel('Years')
plt.ylabel('Contribution')
plt.title("Contribution with Years")
plt.show()

# As we can see from the plot, the given contributions to the project are decreasing almost every year.

#################################################################
# 5) Contributor's loyalty
#################################################################

# Group by the submitter
by_user = data.groupby("user")["pid"].count()
print(by_user)

# Plot the histogram
by_user.hist()
plt.xlabel('User Count')
plt.ylabel('Commit Count')
plt.title("Contributor's Commit Counts")
plt.show()

# As We can see on the histogram, just a little of amount contributors are making much progress on the project

#################################################################
# 6) What files were changed in the last ten pull requests?
#################################################################

# Identify the last 10 pull requests
last_10 = pulls.sort_values(by = 'date').tail(10)

# Join the two data sets
joined_pr =pull_files.merge(last_10, on="pid")

# Identify the unique files
files = set(joined_pr["file"])

# Print the results
print(joined_pr)

#################################################################
# 7) Who made the most pull requests to a given file?
#################################################################

# This is the file we are interested in:
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Identify the commits that changed the file
file_pr = data[data['file'] == file]

# Count the number of changes made by each developer
author_counts = file_pr.groupby('user')["pid","file"].count()
print(author_counts)

# Print the top 3 developers
top_3 = author_counts.nlargest(3, 'file')
print(top_3)

#################################################################
# 8) Who made the last ten pull requests on a given file?
#################################################################

file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Select the pull requests that changed the target file
file_pr = pull_files[pull_files['file'] == file]

# Merge the obtained results with the pulls DataFrame
joined_pr = file_pr.merge(pulls, on="pid")

# Find the users of the last 10 most recent pull requests
users_last_10 = set(joined_pr.nlargest(10, "date")["user"])

# Printing the results
print(users_last_10)

#################################################################
# 9) The pull requests of two special developers
#################################################################

# The developers we are interested in
authors = ['xeno-by', 'soc']

# Get all the developers' pull requests
by_author = pulls[pulls["user"].isin(authors)]
print(by_author)

# Count the number of pull requests submitted each year
counts = by_author.groupby([by_author['user'], by_author['date'].dt.year]).agg({'pid': 'count'}).reset_index()
print(counts)

# Convert the table to a wide format
counts_wide = counts.pivot_table(index='date', columns='user', values='pid', fill_value=0)
print(counts_wide)

# Plot the results
counts_wide.plot(kind='bar')
plt.show()

#################################################################
# 9) Visualizing the contributions of each developer
#################################################################

#In our case, we want to see which of our two developers of interest have the most experience with the code in a given file. 
# We will measure experience by the number of pull requests submitted that affect that file and how recent those pull requests were submitted.

authors = ['xeno-by', 'soc']
file = 'src/compiler/scala/reflect/reify/phases/Calculate.scala'

# Select the pull requests submitted by the authors, from the `data` DataFrame
by_author =data[data['user'].isin(authors)]

# Select the pull requests that affect the file
by_file =by_author[by_author['file'] == file]

# Group and count the number of PRs done by each user each year
grouped = by_file.groupby(['user', by_file['date'].dt.year]).count()['pid'].reset_index()
print(grouped)
# Transform the data into a wide format
by_file_wide = by_file_wide = grouped.pivot_table(index='date', columns='user', values='pid', fill_value=0)

# Plot the results
by_file_wide.plot(kind='bar')
plt.show()