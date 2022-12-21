###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

import pandas as pd

sales_df = pd.read_csv("./datasets/advertising_and_sales_clean.csv")

###########################################
# 2) Creating features
###########################################

import numpy as np

# Create X from the radio column's values
X = sales_df["radio"].values

# Create y from the sales column's values
y = sales_df["sales"].values

# Reshape X
X = X.reshape(-1, 1)

# Check the shape of the features and targets
print(X.shape, y.shape)

###########################################
# 3) Building a linear regression model
###########################################

# Import LinearRegression
from sklearn.linear_model import LinearRegression

# Create the model
reg = LinearRegression()

# Fit the model to the data
reg.fit(X, y)

# Make predictions
predictions = reg.predict(X)

print(predictions[:5])

###########################################
# 4) Visualizing a linear regression model
###########################################

# Import matplotlib.pyplot
import matplotlib.pyplot as plt

# Create scatter plot
plt.scatter(X, y, color="blue")

# Create line plot
plt.plot(X, predictions, color="red")
plt.xlabel("Radio Expenditure ($)")
plt.ylabel("Sales ($)")

# Display the plot
plt.show()

###########################################
# 5) Fit and predict for regression
###########################################

# Import the module
from sklearn.model_selection import train_test_split

# Create X and y arrays
X = sales_df.drop(["sales", "influencer"], axis=1).values
y = sales_df["sales"].values

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Instantiate the model
reg = LinearRegression()

# Fit the model to the data
reg.fit(X_train, y_train)

# Make predictions
y_pred = reg.predict(X_test)
print("Predictions: {}, Actual Values: {}".format(y_pred[:2], y_test[:2]))

###########################################
# 6) Regression performance
###########################################

# Import mean_squared_error
from sklearn.metrics import mean_squared_error

# Compute R-squared
r_squared = reg.score(X_test, y_test)

# Compute RMSE
rmse = mean_squared_error(y_test, y_pred, squared=False)

# Print the metrics
print(
    "R^2: {}".format(r_squared)
)  # The features explain 99.9% of the variance in sales values!
print("RMSE: {}".format(rmse))

###########################################
# 7) Cross-validation for R-squared
###########################################

# Import the necessary modules
from sklearn.model_selection import cross_val_score, KFold

# Create a KFold object
kf = KFold(n_splits=6, shuffle=True, random_state=5)

reg = LinearRegression()

# Compute 6-fold cross-validation scores
cv_scores = cross_val_score(reg, X, y, cv=kf)

# Print scores
print(cv_scores)

# Analyzing cross-validation metrics

# Print the mean
print("Mean: ", np.mean(cv_scores))

# Print the standard deviation
print("Std:", np.std(cv_scores))
# Print the 95% confidence interval
print("Conf. Int.: ", np.quantile(cv_scores, [0.025, 0.975]))

###########################################
# 8) Regularized regression: Ridge
###########################################

# Import Ridge
from sklearn.linear_model import Ridge

alphas = [0.1, 1.0, 10.0, 100.0, 1000.0, 10000.0]
ridge_scores = []
for alpha in alphas:

    # Create a Ridge regression model
    ridge = Ridge(alpha=alpha)

    # Fit the data
    ridge.fit(X_train, y_train)

    # Obtain R-squared
    score = ridge.score(X_test, y_test)
    ridge_scores.append(score)
print(ridge_scores)

###########################################
# 9) Lasso regression for feature importance
###########################################

# Import Lasso
from sklearn.linear_model import Lasso

# Instantiate a lasso regression model
lasso = Lasso(alpha=0.3)

# Fit the model to the data
lasso.fit(X, y)

# Compute and print the coefficients
lasso_coef = lasso.coef_
print(lasso_coef)
plt.bar(sales_df.drop(["sales", "influencer"], axis=1).columns, lasso_coef)
plt.xticks(rotation=45)
plt.show()

# Expenditure on TV advertising is the most important feature in the dataset to predict sales values!
