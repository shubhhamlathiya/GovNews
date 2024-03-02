from requests import get
from flask import Flask, render_template, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/newsfeeds")
def news():
    articles = get_news_articles(region="in")
    return render_template("newsfeeds.html", articles=articles)

@app.route("/explore")
def explore():
    return render_template("explore.html")

@app.route("/trending")
def trending():
    return render_template("tranding.html")

def get_news_articles(date=None, topic=None, region=None):
    # Replace 'your_api_key' with your actual API key from NewsAPI
    api_key = "95f1b09c8eae4dd5b8ceca5c33522cf8"

    # Construct the API endpoint
    url = f"https://newsapi.org/v2/everything?q=Government+of+India&apiKey={api_key}"

    # Make the API request
    response = get(url)

    # Parse the JSON response
    data = response.json()

    # Extract the articles
    articles = data.get("articles", [])

    # Add title, URL, and image URL to each article
    for article in articles:
        article["title"] = article.get("title", "")
        article["url"] = article.get("url", "")
        article["urlToImage"] = article.get("urlToImage", "")
        article["content"] = article.get("content", "")

    return articles


if __name__ == "__main__":
    app.run(debug=True)