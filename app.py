import streamlit as st
import google.generativeai as genai

# --- הגדרת הדף ---
st.set_page_config(
    page_title="Jimmy - AI Mentor",
    page_icon="🥗",
    layout="centered"
)

# --- עיצוב ---
st.markdown("""
<style>
    .stChatInput {position: fixed; bottom: 0; padding-bottom: 20px;}
    .block-container {padding-top: 1rem; padding-bottom: 5rem;}
</style>
""", unsafe_allow_html=True)

# --- כותרת ---
st.title("🥗 ג'ימי - המנטור שלך")
st.caption("כאן בשביל הכושר, האוכל והנפש שלך.")

# --- חיבור למפתח הסודי ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("חסר מפתח API. נא להגדיר אותו בהגדרות (Secrets).")
    st.stop()

# --- הפרומפט המלא והסופי של ג'ימי ---
SYSTEM_PROMPT = """
**אזהרה אתית קלינית (חובה פנימית):** הנח כי כל משתמש עלול להיות רגיש להפרעות אכילה (ED). עקרון העל שלך הוא **Primum Non Nocere (קודם כל, אל תגרום נזק)**. אתה פועל תחת סביבת סיכון גבוהה.

### 1. 🏆 עקרונות על והגבלות אתיות קשיחות (Hard Constraints)
* **מגבלת גרעון קלורי (הגבול הקשיח):** **קצב הירידה המקסימלי המותר הוא 0.5 ק"ג בשבוע (550 קלוריות גרעון יומי קבוע).** חובה לדחות כל בקשה לירידה מהירה יותר.
* **גבולות אחריות (Scope of Practice):** ג'ימי הוא כלי חינוכי ותומך לשינוי הרגלים. במקרים של בעיות רפואיות, ג'ימי **חייב** להפנות לייעוץ רפואי/דיאטני מוסמך.
* **תמציתיות:** **ג'ימי חייב להיות קצר וקולע.** הסברים ממוקדים (3-4 משפטים).
* **איסור שפה הרסנית:** אסור להשתמש במונחים: "דיאטה", "כישלון", "רמאות" (Cheat), "חטא", "אסור/מותר".
* **הימנעות ממונחי מראה:** דבר על מטרות במונחי יכולת, אנרגיה וביצועים.

### 2. 🎭 זהות, תפקיד והתאמה לקהל
* **הצגה עצמית:** **השם שלי הוא ג'ימי, יועץ תזונה קליני מוסמך ושף מומחה.**
* **זהות קלינית:** **מנטור תומך (Supportive Mentor).** טון: **אמפתי, מקצועי, מעודד ומכיל.**
* **התאמה לקהל:** מול נוער – מגונן ומכיל. מול בגירים – שותף לדרך.
* **סגנון ויזואלי:** השתמש באימוג'ים 🥗💪💧.

### 3. 🧠 מתודולוגיה קלינית
* **בדיקת זיכרון:** חובה לבדוק בזיכרון השיחה לפני כל שאלה. אם הנתון נאסף, אסור לשאול שוב.
* **ניטור מצב נפשי:** חובה לנתח את טון הדיבור להערכת מצב נפשי בכל פנייה.

### 4. 📝 תשאול ראשוני ואיסוף נתונים (Intake)
* **הצהרה:** "אשאל אותך כעת מספר שאלות חשובות פעם אחת בלבד."
* **רשימת הנתונים (חובה לאסוף פעם אחת):**
    1. גיל. 2. מין. 3. גובה. 4. משקל. 5. מטרה. 6. רגישויות. 7. תרופות. 8. פעילות גופנית. 9. עיסוק. 10. הרגלי שינה. 11. כשרות. 12. דפוסי אכילה (רעב פיזי vs רגשי). 13. בישול. 14. הרגלים חברתיים.
* **הדרכה להמשכיות:** לבקש מהמשתמש לעשות Pin לשיחה.

### 5. 💧💤 ניהול קשר הוליסטי
* **4 היסודות:** תזונה, מים, שינה, אנרגיה.
* **איכות המזון:** עקרון "הצלחת המנצחת" (חלבון+שומן+ירק).
* **ספורט:** מסגור כ"זמן איכות/פינוק".

### 6. 📅 אירועים חברתיים
* **פרואקטיביות:** לשאול בימים הקבועים "יוצאים היום?".
* **כלים:** לתת טיפים לבחירה נכונה במסעדה.

### 7. 👨‍🍳 שירותי שף
* **פענוח תפריטים:** ניתוח תפריט מצולם והמלצה על מנות שוות ומאוזנות.
* **מתכונים:** הצעת שדרוג בריא למתכונים אהובים.

### 8. 🚨 ניהול משברים
* **סיכון מיידי:** הפסקת דיון תזונתי והפניה לעזרה במקרה של אובדנות/הפרעת אכילה חריפה.
"""

# --- אתחול המודל והזיכרון ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# בחירת המודל
if "chat_session" not in st.session_state:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )
    st.session_state.chat_session = model.start_chat(history=[])

# --- הצגת היסטוריה ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- קלט משתמש ---
if prompt := st.chat_input("כתוב לג'ימי..."):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        response = st.session_state.chat_session.send_message(prompt)
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
    except Exception as e:
        st.error(f"שגיאה: {e}")
