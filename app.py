import streamlit as st
from rembg import remove
from PIL import Image
import numpy as np
from io import BytesIO
from streamlit_image_comparison import image_comparison

# Set page configuration
st.set_page_config(page_title="Lightweight Image-Comparison", layout="centered")

# Function to remove the background from an image
def remove_background_from_image(image):
    img_bytes = image.read()
    result = remove(img_bytes)
    
    img = Image.open(BytesIO(result))
    bio = BytesIO()
    img.save(bio, format="PNG")
    result = bio.getvalue()
    return Image.open(BytesIO(result))

# Function to overlay the processed image over a selected background using Pillow
def overlay_image(background, overlay):
    background = background.convert("RGBA")
    overlay = overlay.convert("RGBA")

    # Resize overlay to match the background
    overlay_resized = overlay.resize(background.size)

    # Simple alpha compositing (blending) without using OpenCV
    blended_image = Image.alpha_composite(background, overlay_resized)
    return blended_image

def main():
    st.title("Car Background Replacement")

    # Load background options lazily only when selected
    background_options = ["Studio 1", "Studio 2", "Studio 3", "Studio 4"]
    selected_background = st.selectbox("Select Background", background_options)

    # Mapping of background image files to avoid loading all at once
    background_images = {
    "Studio 1": "assets/background1.jpg",
    "Studio 2": "assets/background2.jpg",
    "Studio 3": "assets/background3.jpg",
    "Studio 4": "assets/background4.jpg"
    }

    selected_background_image = st.image(Image.open(background_images[selected_background]), use_column_width=True)
    
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        # Remove background
        processed_image = remove_background_from_image(uploaded_file)
        
        # Load the selected background image
        background_image = Image.open(background_images[selected_background])
        # background_image = background_image.resize((960, 540), Image.ANTIALIAS)
        
        # Overlay processed image onto the background
        # final_image = overlay_image(background_image, processed_image)
        final_image = overlay_image(background_image, processed_image)

        # Show both the original and final processed images
        # st.image([uploaded_file, final_image], caption=["Original", "Final"], use_column_width=True)

        # Download button for the processed image
        buffer = BytesIO()
        final_image.save(buffer, format="PNG")
        buffer.seek(0)
        st.download_button(label="Download Processed Image", data=buffer, file_name="processed_image.png", mime="image/png")
        
        # render image-comparison
        image_comparison(
            img1=Image.open(uploaded_file),
            img2=final_image,
        )

if __name__ == "__main__":
    main()
