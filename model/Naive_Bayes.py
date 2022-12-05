import pandas as pd

import re, string

from sklearn import metrics
from sklearn.metrics import accuracy_score, precision_score, classification_report
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

df_fake = pd.read_csv("../data/Fake.csv")
df_true = pd.read_csv("../data/True.csv")

df_fake["class"] = 0
df_true["class"] = 1

for i in range(23480, 23470, -1):
    df_fake.drop([i], axis=0, inplace=True)

for i in range(21416, 21406, -1):
    df_true.drop([i], axis=0, inplace=True)

df_merge = pd.concat([df_fake, df_true], axis=0)

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

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30)

vectorization = TfidfVectorizer()
xv_train = vectorization.fit_transform(x_train)

xv_test = vectorization.transform(x_test)


clf = MultinomialNB().fit(xv_train, y_train)

score = clf.score(xv_train, y_train)
print("Training score: ", score)

predicted = clf.predict(xv_test)

print("precision_score : ", precision_score(y_test, predicted))
print("Accuracy : ", accuracy_score(y_test, predicted))
#print('Matrice de confusion :\n', metrics.confusion_matrix(y_test, predicted))

print(classification_report(y_test, predicted))
from sklearn.metrics import confusion_matrix

matrix = confusion_matrix(y_true=y_test, y_pred=predicted)
print(matrix)
import seaborn as snNew
import matplotlib.pyplot as pltNew

DetaFrame_cm=pd.crosstab(y_test,predicted,rownames=['Actual'],colnames=['Predectide'])
snNew.heatmap(DetaFrame_cm, annot = True, fmt = '.0f')

pltNew.show()

