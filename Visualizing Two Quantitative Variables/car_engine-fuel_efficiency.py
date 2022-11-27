###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

import pandas as pd

mpg = pd.read_csv("datasets/mpg.csv")

###########################################
# 2) What is the relationship between the power of a car's engine ("horsepower") and its fuel efficiency ("mpg")? 
###########################################

# Import Matplotlib and Seaborn
import matplotlib.pyplot as plt
import seaborn as sns

# Create scatter plot of horsepower vs. mpg
sns.relplot(x="horsepower", y="mpg", 
            data=mpg, kind="scatter", 
            size="cylinders",
            hue="cylinders")

# Show plot
plt.show()

# Cars with higher horsepower tend to get a lower number of miles per gallon. They also tend to have a higher number of cylinders.

###########################################
# 3) How fast a car can accelerate ("acceleration") and its fuel efficiency ("mpg"). Do these properties vary by country of origin ("origin")?
###########################################

# Create a scatter plot of acceleration vs. mpg
sns.relplot(kind="scatter", x="acceleration",y="mpg",data=mpg,style="origin",hue="origin" )

# Show plot
plt.show()

# Cars from the USA tend to accelerate more quickly and get lower miles per gallon compared to cars from Europe and Japan.

###########################################
# 4) How has the average miles per gallon achieved by these cars changed over time?
###########################################

# Create line plot
sns.relplot(kind="line",data=mpg, x="model_year", y="mpg")

# Show plot
plt.show()

# The average miles per gallon has generally increased over time.

###########################################
# 5) Does this trend differ by country of origin?
###########################################

# Add markers and make each line have the same style
sns.relplot(x="model_year", y="horsepower", 
            data=mpg, kind="line", 
            ci=None, style="origin", 
            hue="origin",markers=True,dashes=False)

# Show plot
plt.show()

# Now that we've added subgroups, we can see that this downward trend in horsepower was more pronounced among cars from the USA.