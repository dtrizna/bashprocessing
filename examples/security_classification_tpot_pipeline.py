import numpy as np

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import RFE
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.utils import shuffle
from sklearn.metrics import accuracy_score, zero_one_loss, confusion_matrix
from sklearn.model_selection import cross_validate
from imblearn.over_sampling import RandomOverSampler

import sys
from os import path 

RANDOM = 1620
np.random.seed(RANDOM)

scriptpath = ".."
sys.path.append(path.abspath(scriptpath))

from bashprocessing import Parser

with open('../data/nl2bash.cm') as f1:
    benign = f1.readlines()

with open('../data/malicious.cm') as f2:
    malicious = f2.readlines()

Xcm, y = shuffle(benign + malicious, \
                [0] * len(benign) + [1] * len(malicious), \
                random_state=RANDOM)

print("[!] Preprocessing of dataset...")
p = Parser(verbose=True)
cntr, corpus = p.tokenize(Xcm)
X = p.encode(mode="onehot", top_tokens=200)
y = np.array(y).astype(int)

print("[!] Dataset oversampling...")
ros = RandomOverSampler(sampling_strategy='minority', random_state=RANDOM)
Xresampled, y_resampled = ros.fit_resample(X, y)

# Average CV score on the training set was: 0.9975442720183271
exported_pipeline = make_pipeline(
    RFE(estimator=ExtraTreesClassifier(criterion="entropy", max_features=0.05, n_estimators=100), step=0.25),
    MLPClassifier(alpha=0.0001, learning_rate_init=0.001)
)

print("[!] Training with cross validation...")
scores = cross_validate(exported_pipeline, X, y, cv=10,\
                        scoring=('accuracy','f1', 'precision', 'recall'),
                        return_train_score=True)

import pdb;pdb.set_trace()

print("[!] Training RandomOverSampler()...")
#exported_pipeline.fit(X_train_resampled, y_train_resampled)
#results_tr = exported_pipeline.predict(X_train)
#results_te = exported_pipeline.predict(X_test)
