import json
import requests
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

def fetch_news_articles(query):
    API_KEY = '95f1b09c8eae4dd5b8ceca5c33522cf8'
    params = {
        'q': query,
        'sortBy': 'publishedAt',
        # 'country': 'in',
        'apiKey': API_KEY
    }

    try:
        response = requests.get('https://newsapi.org/v2/everything', params=params)
        response.raise_for_status()
        data = response.json()
        articles = data['articles']
        return [article['title'] for article in articles]  # Extracting titles of articles
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Error occurred: {err}')
    return []


news_articles = fetch_news_articles(input("Enter your search query: "))

if not news_articles:
    print("No articles fetched. Exiting...")
    exit()

vectorizer = CountVectorizer(max_df=1.0, min_df=1, stop_words='english')
X = vectorizer.fit_transform(news_articles)

if X.shape[1] == 0:
    print("After preprocessing, no terms remain. Please adjust min_df or max_df parameters.")
    exit()

num_topics = 5

lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(X)

def display_topics(model, feature_names, num_top_words):
    topic_names = ['Topic ' + str(topic_idx + 1) for topic_idx in range(model.n_components)]
    topic_words = []
    for topic_idx, topic in enumerate(model.components_):
        topic_words_indices = topic.argsort()[:-num_top_words-1:-1]
        topic_words.append([feature_names[i] for i in topic_words_indices])
    return topic_names, topic_words

topic_names, topic_words = display_topics(lda, vectorizer.get_feature_names_out(), 5)

topic_assignments = lda.transform(X)

topic_info = {
    "topic_names": topic_names,
    "topic_words": topic_words
}

json_data = json.dumps(topic_info)
print(json_data)