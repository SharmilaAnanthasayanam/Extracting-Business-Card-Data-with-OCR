# Extracting-Business-Card-Data-with-OCR
### About:
Developed a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR.

### Tools used:
* EasyOCR
* SQL
* Streamlit

### Architecture:
<img width="631" alt="image" src="https://github.com/SharmilaAnanthasayanam/Extracting-Business-Card-Data-with-OCR/assets/112562560/96c56e0c-3bb9-47f4-93b6-65b99279457c">

### 1. Login Page :
Authenticate the user into the application using email and password. User can click on signup if not registered already
<img width="631" alt="image" src="https://github.com/SharmilaAnanthasayanam/Extracting-Business-Card-Data-with-OCR/assets/112562560/b89bfa4d-bf1d-4d14-90b1-ece283ec35ac">

### 2. Signup Page :
Create an account for the user by getting username, email and password. After signing up user can go to login page to login into the app.
<img width="631" alt="image" src="https://github.com/SharmilaAnanthasayanam/Extracting-Business-Card-Data-with-OCR/assets/112562560/d6e785c6-b2d8-45d7-ba05-99f93a89147c">

### 3. Bizcard Page :
Enables user to upload the business card image and extract the details.
<img width="631" alt="image" src="https://github.com/SharmilaAnanthasayanam/Extracting-Business-Card-Data-with-OCR/assets/112562560/9c27c04d-391f-4b72-9bfa-09133d0f1d51">

After uploading the image. User can perform the following operations:
* Check and insert the image and its details to database.
<img width="631" alt="image" src="https://github.com/SharmilaAnanthasayanam/Extracting-Business-Card-Data-with-OCR/assets/112562560/8b0901f3-6f67-47af-af27-22f778016515">

* Update the details in database.
<img width="631" alt="image" src="https://github.com/SharmilaAnanthasayanam/Extracting-Business-Card-Data-with-OCR/assets/112562560/5dc9a9bf-1cf6-4891-92ba-a90886296f79">

* Delete the image and its details from database.
<img width="631" alt="image" src="https://github.com/SharmilaAnanthasayanam/Extracting-Business-Card-Data-with-OCR/assets/112562560/a5d56924-ac04-4774-bbc4-deeec4d9dc66">

Logout will take you back to the login page.

Note: Python version 3.8.10 have been used.

