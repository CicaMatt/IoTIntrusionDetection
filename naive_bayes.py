import time
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn import metrics, naive_bayes
from utils.data_setup import DataSetup
from utils.metrics import Metrics

# Data retrieving
data = DataSetup.data_setup(5)

# Removing all duplicates
data = data.drop_duplicates()

# Shuffling rows of dataframe, done due to consecutive dataset entry being similar to each other
print("Shuffling data")
sampler = np.random.permutation(len(data))
data = data.take(sampler)

# dummy encode labels, store separately
# Parallel dataset is created to be used to check later the belonging to a certain class
# si crea un ulteriore dataset dove si associa 0 o 1 in relazione all'appartenza ad un csv, in base al prefisso 'type'
# ad ogni label viene aggiunto all'inizio 'type'
print("Creating a dataset of indicative labels relative to the belonging CSV")
labels_full = pd.get_dummies(data['type'], prefix='type')
# print(labels_full.head())

# drop labels from training dataset
# si eliminano le label dal dataset di training
print("Deleting labels from the training dataset")
data = data.drop(columns='type')

# Feature Scaling - Z-Score Normalization
print("Scaling training set features")
data = StandardScaler().fit_transform(data)
# data = MinMaxScaler().fit_transform(data)
data = pd.DataFrame(data)

# Feature Selection
# data = VarianceThreshold().fit_transform(data)
# data = SelectKBest(chi2, k=100).fit_transform(data, labels_full)
# data = pd.DataFrame(data)

# Feature Extraction
# print("Feature Extraction")
# data = PCA(80).fit_transform(data)
# data = pd.DataFrame(data)

# .values trasforma i dati in formato tabellare DataFrame in un array multidimensionale NumPy
# training data for the neural net
training_data = data.values

# labels for training
labels = labels_full.values


# VALIDATION

# Train/Test split - 80/20
print("Validation - 80/20 split")
x_training, x_testing, y_training, y_testing = train_test_split(training_data, labels, test_size=0.20, random_state=42)
y_training = np.argmax(y_training, axis=1)


# model = naive_bayes.BernoulliNB()
model = naive_bayes.GaussianNB()

start = time.time()
model.fit(x_training, y_training)
print("\nTraining time: " + str(time.time() - start)[0:7] + "s")

# PREDICTION
# predict genera le predizioni in output per i campioni in input
prediction = model.predict(x_testing)
print("Total time: " + str(time.time() - start)[0:7] + "s\n")


# METRICS
Metrics.metrics(y_testing, prediction, flag=1, name='Naive Bayes')
