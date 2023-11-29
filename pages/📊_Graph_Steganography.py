import streamlit as st
import pandas as pd

st.title('Graph Steganography')

# Function Initialization
def encode (pesan):
  pesan_biner = ''.join([format(ord(i), "08b") for i in pesan])

  n = len(pesan_biner)

  bstring = ""
  counter = 0
  arrResult = []
  for i in range(n):
    bstring += pesan_biner[i]
    counter+=1
    if counter == 7:
      counter = 0
      arrResult.append(int(bstring, 2))
      bstring = ""
    elif n-i == 1:
      arrResult.append(int(bstring, 2))
  arrResult.append(n)
  return arrResult

def decode(secret):
  secret, n = secret[:-1], secret[-1]

  binary_strings = [format(num, '07b') if index < len(secret) - 1
    else format(num, '03b') for index, num in enumerate(secret)]

  total_length = sum(len(binary_str) for binary_str in binary_strings)
  padding_needed = n - total_length

  if padding_needed > 0:
      binary_strings[-1] = '0' * padding_needed + binary_strings[-1]

  binary_strings = ''.join(binary_strings)
  
  binary_groups = [binary_strings[i:i+8] for i in range(0, len(binary_strings), 8)]

  char_string = ''.join([chr(int(group, 2)) for group in binary_groups])

  return char_string

# Session state Initialization
if "encode" not in st.session_state:
  st.session_state["encode"] = False
if "decode" not in st.session_state:
  st.session_state["decode"] = False
if "dataEncodeGraph" not in st.session_state:
  st.session_state["dataEncodeGraph"] = ""

tab1, tab2 = st.tabs(["Encode", "Decode"])

### Encode ###
with tab1:
  st.subheader("Encode")
  pesan = st.text_input('Pesan (plainteks)', placeholder="Silahkan isi pesan.")

  if pesan != "":
    barChart = st.toggle('Tampilkan grafik batang')
    lineChart = st.toggle('Tampilkan grafik garis')

    x_label = st.text_input('Label sumbu-x')
    y_label = st.text_input('Label sumbu-y')
    color = st.color_picker('Pilih warna')

    if st.button("Encode", type="primary"):
      st.session_state["encode"] = not st.session_state["encode"]
      load_text = st.text("")
      load_text.write(":orange[Mohon tunggu..]")
      st.session_state["dataEncodeGraph"] = encode(pesan)
      
      chart_data = pd.DataFrame(
        {
            x_label: list(range(1, len(st.session_state["dataEncodeGraph"])+1)),
            y_label: st.session_state["dataEncodeGraph"],
        }
      )

      if barChart:
        st.bar_chart(chart_data, x=x_label, y=y_label, color=color)
      if lineChart:
        st.line_chart(chart_data, x=x_label, y=y_label, color=color)
      
      load_text.write(':green[Pesan berhasil di encode.]')

### Decode ###
with tab2:
  st.subheader("Decode")

  encoded_pesan = st.text_input('Pesan hasil encode (cipherteks)', str(st.session_state["dataEncodeGraph"])[1:-1], placeholder="Silahkan isi pesan. (format: 2, 3, 4, 5)")

  if encoded_pesan != "":
    if st.button("Decode", type="primary"):
      st.session_state["decode"] = not st.session_state["decode"]
      load_text = st.text("")
      load_text.write(":orange[Mohon tunggu..]")
      decoded_data = decode([int(i) for i in encoded_pesan.split(',')])
      load_text.write(':green[Pesan berhasil di decode.]')
      load_text.write(f":green[Hasil ekstraksi pesan: {decoded_data} ]")