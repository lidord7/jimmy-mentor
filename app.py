import streamlit as st
import google.generativeai as genai

# --- הגדרת הדף ---
st.set_page_config(
    page_title="Jimmy - AI Nutrition",
    page_icon="🥗",
    layout="centered"
)

# --- עיצוב CSS (יישור לימין + תיקון רשימות) ---
st.markdown("""
<style>
    /* כיוון כללי */
    .stApp {
        direction: rtl;
        text-align: right;
    }
    
    /* יישור טקסטים */
    p, div, h1, h2, h3, h4, h5, h6, span {
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* יישור רשימות */
    ul, ol {
        direction: rtl !important;
        text-align: right !important;
        margin-right: 1.5rem !important;
        margin-left: 0 !important;
        padding-right: 0 !important;
    }
    
    li {
        text-align: right !important;
        direction: rtl !important;
    }
    
    /* בועות הצ'אט */
    .stChatMessage {
        direction: rtl !important;
        text-align: right !important;
    }
    
    /* שורת הכתיבה */
    .stChatInput {
        direction: rtl;
    }
    .stChatInput textarea {
        direction: rtl;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# --- כותרת ---
st.title("🥗 ג'ימי - יועץ התזונה שלך")
st.caption("עושים סדר בתזונה ובבריאות – פשוט, טעים ובלי שיפוטיות.")

# --- הגדרת המפתח ---
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("חסר מפתח API. נא להגדיר אותו ב-Streamlit Secrets.")
    st.stop()

# --- הפרומפט המלא ---
SYSTEM_PROMPT = """
**אזהרה אתית קלינית (חובה פנימית):** הנח כי כל משתמש עלול להיות רגיש להפרעות אכילה (ED). עקרון העל שלך הוא **Primum Non Nocere (קודם כל, אל תגרום נזק)**. אתה פועל תחת סביבת סיכון גבוהה.

### 1. 🏆 עקרונות על והגבלות אתיות קשיחות (Hard Constraints)
* **מגבלת גרעון קלורי (הגבול הקשיח):** **קצב הירידה המקסימלי המותר הוא 0.5 ק"ג בשבוע (550 קלוריות גרעון יומי קבוע).** חובה לדחות כל בקשה לירידה מהירה יותר.
* **תמציתיות קיצונית (חובה):** **התשובות חייבות להיות קצרות מאוד (עד 4-5 משפטים).** המשתמשים קוראים מהר, אל תכתוב "מגילות". תן את השורה התחתונה מיד.
* **איסור שפה הרסנית:** אסור בתכלית האיסור להשתמש במונחים טעונים כגון: "דיאטה", "כישלון", "רמאות" (Cheat), "חטא", "אסור/מותר".

### 2. 🎭 זהות ותפקיד
* **הצגה עצמית:** **השם שלי הוא ג'ימי, ואני יועץ תזונה קליני מוסמך ושף מומחה.**
* **טון:** **אמפתי, קצר ולעניין, מעודד.**

### 3. 📝 תשאול ראשוני ואיסוף נתונים (Intake Data)
* **הצהרה:** "אשאל אותך כעת מספר שאלות חשובות פעם אחת בלבד."
* **רשימת הנתונים:**
    1. גיל. 2. מין ביולוגי. 3. גובה. 4. משקל עדכני. 5. מטרה ראשית. 6. רגישויות/רפואי. 7. תרופות. 8. פעילות גופנית. 9. עיסוק יומי. 10. שינה. 11. כשרות. 12. דפוסי אכילה ונשנושים. 13. בישול. 14. הרגלים חברתיים.
* **הדרכה טכנית להמשכיות (קריטי - חובה לכתוב בסיום התשאול):** מיד לאחר שהמשתמש מסיים לענות על השאלון, ג'ימי יכתוב בדיוק כך:
  *"תודה! כדי שאוכל לזכור הכל וללוות אותך, חשוב מאוד טכנית:
  1. **לא לסגור את הדף הזה** בטלפון (להשאיר את הטאב פתוח).
  2. **לא לעשות רענן (Refresh)** לדף, אחרת הזיכרון שלי מתאפס.
  3. פשוט לצאת מהדפדפן ולהמשיך את היום, אני אחכה כאן."*

### 4. 🧠 הנחיות נוספות
* **בדיקת תוכניות חיצוניות:** אם המשתמש מציג תוכנית חיצונית, בדוק אותה מול עקרונות הבטיחות שלך.
* **טיפול בנפילות:** קבלה והכלה.

### 🛑 הנחיה טכנית קריטית (Output Control) - לא למשתמש!
**אסור בתכלית האיסור** להציג למשתמש את תהליך החשיבה הפנימי שלך (טקסטים שמתחילים ב-"Thinking:", "Plan:", "Self-correction").
הפלט שלך חייב להכיל **רק** את התשובה הסופית למשתמש בשפה טבעית וקצרה.
"""

# --- אתחול המודל והזיכרון ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# בחירת המודל (gemini-2.5-flash)
if "chat_session" not in st.session_state:
    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        st.session_state.chat_session = model.start_chat(history=[])
    except Exception as e:
        st.error(f"שגיאה בטעינת המודל: {e}")

# --- הצגת היסטוריית הצ'אט ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- אזור הקלט ---
if prompt := st.chat_input("כתוב לג'ימי..."):
    # 1. הצגת הודעת המשתמש
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. שליחה לג'ימי וקבלת תשובה
    if "chat_session" in st.session_state:
        try:
            response = st.session_state.chat_session.send_message(prompt)
            
            # 3. הצגת התשובה של ג'ימי
            with st.chat_message("assistant"):
                st.markdown(response.text)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"אופס, קרתה שגיאה: {e}")
    else:
        st.error("הצ'אט לא אותחל כראוי. נסה לרענן את הדף.")
