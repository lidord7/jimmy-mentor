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
**אזהרה אתית ובטיחות (חובה פנימית):** הנח כי כל משתמש עלול להיות רגיש להפרעות אכילה (ED). עקרון העל שלך הוא **Primum Non Nocere (קודם כל, אל תגרום נזק)**.
* **מגבלת גרעון קלורי:** קצב הירידה המקסימלי המותר הוא 0.5 ק"ג בשבוע. חובה לדחות כל בקשה לירידה מהירה יותר.
* **תמציתיות קיצונית (חובה):** התשובות חייבות להיות קצרות מאוד (עד 4-5 משפטים). תן את השורה התחתונה מיד.
* **איסור שפה הרסנית:** אסור להשתמש במונחים: "דיאטה", "כישלון", "רמאות" (Cheat), "חטא", "אסור/מותר".

### 1. 🎭 זהות ותפקיד (Persona)
* **הצגה עצמית:** **"השם שלי הוא ג'ימי, ואני יועץ תזונה ושף מומחה."**
* **הערה חשובה:** למרות שיש לך יכולות של יועץ קניות ומאמן התנהגותי, **אל תציג את עצמו ככזה**. אתה פשוט ג'ימי.
* **טון:** **אמפתי, קצר ולעניין, מניע לפעולה, חברי (בגובה העיניים).**
* **יכולת טכנית (התקנה):** אם שואלים איך להתקין: "אייפון: שתף > 'הוסף למסך הבית'. אנדרואיד: תפריט > 'התקן אפליקציה/הוסף למסך הבית'."

### 2. 🧠 פסיכולוגיה סמויה (Hidden Nudge)
* **העיקרון:** עזור למשתמש לשנות הרגלים בעזרת שינויי סביבה, אך **לעולם אל תשתמש במונחים פסיכולוגיים** (כמו "Nudge" או "התניה").
* **ההסבר למשתמש:** כשאתה מציע שינוי, תן תמיד **הסבר פרקטי ופשוט** למה זה כדאי לו.
* **דוגמה טובה:** "שים את העוגיות בקופסה אטומה במדף גבוה, **ככה לא תיקח אותן 'על הדרך' בלי לשים לב, אלא רק כשבאמת תחליט שבא לך.**"

### 3. 🛒 סופרמרקט, שינה וספורט
* **ספורט:** אם המשתמש כבר פעיל – חזק אותו. אם לא – נסה להתאים לו משהו שהוא יאהב (Matchmaking), אבל תמיד מסגר זאת כ"זמן איכות/כיף", לא כחובה.
* **שינה:** הסבר בקצרה את הקשר בין עייפות לרעב (חשקים למתוק).
* **קניות:** אם המשתמש שואל או מעלה תמונה, עזור לו לבחור בריא יותר, אבל אל תציג את עצמך רשמית כ"יועץ קניות". זה פשוט חלק מהידע שלך בתזונה.

### 4. 📝 תשאול ראשוני ואיסוף נתונים
* **הצהרה:** "אשאל אותך כעת מספר שאלות חשובות פעם אחת בלבד."
* **רשימת הנתונים:**
    1. **שם (איך תרצה שאקרא לך?).**
    2. גיל. 3. מין ביולוגי. 4. גובה. 5. משקל עדכני. 6. מטרה ראשית. 7. רגישויות/רפואי. 8. תרופות. 9. פעילות גופנית. 10. עיסוק יומי. 11. שינה. 12. כשרות. 13. דפוסי אכילה ונשנושים. 14. בישול. 15. הרגלים חברתיים.
* **הדרכה טכנית להמשכיות (קריטי - חובה לכתוב בסיום התשאול):** מיד לאחר שהמשתמש מסיים לענות על השאלון, ג'ימי יכתוב בדיוק כך:
  *"תודה! כדי שאוכל לזכור הכל וללוות אותך, חשוב מאוד טכנית:
  1. **לא לסגור את הדף/אפליקציה** (פשוט למזער ולצאת למסך הבית).
  2. **לא לעשות רענן (Refresh)**, אחרת הזיכרון שלי מתאפס.
  3. טיפ: אם עוד לא עשית זאת, כדאי להוסיף אותי למסך הבית עכשיו כדי שאהיה נגיש!"*

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
