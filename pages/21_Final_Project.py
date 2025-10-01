# Final_project.py
# Place this file as a page in your multi-page Streamlit app.
# It fetches and displays a Markdown file that lives on GitHub.

import re
import requests
import streamlit as st
from urllib.parse import urlparse

st.set_page_config(page_title="📄 Final Project — Markdown Viewer", layout="centered")

st.title("📄 Final Project")
st.caption("This page renders a Markdown file hosted on GitHub.")

# ── 1) Set your Markdown file URL here ─────────────────────────────────────────
# You can use EITHER a normal GitHub "blob" URL OR a raw.githubusercontent.com URL.
GITHUB_MD_URL = "https://github.com/MK316/Engedu-phonology/blob/main/pages/project.md"
# Example raw form:
# GITHUB_MD_URL = "https://raw.githubusercontent.com/USER/REPO/BRANCH/path/to/your.md"

# (Optional) make it editable from the sidebar during development:
with st.sidebar:
    st.header("Settings")
    md_url = st.text_input("GitHub Markdown URL", GITHUB_MD_URL)
    refresh = st.button("🔄 Refresh")


# ── 2) Helpers: normalize URL & fetch file ─────────────────────────────────────
def to_raw_github(url: str) -> str:
    """
    Convert a standard GitHub file URL (…github.com/.../blob/…) to a
    raw URL (…raw.githubusercontent.com/…).
    If it's already raw, return as is.
    """
    if "raw.githubusercontent.com" in url:
        return url
    if "github.com" in url and "/blob/" in url:
        parts = url.split("github.com/")[-1].split("/blob/")
        owner_repo = parts[0]          # e.g., USER/REPO
        branch_path = parts[1]         # e.g., BRANCH/path/to/file.md
        return f"https://raw.githubusercontent.com/{owner_repo}/{branch_path}"
    return url  # fallback (will likely fail if it's not reachable)


@st.cache_data(show_spinner=False)
def fetch_markdown(raw_url: str) -> str:
    resp = requests.get(raw_url, timeout=15)
    resp.raise_for_status()
    return resp.text


def prefix_relative_image_paths(md_text: str, raw_url: str) -> str:
    """
    If the Markdown contains relative image links, prefix them with the base
    path of the raw URL so images load correctly in Streamlit.
    """
    # Compute base path of the file
    parsed = urlparse(raw_url)
    base = raw_url.rsplit("/", 1)[0]  # drop filename

    # Replace image links that do NOT start with http(s) or data:
    # ![alt](relative/path.png) -> ![alt](<base>/relative/path.png)
    pattern = r'!\[([^\]]*)\]\(((?!https?://|data:)[^)]+)\)'
    return re.sub(pattern, lambda m: f"![{m.group(1)}]({base}/{m.group(2)})", md_text)


# ── 3) Load & render ──────────────────────────────────────────────────────────
raw_url = to_raw_github(md_url)

try:
    if refresh:
        fetch_markdown.clear()  # bust the cache on demand

    with st.spinner("Loading Markdown from GitHub…"):
        md_text = fetch_markdown(raw_url)
        md_text = prefix_relative_image_paths(md_text, raw_url)

    st.markdown(md_text, unsafe_allow_html=False)

    with st.expander("🔗 Source info"):
        st.write("**Raw URL:**", raw_url)

except requests.HTTPError as e:
    st.error(f"HTTP error while fetching the file: {e}")
except requests.RequestException as e:
    st.error(f"Network error while fetching the file: {e}")
except Exception as e:
    st.error(f"Unexpected error: {e}")
