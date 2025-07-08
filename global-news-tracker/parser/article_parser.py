from newspaper import Article                           # Artcile  class - download and extract clean text from a news article page.

def extract_article_content(url: str):
    article = Article(url)                              # Creates an Article object for that URL.
    article.download()                                  #  Downloads the HTML content of the article page.
    article.parse()                                     #  Parses the downloaded HTML to extract: title,text etc.
    return {
        "title": article.title,
        "text": article.text,
        "authors": article.authors,
        "publish_date": str(article.publish_date),
        "url": url
    }
