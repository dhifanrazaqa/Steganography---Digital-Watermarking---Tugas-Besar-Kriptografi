import streamlit as st
from PIL import Image
import pandas as pd
from io import StringIO

def load_image(image_path):
  return Image.open(image_path)

def save_image(image, output_path):
  image.save(output_path)

def embed_watermark(image, watermark_path):
  # Load watermark image
  image = load_image(image)
  watermark = load_image(watermark_path)

  # mbed watermark using LSB method
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

def extract_watermark(embedded_image):
  # Extract watermark by retrieving LSB from each pixel
  embedded_image = load_image(embedded_image)

  watermark_size = embedded_image.size[0]

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

st.title('Digital Watermarking')

tab1, tab2 = st.tabs(["Embed", "Ekstrak"])

#### Embed WM ###
with tab1:
  st.subheader('Embed Watermark')
  st.markdown(':red[Ukuran gambar original dan watermark harus sama]')
  uploaded_img_file = st.file_uploader("Pilih gambar original!", type=['png'])
  uploaded_wm_file = st.file_uploader("Pilih gambar watermark!", type=['png'])

  if uploaded_wm_file is not None and uploaded_img_file is not None:
    load_text = st.text("")
    load_text.write(":orange[Mohon tunggu..]")
    st.image(embed_watermark(uploaded_img_file, uploaded_wm_file), output_format="PNG")
    load_text.write(":green[Hasil image dengan watermark, silahkan klik kanan dan Save as]")

#### Ekstrak WM ###
with tab2:
  st.subheader('Ekstrak Watermark')
  uploaded_extract_file = st.file_uploader("Pilih gambar yang ingin diekstrak!", type=['png'])

  if uploaded_extract_file is not None:
    load_text = st.text("")
    load_text.write(":orange[Mohon tunggu..]")
    st.image(extract_watermark(uploaded_extract_file))
    load_text.write(":green[Watermark:]")