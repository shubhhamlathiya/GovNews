import requests

def get_news_articles(date=None, topic=None, region=None):
    # Replace 'your_api_key' with your actual API key from NewsAPI
    api_key = "95f1b09c8eae4dd5b8ceca5c33522cf8"

    # Construct the API endpoint
    url = f"https://newsapi.org/v2/everything?q=Government+of+India&apiKey={api_key}"

    # Add any additional query parameters for date, topic, or region
    # if date:
    #     url += f"&from={date}"
    # if topic:
    #     url += f"&topic={topic}"
    # if region:
    #     url += f"&region={region}"

    # Make the API request
    response = requests.get(url)

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

# Example usage
articles = get_news_articles("2023-01-01", "pm", "in")

# Print the articles
for article in articles:
    print(f"Title: {article['title']}")
    print(f"URL: {article['url']}")
    print(f"Image URL: {article['urlToImage']}")
    print(f"Content: {article['content']}\n")