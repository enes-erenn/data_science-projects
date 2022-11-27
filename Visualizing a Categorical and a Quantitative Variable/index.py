###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

import pandas as pd
import numpy as np

survey_data = pd.read_csv("datasets/young-survey.csv")
student_data = pd.read_csv("datasets/students.csv")

print(survey_data)

###########################################
# 2) Filtering the data
###########################################

survey_data["Age Category"] = survey_data["Age"]
survey_data["Age Category"] = np.where(survey_data["Age Category"] < 21, "Less than 21", "21+")

survey_data["Interested in Math"] = np.where(pd.to_numeric(survey_data["Mathematics"]) <= 3, False, True)

###########################################
# 3) How much do they use the internet each day?
###########################################

import seaborn as sns
import matplotlib.pyplot as plt

# Create count plot of internet usage
sns.catplot(y="Internet usage", data=survey_data,
            kind="count", col="Age Category")

# Show plot
plt.show()

# It looks like most young people use the internet for a few hours every day, regardless of their age.

###########################################
# 4) What percentage of young people report being interested in math, and does this vary based on gender? 
###########################################

# Create a bar plot of interest in math, separated by gender
sns.catplot(kind="bar", data=survey_data, x="Gender", y="Interested in Math")


# Show plot
plt.show()

#  This plot shows us that males report a much higher interest in math compared to females.

###########################################
# 5) Do students who report higher amounts of studying tend to get better final grades? 
###########################################

# List of categories from lowest to highest
category_order = ["<2 hours", 
                  "2 to 5 hours", 
                  "5 to 10 hours", 
                  ">10 hours"]

# Turn off the confidence intervals
sns.catplot(x="study_time", y="G3",
            data=student_data,
            kind="bar",
            order=category_order,ci=None)

# Show plot
plt.show()

# Students in our sample who studied more have a slightly higher average grade, but it's not a strong relationship.