import glob
import pickle
import os

import pandas as pd
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer


def get_docs_and_years(path):
    docs = []
    years = []
    pickles = glob.glob(f"{path}/*.pickle")
    for pickle_file in pickles:
        year = pickle_file.split('.')[0].split()[2]
        years.append(year)

        with open(pickle_file, 'rb') as f:
            report = pickle.load(f)
            report = re.sub('[^a-zA-Z]', ' ', report)
            report = re.sub('\n', ' ', report)
            report = re.sub('\xa0', ' ', report)
            docs.append(report.lower())

    return docs, years


def get_word_frequency(docs, years):
    stemmer = nltk.stem.SnowballStemmer('english')
    docs = [stemmer.stem(doc) for doc in docs]
    vectorizer = CountVectorizer(stop_words='english')
    counts = vectorizer.fit_transform(docs)
    counts = pd.DataFrame(counts.toarray(), columns=vectorizer.get_feature_names()).transpose()
    counts.columns = years

    return counts


def get_word_list(list_path):
    word_list = []
    for sentiment_class in ['Negative', 'Positive', 'Litigious', 'Uncertainty',
                            'StrongModal', 'WeakModal', 'Constraining']:
        sentiment_list = pd.read_excel(list_path, sheet_name=sentiment_class, header=None)
        sentiment_list.columns = ['Word']
        sentiment_list["Word"] = sentiment_list['Word'].str.lower()
        sentiment_list[sentiment_class] = 1
        sentiment_list = sentiment_list.set_index('Word')[sentiment_class]
        word_list.append(sentiment_list)
    word_list = pd.concat(word_list, axis=1, sort=True).fillna(0)
    return word_list


def analyze_docs(counts, word_list):
    l = []
    tf_percent = counts / counts.sum()
    for word_type in word_list.columns:
        word_type_list = word_list[word_list[word_type] == 1].index
        word_type_frequency = tf_percent.reindex(word_type_list).dropna().sum()
        l.append(word_type_frequency)

    word_type_frequency = pd.concat(l, axis=1)
    word_type_frequency.columns = word_list.columns

    return word_type_frequency


with open('nifty_next_tickers.pickle', 'rb') as f:
    tickers = pickle.load(f)

no_of_stocks = 0
for ticker in tickers:
    reports, years = get_docs_and_years(ticker)
    count = get_word_frequency(reports, years)
    list_path = 'LM_Word_List.xlsx'
    word_list = get_word_list(list_path)
    word_type_frequency = analyze_docs(count, word_list)

    if os.path.exists('Sentiment_analysis.xlsx'):
        with pd.ExcelWriter('Sentiment_analysis.xlsx', mode='a') as f:
            word_type_frequency.to_excel(f, sheet_name=f'{ticker}')
        print(f"Excel output written for {ticker}")
        no_of_stocks += 1
    else:
        with pd.ExcelWriter('Sentiment_analysis.xlsx') as f:
            word_type_frequency.to_excel(f, sheet_name=f'{ticker}')
        print(f"Excel output written for {ticker}")
        no_of_stocks += 1
    print(f"Output written for {no_of_stocks} stocks")
