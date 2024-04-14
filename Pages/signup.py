import streamlit as st
import database
import re
import hashlib

def validate_email(email):
  """Gets the email id and throws warning on two cases:
     1. Invalid Format
     2. Email already exists"""
  pattern = "^[a-zA-Z0-9+_.-]+@[a-zA-Z0-9.-]+\.(com|net|org|gov)+$"
  length = len(email)
  matched = re.match(pattern, email)
  if not matched:
    st.warning("Invalid email ID Format")
  if database.email_exists(email):
    st.warning("Email ID already exists")

def validate_password(password):
  """Gets the password and throws warning if the password is not valid"""
  pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^*-]).{6,}$"
  if not re.match(pattern,password):
    st.warning("""Password must contain atleast
                  * 6 characters
                  * One uppercase letter
                  * One lower case letter
                  * One number
                  * One Special Character.
    """)

#Getting and validating username, email and password
st.subheader(':green[Signup Page]')
sign_email = st.text_input("Enter email")
if sign_email:
  validate_email(sign_email)
sign_password = st.text_input("Enter Password ", type = "password")
if sign_password:
  validate_password(sign_password)
  hash_password = hashlib.md5(sign_password.encode()).hexdigest()
sign_username =  st.text_input("Enter your unique Username")
if sign_username:
  username_exists = database.validate_username(sign_username)
  if username_exists:
    st.warning("Username already exists")
create = st.button(":red[Create account]")
st.markdown('Once you signup please <a href="/login" target="_self">login</a>', unsafe_allow_html=True)

#inserting user details to db
if create:
  output = database.insert_user(sign_username, sign_email, hash_password)
  if output[0]:
    st.success(output[1])
    st.balloons()
  else:
    st.warning(output[1])

#--client.showSidebarNavigation=False
