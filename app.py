import streamlit as st
import google.generativeai as genai
from logic import find_schemes
from streamlit_mic_recorder import speech_to_text # You need to pip install this!
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")


# --- CONFIGURATION ---
st.set_page_config(page_title="YojanaSetu", page_icon="🇮🇳", layout="wide")

# Configure Gemini
genai.configure(api_key=api_key)
model_ai = genai.GenerativeModel('gemini-2.5-flash')

# Initialize session state for user input if it doesn't exist
if 'user_query' not in st.session_state:
    st.session_state.user_query = ""

def get_ai_explanation(query, scheme_data, language):
    try:
        prompt = f"""
        You are 'YojanaSetu AI', a universal guide for Indian Government Welfare.
        Explain this scheme in {language} for a citizen.
        User's Need: {query}
        Scheme Data: {scheme_data}
        
        Provide 3 clear bullet points:
        1. Benefits (What is provided?)
        2. Eligibility (Who is it for?)
        3. Next Steps (How to apply?)
        """
        response = model_ai.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"

with st.sidebar:
    st.title("⚙️ Settings")
    selected_state = st.selectbox("Select Your State", ["National (All India)", "Madhya Pradesh", "Maharashtra", "Uttar Pradesh", "Delhi", "Bihar", "Rajasthan", "Karnataka", "Tamil Nadu", "West Bengal", "Gujarat"])
    language = st.selectbox("Explain in Language", ["English", "Hindi", "Marathi", "Tamil", "Punjabi", "Gujarati"])
    st.markdown("---")
    # Removed the 'Powered by' caption here as requested

st.title("🇮🇳 YojanaSetu AI")
st.markdown("Find the right government scheme in seconds. Speak or type your need.")

col1, col2 = st.columns([4, 1])

with col2:
    st.write("🎙️ Voice Search")
    text_from_voice = speech_to_text(language='en-IN', use_container_width=True, just_once=True, key='STT')
    if text_from_voice:
        st.session_state.user_query = text_from_voice

with col1:
    # BUG FIX: By using key="user_query", Streamlit stops the text box from erasing the Quick Search button clicks!
    st.text_input("Tell me what you need help with:", key="user_query")

# --- QUICK SEARCH CATEGORIES ---
st.write("Or try a quick search:")
cat_cols = st.columns(5)
categories = {
    "🎓 Education": "Student scholarship and school support",
    "🚜 Agriculture": "Farming loan and tractor support",
    "👵 Pensioners": "Old age pension and senior benefits",
    "👩 Widow/Women": "Support for widows and women empowerment",
    "🏥 Healthcare": "Medical insurance and health schemes"
}

def set_quick_search(query_text):
    st.session_state.user_query = query_text

for i, (label, query) in enumerate(categories.items()):
    with cat_cols[i]:
        st.button(label, on_click=set_quick_search, args=(query,))

# --- RESULTS DISPLAY ---
final_query = st.session_state.user_query

if final_query:
    with st.spinner(f"Searching for matches in {selected_state}..."):
        results = find_schemes(final_query, selected_state)
    
    if not results.empty:
        for index, row in results.iterrows():
            with st.expander(f"✨ {row['scheme_name']}"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.write(f"**What you get:** {row['benefits']}")
                    st.write(f"**Who is eligible:** {row['eligibility']}")
                with c2:
                    if st.button(f"Explain in {language} 🤖", key=f"btn_{index}"):
                        with st.spinner("AI is thinking..."):
                            explanation = get_ai_explanation(final_query, row.to_string(), language)
                            st.info(explanation)
                st.caption(f"Category: {row['schemeCategory']} | Level: {row['level']}")
    else:
        st.warning("No exact matches. Try different words!")