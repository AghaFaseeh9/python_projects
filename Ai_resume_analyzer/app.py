# app.py
import streamlit as st
from utils import (
    extract_text_from_pdf,
    compute_ats_score,
    generate_suggestions,
    clean_text,
)
from io import BytesIO

# --- Custom CSS for better look ---


st.set_page_config(page_title="AI Resume Analyzer", layout="centered", page_icon="📄")

st.title("📄 AI-Powered Resume Analyzer")
st.caption(
    "Upload a PDF resume and paste the job description to get an ATS-style score and actionable suggestions."
)

with st.sidebar:
    st.header("How to use")
    st.markdown(
        """
        1. **Upload your resume** (PDF).
        2. **Paste the job description**.
        3. Click **Analyze**.
        """
    )
    st.info("💡 *Tip: Use clear bullet points and quantify achievements.*")
    st.markdown("---")

# --- File upload and JD input ---
resume_file = st.file_uploader("📤 Upload resume (PDF)", type=["pdf"])
jd_text = st.text_area(
    "📝 Paste the job description (or key responsibilities/requirements)", height=200
)

# --- New: Resume text preview toggle ---
show_preview = st.checkbox("Show full resume text preview", value=False)

analyze_btn = st.button("🚀 Analyze Resume")

if analyze_btn:
    if not resume_file:
        st.error("Please upload a PDF resume first.")
    elif not jd_text.strip():
        st.error("Please paste a job description.")
    else:
        with st.spinner("Extracting text from resume..."):
            resume_bytes = resume_file.read()
            resume_text = extract_text_from_pdf(BytesIO(resume_bytes))
            if not resume_text or not resume_text.strip():
                st.warning(
                    "Couldn't extract text reliably from this PDF. Try a different resume PDF (some PDFs are scanned images)."
                )
                st.stop()

        st.success("Resume text extracted successfully!")

        st.subheader("📊 Summary")
        st.write("**Resume preview (first 800 chars):**")
        st.code(
            resume_text[:800] + ("..." if len(resume_text) > 800 else ""),
            language="markdown",
        )
        if show_preview:
            st.write("**Full Resume Text:**")
            st.code(resume_text, language="markdown")

        score, details = compute_ats_score(resume_text, jd_text)
        st.metric(
            label="ATS-style score",
            value=f"{score}%",
            delta=None,
            help="How well your resume matches the job description",
        )

        st.subheader("🔍 Keyword Analysis")
        cols = st.columns(2)
        with cols[0]:
            st.write("**Matched keywords**")
            st.success(
                ", ".join(details.get("matches", [])[:50]) or "No matches found."
            )
        with cols[1]:
            st.write("**Top missing keywords (from JD)**")
            st.warning(
                ", ".join(details.get("missing", [])[:50]) or "No missing keywords."
            )

        st.subheader("🛠 Suggestions")
        suggestions = generate_suggestions(resume_text, details)
        if suggestions:
            for s in suggestions:
                st.write("- ", s)
        else:
            st.info("Your resume looks great! No major suggestions.")

        st.subheader("📈 Diagnostics")
        st.write(f"**Keyword match rate:** {details.get('keyword_score', 0)}%")
        st.write(f"**Quantified lines score:** {details.get('quantify_score', 0)}%")
        st.write(f"**Resume length (words):** {details.get('length_words', 0)}")

        # --- New: Download cleaned resume text ---
        st.markdown("---")
        st.download_button(
            label="⬇️ Download Cleaned Resume Text",
            data=clean_text(resume_text),
            file_name="cleaned_resume.txt",
            mime="text/plain",
            help="Download the extracted and cleaned resume text for your records.",
        )

        # --- New: Simple word cloud ---
        try:
            from wordcloud import WordCloud
            import matplotlib.pyplot as plt

            st.subheader("☁️ Resume Word Cloud")
            wc = WordCloud(width=600, height=300, background_color="white").generate(
                resume_text
            )
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wc, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        except ImportError:
            st.info(
                "Install `wordcloud` and `matplotlib` for word cloud visualization: `pip install wordcloud matplotlib`"
            )
