
import os
import base64
from io import BytesIO
from html import escape

import streamlit as st
from dotenv import load_dotenv
from groq import Groq
from pypdf import PdfReader

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------
load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY", "").strip()
MODEL = os.getenv("GROQ_MODEL", "qwen/qwen3.8-27b").strip()

st.set_page_config(
    page_title="HealthCare AI | Medical Report Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# PROFESSIONAL DARK UI - INSPIRED BY LEGALBOT
# --------------------------------------------------
st.markdown("""
<style>
#MainMenu, footer, [data-testid="stToolbar"] {
    visibility: hidden;
}

.stApp {
    background: #0b0f19;
    color: #f1f5f9;
}

[data-testid="stHeader"] {
    background: transparent;
}

[data-testid="stSidebar"] {
    background: #111827;
    border-right: 1px solid #263449;
}

[data-testid="stSidebar"] * {
    color: #e5edf8;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #67e8f9;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

html, body, [class*="css"] {
    font-family: "Segoe UI", Arial, sans-serif;
}

p, li, label, .stMarkdown {
    font-size: 17px;
    line-height: 1.75;
    color: #e2e8f0;
}

h1 {
    color: #f8fafc !important;
    font-size: 2.35rem !important;
    font-weight: 750 !important;
}

h2 {
    color: #67e8f9 !important;
    font-size: 1.65rem !important;
}

h3 {
    color: #93c5fd !important;
    font-size: 1.25rem !important;
}

[data-testid="stCaptionContainer"] p {
    color: #b8c5d8 !important;
    font-size: 14px !important;
}

.hero {
    background: linear-gradient(115deg, #14243b, #102d3d);
    border: 1px solid #28506a;
    border-left: 5px solid #38bdf8;
    padding: 27px 30px;
    border-radius: 14px;
    margin: 10px 0 22px 0;
}

.hero h2 {
    color: #f8fafc !important;
    margin: 0 0 8px 0;
    font-size: 27px !important;
}

.hero p {
    color: #d5e5f5 !important;
    margin: 0;
    font-size: 17px;
}

.academic-tag {
    display: inline-block;
    background: #172b46;
    border: 1px solid #315b88;
    color: #bfdbfe;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 14px;
    font-weight: 650;
    margin: 2px 0 8px 0;
}

.notice {
    background: #2a2114;
    border: 1px solid #6b4d21;
    border-radius: 9px;
    padding: 13px 16px;
    color: #fde7b0;
    font-size: 15px;
    line-height: 1.7;
    margin: 15px 0 22px 0;
}

.section-card {
    background: #111b2b;
    border: 1px solid #26374d;
    border-radius: 12px;
    padding: 20px;
    margin: 12px 0;
}

.section-heading {
    color: #67e8f9;
    font-size: 19px;
    font-weight: 750;
    margin-bottom: 10px;
}

.status-card {
    background: #111b2b;
    border: 1px solid #2b3d54;
    border-radius: 10px;
    padding: 16px;
    min-height: 94px;
}

.status-label {
    color: #a9bad0;
    font-size: 14px;
    margin-bottom: 6px;
}

.status-value {
    color: #f8fafc;
    font-size: 18px;
    font-weight: 700;
}

.report-header {
    background: #111827;
    border: 1px solid #2b3c53;
    border-bottom: 3px solid #3b82f6;
    border-radius: 11px 11px 0 0;
    padding: 20px 22px;
    margin-top: 25px;
}

.report-label {
    display: inline-block;
    background: #172e4c;
    color: #bfdbfe;
    border: 1px solid #315b88;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 13px;
    font-weight: 750;
    letter-spacing: 0.4px;
}

.report-body {
    background: #101a29;
    border: 1px solid #2b3c53;
    border-top: none;
    border-radius: 0 0 11px 11px;
    padding: 24px;
    margin-bottom: 15px;
}

.report-body p, .report-body li {
    color: #e6edf7;
    font-size: 17px;
    line-height: 1.85;
}

.report-body h1, .report-body h2, .report-body h3 {
    color: #7dd3fc !important;
    margin-top: 20px;
}

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 8px;
    min-height: 43px;
    font-size: 15px;
    font-weight: 650;
}

div.stButton > button[kind="primary"],
div.stFormSubmitButton > button[kind="primary"] {
    background: #1677bd;
    color: white;
    border: 1px solid #38bdf8;
}

div.stTextArea textarea {
    background: #101a29;
    color: #f8fafc;
    border: 1px solid #3a506b;
    border-radius: 9px;
    font-size: 17px;
    line-height: 1.7;
}

[data-testid="stFileUploader"] {
    background: #101a29;
    border: 1px dashed #46617f;
    border-radius: 10px;
    padding: 12px;
}

[data-testid="stFileUploader"] * {
    font-size: 15px;
}

hr {
    border-color: #2b3c53;
}

.small-note {
    color: #a9bad0;
    font-size: 14px;
    line-height: 1.6;
}

.success-seal {
    background: #102a25;
    border: 1px solid #23634f;
    color: #a7f3d0;
    border-radius: 9px;
    padding: 14px 16px;
    font-size: 15px;
    font-weight: 650;
    margin-top: 18px;
}
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# GROQ CLIENT
# --------------------------------------------------
client = Groq(api_key=API_KEY) if API_KEY else None

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "last_files" not in st.session_state:
    st.session_state.last_files = []


# --------------------------------------------------
# DOCUMENT EXTRACTION
# --------------------------------------------------
def extract_document_text(files):
    extracted = []
    errors = []

    for file in files:
        name = file.name.lower()

        try:
            if name.endswith(".txt"):
                text = file.getvalue().decode(
                    "utf-8", errors="replace"
                )
                extracted.append(
                    f"\n--- DOCUMENT: {file.name} ---\n{text[:18000]}"
                )

            elif name.endswith(".pdf"):
                reader = PdfReader(BytesIO(file.getvalue()))
                page_text = []

                for page in reader.pages[:25]:
                    page_text.append(page.extract_text() or "")

                text = "\n".join(page_text)

                if not text.strip():
                    errors.append(
                        f"{file.name}: No selectable text found. "
                        "This may be a scanned PDF requiring OCR."
                    )
                else:
                    extracted.append(
                        f"\n--- DOCUMENT: {file.name} ---\n{text[:22000]}"
                    )

        except Exception as exc:
            errors.append(f"{file.name}: {exc}")

    return "\n".join(extracted), errors


def image_to_data_url(file):
    extension = file.name.lower().rsplit(".", 1)[-1]

    mime_types = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "webp": "image/webp",
    }

    mime = mime_types.get(extension)
    if not mime:
        return None

    encoded = base64.b64encode(file.getvalue()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.title("🩺 HealthCare AI")
    st.caption("Medical Report Assistant")

    st.markdown(
        '<div class="academic-tag">Assignment 10 · GenAI & ML DevOps</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.subheader("System Status")

    if client:
        st.success("● Groq API key detected")
        st.caption(f"Active model: `{MODEL}`")
    else:
        st.error("● Groq API key missing")
        st.caption("Add GROQ_API_KEY to your .env file.")

    st.divider()

    st.subheader("Analysis Features")
    st.markdown("""
    **01 · Report Analysis**

    Summarizes available text in PDF and TXT reports.

    **02 · Image Understanding**

    Describes supported uploaded images.

    **03 · Health Explanation**

    Explains medical terms and report values in simple language.

    **04 · Structured Summary**

    Organizes findings, limitations, and follow-up questions.
    """)

    st.divider()

    st.subheader("Supported Files")
    st.markdown("""
    - PDF documents
    - TXT reports
    - PNG / JPG / JPEG / WEBP images
    """)

    st.divider()

    if st.button("🗑️ Clear Analysis", use_container_width=True):
        st.session_state.analysis_result = None
        st.session_state.last_question = ""
        st.session_state.last_files = []
        st.rerun()

    st.markdown(
        '<p class="small-note">Educational tool only. '
        'Not a substitute for professional medical advice.</p>',
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# MAIN PAGE HEADER
# --------------------------------------------------
st.title("Medical Report Analysis & Health Assistant")

st.markdown(
    '<div class="academic-tag">'
    'Healthcare AI · Groq Powered · KITCoEK'
    '</div>',
    unsafe_allow_html=True,
)

st.markdown("""
<div class="hero">
    <h2>Understand your health reports more clearly.</h2>
    <p>
        Upload a medical report or image, ask a question, and receive
        an organized explanation in clear, easy-to-understand language.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="notice">
    <strong>Important health notice:</strong>
    This assistant provides educational explanations, not a diagnosis.
    It may misread values or images. Confirm important findings with
    a qualified healthcare professional. Seek urgent medical care for
    severe or rapidly worsening symptoms.
</div>
""", unsafe_allow_html=True)

# Status summary cards
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">AI PROVIDER</div>
        <div class="status-value">Groq API</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">INPUT SUPPORT</div>
        <div class="status-value">PDF · TXT · Images</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="status-card">
        <div class="status-label">RESPONSE STYLE</div>
        <div class="status-value">Clear & Structured</div>
    </div>
    """, unsafe_allow_html=True)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------
st.markdown("## 📄 Upload and Analyze")
st.markdown(
    "Enter your question and optionally attach a report or image."
)

with st.form("health_analysis_form", clear_on_submit=False):
    question = st.text_area(
        "What would you like to understand?",
        placeholder=(
            "Example: Summarize this report, explain the values "
            "that are outside the stated reference ranges, and list "
            "questions I should ask my doctor."
        ),
        height=125,
        max_chars=5000,
    )

    uploaded_files = st.file_uploader(
        "Upload medical reports or images",
        type=["pdf", "txt", "png", "jpg", "jpeg", "webp"],
        accept_multiple_files=True,
        help="For best results, use readable documents and clear images.",
    )

    if uploaded_files:
        st.caption(
            f"{len(uploaded_files)} file(s) selected. "
            "Only the first 3 images are sent in one request."
        )

    analyze_button = st.form_submit_button(
        "🔍 Analyze Report",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# ANALYSIS
# --------------------------------------------------
if analyze_button:
    if not API_KEY or not client:
        st.error(
            "Groq API key not found. Add your new key to the "
            ".env file, save it, and restart Streamlit."
        )

    elif not question.strip() and not uploaded_files:
        st.warning("Please enter a question or upload a file.")

    else:
        files = uploaded_files or []
        document_text, extraction_errors = extract_document_text(files)

        image_files = [
            f for f in files
            if f.name.lower().endswith(
                (".png", ".jpg", ".jpeg", ".webp")
            )
        ]

        if len(image_files) > 3:
            st.warning(
                "Only the first 3 images will be sent to the model."
            )

        # If no question was entered, provide a sensible default.
        user_question = question.strip() or (
            "Please explain the uploaded report or image. "
            "Summarize its contents, explain any readable medical "
            "values, identify limitations, and suggest questions "
            "to discuss with a healthcare professional."
        )

        content = [{
            "type": "text",
            "text": (
                "You are a careful healthcare information assistant. "
                "Use simple, clear language and organize your answer "
                "with headings and bullet points. Do not claim to "
                "diagnose a disease. Do not invent values or findings. "
                "Distinguish values explicitly marked outside a report's "
                "reference range from your own interpretation. If the "
                "report lacks units or reference ranges, say so. "
                "Mention when an image or document is unreadable. "
                "Do not recommend starting, stopping, or changing "
                "prescription medication. Encourage professional review "
                "for concerning findings.\n\n"
                f"USER QUESTION:\n{user_question}\n\n"
                f"EXTRACTED DOCUMENT TEXT:\n"
                f"{document_text if document_text else 'No PDF/TXT text extracted.'}"
            )
        }]

        for img in image_files[:3]:
            try:
                data_url = image_to_data_url(img)
                if data_url:
                    content.append({
                        "type": "image_url",
                        "image_url": {"url": data_url},
                    })
            except Exception:
                st.warning(f"Could not prepare image: {img.name}")

        # Show analysis progress and run the request.
        with st.spinner(
            "Groq is reviewing the uploaded information. Please wait..."
        ):
            try:
                response = client.chat.completions.create(
                    model=MODEL,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You provide educational health information "
                                "only. Be careful, transparent, and readable. "
                                "Never fabricate data or claim certainty "
                                "when evidence is incomplete."
                            ),
                        },
                        {
                            "role": "user",
                            "content": content,
                        },
                    ],
                    temperature=0.2,
                    max_tokens=1800,
                    timeout=90,
                )

                answer = response.choices[0].message.content or (
                    "The model returned an empty response. Please try again."
                )

                st.session_state.analysis_result = answer
                st.session_state.last_question = user_question
                st.session_state.last_files = [f.name for f in files]

                if extraction_errors:
                    st.session_state.extraction_errors = extraction_errors
                else:
                    st.session_state.extraction_errors = []

            except Exception as exc:
                st.error("Groq could not complete the analysis.")
                st.code(str(exc))
                st.info(
                    "Check your API key, model access, internet connection, "
                    "API limits, and whether the selected model supports "
                    "image inputs if you uploaded images."
                )


