import streamlit as st
from streamlit_image_comparison import image_comparison
from rembg import remove
from PIL import Image
import cv2
import numpy as np
from io import BytesIO
import os

# set page config
st.set_page_config(page_title="Image-Comparison Example", layout="centered")
    
# Function to remove the background from an image
def remove_background_from_image(image):
    img_bytes = image.read()
    result = remove(img_bytes)

    # Remove the border from the processed image
    img = Image.open(BytesIO(result))
    width, height = img.size
    img = img.crop((1, 1, width - 1, height - 1))
    bio = BytesIO()
    img.save(bio, format="PNG")
    result = bio.getvalue()

    return Image.open(BytesIO(result))
# Function to overlay the processed image over a selected background
def overlay_image(background, overlay):
    b_h, b_w = background.shape[:2]
    o_h, o_w = overlay.shape[:2]

    # Resize overlay to fit the background
    if b_h != o_h or b_w != o_w:
        overlay = cv2.resize(overlay, (b_w, b_h), interpolation=cv2.INTER_AREA)

    # Create a mask for overlay (transparent areas)
    overlay_gray = cv2.cvtColor(overlay, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(overlay_gray, 1, 255, cv2.THRESH_BINARY)
    mask_inv = cv2.bitwise_not(mask)

    # Background for the processed image
    background_part = cv2.bitwise_and(background, background, mask=mask_inv)
    overlay_part = cv2.bitwise_and(overlay, overlay, mask=mask)

    # Combine the images
    combined = cv2.add(background_part, overlay_part)
    return combined

#function to display before and after image
def display_images(image1, image2):
    col1, col2 = st.columns(2)
    with col1:
        st.image(image1, use_column_width=True)
    with col2:
        st.image(image2, use_column_width=True)
        
def main():
    st.title("Car Background Replacement")
    
    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Studios")
        background_options = ["Studio 1", "Studio 2", "Studio 3", "Studio 4"]
        selected_background = st.selectbox("Select Background", background_options)

        if selected_background == "Studio 1":
            background = cv2.imread("background1.jpg")
        elif selected_background == "Studio 2":
            background = cv2.imread("background2.jpg")
        elif selected_background == "Studio 3":
            background = cv2.imread("background3.jpg")
        elif selected_background == "Studio 4":
            background = cv2.imread("background4.jpg")

        st.image(background, use_column_width=True)
        
        
        
    with col2:
        st.header("Before and After")

        # Image uploader
        uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])

        if uploaded_file is not None:
            # Display uploaded image
            st.image(uploaded_file, caption="Original Image", use_column_width=True)

            # Remove background from image
            processed_image = remove_background_from_image(uploaded_file)

            # Convert processed image to NumPy array for overlay
            processed_image_np = np.array(processed_image.convert("RGB"))

            # Load the background image for the overlay
            background_image = np.array(Image.open(f"background{background_options.index(selected_background) + 1}.jpg"))

            # Overlay the processed image on the background
            final_image = overlay_image(background_image, processed_image_np)

            # Slider for before and after view
            # before_after_slider = st.slider("Before vs After", min_value=0, max_value=100, value=50)

            # Blend the original and final images based on slider value
            # original_image = np.array(Image.open(uploaded_file))
            # blended_image = cv2.addWeighted(original_image, before_after_slider / 100.0, final_image, 1 - (before_after_slider / 100.0), 0)
            
            st.image(processed_image, caption="Before vs After", use_column_width=True)

            # Download button for processed image
            buffer = BytesIO()
            processed_image.save(buffer, format="PNG")
            buffer.seek(0)
            
            st.download_button(label="Download Processed Image", data=buffer, file_name="processed_image.png", mime="image/png")
   
    # Slider for before and after view
    if uploaded_file is not None and final_image is not None:
        # render image-comparison
        image_comparison(
            img1=Image.open(uploaded_file),
            img2=Image.fromarray(final_image),
        )
    
if __name__ == "__main__":
    main()

