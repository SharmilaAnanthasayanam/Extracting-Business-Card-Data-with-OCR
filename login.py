import streamlit as st
import database


st.subheader(":green[Login Page]")
login_email = st.text_input("email")
login_password = st.text_input("Password", type = "password")
login_button = st.button(":red[Login]")
st.markdown('To create new account please <a href="/signup" target="_self">sign up</a>', unsafe_allow_html=True)
if login_button:
  output = database.authenticate_user(login_email,login_password)
  if output[0]:
    username = output[1]
    st.session_state["username"] = username.title()
    st.switch_page("pages/bizcard.py")
  else:
    st.warning(output[1])




