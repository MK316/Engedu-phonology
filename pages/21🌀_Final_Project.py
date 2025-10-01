# Final_project.py
# Multi-page Streamlit app page with 3 tabs:
# 1) Render a Markdown file from GitHub
# 2) Play audio files hosted on GitHub (with per-file descriptions)
# 3) Display a PDF hosted on GitHub

import os
import re
import requests
import streamlit as st
from urllib.parse import urlparse, quote

st.caption("This page renders resources (Markdown, audio, PDF) hosted on GitHub.")

# ──────────────────────────────────────────────────────────────────────────────
# 1) Configure your GitHub assets here
GITHUB_MD_URL = "https://github.com/MK316/Engedu-phonology/blob/main/pages/project.md"

AUDIO_FILES = [
    "https://github.com/MK316/Engedu-phonology/raw/main/pages/audio/M01.wav",
    "https://github.com/MK316/Engedu-phonology/raw/main/pages/audio/M02.wav",
    "https://github.com/MK316/Engedu-phonology/raw/main/pages/audio/F01.wav",
    "https://github.com/MK316/Engedu-phonology/raw/main/pages/audio/F02.wav",
    "https://github.com/MK316/Engedu-phonology/raw/main/pages/audio/rainbow_native_female_elevenlabs.mp3",
    "https://github.com/MK316/Engedu-phonology/raw/main/pages/audio/rainbow_native_male_elevenlabs.mp3",
]

# 🔎 Add/edit descriptions here (key = filename only)
DESCRIPTIONS = {
    "M01.wav": "Learner #1 (Male01).",
    "M02.wav": "Learner #2 (Male02).",
    "F01.wav": "Learner #3 (Female01)",
    "F02.wav": "Learner #4 (Female02).",
    "rainbow_native_female.mp3": "Synthesized native female voice — Rainbow passage.",
    "rainbow_native_male.mp3": "Synthesized native male voice — Rainbow passage.",
}

GITHUB_PDF_URL = "https://github.com/MK316/Engedu-phonology/blob/main/pages/audio/rainbow-passsage.pdf"

# Optional: make URLs editable from the sidebar during development
with st.sidebar:
    st.header("Settings")
    md_url = st.text_input("GitHub Markdown URL", GITHUB_MD_URL)
    st.divider()
    st.write("Audio files (comma-separated)")
    audio_csv = st.text_area(
        "GitHub audio URLs",
        value=", ".join(AUDIO_FILES),
        height=120,
        help="Paste one or more GitHub URLs separated by commas.",
    )
    pdf_url = st.text_input("GitHub PDF URL", GITHUB_PDF_URL)
    refresh = st.button("🔄 Refresh cache")

# Turn comma-separated audio into a list
AUDIO_FILES = [u.strip() for u in audio_csv.split(",") if u.strip()]

# ──────────────────────────────────────────────────────────────────────────────
# 2) Helpers
def to_raw_github(url: str) -> str:
    if not url:
        return url
    if "raw.githubusercontent.com" in url:
        return url
    if "github.com" in url and "/blob/" in url:
        parts = url.split("github.com/")[-1].split("/blob/")
        owner_repo = parts[0]
        branch_path = parts[1]
        return f"https://raw.githubusercontent.com/{owner_repo}/{branch_path}"
    return url

@st.cache_data(show_spinner=False)
def fetch_text(raw_url: str) -> str:
    resp = requests.get(raw_url, timeout=15)
    resp.raise_for_status()
    return resp.text

def prefix_relative_image_paths(md_text: str, raw_url: str) -> str:
    if not raw_url:
        return md_text
    base = raw_url.rsplit("/", 1)[0]
    pattern = r'!\[([^\]]*)\]\(((?!https?://|data:)[^)]+)\)'
    return re.sub(pattern, lambda m: f"![{m.group(1)}]({base}/{m.group(2)})", md_text)

def pdf_iframe_url(github_url: str) -> str:
    raw = to_raw_github(github_url)
    return f"https://drive.google.com/viewerng/viewer?embedded=true&url={quote(raw, safe='')}"

def filename_from_url(u: str) -> str:
    """Return just the file name (used to look up descriptions)."""
    return os.path.basename(urlparse(u).path)

# ──────────────────────────────────────────────────────────────────────────────
# 3) Tabs
tab1, tab2, tab3 = st.tabs(["📄 Markdown", "🔊 Audio", "📑 PDF"])

# ── Tab 1: Markdown ───────────────────────────────────────────────────────────
with tab1:
    raw_md_url = to_raw_github(md_url)
    try:
        if refresh:
            fetch_text.clear()
        with st.spinner("Loading Markdown from GitHub…"):
            md_text = fetch_text(raw_md_url)
            md_text = prefix_relative_image_paths(md_text, raw_md_url)
        st.markdown(md_text, unsafe_allow_html=False)
        with st.expander("🔗 Source info"):
            st.write("**Raw URL:**", raw_md_url)
    except requests.HTTPError as e:
        st.error(f"HTTP error while fetching the Markdown file: {e}")
    except requests.RequestException as e:
        st.error(f"Network error while fetching the Markdown file: {e}")
    except Exception as e:
        st.error(f"Unexpected error: {e}")

# ── Tab 2: Audio (with descriptions) ─────────────────────────────────────────
with tab2:
    st.subheader("Audio files from GitHub")
    if not AUDIO_FILES:
        st.info("Add GitHub audio URLs in the sidebar to list them here.")
    for i, url in enumerate(AUDIO_FILES, start=1):
        raw_audio = to_raw_github(url)
        fname = filename_from_url(url)
        desc = DESCRIPTIONS.get(
            fname,
            "No description provided. Update `DESCRIPTIONS` in the code to add one.",
        )

        st.markdown(f"**Track {i} — {fname}**")
        st.audio(raw_audio)
        st.write(desc)           # ← your text description here
        st.caption(raw_audio)    # shows the resolved raw URL
        st.divider()

# ── Tab 3: PDF ────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("PDF from GitHub")
    if not pdf_url:
        st.info("Provide a GitHub PDF URL in the sidebar.")
    else:
        try:
            viewer = pdf_iframe_url(pdf_url)
            st.components.v1.iframe(src=viewer, width=None, height=800)
            with st.expander("🔗 Source info"):
                st.write("**Raw PDF URL:**", to_raw_github(pdf_url))
        except Exception as e:
            st.error(f"Could not display the PDF: {e}")
