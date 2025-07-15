import streamlit as st
from tempfile import NamedTemporaryFile                               #built inn python mdoule
from transcriber.whisper_transcriber import transcribe_audio
from summarizer.mistral_summarizer import run_mistral
from utils.prompt_builder import build_prompt
from fpdf import FPDF
import base64

# Set page layout and style
st.set_page_config(
    page_title="Meeting Summarizer Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject CSS for styling UI with header, navbar, and footer
st.markdown("""
    <style>
    #MainMenu , header {visibility: hidden; display: none;}
    footer {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #0f8ea3, #0b0f2e, #912558);
        color: #ffffff;
    }

    .custom-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background: rgba(0, 0, 0, 0.5);
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        z-index: 999;
    }

    .navbar-logo {
        font-size: 1.5rem;
        font-weight: bold;
        color: #ffffff;
    }

    .navbar-menu {
        display: flex;
        gap: 1.5rem;
    }

    .navbar-menu a {
        color: #ffffff;
        text-decoration: none;
        font-weight: 500;
        font-size: 1rem;
    }

    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        text-align: center;
    }

    .subtitle {
        font-size: 1.2rem;
        color: #dddddd;
        margin-bottom: 2rem;
        text-align: center;
    }

    section[data-testid="stFileUploaderDropzone"] {
        background: rgba(255, 255, 255, 0.07) !important;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.25);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }

    section[data-testid="stFileUploaderDropzone"] button {
        background-color: rgba(255, 255, 255, 0.2) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600;
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: all 0.2s ease-in-out;
    }

    section[data-testid="stFileUploaderDropzone"] button:hover {
        background-color: rgba(255, 255, 255, 0.35) !important;
        color: #000000 !important;
    }

    .content-box {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1rem;
        white-space: pre-wrap;
        font-family: 'Courier New', Courier, monospace;
        color: #ffffff;
        margin-top: 2rem;
    }

    .footer {
        text-align: center;
        padding: 1.5rem;
        font-size: 0.9rem;
        color: #bbbbbb;
        margin-top: 4rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header with navbar
st.markdown("""
<div class="custom-header">
    <div class="navbar-menu">
        <a href="#">Home</a>
        <a href="#">Transcribe</a>
        <a href="#">Notes</a>
        <a href="#">Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Title and subtitle
st.markdown("<div class='title'>📝Meeting Mate</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Upload your meeting audio and generate structured notes & tasks using local AI</div>", unsafe_allow_html=True)

# Upload
audio_file = st.file_uploader("Upload meeting audio", type=["mp3", "wav", "m4a", "webm"])

# PDF Export function
def generate_pdf(summary_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for line in summary_text.splitlines():
        pdf.multi_cell(0, 10, line)
    return pdf.output(dest="S").encode("latin-1")

# Processing
if audio_file:
    st.audio(audio_file)

    with NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(audio_file.read())
        temp_path = tmp.name

    with st.spinner("Transcribing with Whisper..."):
        transcript = transcribe_audio(temp_path)
    st.success("✅ Transcription complete!")
    st.markdown(f"<div class='content-box'>{transcript}</div>", unsafe_allow_html=True)

    with st.spinner("Generating your Notes....hold a bit longer"):
        prompt = build_prompt(transcript)
        summary = run_mistral(prompt)
    st.success("✅ Notes ready!..TADA!")
    st.markdown(f"<div class='content-box'>{summary}</div>", unsafe_allow_html=True)

    pdf_bytes = generate_pdf(summary)                       # get raw PDF bytes
    b64 = base64.b64encode(pdf_bytes).decode()             # encode those bytes to a Base64 string
   # href = f'<a href="data:application/octet-stream;base64,{b64}" download="meeting_notes.pdf" style="color:#ffffff; text-decoration:none; font-weight:bold;">📄 Download Notes as PDF</a>'
    #st.markdown(href, unsafe_allow_html=True)
    st.markdown(f"""
    <div style="display: flex; justify-content: center; margin-top: 2rem;">
        <a href="data:application/octet-stream;base64,{b64}" download="meeting_notes.pdf"
           style="
                background: rgba(255, 255, 255, 0.15);
                color: #ffffff;
                padding: 0.75rem 1.5rem;
                border-radius: 12px;
                font-weight: 600;
                text-decoration: none;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.25);
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
                transition: all 0.3s ease;
                font-size: 1rem;
            "
           onmouseover="this.style.background='rgba(255,255,255,0.35)'; this.style.color='#000';"
           onmouseout="this.style.background='rgba(255,255,255,0.15)'; this.style.color='#fff';">
           📄 Download Notes as PDF
        </a>
    </div>
""", unsafe_allow_html=True)


# Footer
st.markdown("""
<div class="footer">
    © 2025 AI MeetingMate | Designed with ❤️ for productive teams
</div>
""", unsafe_allow_html=True)
