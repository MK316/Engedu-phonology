import streamlit as st
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="📘 16-Week Course Schedule", layout="wide")
st.title("📘 Course Overview")

tab1, tab2, tab3 = st.tabs(["Schedule", "Syllabus", "TBA"])

with tab1:

    # Table header
    table_header = "| Date | Chapter | Keywords | Assignments & Activities | Remark |\n"
    table_divider = "|------|---------|----------|---------------------------|--------|\n"
    
    # Start-of-term date (used to compute the first Thursday)
    start_date = datetime(2025, 9, 2)  # Tuesday
    # Compute the first Thursday in (or after) the start week
    # Monday=0 ... Thursday=3
    first_thursday = start_date + timedelta(days=(3 - start_date.weekday()) % 7)

    # Fill only Thursdays you care about
    schedule_content = {
        "2025-09-04": ["Ch. 1", "Syllabus, Course overview", "Grouping", "Reading AEP Chapter 1"],
        "2025-09-11": ["", "", "", ""],
        "2025-09-18": ["", "", "", ""],
        "2025-09-25": ["", "", "", ""],
        "2025-10-02": ["", "", "", "🔴 Midterm #1"],
        "2025-10-09": ["", "", "", ""],   # Thursday (will be red)
        "2025-10-16": ["", "", "", ""],
        "2025-10-23": ["", "", "", ""],
        "2025-10-30": ["", "", "", ""],
        "2025-11-06": ["", "", "", ""],
        "2025-11-13": ["", "", "", ""],
        "2025-11-20": ["", "", "", ""],
        "2025-11-27": ["", "", "", ""],
        "2025-12-04": ["", "", "", ""],
        "2025-12-11": ["", "", "", ""],
        "2025-12-18": ["", "", "", "🔴 Final exam"],
    }
    
    def format_date(d: datetime) -> str:
        s = d.strftime("%Y-%m-%d")
        # highlight only Oct. 9
        if s == "2025-10-09":
            return f"<span style='color:red'>{d.strftime('%b. %d')}</span>"
        return d.strftime("%b. %d")

    # Build the markdown
    table_md = ""
    for week in range(16):
        # Tag per week (unchanged)
        if 7 <= (week + 1) <= 11:
            emoji, tag = "💙", " (Academic trip) 〽️ 〽️ 〽️ 〽️ 〽️ 〽️ 〽️"
        else:
            emoji, tag = "🗓️", ""
        week_label = f"**{emoji} Week {week + 1:02d}{tag}**"
        table_md += f"\n{week_label}\n\n"
        table_md += table_header + table_divider

        # Thursday of this week
        thursday = first_thursday + timedelta(weeks=week)

        # Row for Thursday only
        thu_data = schedule_content.get(thursday.strftime("%Y-%m-%d"), ["", "", "", ""])
        table_md += (
            f"| {format_date(thursday)} | {thu_data[0]} | {thu_data[1]} "
            f"| {thu_data[2]} | {thu_data[3]} |\n"
        )

    # Show the table
    st.markdown(table_md, unsafe_allow_html=True)

# ---------------- Tab 2: Syllabus / Course Info ----------------
with tab2:
    st.markdown("## 💦 **Phonology & English Education (Fall 2025)**")
    st.caption("Quick syllabus overview")

    # --- Top section: key facts + QR/link ---
    col1, col2 = st.columns([3, 2], vertical_alignment="top")

    with col1:
        st.markdown(
            """
            **• Instructor:** Miran Kim (Professor, Rm# 301-316)  
            **• Meeting Schedule:** Thursdays (6–7:50 pm)  
            **• Digital classroom:** [MK316.github.io](https://MK316.github.io)  — course apps & resources  
            **• LMS:** rec.ac.kr/gnu  
            **• Classroom:** 301-317 
            """,
        )

    with col2:
        QR_URL = "https://github.com/MK316/english-phonetics/raw/main/pages/images/qr_phonetics.png"
        st.image(QR_URL, caption="Digital classroom QR", width=150)  # set width in pixels
    st.divider()

    # --- Course overview ---
    st.markdown("### 📝 Course overview")
    st.markdown(
        """
        This course provides an introduction to English phonology, focusing on the sound system of English, and the rules and principles that govern its pronunciation. Additionally, it covers fundamental concepts in phonetics to help students grasp the articulation of English sounds (Basic Phonetics). Designed specifically for students preparing for careers in English education, this course equips future English teachers with the necessary skills to articulate, describe, and teach English pronunciation effectively. Throughout the course, students will explore phonological differences between Korean and English. This knowledge will enable them to anticipate and address the specific challenges Korean learners might face when learning English pronunciation, enhancing their teaching effectiveness.
        """
    )


    # --- Textbook & Software ---
    st.markdown("### 📚 Textbook & Software")
    tb, sw = st.columns(2)
    with tb:
        st.markdown(
            """
            **Textbook**  
            1. Applied English Phonology (4th edition) by Mehmet Yavaʂ (2020), Wiley Blackwell. (Selected chapters)
            2. A Course in Phonetics (7th edition) by Ladefoged P. & Keith J. (2014), CENGAGE. 
            
            (Selected chapters; Pdf files will be posted online.)  
            * Note: There can be additional readings from other textbooks. Pdf files will be posted online.

            """
        )
    with sw:
        st.markdown(
            """
            **Software**  
            Praat — download: <http://www.fon.hum.uva.nl/praat/download_win.html>
            """
        )

    st.divider()

    # --- Evaluation table ---
    st.markdown("### ✅ Evaluation")
    data = [
        ["Attendance & class participation", "10%", "Unexcused absence (−1); late check-in (−0.2)"],
        ["Quizzes", "30%", "TBA"],
        ["Exam", "30%", "Final exam"],
        ["Assignments", "30%", "Group activities: Exercises (5), Transcription (5)"],
    ]
    df = pd.DataFrame(data, columns=["Component", "Percentage", "Notes"])

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Component": st.column_config.Column(width="medium"),
            "Percentage": st.column_config.Column(width=90),
            "Notes": st.column_config.Column(width="large"),
        },
    )

    st.info(
        "Note: The course schedule can be subject to change. "
        "Most updates will be posted here."
    )
