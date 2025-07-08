import streamlit as st
from datetime import datetime
from fetcher.google_news import fetch_news_rss
from parser.article_parser import extract_article_content
from summarizer.llm_summarizer import summarize_with_llm

st.set_page_config(page_title="🗞️ Global News Portal", layout="wide")

# Top heading
today = datetime.now().strftime("%A, %d %B %Y")
st.markdown(f"<h1 style='text-align: center; color: white;'>📰 Global News Highlights</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center; color: gray;'>{today}</h4>", unsafe_allow_html=True)
st.markdown("---")

# Load articles on first load
if "articles" not in st.session_state:
    with st.spinner(" Fetching top news..."):
        headlines = fetch_news_rss()
        summarized = []
        for news in headlines[:6]:  # Limit
            try:
                article = extract_article_content(news["link"])
                summary = summarize_with_llm(article["text"])
                summarized.append({
                    "title": article["title"],
                    "summary": summary,
                    "url": article["url"],
                    "published": news.get("published", "Just now"),
                    "image": article.get("top_image", None)  # Optional
                })
            except Exception as e:
                summarized.append({
                    "title": news["title"],
                    "summary": f" Error: {e}",
                    "url": news["link"],
                    "published": "N/A",
                    "image": None
                })
        st.session_state.articles = summarized

# Refresh Button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🔁 Refresh News"):
    st.session_state.pop("articles")
    st.rerun()

# Grid layout (2 columns)
cols = st.columns(2)

for idx, article in enumerate(st.session_state.articles):
    col = cols[idx % 2]

    with col:
        st.markdown(
            f"""
            <div style="background-color: #111; padding: 16px; border-radius: 10px; margin-bottom: 16px;">
                <h3 style="color: #fff;">{article['title']}</h3>
                <p style="color: #ccc;">🕒 {article['published']}</p>
                <p style="color: #ddd;">{article['summary']}</p>
                <a href="{article['url']}" target="_blank" style="color: #1f77b4;">Read Full Article 🔗</a>
            </div>
            """,
            unsafe_allow_html=True
        )
