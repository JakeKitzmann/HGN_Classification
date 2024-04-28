import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from IPython.display import display
import pandas as pd
import seaborn as sns
from sklearn import (datasets, metrics,
                     model_selection as skms,
                     naive_bayes, neighbors)
test_data = pd.read_csv("Server/Classification/test.csv")
test_data.head()
import matplotlib.pyplot as plt
# Helper function for data distribution
# Visualize the proportion of borrowers
print(test_data.columns)
def show_test_distrib(data):
  count = ""
  if isinstance(data, pd.DataFrame):
      count = data["Intoxication"].value_counts()
  else:
      count = data.value_counts()


  count.plot(kind = 'pie', explode = [0, 0.1], 

              figsize = (6, 6), autopct = '%1.1f%%', shadow = True)
  plt.ylabel("EyeData: Sober Vs. Drunk")
  plt.legend(["Sober Data", "Drunk Data"])
  plt.show()


# Visualize the proportion of borrowers
show_test_distrib(test_data)

features = test_data[['left_vector', 'right_vector']]
target = test_data['Intoxication']

# Split the data into a training set and a test set
(train_ftrs, test_ftrs, train_tgt, test_tgt) = skms.train_test_split(features, target, test_size=.25)

# Display the first few rows of the test features and targets
test_data['Intoxication'] = test_data['Intoxication'].map({1: 'drunk', 0: 'sober'})
display(pd.concat([test_data.head(3),
                   test_data.tail(3)]))
kNN_model = neighbors.KNeighborsClassifier(n_neighbors=3)
kNN_fit = kNN_model.fit(train_ftrs, train_tgt)
kNN_predictions = kNN_fit.predict(test_ftrs)
kNN_score = metrics.accuracy_score(test_tgt, kNN_predictions)
print(f'kNN model accuracy: {kNN_score:0.2f}')
new_data = pd.read_csv("Server/Classification/new.csv")

# Assuming new_data is a DataFrame containing the new samples to classify
new_features = new_data[['left_vector', 'right_vector']]
# Predict using the trained model
new_predictions = kNN_model.predict(new_features)

# Optionally, convert predictions back to readable labels if necessary
new_data['Intoxication_Prediction'] = new_predictions
new_data['Intoxication_Prediction'] = new_data['Intoxication_Prediction'].map({1: 'drunk', 0: 'sober'})

# Display the predictions
print(new_data[['left_vector', 'right_vector','Intoxication_Prediction']])
show_test_distrib(new_data)
def classify_person(predictions, threshold=0.5):
    # Calculate the percentage of predictions that are 'Intoxicated'
    percentage_intoxicated = np.mean(predictions == 1)  # assuming '1' stands for 'Intoxicated'
    
    # Compare against the threshold
    if percentage_intoxicated > threshold:
        return 'Intoxicated'
    else:
        return 'Sober'

# Example usage:
overall_classification = classify_person(new_data, threshold=0.5)
print(f'Overall classification: {overall_classification}')