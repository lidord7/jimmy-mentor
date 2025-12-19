import streamlit as st
import google.generativeai as genai

st.title("🛠️ בדיקת מודלים זמינים")

# בדיקת מפתח
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
    st.success("✅ מפתח API נמצא, מנסה להתחבר לגוגל...")

    try:
        # בקשה מגוגל לקבל את כל המודלים הזמינים למפתח הזה
        st.write("---")
        st.subheader("רשימת המודלים הפתוחים עבורך:")
        
        found_any = False
        for m in genai.list_models():
            # אנחנו מחפשים רק מודלים שיודעים לייצר טקסט (generateContent)
            if 'generateContent' in m.supported_generation_methods:
                st.code(m.name) # מדפיס את השם המדויק שצריך להעתיק
                found_any = True
        
        if not found_any:
            st.error("❌ לא נמצאו מודלים זמינים. ייתכן שהמפתח לא תקין או שאין הרשאות.")
            
    except Exception as e:
        st.error(f"שגיאה בהתחברות לגוגל: {e}")
else:
    st.error("חסר מפתח API ב-Secrets.")
