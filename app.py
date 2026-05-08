import streamlit as st
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import google.generativeai as genai
import io
import random

# --- 1. CORE SYSTEM ARCHITECTURE ---
st.set_page_config(
    page_title="Luxe Literacy Pro | Developed by Simiyu Lawrence",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ENGINE: AI CONFIGURATION ---
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"AI System Error: {e}")

# --- 3. PREMIUM CSS (CRYSTAL THEME + BRANDED FOOTER) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    .stApp { background-color: #f8fafc; font-family: 'Plus Jakarta Sans', sans-serif; }

    .main-card {
        background: #ffffff;
        padding: 2.5rem;
        border-radius: 28px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.03);
        margin-bottom: 24px;
    }

    h1, h2, h3 { color: #0f172a !important; font-weight: 800 !important; }

    /* Custom Feedback Badges */
    .status-msg {
        padding: 1.25rem;
        border-radius: 18px;
        font-weight: 700;
        text-align: center;
        margin: 1rem 0;
        border: 2px solid transparent;
        animation: fadeIn 0.4s ease;
    }
    .st-success { background: #ecfdf5; color: #065f46; border-color: #10b981; }
    .st-error { background: #fff1f2; color: #9f1239; border-color: #f43f5e; }
    .st-captured { background: #f1f5f9; color: #1e293b; border-color: #cbd5e1; font-style: italic; }

    .stButton > button {
        border-radius: 14px !important;
        font-weight: 700 !important;
        background: #2563eb !important;
        color: white !important;
        transition: 0.3s ease !important;
    }

    /* SIMIYU LAWRENCE BRANDED FOOTER */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: #64748b;
        text-align: center;
        padding: 12px;
        font-size: 0.9rem;
        border-top: 1px solid #e2e8f0;
        z-index: 1000;
    }
    .footer-name { color: #2563eb; font-weight: 800; }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    </style>

    <div class="footer">
        Developed by <span class="footer-name">Simiyu Lawrence</span> | 
        Professional Software Engineer | 📞 <b>0748820547</b>
    </div>
    """, unsafe_allow_html=True)

# --- 4. DATA REPOSITORY (Expanded & Intact) ---
word_bank = [
    {"word": "Elephant", "syllable": "EL-e-phant", "sentence": "The elephant is the largest animal in the Savannah.", "pattern": "ph"},
    {"word": "Alphabet", "syllable": "AL-pha-bet", "sentence": "There are 26 letters in the alphabet.", "pattern": "ph"},
    {"word": "Dolphin", "syllable": "DOL-phin", "sentence": "A dolphin is a very smart sea animal.", "pattern": "ph"},
    {"word": "Graph", "syllable": "GRAPH", "sentence": "We drew a graph in math class.", "pattern": "ph"},
    {"word": "Knife", "syllable": "KNIFE", "sentence": "Be careful with a sharp knife.", "pattern": "kn"},
    {"word": "Three", "syllable": "THREE", "sentence": "A triangle has three sides.", "pattern": "th"}
]

# --- 5. SESSION STATE ---
if 'target_word' not in st.session_state:
    st.session_state.current_data = random.choice(word_bank)
    st.session_state.target_word = st.session_state.current_data["word"]
    st.session_state.score = 0
    st.session_state.streak = 0
    st.session_state.chat_history = []

data = st.session_state.current_data
target = st.session_state.target_word

# --- 6. SIDEBAR PROGRESS ---
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>👑 Mastery Hub</h2>", unsafe_allow_html=True)
    st.divider()
    st.metric("Total Mastered", st.session_state.score)
    st.metric("Win Streak", f"🔥 {st.session_state.streak}")
    st.divider()
    if st.button("NEW WORD", use_container_width=True):
        st.session_state.streak = 0
        del st.session_state['target_word']
        st.rerun()

# --- 7. MAIN INTERFACE ---
col_lab, col_ai = st.columns([1.1, 0.9], gap="large")

with col_lab:
    st.markdown("<h1>Literacy Laboratory</h1>", unsafe_allow_html=True)
    
    # MODULE I: PRONUNCIATION (THE CRITICAL UPDATE)
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("🔊 Step 1: Voice Verification")
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔊 HEAR REFERENCE", use_container_width=True):
            tts = gTTS(text=target, lang='en')
            audio_fp = io.BytesIO()
            tts.write_to_fp(audio_fp)
            st.audio(audio_fp)
    with c2:
        # THE MIC CAPTURE
        heard = speech_to_text(language='en', start_prompt="🎤 RECORD NOW", key='voice_cap')

    if heard:
        # FEATURE 1: SHOW WHAT WAS SPOKEN FIRST
        st.markdown(f"<div class='status-msg st-captured'>I heard you say: \"<b>{heard}</b>\"</div>", unsafe_allow_html=True)
        
        # FEATURE 2: COMPARE & PROVIDE MATCHING FEEDBACK
        if heard.lower().strip(" .?!") == target.lower():
            st.balloons()
            st.markdown("<div class='status-msg st-success'>🌟 BRILLIANT! Your pronunciation is perfect.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='status-msg st-error'>❌ TRY AGAIN! That sound doesn't match the word.</div>", unsafe_allow_html=True)
            # FEATURE 3: KEEP HINTS INTACT
            with st.expander("🔍 Need a Phonics Hint?"):
                st.write(f"Syllables: **{data['syllable']}**")
                st.write(f"Context Sentence: *\"{data['sentence']}\"*")
    st.markdown("</div>", unsafe_allow_html=True)

    # MODULE II: SPELLING (KEEPING ALL LOGIC UNCHANGED)
    st.markdown("<div class='main-card'>", unsafe_allow_html=True)
    st.subheader("✍️ Step 2: Spelling Mastery")
    u_spell = st.text_input("Type the word you practiced:").strip()
    
    if u_spell:
        if u_spell.lower() == target.lower():
            st.balloons()
            st.markdown("<div class='status-msg st-success'>✅ CORRECT! Mastery point awarded.</div>", unsafe_allow_html=True)
            if st.button("UNLOCK NEXT WORD ➡️", type="primary", use_container_width=True):
                st.session_state.score += 1
                st.session_state.streak += 1
                del st.session_state['target_word']
                st.rerun()
        else:
            st.markdown("<div class='status-msg st-error'>⚠️ WRONG SPELLING. Check the word patterns.</div>", unsafe_allow_html=True)
            if "f" in u_spell.lower() and data['pattern'] == "ph":
                st.info(f"💡 Phonics Rule: In '{target}', we use 'PH' for the /f/ sound.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 8. AI TUTOR (RECTIFIED RATE LIMIT ERROR) ---
with col_ai:
    st.markdown("<h1>AI Buddy Hub</h1>", unsafe_allow_html=True)
    st.markdown("<div class='main-card' style='height: 80vh;'>", unsafe_allow_html=True)
    chat_box = st.container(height=550, border=False)
    with chat_box:
        for m in st.session_state.chat_history:
            with st.chat_message(m["role"]):
                st.write(m["content"])

    if prompt := st.chat_input("Ask a question..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with chat_box:
            with st.chat_message("user"):
                st.write(prompt)
            with st.chat_message("assistant"):
                # RECTIFICATION BLOCK STARTS HERE
                try:
                    res = model.generate_content(f"Literacy coach for word '{target}': {prompt}")
                    st.write(res.text)
                    st.session_state.chat_history.append({"role": "assistant", "content": res.text})
                except Exception as e:
                    if "429" in str(e) or "ResourceExhausted" in str(e):
                        st.warning("⚠️ The AI is a bit busy. Please wait 1 minute before asking another question.")
                    else:
                        st.error("An unexpected error occurred. Please try again.")
                # RECTIFICATION BLOCK ENDS HERE
    st.markdown("</div>", unsafe_allow_html=True)
