import streamlit as st

st.markdown("### Phonology & English Education")
st.caption(
    "Fall 2025. This space provides lecture slides, short videos, and interactive apps for "
    "practicing English phonetics and phonology. We’ll cover articulatory and acoustic basics, "
    "IPA skills, and classroom applications tailored for English education majors."
)


col_l, col_c, col_r = st.columns([1,2,1])
with col_c:
    st.image("https://github.com/MK316/classmaterial/raw/main/images/bg01.png",
             caption="Teaching is one of the best ways to learn.", width=300)
    st.image("https://github.com/MK316/classmaterial/raw/main/images/engedu-qr.png",
             caption="Access QR", width=100)
