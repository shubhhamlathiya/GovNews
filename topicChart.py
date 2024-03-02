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



def show_topic_assignments_chart(topic_assignments, topic_names, topic_words):
    doc_topics = topic_assignments.sum(axis=0)

    # Create an array of topic labels
    labels = np.arange(doc_topics.shape[0])

    fig, ax = plt.subplots()
    ax.barh(labels, doc_topics, color=[f'C{i}' for i in range(len(topic_names))])
    ax.set_xlabel('Number of Articles')
    ax.set_title('Top words for each topic')
    ax.set_yticks(labels)

    # Add a new line for the topic names
    # plt.gca().set_ylabel('\n'.join(topic_names), fontsize=12, fontweight='bold')

    # Update y-tick labels with wrapped topic names
    ax.set_yticklabels([f'{topic_name}: {"\n".join(topic_words[i])}' for i, topic_name in enumerate(topic_names)])
    plt.show()




show_topic_assignments_chart(topic_assignments, topic_names, topic_words)