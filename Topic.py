import requests
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation

# Function to fetch news articles from News API
def fetch_news_articles():
    API_KEY = '95f1b09c8eae4dd5b8ceca5c33522cf8'
    params = {
        'q': 'government of india',
        # 'from': '2024-01-29',
        'sortBy': 'publishedAt',
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

# Fetch news articles
news_articles = fetch_news_articles()

# Check if there are any articles fetched
if not news_articles:
    print("No articles fetched. Exiting...")
    exit()

# Create a CountVectorizer to convert text data into a matrix of token counts
vectorizer = CountVectorizer(max_df=1.0, min_df=1, stop_words='english')
X = vectorizer.fit_transform(news_articles)

# Check if the vocabulary is empty
if X.shape[1] == 0:
    print("After preprocessing, no terms remain. Please adjust min_df or max_df parameters.")
    exit()

# Define the number of topics
num_topics = 5

# Apply Latent Dirichlet Allocation (LDA) to identify topics
lda = LatentDirichletAllocation(n_components=num_topics, random_state=42)
lda.fit(X)

# Function to display the top words for each topic
def display_topics(model, feature_names, num_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print(f"Topic {topic_idx+1}:")
        topic_words_indices = topic.argsort()[:-num_top_words-1:-1]
        topic_words = [feature_names[i] for i in topic_words_indices]
        print(" ".join(topic_words))

num_top_words = 5
print("Top words for each topic:")
display_topics(lda, vectorizer.get_feature_names_out(), num_top_words)

# Assign topics to documents
topic_assignments = lda.transform(X)
print("\nTopic assignments for each document:")
for i, topic in enumerate(topic_assignments):
    print(f"Document {i+1} -> Topic: {topic.argmax()+1}")
