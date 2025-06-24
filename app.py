import streamlit as st
import google.generativeai as genai
import os
import io
from dotenv import load_dotenv
from PIL import Image


# Load the API key from .env  
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel('gemini-2.0-flash-001')

# Function to get Gemini response for TEXT and IMAGE
def get_nutrition_response(user_input: str, image=None):
    
    prompt = f"""
    You are a certified nutritionist chatbot. Please help the user based on their question below.
    Question: {user_input}
    List the calories of food items in the image if image provided.
    Respond in a friendly, clear, and helpful way. Suggest healthy foods, diet tips, or explanations as needed.
    """
    inputs = [prompt]

    # re-encoding image to base64-encoded bytes
    if image:
        image_bytes = io.BytesIO()
        image.save(image_bytes, format='PNG')
        image_bytes = image_bytes.getvalue()
        inputs.append({
            "mime_type": "image/png", "data": image_bytes
        })

    response = model.generate_content(inputs)
    return response.text

# Streamlit UI
st.set_page_config(page_title="Nutrition Assistant", page_icon="🥦")
st.title("🥦 Gemini-Powered Nutrition Assistant")
st.write("Ask me anything about your diet, nutrition, or healthy food choices!")

# Text Input
user_input = st.text_area("Enter your question or concern here:", height=150)

# Image Uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Preview Uploaded Image
if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_container_width=True)


# Submit Button
if st.button("Get Advice"):
    if not user_input and not uploaded_image:
        st.warning("Please enter your query or upload an image.")
    else:
        user_input = user_input or "Analyze this image for nutritional content."
        
        with st.spinner("Analyzing..."):
            output = get_nutrition_response(user_input, image if uploaded_image else None)
        
        st.write(output)
