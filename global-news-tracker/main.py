from fetcher.google_news import fetch_news_rss
from parser.article_parser import extract_article_content
from summarizer.llm_summarizer import summarize_with_llm


def run_pipeline():
    headlines = fetch_news_rss()
    results = []

    for news in headlines[:5]:  # Limit for testing
        try:
            article = extract_article_content(news["link"])
        except Exception as e:
            print(f"Failed to process")

    summary = summarize_with_llm(article["text"], model="mistral")
    print("🧠 Summary:\n", summary)



if __name__ == "__main__":
    run_pipeline()