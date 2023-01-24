import os
import re
import pandas as pd
from io import StringIO
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle
from sklearn.calibration import CalibratedClassifierCV
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectPercentile, chi2
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report
from sklearn.svm import LinearSVC, SVC
from sklearn.naive_bayes import GaussianNB, BernoulliNB, MultinomialNB
from sklearn.linear_model import LogisticRegression
import string
from sklearn.feature_extraction.text import TfidfVectorizer


class SVM:
    #filename = "C:\\Users\\Abderrahim\\PycharmProjects\\M2_SID_FK\\model\\SVM.sav"
    filename = os.path.dirname(os.path.realpath(__file__))+"\\SVM.sav"
    def wordopt(self, text):
        text = text.lower()
        text = re.sub('\[.*?\]', '', text)
        text = re.sub("\\W", " ", text)
        text = re.sub('(?P<url>https?://[^\s]+)', 'URL', text)
        text = re.sub('<.*?>+', '', text)
        text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
        text = re.sub('\n', '', text)
        text = re.sub('\w*\d\w*', '', text)
        return text

    def __init__(self):
        self.clf = pickle.load(open(self.filename, 'rb'))

    def train(self):
        # df_true = pd.read_csv("data/True.csv")
        # df_fake = pd.read_csv("data/Fake.csv")
        #df = pd.read_csv("../data/data_set_svm.csv", delimiter=";")
        df=pd.read_csv("../data/data_set_tweet_user_features.csv", delimiter=';')
        #tester NB
        #tester SGD
        #tester selection de features (ACP)
        df = df.sample(frac=1)
        df["tweet__text"] =df["tweet__text"].apply(self.wordopt)
        x=df["tweet__text"]
        y=df["tweet__fake"]
        #df_t = pd.read_csv("../data/testset_svm.csv", delimiter=";")
        #df=df.drop(["d"], axis=1)
        #df_t=df_t.drop(["d"], axis=1)
        #df_test = df_t[['tweet__contains_spelling_mistake', 'tweet__nr_of_sentiment_words', 'tweet__possibly_sensitive', 'tweet__truncated', 'tweet__is_ww_trending_topic', 'tweet__subjectivity_score', 'tweet__sentiment_score', 'tweet__nr_of_sentences', 'tweet__nr_of_unicode_emojis', 'tweet__contains_unicode_emojis', 'tweet__contains_face_positive_emojis', 'tweet__contains_face_negative_emojis', 'tweet__contains_face_neutral_emojis', 'tweet__nr_of_ascii_emojis', 'tweet__contains_ascii_emojis', 'tweet__has_place', 'tweet__has_location', 'tweet__nr_of_words', 'tweet__ratio_adjectives', 'tweet__ratio_nouns', 'tweet__ratio_verbs', 'tweet__contains_named_entities', 'tweet__contains_pronouns', 'tweet__avg_word_length', 'tweet__nr_of_slang_words', 'tweet__ratio_uppercase_letters', 'tweet__ratio_capitalized_words', 'tweet__ratio_all_capitalized_words', 'tweet__nr_of_tokens', 'tweet__ratio_tokens_before_after_prepro', 'tweet__text_length', 'tweet__percent_of_text_used', 'tweet__ratio_words_tokens', 'tweet__nr_of_urls', 'tweet__contains_urls', 'tweet__avg_url_length', 'tweet__contains_stock_symbol', 'tweet__nr_of_punctuations', 'tweet__contains_punctuation', 'tweet__ratio_punctuation_tokens', 'tweet__nr_of_exclamation_marks', 'tweet__contains_exclamation_mark', 'tweet__multiple_exclamation_marks', 'tweet__nr_of_question_marks', 'tweet__contains_question_mark', 'tweet__multiple_question_marks', 'tweet__contains_character_repetitions', 'tweet__contains_slang', 'tweet__is_all_uppercase', 'tweet__contains_uppercase_text', 'tweet__nr_of_medias', 'tweet__contains_media', 'tweet__nr_of_user_mentions', 'tweet__contains_user_mention', 'tweet__nr_of_hashtags', 'tweet__contains_hashtags', 'tweet__nr_of_popular_hashtag', 'tweet__contains_popular_hashtag', 'tweet__additional_preprocessed_is_empty', 'tweet__contains_sentiment', 'tweet__ratio_stopwords', 'tweet__day_of_week', 'tweet__day_of_month', 'tweet__month_of_year', 'tweet__am_pm', 'tweet__hour_of_day', 'tweet__quarter_of_year', 'tweet__tf_idf_sum', 'tweet__tf_idf_sum_grouped_by_user', 'tweet__bigram_tf_idf_sum', 'user__at_least_30_follower', 'user__avg_hashtags_per_tweet', 'user__avg_post_time', 'user__avg_time_between_tweets', 'user__avg_urls_per_tweet', 'user__avg_user_mention_per_tweet', 'user__created_days_ago', 'user__created_hour_of_day', 'user__default_profile', 'user__desc_contains_hashtags', 'user__desc_contains_url', 'user__desc_contains_user_mention', 'user__desc_length', 'user__favourites_count', 'user__favourites_per_follower', 'user__followers_count', 'user__friends_count', 'user__friends_per_favourite', 'user__friends_per_follower', 'user__geo_enabled', 'user__has_country', 'user__has_desc', 'user__has_extended_profile', 'user__has_favourites', 'user__has_friends', 'user__has_list', 'user__has_location', 'user__has_no_desc_and_loc', 'user__has_physical_address', 'user__has_profile_background_image', 'user__has_tweets_in_different_lang', 'user__is_following_more_than_100', 'user__is_translator_type_regular', 'user__listed_count', 'user__max_time_between_tweets', 'user__median_time_between_tweets', 'user__min_time_between_tweets', 'user__nr_of_quotes', 'user__nr_of_quotes_per_tweet', 'user__nr_of_replies', 'user__nr_of_replies_per_tweet', 'user__nr_of_retweets', 'user__nr_of_retweets_per_tweet', 'user__percent_with_hashtag', 'user__percent_with_url', 'user__percent_with_user_mention', 'user__profile_background_tile', 'user__profile_use_background_image', 'user__statuses_count', 'user__tweets_in_different_lang', 'user__tweets_per_day', 'user__tweets_per_month', 'user__tweets_per_week', 'user__url_length', 'user__url_tld_type', 'user__uses_quotes', 'user__uses_replies', 'user__uses_retweets', 'user__verified', 'tweet__contains_number', 'tweet__contains_quote', 'tweet__nr_pos_sentiment_words', 'tweet__nr_neg_sentiment_words', 'tweet__ratio_pos_sentiment_words', 'tweet__ratio_neg_sentiment_words', 'tweet__contains_pos_trigram_O_V_P', 'tweet__contains_pos_trigram_^_V_D', 'tweet__contains_pos_trigram_^_V_P', 'tweet__contains_pos_trigram_,_A_N', 'tweet__contains_pos_trigram_P_N_P', 'tweet__contains_pos_trigram_,_N_,', 'tweet__contains_pos_trigram_V_P_V', 'tweet__contains_pos_trigram_N_N_V', 'tweet__contains_pos_trigram_,_G_N', 'tweet__contains_pos_trigram_O_,_G', 'tweet__contains_pos_trigram_N_,_^', 'tweet__contains_pos_trigram_,_D_N', 'tweet__contains_pos_trigram_V_R_V', 'tweet__contains_pos_trigram_P_D_A', 'tweet__contains_pos_trigram_V_N_P', 'tweet__contains_pos_trigram_V_N_N', 'tweet__contains_pos_trigram_N_V_D', 'tweet__contains_pos_trigram_A_N_P', 'tweet__contains_pos_trigram_N_U_U', 'tweet__contains_pos_trigram_A_N_,', 'tweet__contains_pos_trigram_N_N_,', 'tweet__contains_pos_trigram_N_P_D', 'tweet__contains_pos_trigram_P_N_N', 'tweet__contains_pos_trigram_P_^_U', 'tweet__contains_pos_trigram_,_^_V', 'tweet__contains_pos_trigram_V_D_N', 'tweet__contains_pos_trigram_^_^_,', 'tweet__contains_pos_trigram_O_V_V', 'tweet__contains_pos_trigram_P_V_^', 'tweet__contains_pos_trigram_D_N_V', 'tweet__contains_pos_trigram_P_V_D', 'tweet__contains_pos_trigram_N_N_P', 'tweet__contains_pos_trigram_V_P_D', 'tweet__contains_pos_trigram_N_P_A', 'tweet__contains_pos_trigram_P_^_N', 'tweet__contains_pos_trigram_,_,_U', 'tweet__contains_pos_trigram_,_N_V', 'tweet__contains_pos_trigram_^_V_V', 'tweet__contains_pos_trigram_D_N_N', 'tweet__contains_pos_trigram_P_A_N', 'tweet__contains_pos_trigram_N_V_A', 'tweet__contains_pos_trigram_N_V_N', 'tweet__contains_pos_trigram_A_N_V', 'tweet__contains_pos_trigram_^_^_V', 'tweet__contains_pos_trigram_A_N_N', 'tweet__contains_pos_trigram_D_A_N', 'tweet__contains_pos_trigram_,_U_U', 'tweet__contains_pos_trigram_^_N_P', 'tweet__contains_pos_trigram_O_V_D', 'tweet__contains_pos_trigram_P_D_^', 'tweet__contains_pos_trigram_N_V_R', 'tweet__contains_pos_trigram_N_,_N', 'tweet__contains_pos_trigram_V_^_,', 'tweet__contains_pos_trigram_V_D_A', 'tweet__contains_pos_trigram_V_A_N', 'tweet__contains_pos_trigram_N_N_U', 'tweet__contains_pos_trigram_D_N_P', 'tweet__contains_pos_trigram_^_,_G', 'tweet__contains_pos_trigram_V_N_,', 'tweet__contains_pos_trigram_P_N_,', 'tweet__contains_pos_trigram_N_P_V', 'tweet__contains_pos_trigram_,_O_V', 'tweet__contains_pos_trigram_,_^_^', 'tweet__contains_pos_trigram_V_P_N', 'tweet__contains_pos_trigram_^_N_V', 'tweet__contains_pos_trigram_N_P_N', 'tweet__contains_pos_trigram_V_V_D', 'tweet__contains_pos_trigram_^_N_U', 'tweet__contains_pos_trigram_P_D_N', 'tweet__contains_pos_trigram_D_N_U', 'tweet__contains_pos_trigram_P_^_,', 'tweet__contains_pos_trigram_N_,_U', 'tweet__contains_pos_trigram_N_V_P', 'tweet__contains_pos_trigram_,_G_,', 'tweet__contains_pos_trigram_^_,_^', 'tweet__contains_pos_trigram_N_P_^', 'tweet__contains_pos_trigram_^_N_N', 'tweet__contains_pos_trigram_P_N_U', 'tweet__contains_pos_trigram_V_^_^', 'tweet__contains_pos_trigram_A_N_U', 'tweet__contains_pos_trigram_^_^_^', 'tweet__contains_pos_trigram_N_N_N', 'tweet__contains_pos_trigram_V_P_^', 'tweet__contains_pos_trigram_P_V_N', 'tweet__contains_pos_trigram_D_^_N', 'tweet__contains_pos_trigram_P_^_^', 'tweet__contains_pos_trigram_A_A_N', 'tweet__contains_pos_trigram_^_U_U', 'tweet__contains_pos_trigram_^_^_N', 'tweet__contains_pos_trigram_D_N_,', 'tweet__contains_pos_trigram_V_V_P', 'tweet__contains_pos_trigram_N_,_V', 'tweet__contains_pos_trigram_^_^_U', 'tweet__contains_pos_trigram_N_,_,', 'tweet__contains_pos_trigram_V_O_V', 'tweet__contains_pos_trigram_^_N_,', 'tweet__contains_pos_trigram_P_V_P', 'tweet__contains_pos_trigram_N_V_V', 'tweet__contains_pos_trigram_^_,_U', 'tweet__contains_pos_trigram_^_^_P', 'tweet__fake', 'user__id', 'tweet__id', 'tweet__d2v_0', 'tweet__d2v_1', 'tweet__d2v_2', 'tweet__d2v_3', 'tweet__d2v_4', 'tweet__d2v_5', 'tweet__d2v_6', 'tweet__d2v_7', 'tweet__d2v_8', 'tweet__d2v_9', 'tweet__d2v_10', 'tweet__d2v_11', 'tweet__d2v_12', 'tweet__d2v_13', 'tweet__d2v_14', 'tweet__d2v_15', 'tweet__d2v_16', 'tweet__d2v_17', 'tweet__d2v_18', 'tweet__d2v_19', 'tweet__d2v_20', 'tweet__d2v_21', 'tweet__d2v_22', 'tweet__d2v_23', 'tweet__d2v_24', 'tweet__d2v_25', 'tweet__d2v_26', 'tweet__d2v_27', 'tweet__d2v_28', 'tweet__d2v_29', 'tweet__d2v_30', 'tweet__d2v_31', 'tweet__d2v_32', 'tweet__d2v_33', 'tweet__d2v_34', 'tweet__d2v_35', 'tweet__d2v_36', 'tweet__d2v_37', 'tweet__d2v_38', 'tweet__d2v_39', 'tweet__d2v_40', 'tweet__d2v_41', 'tweet__d2v_42', 'tweet__d2v_43', 'tweet__d2v_44', 'tweet__d2v_45', 'tweet__d2v_46', 'tweet__d2v_47', 'tweet__d2v_48', 'tweet__d2v_49', 'tweet__d2v_50', 'tweet__d2v_51', 'tweet__d2v_52', 'tweet__d2v_53', 'tweet__d2v_54', 'tweet__d2v_55', 'tweet__d2v_56', 'tweet__d2v_57', 'tweet__d2v_58', 'tweet__d2v_59', 'tweet__d2v_60', 'tweet__d2v_61', 'tweet__d2v_62', 'tweet__d2v_63', 'tweet__d2v_64', 'tweet__d2v_65', 'tweet__d2v_66', 'tweet__d2v_67', 'tweet__d2v_68', 'tweet__d2v_69', 'tweet__d2v_70', 'tweet__d2v_71', 'tweet__d2v_72', 'tweet__d2v_73', 'tweet__d2v_74', 'tweet__d2v_75', 'tweet__d2v_76', 'tweet__d2v_77', 'tweet__d2v_78', 'tweet__d2v_79', 'tweet__d2v_80', 'tweet__d2v_81', 'tweet__d2v_82', 'tweet__d2v_83', 'tweet__d2v_84', 'tweet__d2v_85', 'tweet__d2v_86', 'tweet__d2v_87', 'tweet__d2v_88', 'tweet__d2v_89', 'tweet__d2v_90', 'tweet__d2v_91', 'tweet__d2v_92', 'tweet__d2v_93', 'tweet__d2v_94', 'tweet__d2v_95', 'tweet__d2v_96', 'tweet__d2v_97', 'tweet__d2v_98', 'tweet__d2v_99', 'tweet__d2v_100', 'tweet__d2v_101', 'tweet__d2v_102', 'tweet__d2v_103', 'tweet__d2v_104', 'tweet__d2v_105', 'tweet__d2v_106', 'tweet__d2v_107', 'tweet__d2v_108', 'tweet__d2v_109', 'tweet__d2v_110', 'tweet__d2v_111', 'tweet__d2v_112', 'tweet__d2v_113', 'tweet__d2v_114', 'tweet__d2v_115', 'tweet__d2v_116', 'tweet__d2v_117', 'tweet__d2v_118', 'tweet__d2v_119', 'tweet__d2v_120', 'tweet__d2v_121', 'tweet__d2v_122', 'tweet__d2v_123', 'tweet__d2v_124', 'tweet__d2v_125', 'tweet__d2v_126', 'tweet__d2v_127', 'tweet__d2v_128', 'tweet__d2v_129', 'tweet__d2v_130', 'tweet__d2v_131', 'tweet__d2v_132', 'tweet__d2v_133', 'tweet__d2v_134', 'tweet__d2v_135', 'tweet__d2v_136', 'tweet__d2v_137', 'tweet__d2v_138', 'tweet__d2v_139', 'tweet__d2v_140', 'tweet__d2v_141', 'tweet__d2v_142', 'tweet__d2v_143', 'tweet__d2v_144', 'tweet__d2v_145', 'tweet__d2v_146', 'tweet__d2v_147', 'tweet__d2v_148', 'tweet__d2v_149', 'tweet__d2v_150', 'tweet__d2v_151', 'tweet__d2v_152', 'tweet__d2v_153', 'tweet__d2v_154', 'tweet__d2v_155', 'tweet__d2v_156', 'tweet__d2v_157', 'tweet__d2v_158', 'tweet__d2v_159', 'tweet__d2v_160', 'tweet__d2v_161', 'tweet__d2v_162', 'tweet__d2v_163', 'tweet__d2v_164', 'tweet__d2v_165', 'tweet__d2v_166', 'tweet__d2v_167', 'tweet__d2v_168', 'tweet__d2v_169', 'tweet__d2v_170', 'tweet__d2v_171', 'tweet__d2v_172', 'tweet__d2v_173', 'tweet__d2v_174', 'tweet__d2v_175', 'tweet__d2v_176', 'tweet__d2v_177', 'tweet__d2v_178', 'tweet__d2v_179', 'tweet__d2v_180', 'tweet__d2v_181', 'tweet__d2v_182', 'tweet__d2v_183', 'tweet__d2v_184', 'tweet__d2v_185', 'tweet__d2v_186', 'tweet__d2v_187', 'tweet__d2v_188', 'tweet__d2v_189', 'tweet__d2v_190', 'tweet__d2v_191', 'tweet__d2v_192', 'tweet__d2v_193', 'tweet__d2v_194', 'tweet__d2v_195', 'tweet__d2v_196', 'tweet__d2v_197', 'tweet__d2v_198', 'tweet__d2v_199', 'tweet__d2v_200', 'tweet__d2v_201', 'tweet__d2v_202', 'tweet__d2v_203', 'tweet__d2v_204', 'tweet__d2v_205', 'tweet__d2v_206', 'tweet__d2v_207', 'tweet__d2v_208', 'tweet__d2v_209', 'tweet__d2v_210', 'tweet__d2v_211', 'tweet__d2v_212', 'tweet__d2v_213', 'tweet__d2v_214', 'tweet__d2v_215', 'tweet__d2v_216', 'tweet__d2v_217', 'tweet__d2v_218', 'tweet__d2v_219', 'tweet__d2v_220', 'tweet__d2v_221', 'tweet__d2v_222', 'tweet__d2v_223', 'tweet__d2v_224', 'tweet__d2v_225', 'tweet__d2v_226', 'tweet__d2v_227', 'tweet__d2v_228', 'tweet__d2v_229', 'tweet__d2v_230', 'tweet__d2v_231', 'tweet__d2v_232', 'tweet__d2v_233', 'tweet__d2v_234', 'tweet__d2v_235', 'tweet__d2v_236', 'tweet__d2v_237', 'tweet__d2v_238', 'tweet__d2v_239', 'tweet__d2v_240', 'tweet__d2v_241', 'tweet__d2v_242', 'tweet__d2v_243', 'tweet__d2v_244', 'tweet__d2v_245', 'tweet__d2v_246', 'tweet__d2v_247', 'tweet__d2v_248', 'tweet__d2v_249', 'tweet__d2v_250', 'tweet__d2v_251', 'tweet__d2v_252', 'tweet__d2v_253', 'tweet__d2v_254', 'tweet__d2v_255', 'tweet__d2v_256', 'tweet__d2v_257', 'tweet__d2v_258', 'tweet__d2v_259', 'tweet__d2v_260', 'tweet__d2v_261', 'tweet__d2v_262', 'tweet__d2v_263', 'tweet__d2v_264', 'tweet__d2v_265', 'tweet__d2v_266', 'tweet__d2v_267', 'tweet__d2v_268', 'tweet__d2v_269', 'tweet__d2v_270', 'tweet__d2v_271', 'tweet__d2v_272', 'tweet__d2v_273', 'tweet__d2v_274', 'tweet__d2v_275', 'tweet__d2v_276', 'tweet__d2v_277', 'tweet__d2v_278', 'tweet__d2v_279', 'tweet__d2v_280', 'tweet__d2v_281', 'tweet__d2v_282', 'tweet__d2v_283', 'tweet__d2v_284', 'tweet__d2v_285', 'tweet__d2v_286', 'tweet__d2v_287', 'tweet__d2v_288', 'tweet__d2v_289', 'tweet__d2v_290', 'tweet__d2v_291', 'tweet__d2v_292', 'tweet__d2v_293', 'tweet__d2v_294', 'tweet__d2v_295', 'tweet__d2v_296', 'tweet__d2v_297', 'tweet__d2v_298', 'tweet__d2v_299', 'tweet__topic_0', 'tweet__topic_1', 'tweet__topic_2', 'tweet__topic_3', 'tweet__topic_4', 'tweet__topic_5', 'tweet__topic_6', 'tweet__topic_7', 'tweet__topic_8', 'tweet__topic_9', 'tweet__topic_10', 'tweet__topic_11', 'tweet__topic_12', 'tweet__topic_13', 'tweet__topic_14', 'tweet__topic_15', 'tweet__topic_16', 'tweet__topic_17', 'tweet__topic_18', 'tweet__topic_19', 'tweet__topic_20', 'tweet__topic_21', 'tweet__topic_22', 'tweet__topic_23', 'tweet__topic_24', 'tweet__topic_25', 'tweet__topic_26', 'tweet__topic_27', 'tweet__topic_28', 'tweet__topic_29', 'tweet__topic_30', 'tweet__topic_31', 'tweet__topic_32', 'tweet__topic_33', 'tweet__topic_34', 'tweet__topic_35', 'tweet__topic_36', 'tweet__topic_37', 'tweet__topic_38', 'tweet__topic_39', 'tweet__topic_40', 'tweet__topic_41', 'tweet__topic_42', 'tweet__topic_43', 'tweet__topic_44', 'tweet__topic_45', 'tweet__topic_46', 'tweet__topic_47', 'tweet__topic_48', 'tweet__topic_49', 'tweet__topic_50', 'tweet__topic_51', 'tweet__topic_52', 'tweet__topic_53', 'tweet__topic_54', 'tweet__topic_55', 'tweet__topic_56', 'tweet__topic_57', 'tweet__topic_58', 'tweet__topic_59', 'tweet__topic_60', 'tweet__topic_61', 'tweet__topic_62', 'tweet__topic_63', 'tweet__topic_64', 'tweet__topic_65', 'tweet__topic_66', 'tweet__topic_67', 'tweet__topic_68', 'tweet__topic_69', 'tweet__topic_70', 'tweet__topic_71', 'tweet__topic_72', 'tweet__topic_73', 'tweet__topic_74', 'tweet__topic_75', 'tweet__topic_76', 'tweet__topic_77', 'tweet__topic_78', 'tweet__topic_79', 'tweet__topic_80', 'tweet__topic_81', 'tweet__topic_82', 'tweet__topic_83', 'tweet__topic_84', 'tweet__topic_85', 'tweet__topic_86', 'tweet__topic_87', 'tweet__topic_88', 'tweet__topic_89']]
        #df_test = pd.read_csv("../data/test.csv")

        # df_fake["class"] = 0
        # df_true["class"] = 1
        # df_test["class"] = 0
        # df_merge = pd.concat([df_fake, df_true], axis=0)
        # df_merge.head(10)

        # df = df_merge.drop(["title", "subject", "date"], axis=1)

        df = df.sample(frac=1)
        # df.reset_index(inplace=True)
        # df_test.reset_index(inplace=True)
        # df.drop(["index"], axis=1, inplace=True)
        # df_test.drop(["index"], axis=1, inplace=True)

        # df["text"] = df["text"].apply(self.wordopt)
        # x = df["text"]
        # y = df["class"]

        # df_test["text"] = df_test["text"].apply(self.wordopt)
        # test_x = df_test["text"]
        # test_y = df_test["class"]

        #y = df["tweet__fake"]
        #x = df.drop(["tweet__fake"], axis=1)
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.7)
        #y_test = df_test["tweet__fake"]
        #print(y)
        #x_test = df_test.drop(["tweet__fake"], axis=1)
        #x=np.ascontiguousarray(x)
        #y=np.ascontiguousarray(y)
        #y_test = np.ascontiguousarray(y_test)
        #x_test = np.ascontiguousarray(x_test)
        print(y.__len__())
        print(x.__len__())
        #print(x.flags)


        # xv_test = vectorization.transform(x_test)
        # vtest_x = vectorization.transform(test_x)

        clf = Pipeline([('tf-idf', TfidfVectorizer()),('scaler', StandardScaler(with_mean=False)),
                       ('clf', LogisticRegression(solver='lbfgs', max_iter=15000, verbose=1))])
        #'LR', LogisticRegression(solver='lbfgs', max_iter=15000, verbose=1)
        #clf = SVC(kernel='linear', C=1.0, probability=True)
        #clf=GaussianNB()
        #clf=LinearSVC(verbose=True, max_iter=50000)
        #clf=EMRVC(kernel="linear",max_iter=50000,verbose=True)
        print("fitting")
        clf.fit(x_train,y_train)
        predictions = clf.predict(x_test)
        cm = confusion_matrix(y_test, predictions, labels=clf.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
        disp.plot()
        plt.show()
        self.clf = clf
        pickle.dump(clf, open(self.filename, 'w+b'))

    def predict(self, input_string):
        DATA = StringIO("text\n" + input_string)
        df = pd.read_csv(DATA, sep=';')
        df["text"] = df["text"].apply(self.wordopt)

        out = self.clf.predict_proba(df["text"])
        print(out)
        if (out[0][0] > out[0][1]):
            return 'is true with {:.2f} certainty.'.format(out[0][0]*100)
            # return "is true with " + str(out[0][0]*100) + " certainty."
        else:
            return 'is false with {:.2f} certainty.'.format(out[0][1] * 100)
            # return "is false with " + str(out[0][1]*100) + " certainty."

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

if __name__ == '__main__':
    svm=SVM()
    svm.train()