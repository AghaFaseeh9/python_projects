# utils.py
import re
from typing import List, Tuple, Dict
import pdfplumber
import spacy
import streamlit as st
from collections import Counter

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    st.error(
        "spaCy model 'en_core_web_sm' not found. Please run: "
        "`python -m spacy download en_core_web_sm` in your terminal."
    )
    nlp = None


def extract_text_from_pdf(file_path_or_buffer) -> str:
    """Extract text from PDF file-like object or path using pdfplumber."""
    text_chunks = []
    try:
        with pdfplumber.open(file_path_or_buffer) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    text_chunks.append(text)
    except Exception:
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(file_path_or_buffer)
            for p in reader.pages:
                t = p.extract_text()
                if t:
                    text_chunks.append(t)
        except Exception:
            # Return a clear message if extraction fails
            return "[ERROR] Could not extract text from PDF. Try another file."
    return "\n".join(text_chunks)


def clean_text(text: str) -> str:
    text = text or ""
    # Remove multiple spaces and weird characters
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def get_keywords(text: str, top_n: int = 30) -> List[str]:
    """Return a list of candidate keywords from text using spaCy: nouns, noun_chunks, and named entities."""
    if nlp is None:
        return []
    doc = nlp(text)
    candidates = []
    for chunk in doc.noun_chunks:
        token = chunk.text.strip().lower()
        if len(token) > 2:
            candidates.append(token)
    for ent in doc.ents:
        token = ent.text.strip().lower()
        if len(token) > 2:
            candidates.append(token)
    for token in doc:
        if token.pos_ in ("NOUN", "PROPN") and not token.is_stop and token.is_alpha:
            candidates.append(token.lemma_.lower())
    freq = Counter(candidates)
    most = [k for k, _ in freq.most_common(top_n)]
    return most


def compute_ats_score(resume_text: str, jd_text: str) -> Tuple[float, Dict]:
    """Compute a simple ATS score based on keyword overlap and heuristics.

    Returns score (0-100) and a details dict with lists of missing keywords and matches.
    """
    resume_text = clean_text(resume_text).lower()
    jd_text = clean_text(jd_text).lower()

    jd_keywords = get_keywords(jd_text, top_n=40)
    resume_keywords = get_keywords(resume_text, top_n=80)

    jd_set = set(jd_keywords)
    resume_set = set(resume_keywords)

    matches = sorted(list(jd_set & resume_set))
    missing = sorted(list(jd_set - resume_set))

    # Basic scoring: keyword match ratio + presence of numbers (quantified achievements)
    if len(jd_set) == 0:
        keyword_score = 0.0
    else:
        keyword_score = len(matches) / len(jd_set)

    # quantify_score: proportion of resume lines containing digits (simple heuristic)
    lines = [l for l in resume_text.splitlines() if l.strip()]
    if len(lines) == 0:
        quantify_score = 0.0
    else:
        num_lines_with_digits = sum(1 for l in lines if any(ch.isdigit() for ch in l))
        quantify_score = num_lines_with_digits / len(lines)

    # length penalty / bonus (very short resumes are penalized)
    words = resume_text.split()
    if len(words) < 150:
        length_factor = 0.85
    elif len(words) > 800:
        length_factor = 0.95
    else:
        length_factor = 1.0

    # combine
    raw_score = (keyword_score * 0.6 + quantify_score * 0.3) * length_factor
    final_score = round(raw_score * 100, 1)

    details = {
        "jd_keywords": jd_keywords,
        "resume_keywords": resume_keywords,
        "matches": matches,
        "missing": missing,
        "keyword_score": round(keyword_score * 100, 1),
        "quantify_score": round(quantify_score * 100, 1),
        "length_words": len(words),
    }

    return final_score, details


def generate_suggestions(resume_text: str, details: Dict) -> List[str]:
    """Create human-friendly suggestions based on analysis details."""
    suggestions = []
    missing = details.get("missing", [])
    if missing:
        suggestions.append(
            f"Consider adding {min(len(missing),6)} important keyword(s) from the job description (e.g. {', '.join(missing[:6])})."
        )
    else:
        suggestions.append(
            "Great — your resume contains most of the key terms from the job description."
        )

    # Quantify achievements recommendation
    if details.get("quantify_score", 0) < 25:
        suggestions.append(
            "Only a few bullet points contain numbers. Try quantifying achievements (e.g. 'Reduced load time by 40%' or 'Managed a team of 4')."
        )
    else:
        suggestions.append("Good use of quantified achievements — keep it up.")

    # Length advice
    lw = details.get("length_words", 0)
    if lw < 300:
        suggestions.append(
            "Your resume looks short — consider expanding with measurable achievements and relevant projects."
        )
    elif lw > 1200:
        suggestions.append(
            "Your resume is long — consider trimming repetitive items and focusing on impact."
        )

    # Actionable formatting tip
    suggestions.append(
        "Use bullet points for achievements and start bullets with action verbs ("
        + "e.g., 'Implemented', 'Designed', 'Reduced')."
    )

    return suggestions


def extract_contact_info(text: str) -> Dict[str, str]:
    """Extract email and phone number from text."""
    email = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    phone = re.search(r"\+?\d[\d\s\-()]{8,}\d", text)
    return {
        "email": email.group(0) if email else "",
        "phone": phone.group(0) if phone else "",
    }
