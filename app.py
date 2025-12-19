import streamlit as st
import google.generativeai as genai

# --- הגדרת הדף ---
st.set_page_config(
    page_title="Jimmy - AI Mentor",
    page_icon="🥗",
    layout="centered"
)

# --- עיצוב CSS שיראה כמו אפליקציה ---
st.markdown("""
<style>
    .stChatInput {position: fixed; bottom: 0; padding-bottom: 20px;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
</style>
""", unsafe_allow_html=True)

# --- כותרת ---
st.title("🥗 ג'ימי - המנטור שלך")
st.caption("כאן בשביל הכושר, האוכל והנפש שלך.")

# --- הגדרת המפתח (סודי) ---
# אנחנו נגדיר את זה בהמשך בתוך Streamlit
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("חסר מפתח API. אנא הגדר אותו בהגדרות האפליקציה.")
    st.stop()

# --- הפרומפט המלא (כאן מדביקים את הטקסט הענק) ---
SYSTEM_PROMPT = """
העתק לכאן את כל הפרומפט הארוך שיצרנו עבור ג'ימי (מההודעה האחרונה).
פשוט תמחק את השורה הזו ותדביק את הכל בין המרכאות המשולשות.
"""

# --- אתחול המודל והזיכרון ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# בחירת המודל (משתמשים ב-Flash המהיר והחכם)
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat_session = model.start_chat(history=[])

# --- הצגת היסטוריית הצ'אט ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- אזור הקלט (איפה שהמשתמש כותב) ---
if prompt := st.chat_input("כתוב לג'ימי..."):
    # 1. הצגת הודעת המשתמש
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. שליחה לג'ימי וקבלת תשובה
    try:
        response = st.session_state.chat_session.send_message(prompt)
        
        # 3. הצגת התשובה של ג'ימי
        with st.chat_message("assistant"):
            st.markdown(response.text)
        
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
    except Exception as e:
        st.error(f"אופס, קרתה שגיאה: {e}")