# --------------------------------------------------
# ANALYSIS RESULTS
# --------------------------------------------------
if st.session_state.analysis_result:
    st.markdown("""
    <div class="report-header">
        <span class="report-label">HEALTHCARE REPORT</span>
        <h2 style="margin-top:14px; margin-bottom:4px;">
            Analysis & Explanation
        </h2>
        <p style="color:#bdcbe0; font-size:15px; margin:0;">
            Review the explanation below and verify important findings
            with a qualified healthcare professional.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.last_files:
        file_names = ", ".join(st.session_state.last_files)
        st.markdown(
            f'<div class="section-card"><strong>📎 Uploaded files</strong>'
            f'<p>{escape(file_names)}</p></div>',
            unsafe_allow_html=True,
        )

    with st.container(border=True):
        st.markdown("### AI Analysis")
        st.markdown(st.session_state.analysis_result)

    errors = st.session_state.get("extraction_errors", [])
    if errors:
        with st.expander("Document reading notes"):
            for error in errors:
                st.warning(error)

    st.markdown("""
    <div class="success-seal">
        ✓ Analysis generated. Review the explanation carefully;
        AI-generated interpretations can contain errors.
    </div>
    """, unsafe_allow_html=True)

    download_text = (
        "HEALTHCARE REPORT ANALYSIS\n\n"
        f"Question:\n{st.session_state.last_question}\n\n"
        f"Files:\n{', '.join(st.session_state.last_files)}\n\n"
        f"Analysis:\n{st.session_state.analysis_result}\n\n"
        "Disclaimer: Educational information only. "
        "Not a medical diagnosis or substitute for professional care."
    )

    st.download_button(
        "⬇️ Download Analysis (.txt)",
        data=download_text,
        file_name="healthcare_report_analysis.txt",
        mime="text/plain",
        use_container_width=True,
    )

st.divider()
st.markdown(
    '<p class="small-note" style="text-align:center;">'
    'Healthcare AI Assistant · Powered by Groq · Educational use only'
    '</p>',
    unsafe_allow_html=True,
)
