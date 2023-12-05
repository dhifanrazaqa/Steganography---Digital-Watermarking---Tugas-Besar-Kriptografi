import streamlit as st
import numpy as np
from PIL import Image

# Function Initialization
def Encode(src, message):

    img = Image.open(src, 'r')
    width, height = img.size
    array = np.array(list(img.getdata()))

    if img.mode == 'RGB':
        n = 3
    elif img.mode == 'RGBA':
        n = 4
    total_pixels = array.size//n

    message += "$t3g0"
    b_message = ''.join([format(ord(i), "08b") for i in message])
    req_pixels = len(b_message)

    if req_pixels > total_pixels:
        print("ERROR: Need larger file size")

    else:
        index=0
        for p in range(total_pixels):
            for q in range(0, 3):
                if index < req_pixels:
                    array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
                    index += 1

    array=array.reshape(height, width, n)
    enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    return enc_img

def Decode(src):
  img = Image.open(src, 'r')
  array = np.array(list(img.getdata()))

  if img.mode == 'RGB':
      n = 3
  elif img.mode == 'RGBA':
      n = 4
  total_pixels = array.size//n

  hidden_bits = ""
  for p in range(total_pixels):
      for q in range(0, 3):
          hidden_bits += (bin(array[p][q])[2:][-1])

  hidden_bits = [hidden_bits[i:i+8] for i in range(0, len(hidden_bits), 8)]

  message = ""
  for i in range(len(hidden_bits)):
      if message[-5:] == "$t3g0":
          break
      else:
          message += chr(int(hidden_bits[i], 2))
  if "$t3g0" in message:
      return message[:-5]
  else:
      return ""

st.title("Image Steganography")
tab1, tab2 = st.tabs(["Embed", "Ekstrak"])

#### Embed Pesan ###
with tab1:
  st.subheader("Embed Pesan")
  pesan = st.text_input('Pesan yang ingin disembunyikan', placeholder="Silahkan isi pesan.")
  uploaded_embed_file = st.file_uploader("Pilih gambar!", type=['png'])
  
  if pesan is not "" and uploaded_embed_file is not None:
    if st.button("Embed", type="primary"):
      load_text = st.text("")
      load_text.write(":orange[Mohon tunggu..]")
      st.image(Encode(uploaded_embed_file, pesan), output_format="PNG")
      load_text.write(":green[Hasil image setelah disisipi pesan, silahkan klik kanan Save as]")

#### Ekstrak Pesan ###
with tab2:
  st.subheader("Ekstrak Pesan")
  uploaded_extract_file = st.file_uploader("Pilih gambar yang ingin diekstrak!", type=['png'])

  if uploaded_extract_file is not None:
    load_text = st.text("")
    load_text.write(":orange[Mohon tunggu..]")
    load_text.write(f":green[Hasil ekstraksi pesan: {Decode(uploaded_extract_file)} ]")
