import feedparser
import random
from urllib.parse import urlparse

def fetch_news_rss():
    # Real topic-specific feeds, not vague Google queries
    feed_urls = {
        "World": "http://feeds.bbci.co.uk/news/world/rss.xml",
        "Technology": "http://feeds.feedburner.com/TechCrunch/",
        "India": "https://feeds.feedburner.com/ndtvnews-india-news",
        "Science": "https://www.sciencedaily.com/rss/all.xml"
    }

    all_articles = []
    seen_links = set()

    for topic, url in feed_urls.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:  # Take top 10 from each to limit spam
            title = entry.title.strip()
            link = entry.link.strip()
            published = entry.get("published", "Just now")
            source = urlparse(link).netloc.replace("www.", "")

            if link not in seen_links:
                seen_links.add(link)
                all_articles.append({
                    "title": title,
                    "link": link,
                    "published": published,
                    "source": source,
                    "topic": topic
                })

    random.shuffle(all_articles)
    return all_articles

# Example usage
if __name__ == "__main__":
    articles = fetch_news_rss()
    for article in articles:
        print(f"[{article['topic']}] {article['title']} ({article['source']})")
        print(f"Link: {article['link']}")
        print(f"Published: {article['published']}")
        print("-" * 80)
