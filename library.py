import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime
from database import execute_query, execute_commit


def borrow_flow():
    search_term = entry_search.get().strip()
    if not search_term:
        messagebox.showwarning("Input Required", "Enter a book title to search.")
        return

    query = "SELECT book_id, title, author FROM available_books WHERE title LIKE %s"
    results = execute_query(query, (f"%{search_term}%",))

    if not results:
        messagebox.showinfo("No Results", "No books were found with that title.")
        return

    
    books_text = "\n".join([f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]}" for row in results])
    messagebox.showinfo("Search Results", f"Books found:\n\n{books_text}")

    try:
        book_id = int(simpledialog.askstring("Borrow Book", "Enter the Book ID you want to borrow:"))
    except (TypeError, ValueError):
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    
    valid_id = any(book_id == row[0] for row in results)
    if not valid_id:
        messagebox.showerror("Invalid ID", "Book ID not in search results.")
        return

  
    check_query = "SELECT borrower_name FROM borrowed_books WHERE book_id = %s"
    borrowed = execute_query(check_query, (book_id,))
    if borrowed:
        messagebox.showwarning("Unavailable", f"This book is already borrowed by {borrowed[0][0]}.")
        return

    borrower_name = simpledialog.askstring("Borrower Name", "Enter your full name:")
    if not borrower_name:
        messagebox.showerror("Input Required", "Borrower name cannot be empty.")
        return

    insert_query = "INSERT INTO borrowed_books (book_id, borrower_name, borrow_date) VALUES (%s, %s, %s)"
    borrow_date = datetime.date.today().isoformat()

    if execute_commit(insert_query, (book_id, borrower_name, borrow_date)):
        messagebox.showinfo("Success", f"Book granted to {borrower_name}!")
    else:
        messagebox.showerror("Error", "Could not borrow the book.")


def return_flow():
    try:
        book_id = int(simpledialog.askstring("Return Book", "Enter the Book ID you want to return:"))
    except (TypeError, ValueError):
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return

    check_query = "SELECT * FROM borrowed_books WHERE book_id = %s"
    borrowed = execute_query(check_query, (book_id,))
    if not borrowed:
        messagebox.showinfo("Not Found", "This book is not currently borrowed.")
        return

    delete_query = "DELETE FROM borrowed_books WHERE book_id = %s"
    if execute_commit(delete_query, (book_id,)):
        messagebox.showinfo("Returned", "Book successfully returned!")
    else:
        messagebox.showerror("Error", "Could not return the book.")



root = tk.Tk()
root.title("Library Management System")
root.geometry("500x350")
root.configure(bg="#f0f0f0")


tk.Label(
    root,
    text=" Library Management System",
    font=("Arial", 20, "bold"),
    bg="#f0f0f0"
).pack(pady=20)


tk.Label(root, text="Book Title:", font=("Arial", 14), bg="#f0f0f0").pack()
entry_search = tk.Entry(root, width=35, font=("Arial", 14))
entry_search.pack(pady=10)


tk.Button(
    root,
    text="Borrow",
    width=20,
    height=2,
    font=("Arial", 14, "bold"),
    bg="#4CAF50",
    fg="white",
    command=borrow_flow
).pack(pady=10)

tk.Button(
    root,
    text="Return",
    width=20,
    height=2,
    font=("Arial", 14, "bold"),
    bg="#f44336",
    fg="white",
    command=return_flow
).pack(pady=10)

root.mainloop()