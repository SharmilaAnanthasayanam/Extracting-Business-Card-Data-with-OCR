from math import e
import mysql.connector
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()

password = os.getenv("db_pass")
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password = password,
    database = 'bizcard'
)
mycursor = mydb.cursor()

def create_database(database_name):
  """Gets database name and creates database in Mysqlworkbench"""
  query = f"CREATE DATABASE {database_name};"
  mycursor.execute(query)

def create_table(table_name,*argv, ):
  """Gets the tablename and its columns with datatype and creates the table in database."""
  mycursor.execute(f"CREATE TABLE {table_name} (id int)")
  for arg in argv :
    Alter_query = f"""ALTER TABLE {table_name}
                    ADD {arg}"""
    mycursor.execute(Alter_query)
    mydb.commit()

def add_primarykey(table_name, column_name):
  """Gets the table name and column name and make the column as primary key"""
  QUERY = f"""ALTER TABLE {table_name}
              ADD PRIMARY KEY ({column_name});"""
  mycursor.execute(QUERY)

def add_unique_constraint(table_name, column_name):
  """Gets the table name and column name and adds unique constraint to the column"""
  QUERY = f"""ALTER TABLE {table_name} 
              ADD CONSTRAINT UC_Person UNIQUE ({column_name});"""

def add_notnull_constraint(table_name, column_name, datatype):
  """Gets Table name, column name and datatype and adds notnum constraint to given column"""
  QUERY = f"""ALTER TABLE {table_name}
              MODIFY COLUMN {column_name} {datatype} NOT NULL"""

def add_foreignkey(fk_table, pk_table, column_name):
  """Gets foreign ket table, Primary key table and column name 
     and add foreign key constraint to the given column."""
  QUERY = f"""ALTER TABLE {fk_table}
          ADD FOREIGN KEY ({column_name}) REFERENCES {pk_table}({column_name});"""
  mycursor.execute(QUERY)

def drop_table(table_name):
  """Gets the table name and drops the table"""
  mycursor.execute(f"DROP TABLE {table_name};")

def show_tables():
  """Shows the list of tables in database"""
  mycursor.execute("SHOW TABLES;")
  return mycursor.fetchall()

def describe_tables():
  """Describe the tabeles in the database"""
  tables_list = show_tables()
  for l in range(len(tables_list)):
    if tables_list[l][0]:
      mycursor.execute(f"DESCRIBE {tables_list[l][0]}")
      st.write(mycursor.fetchall())

def clear_database():
  """Clear the tables phoneno_details and card_details"""
  mycursor.execute("DELETE FROM phoneno_details;")
  mycursor.execute("DELETE FROM card_details;")

def insert(info_dict, card_id, image):
  """Gets the info_dict, card_id and image 
     and inserts the data into card_details and phoneno_details tables."""
  INSERT_QUERY = """INSERT INTO card_details (id, company, owner_name, designation, website_url, email_id, address, image)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
  mycursor.execute(INSERT_QUERY, (
      card_id,
      info_dict["Company"],
      info_dict["Owner Name"],
      info_dict["Designation"],
      info_dict["Website URL"], 
      info_dict["Email_ID"],
      info_dict["Address"],
      image
  ))
  for number in info_dict["Phone Number"]:
    PHONENO_QUERY = """INSERT INTO phoneno_details (id, phone_number)
                     VALUES (%s, %s)"""
    mycursor.execute(PHONENO_QUERY,(
        card_id,
        number   
    ))
  mydb.commit()

def drop_column(table_name, column_name):
  """Gets the table name and column name and drops the column in database."""
  QUERY = f"""ALTER TABLE {table_name} DROP COLUMN {column_name};"""
  mycursor.execute(QUERY)
  mydb.commit()

def insert_user(username, email, password):
  """Gets username, email and password and inserts the details to user_auth table"""
  try:
    QUERY = """INSERT INTO user_auth (user_name, email, password)
                      VALUES (%s, %s, %s)"""
    mycursor.execute(QUERY,(username, email, password))
    mydb.commit()
    return [True, "Account Created Successfully"]
  except Exception as e:
    message = f"An error occured: {e}"
    return [False, message]

def update(info_dict, card_id):
  """Gets the info_dict, card_id and updates the database where the card id matches"""
  QUERY = f"""UPDATE card_details 
              SET company = '{info_dict["Company"]}',
                  owner_name = '{info_dict["Owner Name"]}',
                  designation = '{info_dict["Designation"]}',
                  website_url = '{info_dict["Website URL"]}',
                  email_id = '{info_dict["Email_ID"]}',
                  address = '{info_dict["Address"]}'
              WHERE id = '{card_id}'
                 """
  mycursor.execute(QUERY)
  DELETE_QUERY = f"""DELETE FROM phoneno_details where id = {card_id};"""
  mycursor.execute(DELETE_QUERY)
  for number in info_dict["Phone Number"]:
    PHONENO_QUERY = """INSERT INTO phoneno_details (id, phone_number)
                     VALUES (%s, %s)"""
    mycursor.execute(PHONENO_QUERY,(
        card_id,
        number   
    ))
  mydb.commit()

def authenticate_user(email, password):
  """Gets the email and password.
     Validates if the given email exists in db else return False and Invalid email message.
     Checks if the given password matches and 
     returs True and username if password matches
     else returns False and Incorrect password message"""
  QUERY = f"""SELECT * from user_auth where email = '{email}'""" 
  mycursor.execute(QUERY)
  user_details = mycursor.fetchall()
  if user_details:
    db_username = user_details[0][0]
    db_email = user_details[0][1]
    db_password = user_details[0][2]
    if password == db_password:
      return [True, db_username]
    else:
      return [False, "Incorrect Password"]
  else:
    return [False,"Invalid email"]

def validate_username(username):
  """Gets the username and returns True if the user already exists else False"""
  QUERY = f"""SELECT * FROM user_auth  WHERE user_name = '{username}' """
  mycursor.execute(QUERY)
  return mycursor.fetchall()

def email_exists(email):
  """Gets the email id and returns True if the email already exists else False"""
  QUERY = f"""SELECT * FROM user_auth  WHERE email = '{email}' """
  mycursor.execute(QUERY)
  return mycursor.fetchall()

def delete(card_id):
  """Gets the card id and deletes the data from the database"""
  QUERY = f"""DELETE FROM phoneno_details where id = '{card_id}'"""
  mycursor.execute(QUERY)
  QUERY = f"""DELETE FROM card_details where id = '{card_id}'"""
  mycursor.execute(QUERY)
  mydb.commit()

def view_table(table_name):
  """Gets the tables name and returns the value inside the table"""
  SELECT_QUERY = f"SELECT * from {table_name};"
  mycursor.execute(SELECT_QUERY)
  return mycursor.fetchall()

def get_image(owner):
  """Gets the owner and returns the image of the owner"""
  SELECT_QUERY = f"SELECT image from card_details where owner_name = '{owner}' ;"
  mycursor.execute(SELECT_QUERY)
  return mycursor.fetchall()

def existing(owner, company):
  """Gets the owner and company. Returns the card id of the given owner and company"""
  QUERY = f"""SELECT id from card_details where owner_name = '{owner}'
              and company = '{company}';"""
  mycursor.execute(QUERY)
  return mycursor.fetchall()

def get_card_id():
  """Returns the largest card id"""
  QUERY = f"""SELECT id FROM card_details ORDER BY id DESC LIMIT 1"""
  mycursor.execute(QUERY)
  return mycursor.fetchall()

