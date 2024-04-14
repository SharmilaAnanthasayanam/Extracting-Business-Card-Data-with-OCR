import streamlit as st
import database
import hashlib

#Getting user email and password
st.subheader(":green[Login Page]")
login_email = st.text_input("email")
login_password = st.text_input("Password", type = "password")
login_button = st.button(":red[Login]")
st.markdown('To create new account please <a href="/signup" target="_self">sign up</a>', unsafe_allow_html=True)

#password authentication and moving to bizcard page
if login_button:
  hash_login_password = hashlib.md5(login_password.encode()).hexdigest()
  output = database.authenticate_user(login_email,hash_login_password)
  if output[0]:
    username = output[1]
    st.session_state["username"] = username.title()
    st.switch_page("pages/bizcard.py")
  else:
    st.warning(output[1])




