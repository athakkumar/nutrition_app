import streamlit as st
import google.generativeai as genai
import os
import io
from dotenv import load_dotenv
from PIL import Image

# Load API key and configure Gemini
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Streamlit page settings
st.set_page_config(
    page_title="Nutrition Assistant",
    page_icon="🥦",
    layout="centered"
)

# Custom CSS for compact layout & button polish
st.markdown("""
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .stTextArea textarea {
        min-height: 100px !important;
    }
    .st-expanderContent {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
    img {
        max-height: 250px;
        object-fit: contain;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        font-size: 16px;
        padding: 0.5em 2em;
        margin-top: 0.5em;
        border: none;
        outline: none;
        box-shadow: none;
        transition: background-color 0.2s ease-in-out;
    }
    .stButton button:hover {
        background-color: #45a049;
        color: white;
    }
    .stButton button:focus, .stButton button:active {
        background-color: #45a049 !important;
        color: white !important;
        border: none;
        outline: none;
        box-shadow: 0 0 0 3px rgba(76, 175, 80, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# App Title
st.title("🥦 AI Nutrition Assistant")
st.caption("Ask about meals, calories, or upload food images for estimates!")

# Main input section
st.markdown("### 📝 Your Question")
user_input = st.text_area(
    label="",
    placeholder="e.g. Suggest a healthy dinner with high protein.",
    height=80
)

uploaded_image = st.file_uploader("📷 Upload Food Image", type=["jpg", "jpeg", "png"])
image = None
if uploaded_image:
    image = Image.open(uploaded_image)

# Submit button stays right below inputs
submit = st.button("🍽️ Get Nutrition Advice")

# Image preview moved to sidebar
if uploaded_image:
    with st.sidebar:
        st.markdown("### 📸 Preview")
        st.image(image, use_container_width=True, caption=None)



# Gemini Call Function
def get_nutrition_response(user_input: str, image=None):
    prompt = f"""
    You are a certified nutritionist chatbot. Help the user with the question below.

    Question: {user_input}

    If an image is provided, identify food items and estimate calories.
    Respond in a friendly, helpful, and clear way.
    """
    inputs = [prompt]

    if image:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        inputs.append({"mime_type": "image/png", "data": image_bytes})

    try:
        response = model.generate_content(inputs)
        return response.text
    except Exception as e:
        return f"⚠️ Error: {str(e)}"

# Submit Button
output = None
if submit:
    if not user_input and not uploaded_image:
        st.warning("Please enter a question or upload an image.")
    else:
        user_input = user_input or "Analyze this image for nutritional content."
        with st.spinner("Analyzing... 🥗"):
            output = get_nutrition_response(user_input, image)

# Display Gemini Response (collapsible)
if output:
    with st.expander("🧠 AI's Response", expanded=True):
        st.write(output)
