import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the API key from .env  
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Function to get Gemini response
def get_nutrition_response(user_input):
    prompt = f"""
    You are a certified nutritionist chatbot. Please help the user based on their question below.

    Question: {user_input}

    Respond in a friendly, clear, and helpful way. Suggest healthy foods, diet tips, or explanations as needed.
    """
    response = model.generate_content(prompt)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Nutrition Assistant", page_icon="🥦")
st.title("🥦 Gemini-Powered Nutrition Assistant")
st.write("Ask me anything about your diet, nutrition, or healthy food choices!")

user_input = st.text_area("Enter your question or concern here:", height=150)

if st.button("Get Advice"):
    if user_input.strip() == "":
        st.warning("Please enter a question first.")
    else:
        with st.spinner("Thinking..."):
            output = get_nutrition_response(user_input)
            st.success("Here's some advice:")
            st.write(output)



#this is the change i made in app.py