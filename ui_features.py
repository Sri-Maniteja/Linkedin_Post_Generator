import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post, generate_variations
import time

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="💼", layout="wide")

# ------------------ State ------------------
if "dark" not in st.session_state:
    st.session_state.dark = False

if "history" not in st.session_state:
    st.session_state.history = []

# ------------------ Styling ------------------
def apply_theme():
    if st.session_state.dark:
        bg = "#0f172a"
        panel = "#020617"
        text = "#e5e7eb"
        accent = "#3b82f6"
    else:
        bg = "#f5f7fb"
        panel = "#ffffff"
        text = "#111827"
        accent = "#2563eb"

    st.markdown(f"""
    <style>
        body {{ background: {bg}; color: {text}; }}
        .main {{ background: {panel}; border-radius: 14px; padding: 2rem; }}
        .stButton>button {{ background: {accent}; color: white; border-radius: 10px; }}
        .block-container {{ padding-top: 2rem; }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ------------------ Sidebar ------------------
with st.sidebar:
    st.title("Settings")
    st.toggle("Dark Mode", key="dark")
    st.divider()
    st.subheader("Post History")
    for i, post in enumerate(st.session_state.history[::-1][:5], 1):
        st.markdown(f"**Post {i}**")
        st.caption(post[:120] + "...")

# ------------------ Main UI ------------------
st.title("LinkedIn Post Generator")

length_options = ["Short", "Medium", "Long"]
language_options = ["English", "Hinglish"]

fs = FewShotPosts()
tags = fs.get_tags()

c1, c2, c3 = st.columns(3)

with c1:
    tag = st.selectbox("Topic", tags)
with c2:
    length = st.selectbox("Length", length_options)
with c3:
    lang = st.selectbox("Language", language_options)

# ------------------ Generate ------------------
if st.button("Generate"):
    with st.spinner("Crafting your post..."):
        time.sleep(0.8)
        post = generate_post(length, lang, tag)
        st.session_state.history.append(post)
        st.session_state.current = post
        st.session_state.pop("variations", None)

# ------------------ Response Panel ------------------
if "current" in st.session_state:

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    colA, colB, colC, colD = st.columns([6, 1, 1, 1])

    with colA:
        st.markdown("### Your Post")

    with colB:
        if st.button("Edit"):
            st.session_state.edit_mode = not st.session_state.edit_mode

    with colC:
        st.download_button("TXT", st.session_state.current, "post.txt")

    with colD:
        st.markdown(
            """<a href="https://www.linkedin.com/feed/" target="_blank">
            <button>LinkedIn</button></a>""",
            unsafe_allow_html=True
        )

    if st.session_state.edit_mode:
        edited = st.text_area(
            "", st.session_state.current, height=220, label_visibility="collapsed"
        )
        st.session_state.current = edited
    else:
        st.code(st.session_state.current, language=None)

# ------------------ Post Variations ------------------
if "current" in st.session_state:

    st.divider()

    if st.button("Generate Variations"):
        with st.spinner("Creating variations..."):
            text = generate_variations(st.session_state.current)
            st.session_state.variations = text.split("\n\n")

    if "variations" in st.session_state:
        st.subheader("Choose the best version")

        for i, variant in enumerate(st.session_state.variations, 1):
            st.markdown(f"**Version {i}**")
            st.code(variant.strip(), language=None)
