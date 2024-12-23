import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(
    page_title="Image Alt Text Generator",
    page_icon="🖼️"
)

def generate_alt_text(image):
    """Generate alt text using the HuggingFace Inference API"""
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": f"Bearer {st.secrets['huggingface_token']}"}
    
    # Convert image to bytes
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()
    
    try:
        response = requests.post(API_URL, headers=headers, data=image_bytes)
        result = response.json()
        return result[0]['generated_text']
    except Exception as e:
        st.error(f"Error generating alt text. Please try again.")
        return None

st.title("Image Alt Text Generator")
st.write("Upload an image to generate descriptive alt text!")

uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # Display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    
    # Generate alt text
    with st.spinner("Generating alt text..."):
        alt_text = generate_alt_text(image)
        
    if alt_text:
        st.success("Alt Text Generated!")
        st.write(alt_text)
        
        # Display HTML code
        html_code = f'<img src="{uploaded_file.name}" alt="{alt_text}" />'
        st.code(html_code, language="html")
