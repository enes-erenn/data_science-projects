###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

import pandas as pd

student_data = pd.read_csv("datasets/students.csv")

###########################################
# 2) How much time students study each week?
###########################################

import seaborn as sns
import matplotlib.pyplot as plt

# Create a scatter plot with seaborn relplot to see the relationship between variables
sns.relplot(x="absences", y="G3", 
            data=student_data,
            kind="scatter", 
            row="study_time")

# Show plot
plt.show()

###########################################
# 3) Does a student's first semester grade ("G1") tend to correlate with their final grade ("G3")?
###########################################

# Adjust further to add subplots based on family support
sns.relplot(x="G1", y="G3", 
            data=student_data,
            kind="scatter", 
            col="schoolsup",
            col_order=["yes", "no"],
            row="famsup",
            row_order=["yes","no"]
            )

# Show plot
plt.show()

# It looks like the first semester grade does correlate with the final grade, regardless of what kind of support the student received.