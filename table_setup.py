import mysql.connector
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import database

password = os.getenv("db_pass")

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = password,
    database = 'bizcard'
)
mycursor = mydb.cursor()

def table_setup_func():
    database.create_table("card_details", "company VARCHAR(255)", "owner_name VARCHAR(255)",
                "designation VARCHAR(255)", "website_url VARCHAR(255)", "email_id VARCHAR(255)",
                "address VARCHAR(255)", "image LONGBLOB")
    database.create_table("phoneno_details", "phone_number VARCHAR(255)")
    database.add_primarykey("card_details", "id")
    database.add_foreignkey("phoneno_details", "card_details", "id")
    database.create_table("user_auth","user_name varchar(255) NOT NUll", "email varchar(255)", "password varchar(255)")
    database.add_primarykey("user_auth", "email")
    database.add_unique_constraint("user_auth","user_name")
    database.drop_column("user_auth", "id")
    mydb.commit()

table_setup_func()