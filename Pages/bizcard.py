import easyocr
import streamlit as st
import cv2 as cv
import numpy as np
import re
import database
import json
from streamlit_lottie import st_lottie
import base64

def load_lottiefile(filepath: str):
    """Gets the file path and returns the file in dict format"""
    with open(filepath, "r", encoding="utf8") as f:
        return json.load(f)

def UI_communication(value):
      """Gets the String and displays it with the animation"""
      st.markdown(f"<h4 style='text-align: center;'>{value}</h4>", unsafe_allow_html=True)
      lottie_streamlit = load_lottiefile("Loading.json")
      st.lottie(lottie_streamlit, speed=1.0, reverse = False, height=200)

#Welcome message
st.subheader(f":orange[Welcome {st.session_state['username']}!]") 
uploaded_file = st.file_uploader("Choose a file")

loading_holder = st.empty()
if uploaded_file:
  with loading_holder.container():
    UI_communication("Loading...")

  #Image processing
  bytes_data = uploaded_file.getvalue()
  image_array = cv.imdecode(np.frombuffer(bytes_data, np.uint8), -1)
  cv.imwrite("image.png", image_array)
  file = open('image.png','rb').read()
  encoded_image = base64.b64encode(file)

  #resizing
  resized_image = cv.resize(image_array, (1000,590))

  #converting to grayscale
  gray_image = cv.cvtColor(resized_image, cv.COLOR_BGR2GRAY)

  #Character Recognition
  reader = easyocr.Reader(['en']) # specify the language 
  result = reader.readtext(gray_image)
  info = []

  for (bbox, text, prob) in result:
      info.append(text)
  info_dict = {"Phone Number":[], "Owner Name":"", "Designation": "", "Email_ID":[],
              "Website URL": "" , "Address":"", "Company":"" }
  info_dict["Owner Name"] = info[0].lower()
  info.pop(0)
  info_dict["Designation"] = info[0].lower()
  info.pop(0)
  info_copy = info.copy()
  for value in info_copy:
    mobile_pattern = r"\+?\d{1,3}-\d{1,3}-\d{1,4}"
    email_pattern = r"^[a-zA-Z0-9]+@[a-zA-Z0-9]+\.[a-zA-Z]{2,4}$"
    url_pattern = r'^(www|WWW).*\.com'
    address_pattern = r"\d+.*[A-Za-z]+(?: St.| Avenue| Rd.| Highway| Ln|\b)"
    pincode_pattern = r'\b\d{6}|\d{7}\b'
    if re.match(mobile_pattern, value):
      info_dict["Phone Number"].append(value)
      info.remove(value)
    if re.match(email_pattern, value):
      info_dict["Email_ID"] = value
      info.remove(value)
    if re.search(url_pattern, value.lower()):
      info_dict["Website URL"] = value
      info.remove(value)
    if re.match(address_pattern, value):
      info_dict["Address"] =  value
      info.remove(value)
    if re.search(pincode_pattern, value):
      info_dict["Address"] = info_dict.get("Address", "") + " " + value
      info.remove(value)
  info_dict["Company"] = " ".join(info).lower()

  loading_holder.empty()

  #Displaying fetched details
  st.write(":blue[Please find the fetched details below and feel free to edit as required]")

  info_dict["Company"]  = st.text_input(':green[Company]', info_dict["Company"].title() )
  col1, col2 = st.columns(2)
  with col1:
    info_dict["Owner Name"]  = st.text_input(':green[Owner Name]', info_dict["Owner Name"].title() )
    info_dict["Phone Number"]  = st.text_input(':green[Phone Number]',  [i.title() for i in info_dict["Phone Number"]] )
    info_dict["Website URL"]  = st.text_input(':green[Website URL]', info_dict["Website URL"] )
  with col2:
    info_dict["Designation"] = st.text_input(':green[Designation]', info_dict["Designation"].title())
    info_dict["Email_ID"]  = st.text_input(':green[Email_ID]', info_dict["Email_ID"] )
    info_dict["Address"]  = st.text_input(':green[Address]', info_dict["Address"])

  for i in ["[","]","'", " "]:
    info_dict["Phone Number"] = info_dict["Phone Number"].replace(i,"")
  info_dict["Phone Number"] = info_dict["Phone Number"].split(",")
  
  #Database operations
  card_id = database.existing(info_dict["Owner Name"], info_dict["Company"])
  if card_id:
    card_id = card_id[0][0]
    message = ""
    col1, col2, col3 = st.columns(3)
    with col1:
      clicked = st.button(":red[Update to Database]")
      if clicked:
        database.update(info_dict, card_id)
        message = "Updated data Successfully!"   
    with col2:
      clicked = st.button(":red[Delete from Database]")
      if clicked:
        database.delete(card_id)
        message = "Deleted data Successfully"
    if message:
      st.success(message, icon="✅")
  else:
    clicked = st.button(":red[Insert to Database]")
    if clicked:
      if database.get_card_id():
        card_id = database.get_card_id()[0][0] + 1
      else:
        card_id = 1
      database.insert(info_dict, card_id, encoded_image)
      st.success('Inserted data Successfully!', icon="✅")

#logout button
col1, col2 = st.columns([15,2])
with col2:
  clicked = st.button(":blue[logout]")
  if clicked:
    st.switch_page("login.py")

  # st.table(database.view_table("card_details"))
  # st.table(database.view_table("phoneno_details"))

  # data = database.get_image(info_dict["Owner Name"])
  # image = data[0][0]
  # binary_data = base64.b64decode(image)
  # image = Image.open(io.BytesIO(binary_data))
  # st.image(image)
  
  

  
