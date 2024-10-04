import os
from rembg import remove
from PIL import Image

def remove_background_from_images(input_dir, output_dir):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through all files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".jpeg") or filename.endswith(".png"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Open the image
            with open(input_path, 'rb') as input_file:
                img_data = input_file.read()

            # Remove background
            result = remove(img_data)
  
            # Save the resulting image
            with open(output_path, 'wb') as output_file:
                output_file.write(result)

            print(f"Processed {filename}")

if __name__ == "__main__":
    input_directory = "Car"  # Folder containing the input images
    output_directory = "output_images"  # Folder to save output images
    remove_background_from_images(input_directory, output_directory)
