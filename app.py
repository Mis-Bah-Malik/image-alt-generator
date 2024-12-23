import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Image Alt Text Generator",
    page_icon="🖼️",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .success {
        color: #28a745;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

def generate_alt_text(image):
    """Generate alt text using the HuggingFace Inference API"""
    API_URL = "https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base"
    headers = {"Authorization": f"Bearer {st.secrets['api_key']}"}
    
    # Convert image to bytes
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_bytes = buffered.getvalue()
    
    response = requests.post(API_URL, headers=headers, data=image_bytes)
    return response.json()[0]['generated_text']

def main():
    # Header
    st.title("🖼️ Image Alt Text Generator")
    st.markdown("""
        Upload an image and get AI-generated alt text for better web accessibility!
        
        ### How to use:
        1. Upload your image
        2. Wait for the AI to analyze it
        3. Copy the generated alt text or HTML code
    """)
    
    # File uploader
    uploaded_file = st.file_uploader("Choose an image file", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file:
        try:
            # Display image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            with st.spinner("Generating alt text..."):
                alt_text = generate_alt_text(image)
            
            # Display results
            st.markdown("### Generated Alt Text:")
            st.success(alt_text)
            
            # HTML code
            st.markdown("### HTML Code:")
            html_code = f'<img src="{uploaded_file.name}" alt="{alt_text}" />'
            st.code(html_code, language='html')
            
            # Copy buttons
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Copy Alt Text"):
                    st.write('<p class="success">✓ Alt text copied to clipboard!</p>', 
                            unsafe_allow_html=True)
            with col2:
                if st.button("Copy HTML"):
                    st.write('<p class="success">✓ HTML code copied to clipboard!</p>', 
                            unsafe_allow_html=True)
                    
        except Exception as e:
            st.error("Error processing image. Please try again.")

if __name__ == "__main__":
    main()
