# app.py
import streamlit as st
import fitz  # PyMuPDF
from transformers import pipeline


from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM

@st.cache_resource                                                                          # decorator that tells streamlit to load the fun only once an d reuse
def load_summarizer():
    model_name = "facebook/bart-large-cnn"                                                  # A pre-trained neural network model for summarisation
    tokenizer = AutoTokenizer.from_pretrained(model_name)                                   #Automatically loads the tokenizer that matches the model.
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)                               #AutoModelForSeq2SeqLM = a class that loads models meant for Sequence-to-Sequence Language Modeling.
    return pipeline("summarization", model=model, tokenizer=tokenizer, framework="pt")      #pipeline() is a high-level shortcut in Hugging Face that bundles the model + tokenizer + task into one callable function


def extract_text_from_pdf(uploaded_file):
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, max_tokens=1024):
    """Split long text into chunks for summarization model."""
    import textwrap
    return textwrap.wrap(text, width=max_tokens, break_long_words=False)

def summarize_text(text, summarizer):
    chunks = chunk_text(text)
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)

# --- Streamlit UI ---
st.title("Document Summarizer")
uploaded_pdf = st.file_uploader("Upload a PDF document", type="pdf")

if uploaded_pdf:
    with st.spinner("Extracting text..."):
        pdf_text = extract_text_from_pdf(uploaded_pdf)
        st.success("Text extracted!")

        if st.button("Summarize"):
            with st.spinner("Summarizing..."):
                summarizer = load_summarizer()                           #becoz pipeline() bundles to one callable fun
                summary = summarize_text(pdf_text, summarizer)
                st.subheader("📝 Summary")
                st.write(summary)