import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv() 


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_connection():

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def close_connection(conn):
    if conn and conn.is_connected():
        conn.close()

def execute_query(query, params=None):
    
    conn = get_connection()
    if not conn:
        return None
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cursor.close()
        close_connection(conn)

def execute_commit(query, params=None):
  
    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return True
    except Error as e:
        print(f"Error executing commit: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        close_connection(conn)

def add_borrowed_book(new_borrow_id, book_id, borrower_name, borrow_date):

    conn = get_connection()
    if not conn:
        return False
    cursor = conn.cursor()
    
    insert_query = "INSERT INTO borrowed_books (borrow_id, book_id, borrower_name, borrow_date) VALUES (%s, %s, %s, %s)"
    
    try:
        cursor.execute(insert_query, (new_borrow_id, book_id, borrower_name, borrow_date))
        conn.commit()
        return True
    except Error as e:
        print(f"Error executing add_borrowed_book: {e}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()