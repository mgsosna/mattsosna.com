import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import train_test_split

is_spam = np.concatenate(
    [
        np.random.choice([0, 1], p=[0.9, 0.1], size=200),
        np.random.choice([0, 1], p=[0.8, 0.2], size=200),
        np.random.choice([0, 1], p=[0.6, 0.4], size=200),
        np.random.choice([0, 1], p=[0.4, 0.6], size=200),
        np.random.choice([0, 1], p=[0.1, 0.9], size=200),
    ]
)

feature_1 = range(1000) + np.random.normal(0, 1, 1000)
feature_2 = range(1000) + np.random.normal(0, 0.1, 1000)

df = pd.DataFrame(
    {
        'is_spam': is_spam,
        'feature_1': feature_1,
        'feature_2': feature_2,
    }
)

#########################################################
X = df[['feature_1', 'feature_2']]
y = df['is_spam']

X_train, X_test, y_train, y_test = train_test_split(X, y)

mod = LogisticRegression()
mod.fit(X_train, y_train)

############################################################
preds = mod.predict_proba(X_test)[:,1]
precision, recall, thresholds = precision_recall_curve(y_test, preds)

df = pd.DataFrame(
    {
        'precision': precision[:-1],
        'recall': recall[:-1],
        'threshold': thresholds,
    }
)

print(df)
