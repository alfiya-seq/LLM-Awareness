from transformers import pipeline

# Load the summarization pipeline once
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_with_llm(text: str) -> str:
    """
    Summarize the article using Hugging Face Transformers.
    """
    # Shorten long articles (BART has a max token limit ~1024)
    max_len = 1024
    input_text = text[:max_len]

    try:
        summary = summarizer(input_text, max_length=130, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"⚠️ Failed to summarize: {e}"
