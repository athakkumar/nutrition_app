import streamlit as st
import google.generativeai as genai
import os
import io
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Streamlit page setup
st.set_page_config(
    page_title="Nutrition Assistant",
    page_icon="🥦",
    layout="centered"
)

# Custom CSS for UI polish
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    h1 {
        text-align: center;
        color: #4CAF50;
    }
    .stButton button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
    font-size: 16px;
    padding: 0.5em 2em;
    margin-top: 1em;
    border: none;
    outline: none;
    box-shadow: none;
    transition: background-color 0.2s ease-in-out;
    }

    .stButton button:hover {
    background-color: #45a049;
    color: white;
    }

    .stButton button:focus, 
    .stButton button:active {
    background-color: #45a049 !important;
    color: white !important;
    border: none;
    outline: none;
    box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.4); /* soft green glow */
    }
    </style>
""", unsafe_allow_html=True)


# Title and instructions
st.title("🥦 Gemini-Powered Nutrition Assistant")
st.subheader("Ask me anything about your meals, calories, or healthy food choices.")
st.caption("You can also upload a food image to get a calorie estimate!")

# User text input
user_input = st.text_area("📝 Your Question", placeholder="e.g. What should I eat for a high-protein breakfast?", height=150)

# Image upload
uploaded_image = st.file_uploader("📷 Upload a Food Image (optional)", type=["jpg", "jpeg", "png"])
image = None

if uploaded_image:
    image = Image.open(uploaded_image)
    st.image(image, caption="📸 Uploaded Image Preview", use_container_width=True)

# Nutrition function
def get_nutrition_response(user_input: str, image=None):
    prompt = f"""
    You are a certified nutritionist chatbot. Help the user based on the following question.

    User Question: {user_input}

    If an image is provided, analyze it and list any visible food items with estimated calories and total calories.
    For example:
    1. 2 Apples: 50 kcal
    2. 50grams rice: 100 kcal
    _ _ _ _ so on.
    Total calories: 150 kcal

    Also, offer health tips, diet suggestions, or related information.

    Respond in a friendly and informative way.
    """
    inputs = [prompt]

    if image:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        inputs.append({
            "mime_type": "image/png",
            "data": image_bytes
        })

    try:
        response = model.generate_content(inputs)
        return response.text
    except Exception as e:
        return f"⚠️ Oops! Something went wrong:\n\n**{str(e)}**"

# Submit button
if st.button("🍽️ Get Nutrition Advice"):
    if not user_input and not uploaded_image:
        st.warning("Please enter a question or upload an image.")
    else:
        user_input = user_input or "Analyze this image for nutritional content."

        with st.spinner("Analyzing your food... 🍳🥗🍎"):
            output = get_nutrition_response(user_input, image)

        st.markdown("### 🧠 Gemini's Response")
        st.write(output)
