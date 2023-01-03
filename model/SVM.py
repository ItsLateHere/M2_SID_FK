import pandas as pd
from io import StringIO
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.svm import SVC
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer


class SVM:
    filename = "C:\\Users\\Abderrahim\\PycharmProjects\\M2_SID_FK\\model\\SVM.sav"
    def wordopt(self, text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W", " ", text)
        text = re.sub('https?://\S+|www\.\S+', '', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    def __init__(self):
        self.clf = pickle.load(open(self.filename, 'rb'))

    def train(self):
        df_true = pd.read_csv("data/True.csv")
        df_fake = pd.read_csv("data/Fake.csv")

        # df_test = pd.read_csv("../data/test.csv")

        df_fake["class"] = 0
        df_true["class"] = 1
        # df_test["class"] = 0

        for i in range(23480, 23470, -1):
            df_fake.drop([i], axis=0, inplace=True)

        for i in range(21416, 21406, -1):
            df_true.drop([i], axis=0, inplace=True)

        df_merge = pd.concat([df_fake, df_true], axis=0)
        df_merge.head(10)

        df = df_merge.drop(["title", "subject", "date"], axis=1)

        df = df.sample(frac=1)

        df.reset_index(inplace=True)
        # df_test.reset_index(inplace=True)
        df.drop(["index"], axis=1, inplace=True)
        # df_test.drop(["index"], axis=1, inplace=True)

        df["text"] = df["text"].apply(self.wordopt)
        x = df["text"]
        y = df["class"]

        # df_test["text"] = df_test["text"].apply(self.wordopt)
        # test_x = df_test["text"]
        # test_y = df_test["class"]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.40)

        # xv_test = vectorization.transform(x_test)
        # vtest_x = vectorization.transform(test_x)

        clf = Pipeline([('tfidf', TfidfVectorizer(),),
                        ('svm', SVC(kernel='linear', C=1.0, probability=True))])
        clf.fit(x_train, y_train)
        predictions = clf.predict(x_test)
        cm = confusion_matrix(y_test, predictions, labels=clf.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels = clf.classes_)
        disp.plot()
        plt.show()
        self.clf = clf
        pickle.dump(clf, open(self.filename, 'w+b'))

    def predict(self, input_string):
        DATA=StringIO("text\n"+input_string)
        df=pd.read_csv(DATA,sep=";")
        df["text"] = df["text"].apply(self.wordopt)
        vectorization = TfidfVectorizer()
        #input_v = vectorization.fit_transform(df["text"])

        out = self.clf.predict_proba(df["text"])
        print(out)
        if (out[0][0] > out[0][1]):
            return "is false with " + str(out[0][0]) + " certainty."
        else:
            return "is true with " + str(out[0][1]) + " certainty."

# print(clf.predict_proba(xv_test))
# pred = clf.predict(xv_test)
# clf.score(xv_test, y_test)

# print(classification_report(y_test, pred))

# scores = cross_val_score(clf, xv_test, y_test, cv=10, n_jobs=10)
# print(scores)


# print(clf.predict_proba(vtest_x))
# pred_test = clf.predict(vtest_x)

# print(classification_report(test_y, pred_test))

# pickle.dump(clf, open(filename, 'w+b'))
