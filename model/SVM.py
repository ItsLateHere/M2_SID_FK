import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer

df_fake = pd.read_csv("../data/Fake.csv")
df_true = pd.read_csv("../data/True.csv")

df_fake["class"] = 0
df_true["class"] = 1

for i in range(23480, 23470, -1):
    df_fake.drop([i], axis=0, inplace=True)

for i in range(21416, 21406, -1):
    df_true.drop([i], axis=0, inplace=True)

df_merge = pd.concat([df_fake, df_true], axis=0)
df_merge.head(10)

df = df_merge.drop(["title", "subject", "date"], axis=1)

df = df.sample(frac=1)

df.reset_index(inplace=True)
df.drop(["index"], axis=1, inplace=True)


def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W", " ", text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text


df["text"] = df["text"].apply(wordopt)

x = df["text"]
y = df["class"]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.40)

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)
xv_test = vectorization.transform(x_test)

filename = "SVM.sav"
# clf =pickle.load(open(filename, 'rb'))
clf = SVC(kernel='linear', C=1.0, probability=True)
clf.fit(xv_train, y_train)
print(clf.predict_proba(xv_test))
pred = clf.predict(xv_test)
clf.score(xv_test, y_test)

print(classification_report(y_test, pred))

pickle.dump(clf, open(filename, 'wb'))
