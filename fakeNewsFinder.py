import textblob
import requests
import matplotlib.pyplot as plt
import numpy as np

# Set up NewsAPI
api_key = "95f1b09c8eae4dd5b8ceca5c33522cf8"
url = f"https://newsapi.org/v2/everything?q=Government+of+India&apiKey={api_key}"

# Fetch news articles
response = requests.get(url)
articles = response.json()

def analyze_sentiment(text):
    blob = textblob.TextBlob(text)
    polarity = blob.sentiment.polarity
    subjectivity = blob.sentiment.subjectivity

    return {
        "polarity": polarity,
        "subjectivity": subjectivity
    }

# Analyze sentiment of news articles
sentiment_polarity = [analyze_sentiment(article['description'])['polarity'] for article in articles["articles"]]

# Count positive and negative words in news articles
positive_count = [len([word for word in article['title'].split() if textblob.TextBlob(word).sentiment.polarity > 0.0]) for article in articles["articles"]]
negative_count = [len([word for word in article['title'].split() if textblob.TextBlob(word).sentiment.polarity < 0.0]) for article in articles["articles"]]

# Create histograms of sentiment polarity
positive, bins_positive, patches_positive = plt.hist([polarity for polarity in sentiment_polarity if polarity > 0.0], bins=5, alpha=0.5, label='Positive')
negative, bins_negative, patches_negative = plt.hist([polarity for polarity in sentiment_polarity if polarity < 0.0], bins=5, alpha=0.5, label='Negative')
neutral, bins_neutral, patches_neutral = plt.hist([polarity for polarity in sentiment_polarity if polarity == 0.0], bins=5, alpha=0.5, label='Neutral')

plt.xlabel("Sentiment Polarity")
plt.ylabel("Count")
plt.title("Sentiment Analysis of News Articles")
plt.legend()
plt.show()

# Count positive and negative news articles
positive_news = len(np.where(np.array(sentiment_polarity) > 0.0)[0])
negative_news = len(np.where(np.array(sentiment_polarity) < 0.0)[0])

# Create bar chart of sentiment counts
plt.bar("Positive", positive_news)
plt.bar("Negative", negative_news)

plt.xlabel("Sentiment")
plt.ylabel("Count")
plt.title("Sentiment Count of News Articles")
plt.show()

print(f"Positive news articles: {positive_news}")
print(f"Negative news articles: {negative_news}")