import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post, generate_variations, improve_hook
import time

st.set_page_config(page_title="LinkedIn Post Generator", page_icon="💼", layout="wide")

# ---------- State ----------
if "dark" not in st.session_state:
    st.session_state.dark = False

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Styling ----------
def apply_theme():
    if st.session_state.dark:
        bg = "#0f172a"
        card = "#020617"
        text = "#e5e7eb"
        accent = "#3b82f6"
        border = "#1e293b"
    else:
        bg = "#f5f7fb"
        card = "#ffffff"
        text = "#111827"
        accent = "#2563eb"
        border = "#e5e7eb"

    st.markdown(f"""
    <style>
        body {{ background: {bg}; color: {text}; }}
        .block-container {{ padding: 2.5rem 3rem; }}
        .card {{
            background: {card};
            border: 1px solid {border};
            border-radius: 14px;
            padding: 1.5rem;
            margin-top: 1.2rem;
        }}
        .toolbar {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: .6rem;
        }}
        .actions {{
            display: flex;
            gap: .4rem;
        }}
        .stButton>button {{
            background: {accent};
            color: white;
            border-radius: 8px;
            font-weight: 500;
        }}
    </style>
    """, unsafe_allow_html=True)

apply_theme()

# ---------- Sidebar ----------
with st.sidebar:
    st.title("Settings")
    st.toggle("Dark Mode", key="dark")
    st.divider()
    st.subheader("Post History")
    for post in st.session_state.history[::-1][:5]:
        st.caption(post[:120] + "...")

# ---------- Header ----------
st.title("LinkedIn Post Generator")

# ---------- Controls ----------
fs = FewShotPosts()
tags = fs.get_tags()

st.markdown('<div class="card">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    tag = st.selectbox("Topic", tags)
with c2:
    length = st.selectbox("Length", ["Short", "Medium", "Long"])
with c3:
    lang = st.selectbox("Language", ["English", "Hinglish"])

if st.button("Generate"):
    with st.spinner("Crafting your post..."):
        time.sleep(0.6)
        post = generate_post(length, lang, tag)
        st.session_state.history.append(post)
        st.session_state.current = post
        st.session_state.pop("variations", None)

st.markdown('</div>', unsafe_allow_html=True)

# ---------- Unified Response Panel ----------
if "current" in st.session_state:

    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False

    st.markdown('<div class="card">', unsafe_allow_html=True)

    left, right = st.columns([6, 2])

    with left:
        st.markdown("### Your Post")

    with right:
        a1, a2, a3 = st.columns(3)
        with a1:
            if st.button("Edit"):
                st.session_state.edit_mode = not st.session_state.edit_mode
        with a2:
            if st.button("Improve"):
                with st.spinner("Improving..."):
                    st.session_state.current = improve_hook(st.session_state.current)
        with a3:
            st.download_button("⬇", st.session_state.current, "post.txt")

    if st.session_state.edit_mode:
        edited = st.text_area("", st.session_state.current, height=220, label_visibility="collapsed")
        st.session_state.current = edited
    else:
        st.code(st.session_state.current, language=None)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Variations ----------
if "current" in st.session_state:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("Generate Variations"):
        with st.spinner("Creating variations..."):
            text = generate_variations(st.session_state.current)
            st.session_state.variations = text.split("\n\n")

    if "variations" in st.session_state:
        st.subheader("Choose the best version")
        for i, v in enumerate(st.session_state.variations, 1):
            st.markdown(f"**Version {i}**")
            st.code(v.strip(), language=None)

    st.markdown('</div>', unsafe_allow_html=True)
