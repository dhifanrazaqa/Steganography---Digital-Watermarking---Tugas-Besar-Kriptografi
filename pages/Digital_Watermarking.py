import streamlit as st
from PIL import Image
import pandas as pd
from io import StringIO

def load_image(image_path):
    return Image.open(image_path)

def save_image(image, output_path):
    image.save(output_path)

def embed_watermark(image, watermark_path):
    # Step 1: Load watermark image
    watermark = load_image(watermark_path)

    # Step 2: Embed watermark using LSB method
    image_data = image.getdata()
    watermark_data = watermark.getdata()
    embedded_data = []
    # len(image_data) = widht * height
    for i in range(len(image_data)):
        pixel = list(image_data[i])
        watermark_pixel = list(watermark_data[i % len(watermark_data)])  # Repeating watermark if it's smaller than the image
        # R value
        pixel[0] = (pixel[0] & 0xFE) | (watermark_pixel[0] >> 7)
        # G value
        pixel[1] = (pixel[1] & 0xFE) | ((watermark_pixel[0] >> 6) & 0x01)
        # B value
        pixel[2] = (pixel[2] & 0xFE) | ((watermark_pixel[0] >> 5) & 0x03)
        embedded_data.append(tuple(pixel))

    # Create a new image with the embedded watermark
    embedded_image = Image.new('RGB', image.size)
    embedded_image.putdata(embedded_data)

    return embedded_image

def extract_watermark(embedded_image, watermark_size):
    # Step 3: Extract watermark by retrieving LSB from each pixel
    embedded_data = embedded_image.getdata()
    extracted_data = []

    for i in range(len(embedded_data)):
        pixel = list(embedded_data[i])
        extracted_byte = ((pixel[0] & 0x01) << 7) | ((pixel[1] & 0x01) << 6) | ((pixel[2] & 0x03) << 5)
        extracted_data.append(extracted_byte)

    # Create a new image with the extracted watermark
    extracted_watermark = Image.new('L', (watermark_size, watermark_size))
    extracted_watermark.putdata(extracted_data)

    return extracted_watermark

def extract_watermark_from_png(embedded_image_path, watermark_size):
    # Load the embedded image (PNG format)
    embedded_image = load_image(embedded_image_path)

    # Extract watermark using the specified size
    extracted_watermark = extract_watermark(embedded_image, watermark_size)

    # Save the extracted watermark image
    save_image(extracted_watermark, 'wa_extract.png')

st.title('Digital Watermarking')

uploaded_file = st.file_uploader("Choose a file", type=['png','jpg'])
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    st.write(stringio)

    # To read file as string:
    string_data = stringio.read()
    st.write(string_data)

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)