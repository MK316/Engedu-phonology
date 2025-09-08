import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📘 16-Week Course Schedule", layout="wide")
st.title("📘 Course Overview")

tab1, tab2 = st.tabs(["Schedule", "TBA"])

with tab1:
    st.caption("Textbooks: T1. A course in phonetics, T2. Applied English Phonology (AEP)")
    # Table header
    table_header = "| Date | Chapter | Keywords | Assignments & Activities | Remark |\n"
    table_divider = "|------|---------|----------|---------------------------|--------|\n"
    
    # Start on Tuesday, September 2, 2025
    start_date = datetime(2025, 9, 2)
    
    
    
    # ✅ STEP 1: Fill only the weeks you want — here, Week 3 has data (Sept. 16 & 18)
    schedule_content = {
        "2025-09-04": ["Ch. 1", "Syllabus, Course overview, Vocal anatomy", "","Summary note-taking"],

        "2025-09-11": ["Ch. 1 (Phonetics pdf)", "Articulation and acoustics", "📌 Lecture video on LMS (Ch1 Acoustics)", "Summary note-taking"],

        "2025-09-18": ["", "", "", ""],

        "2025-09-25": ["", "", "", ""],

        "2025-10-02": ["", "", "", "🔴 Quiz1 #1"],

        "2025-10-09": ["", "", "", ""],

        "2025-10-16": ["", "", "", ""],

        "2025-10-23": ["", "", "", ""],

        "2025-10-30": ["", "", "", ""],

        "2025-11-06": ["", "", "", ""],

        "2025-11-13": ["", "", "", ""],

        "2025-11-20": ["", "", "", ""],

        "2025-11-27": ["", "", "", ""],

        "2025-12-04": ["", "", "", ""],

        "2025-12-11": ["", "", "", ""],

        "2025-12-18": ["", "", "", "🔴 Final exam"]
    }
    
    # ✅ STEP 2: Build the markdown table
    table_md = ""
    
    table_md = ""
    
    for week in range(16):
        # --- choose emoji/tag first ---
        if 7 <= (week + 1) <= 11:
            emoji, tag = "💙", " (Academic trip) 〽️ 〽️ 〽️ 〽️ 〽️ 〽️ 〽️"
        else:
            emoji, tag = "🗓️", ""
    
        # --- label & header (once) ---
        week_label = f"**{emoji} Week {week + 1:02d}{tag}**"
        table_md += f"\n{week_label}\n\n"
        table_md += table_header + table_divider
    
        # --- dates for this week ---
        tuesday  = start_date + timedelta(weeks=week)
        thursday = tuesday + timedelta(days=2)
    
        # --- format date (red for Oct 7 & 9 only) ---
        def format_date(d):
            s = d.strftime("%Y-%m-%d")
            if s in ("2025-10-07", "2025-10-09"):
                return f"<span style='color:red'>{d.strftime('%b. %d')}</span>"
            return d.strftime("%b. %d")
    
        # --- fetch content once for each date ---
        tue_data = schedule_content.get(tuesday.strftime("%Y-%m-%d"),  ["", "", "", ""])
        thu_data = schedule_content.get(thursday.strftime("%Y-%m-%d"), ["", "", "", ""])
    
        # --- append EXACTLY TWO ROWS (do not append anywhere else) ---
        table_md += f"| {format_date(tuesday)}  | {tue_data[0]} | {tue_data[1]} | {tue_data[2]} | {tue_data[3]} |\n"
        table_md += f"| {format_date(thursday)} | {thu_data[0]} | {thu_data[1]} | {thu_data[2]} | {thu_data[3]} |\n"
    

    # ✅ STEP 3: Display it
    st.markdown(table_md, unsafe_allow_html=True)



# ---------------- Tab 2: Syllabus / Course Info ----------------

