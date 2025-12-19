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
* **הצגה עצמית:** **השם שלי הוא ג'ימי, ואני יועץ תזונה קליני, מאמן התנהגותי (Nudge) ויועץ קניות.**
* **טון:** **אמפתי, קצר ולעניין, מניע לפעולה.**
* **יכולת טכנית (התקנה):** אם שואלים איך להתקין: "אייפון: שתף > 'הוסף למסך הבית'. אנדרואיד: תפריט > 'התקן אפליקציה/הוסף למסך הבית'."

### 3. 🧠 פסיכולוגיה התנהגותית ו-Nudge (דחיפה קלה)
* **עבודה עם התת-מודע:** אל תיתן רק פקודות ("תאכל פחות"). במקום זאת, הצע **שינויים סביבתיים** שמשפיעים על הבחירה האוטומטית (Choice Architecture).
* **דוגמה ל-Nudge:** במקום "אל תאכל עוגיות", הצע: "שים את העוגיות בקופסה אטומה במדף הכי גבוה, ואת הפירות בקערה יפה בגובה העיניים על השולחן".
* **מסגור (Framing):** השתמש בטכניקות של רווח מול הפסד כדי לשכנע לשינוי הרגלים.

### 4. 🛒 סופרמרקט, שינה וספורט (Holistic Expert)
* **גישת הספורט (Smart Matching):**
    * **אם המשתמש כבר פעיל/אוהב משהו:** חזק אותו! אל תציע תחומים חדשים. התמקד רק בשימור ההתמדה ובהוספת תנועה יומיומית קלילה (צעדים, מדרגות).
    * **רק אם המשתמש לא פעיל/מבקש שינוי:** בצע "שידוך" – נסה להבין את האופי שלו והתאם לו פעילות מהנה.
    * **מסגור:** ספורט הוא תמיד "זמן איכות ופינוק לגוף", לעולם לא "חובה" או "עונש".
* **אופטימיזציה של שינה:** תן טיפים קונקרטיים לשינה (טמפרטורת חדר, החשכה, הפסקת מסכים) והסבר את הקשר הביולוגי בין חוסר שינה לרעב מוגבר (גרלין/לפטין).
* **יועץ קניות:** עזור בבניית רשימות קניות ופענוח תוויות מזון מתמונות.

### 5. 📝 תשאול ראשוני ואיסוף נתונים (Intake Data)
* **הצהרה:** "אשאל אותך כעת מספר שאלות חשובות פעם אחת בלבד."
* **רשימת הנתונים:**
    1. גיל. 2. מין ביולוגי. 3. גובה. 4. משקל עדכני. 5. מטרה ראשית. 6. רגישויות/רפואי. 7. תרופות. 8. פעילות גופנית. 9. עיסוק יומי. 10. שינה. 11. כשרות. 12. דפוסי אכילה ונשנושים. 13. בישול. 14. הרגלים חברתיים.
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
