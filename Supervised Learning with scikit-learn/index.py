###########################################
# 1) Loading the csv data with pandas pkg.
###########################################

import pandas as pd

churn_df = pd.read_csv("./datasets/telecom_churn_clean.csv")

###########################################
# 2) Classification
###########################################

# Import KNeighborsClassifier
from sklearn.neighbors import KNeighborsClassifier

# Create arrays for the features and the target variable
y = churn_df["churn"].values  # Consist of results (labels)
X = churn_df[["account_length", "customer_service_calls"]].values  # Consist of features

# Create a KNN classifier with 6 neighbors
knn = KNeighborsClassifier(n_neighbors=6)

# Fit the classifier to the data
knn.fit(X, y)

###########################################
# 3) Prediction
###########################################

import numpy as np

# Random "feature" values to predict the result (label)
X_new = np.array([[30.0, 17.5], [107.0, 24.1], [213.0, 10.9]])

# Predict the labels for the X_new
y_pred = knn.predict(X_new)

# Print the predictions for X_new
print("Predictions: {}".format(y_pred))  # Result: 0,1,0

###########################################
# 4) Measuring model performance
###########################################

# Import the module
from sklearn.model_selection import train_test_split

X = churn_df.drop(
    "churn", axis=1
).values  # Dropping the column of labels and selecting only features
y = churn_df["churn"].values  # Selecting label

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

knn = KNeighborsClassifier(n_neighbors=5)

# Fit the classifier to the training data
knn.fit(X_train, y_train)

# Print the accuracy
print("The model's accuracy for the test data: ", knn.score(X_test, y_test))

###########################################
# 5) Overfitting and underfitting
###########################################

# Create neighbors
neighbors = np.arange(1, 13)
train_accuracies = {}
test_accuracies = {}

# Training the model according to the different KNN sizes through the loop
for neighbor in neighbors:

    # Set up a KNN Classifier
    knn = KNeighborsClassifier(n_neighbors=neighbor)

    # Fit the model
    knn.fit(X_train, y_train)

    # Compute accuracy
    train_accuracies[neighbor] = knn.score(X_train, y_train)
    test_accuracies[neighbor] = knn.score(X_test, y_test)

print(neighbors, "\n", train_accuracies, "\n", test_accuracies)

###########################################
# 6) Visualizing model complexity
###########################################

import matplotlib.pyplot as plt

# Add a title
plt.title("KNN: Varying Number of Neighbors")


# Plot test accuracies
plt.plot(neighbors, test_accuracies.values(), label="Testing Accuracy")
# Plot training accuracies
plt.plot(neighbors, train_accuracies.values(), label="Training Accuracy")

plt.legend()
plt.xlabel("Number of Neighbors")
plt.ylabel("Accuracy")

# Display the plot
plt.show()

# For the test set, accuracy peaks with 9 neighbors,
