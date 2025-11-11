# Python-Library-System
# Library Management System

## Overview
This project is a simple **Library Management System** built using **Python (Tkinter GUI)** and **MySQL**.  
It allows users to:
- Search for available books  
- Borrow books (records the borrower's name and date)  
- Return borrowed books  

The project demonstrates database connectivity, CRUD operations, and GUI interaction.

---

## Tech Stack
**Language:** Python  
**GUI Framework:** Tkinter  
**Database:** MySQL  
**Environment Management:** python-dotenv  

---

## Environment Variables
Create a `.env` file in your project directory with the following content:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=library_db
