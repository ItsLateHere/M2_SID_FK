import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.linear_model import SGDClassifier

from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report
from sklearn.metrics import confusion_matrix

import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text)
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)
    return text

df_fake = pd.read_csv("../data/Fake.csv")
df_true = pd.read_csv("../data//True.csv")

df_fake["class"] = 0
df_true["class"] = 1
df_merge = pd.concat([df_fake, df_true], axis =0 )
# df_merge.head(10)
df = df_merge.drop(["title","date"], axis = 1)
# df.head(10)
df2 = pd.read_csv("../data/another_train_set.csv")
df = pd.concat([df,df2],axis=0)
# df.shape
df = df.sample(frac = 1)
# df.head(10)
# df.columns
df["text"] = df["text"].apply(wordopt)
df.reset_index(inplace = True)
df.drop(["index"], axis = 1, inplace = True)
x = df["text"]
y = df["class"]
vectorization = TfidfVectorizer()
xv = vectorization.fit_transform(x)

sgdc = SGDClassifier(max_iter=1000, tol=0.01)
sgdc.fit(xv, y)
score = sgdc.score(xv, y)
print("Training score: ", score)

scores = cross_val_score(sgdc, xv, y, cv=5)
scores

df_test = pd.read_csv("../data/test.csv")
df_test = df_test.sample(frac = 1)
# df_test.shape

df_test["text"] = df_test["text"].apply(wordopt)
df_test.reset_index(inplace = True)
df_test = df_test.drop(["index"], axis = 1)

xtest=df_test["text"]
ytest= df_test["class"]
xvtest = vectorization.transform(xtest)

ypred = sgdc.predict(xvtest)
score = sgdc.score(xvtest, ytest)
print("Test score: ", score)

cm = confusion_matrix(ytest, ypred)
cm=pd.crosstab(ytest,ypred,rownames=['Actual'],colnames=['Predectide'])
sns.heatmap(cm,annot=True,fmt='.2f')
print(classification_report(ytest, ypred))