"""
Library Management System GUI Application

This module implements a graphical user interface for a library management system
using tkinter. It provides functionality for managing books, borrowing, and returns.
"""

# Standard library imports
import csv
import json
import os
from datetime import datetime, timedelta

# Third-party imports
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkinter.font import Font
import tkinter.font as tkfont

# Global variables
books = []
borrowed_books = []
app = None
tree = None
content_frame = None
main_container = None

# Style variables
primary_color = "#2c3e50"    # Dark blue
secondary_color = "#3498db"   # Light blue
accent_color = "#e74c3c"     # Red
bg_color = "#ecf0f1"         # Light gray
text_color = "#2c3e50"       # Dark blue
success_color = "#2ecc71"    # Green

# Font configurations
title_font = None
subtitle_font = None
button_font = None
text_font = None
style = None

def setup_fonts():
    """Setup font configurations"""
    global title_font, subtitle_font, button_font, text_font
    title_font = Font(family="Helvetica", size=24, weight="bold")
    subtitle_font = Font(family="Helvetica", size=16, weight="bold")
    button_font = Font(family="Helvetica", size=11)
    text_font = Font(family="Helvetica", size=10)

def configure_styles():
    """Configure the application styles"""
    global style
    style = ttk.Style()
    style.theme_use('clam')
    
    # Frame styles
    style.configure('Main.TFrame', background=bg_color)
    style.configure('Content.TFrame', background=bg_color)
    style.configure('Sidebar.TFrame', background=primary_color)
    
    # Button styles
    style.configure('Sidebar.TButton',
                   font=button_font,
                   background=primary_color,
                   foreground='white',
                   padding=10)
    
    style.map('Sidebar.TButton',
              background=[('active', secondary_color)],
              foreground=[('active', 'white')])
    
    # Label styles
    style.configure('Title.TLabel',
                   font=title_font,
                   background=bg_color,
                   foreground=text_color)
    
    style.configure('Subtitle.TLabel',
                   font=subtitle_font,
                   background=bg_color,
                   foreground=text_color)
    
    # Entry styles
    style.configure('Custom.TEntry',
                   font=text_font,
                   padding=5)
    
    # Treeview styles
    style.configure('Custom.Treeview',
                   font=text_font,
                   rowheight=30,
                   background=bg_color,
                   fieldbackground=bg_color,
                   foreground=text_color)
    
    style.configure('Custom.Treeview.Heading',
                   font=button_font,
                   background=primary_color,
                   foreground='white')
    
    style.map('Custom.Treeview',
              background=[('selected', secondary_color)],
              foreground=[('selected', 'white')])
    
    # Delete button style
    style.configure('Delete.TButton',
                   font=button_font,
                   background=accent_color,
                   foreground='white',
                   padding=10)
    
    style.map('Delete.TButton',
              background=[('active', '#c0392b')],  # Darker red on hover
              foreground=[('active', 'white')])

def create_header():
    """Create the application header with gradient effect"""
    header_frame = tk.Frame(app, height=60, bg=primary_color)
    header_frame.pack(fill='x', pady=(0, 20))
    
    canvas = tk.Canvas(header_frame, height=60, bg=primary_color, highlightthickness=0)
    canvas.pack(fill='x')
    canvas.create_text(40, 30, text="Library Management System",
                     font=title_font, fill='white', anchor='w')

def create_sidebar():
    """Create the navigation sidebar with buttons"""
    sidebar = ttk.Frame(main_container, style='Sidebar.TFrame')
    sidebar.pack(side="left", fill="y", padx=0, pady=0)

    buttons = [
        ("📚 View Books", show_books_view),
        ("➕ Add Book", show_add_book_view),
        ("📖 Borrow Book", show_borrow_view),
        ("↩️ Return Book", show_return_view),
        ("📋 Borrowed Books", show_borrowed_books_view),
        ("⏰ Overdue Books", show_overdue_view)
    ]

    for text, command in buttons:
        btn = ttk.Button(sidebar, text=text, command=command, style='Sidebar.TButton')
        btn.pack(pady=5, padx=10, fill="x")

def clear_content():
    """Clear all widgets from the content frame"""
    for widget in content_frame.winfo_children():
        widget.destroy()

def validate_year_input(value):
    """Validate that the year input is a valid 4-digit number"""
    if value == "":
        return True
    try:
        year = int(value)
        current_year = datetime.now().year
        return len(value) <= 4 and 1000 <= year <= current_year
    except ValueError:
        return False

def load_data():
    """Load books and borrowed books data from JSON files"""
    global books, borrowed_books
    try:
        if os.path.exists('books.json'):
            with open('books.json', 'r') as f:
                books = json.load(f)
        if os.path.exists('borrowed_books.json'):
            with open('borrowed_books.json', 'r') as f:
                borrowed_books = json.load(f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {str(e)}")

def save_data():
    """Save books and borrowed books data to JSON files"""
    try:
        with open('books.json', 'w') as f:
            json.dump(books, f, indent=4)
        with open('borrowed_books.json', 'w') as f:
            json.dump(borrowed_books, f, indent=4)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {str(e)}")

def initialize_gui():
    """Initialize the main GUI window and setup"""
    global app, main_container, content_frame
    
    app = tk.Tk()
    app.title("Library Management System")
    app.geometry("1200x700")
    
    setup_fonts()
    configure_styles()
    
    app.configure(bg=bg_color)
    create_header()

    main_container = ttk.Frame(app, style='Main.TFrame')
    main_container.pack(fill="both", expand=True, padx=20, pady=(0, 20))

    create_sidebar()
    content_frame = ttk.Frame(main_container, style='Content.TFrame')
    content_frame.pack(side="right", fill="both", expand=True, padx=(20, 0))

    show_books_view()

def run():
    """Start the application"""
    load_data()
    initialize_gui()
    app.mainloop()

def show_books_view():
    clear_content()
    
    # Title
    title = ttk.Label(content_frame, text="Library Books", style='Title.TLabel')
    title.pack(pady=20)

    # Search frame
    search_frame = ttk.Frame(content_frame, style='Content.TFrame')
    search_frame.pack(fill='x', padx=20, pady=(0, 20))

    search_entry = ttk.Entry(search_frame, width=40, style='Custom.TEntry')
    search_entry.pack(side="left", padx=10)
    search_entry.insert(0, "Search by title or author...")
    
    def on_focus_in(event):
        if search_entry.get() == "Search by title or author...":
            search_entry.delete(0, 'end')
            
    def on_focus_out(event):
        if search_entry.get() == "":
            search_entry.insert(0, "Search by title or author...")
        
    search_entry.bind('<FocusIn>', on_focus_in)
    search_entry.bind('<FocusOut>', on_focus_out)

    # Table setup
    table_frame = ttk.Frame(content_frame, style='Content.TFrame')
    table_frame.pack(fill='both', expand=True, padx=20, pady=20)

    columns = ('ID', 'Title', 'Author', 'Year', 'Status')
    global tree
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Custom.Treeview')

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    def update_table(search_term=""):
        # Clear current items
        for item in tree.get_children():
            tree.delete(item)

        # Filter and display books
        for book in books:
            if (search_term == "" or search_term.lower() in book['title'].lower() or 
                search_term.lower() in book['author'].lower()):
                status = "Available" if book['available'] else "Borrowed"
                status_color = success_color if book['available'] else accent_color
                tree.insert('', 'end', values=(book['id'], book['title'], book['author'], 
                                        book['publication_year'], status))

    def on_search():
        search_term = search_entry.get()
        if search_term == "Search by title or author...":
            search_term = ""
        update_table(search_term)

    # Search button
    search_btn = ttk.Button(search_frame, text="🔍 Search", command=on_search)
    search_btn.pack(side="left", padx=10)

    # Reset button
    reset_btn = ttk.Button(search_frame, text="🔄 Reset", command=lambda: (
        search_entry.delete(0, 'end'),
        search_entry.insert(0, "Search by title or author..."),
        update_table("")
    ))
    reset_btn.pack(side="left", padx=10)

    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Create delete button frame
    button_frame = ttk.Frame(content_frame, style='Content.TFrame')
    button_frame.pack(fill='x', padx=20, pady=10)

    # Add export button
    export_btn = ttk.Button(button_frame, text="Export to CSV", command=export_to_csv, style='Sidebar.TButton')
    export_btn.pack(side='right', padx=5)

    # Add edit button
    edit_btn = ttk.Button(button_frame, text="Edit Book", command=show_edit_book_dialog, style='Sidebar.TButton')
    edit_btn.pack(side='left', padx=5)

    def delete_selected():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return
        
        # Get the book ID from the selected item
        book_values = tree.item(selected_item)['values']
        book_id = book_values[0]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", 
                            f"Are you sure you want to delete the book '{book_values[1]}'?"):
            # Check if book is borrowed
            book = next((b for b in books if b['id'] == book_id), None)
            if book and not book['available']:
                messagebox.showerror("Error", 
                                "Cannot delete a borrowed book. Please wait for it to be returned.")
                return
            
            # Remove from books list
            books = [b for b in books if b['id'] != book_id]
            # Remove from borrowed_books if present
            borrowed_books = [b for b in borrowed_books if b['book_id'] != book_id]
            
            # Save changes
            save_data()
            
            # Remove from treeview
            tree.delete(selected_item)
            messagebox.showinfo("Success", "Book deleted successfully!")

    # Add delete button
    delete_btn = ttk.Button(button_frame, text="🗑️ Delete Selected Book", 
                        command=delete_selected, style='Delete.TButton')
    delete_btn.pack(side='right', padx=5)
    
    # Pack elements
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Initial table population
    update_table()

def show_add_book_view():
    clear_content()
    
    # Title
    title = ttk.Label(content_frame, text="Add New Book", style='Title.TLabel')
    title.pack(pady=20)
    
    # Create form
    form_frame = ttk.Frame(content_frame, style='Content.TFrame')
    form_frame.pack(pady=20)
    
    # Title
    title_label = ttk.Label(form_frame, text="Title:", style='Subtitle.TLabel')
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky='e')
    title_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
    title_entry.grid(row=0, column=1, padx=10, pady=10)
    
    # Author
    author_label = ttk.Label(form_frame, text="Author:", style='Subtitle.TLabel')
    author_label.grid(row=1, column=0, padx=10, pady=10, sticky='e')
    author_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
    author_entry.grid(row=1, column=1, padx=10, pady=10)
    
    # Year
    year_label = ttk.Label(form_frame, text="Publication Year:", style='Subtitle.TLabel')
    year_label.grid(row=2, column=0, padx=10, pady=10, sticky='e')
    year_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry', validate='key', 
                         validatecommand=(validate_year_input, '%P'))
    year_entry.grid(row=2, column=1, padx=10, pady=10)
    
    def add_book():
        title = title_entry.get()
        author = author_entry.get()
        year = year_entry.get()

        if title and author and year:
            book = {
                'id': len(books) + 1,
                'title': title,
                'author': author,
                'publication_year': year,
                'available': True
            }
            books.append(book)
            save_data()
            messagebox.showinfo("Success", f"Book '{title}' added successfully!")
            title_entry.delete(0, 'end')
            author_entry.delete(0, 'end')
            year_entry.delete(0, 'end')
        else:
            messagebox.showerror("Error", "Please fill all fields!")

    # Submit button
    submit_btn = ttk.Button(form_frame, text="Add Book", command=add_book)
    submit_btn.grid(row=3, column=1, padx=10, pady=20)

def show_borrow_view():
    clear_content()
    
    # Title
    title = ttk.Label(content_frame, text="Borrow Book", style='Title.TLabel')
    title.pack(pady=20)

    # Form
    form_frame = ttk.Frame(content_frame, style='Content.TFrame')
    form_frame.pack(pady=20, padx=20)

    # Book ID
    ttk.Label(form_frame, text="Book ID", style='Subtitle.TLabel').pack(pady=(0, 5))
    book_id_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
    book_id_entry.pack(pady=(0, 20))

    # Student Name
    ttk.Label(form_frame, text="Student Name", style='Subtitle.TLabel').pack(pady=(0, 5))
    student_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
    student_entry.pack(pady=(0, 20))

    def borrow_book():
        try:
            book_id = int(book_id_entry.get())
            student_name = student_entry.get()

            if not student_name:
                messagebox.showerror("Error", "Please enter student name!")
                return

            for book in books:
                if book['id'] == book_id and book['available']:
                    book['available'] = False
                    borrow_date = datetime.now()
                    due_date = borrow_date + timedelta(days=14)
                    
                    borrowed_info = {
                        'book_id': book_id,
                        'book_title': book['title'],
                        'student_name': student_name,
                        'borrow_date': borrow_date.strftime('%Y-%m-%d'),
                        'due_date': due_date.strftime('%Y-%m-%d')
                    }
                    
                    borrowed_books.append(borrowed_info)
                    save_data()
                    messagebox.showinfo("Success", 
                        f"Book '{book['title']}' has been borrowed by {student_name}.\n"
                        f"Due date: {due_date.strftime('%Y-%m-%d')}")
                    book_id_entry.delete(0, 'end')
                    student_entry.delete(0, 'end')
                    return

            messagebox.showerror("Error", "Book not available or invalid book ID!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid book ID!")

    # Submit button
    submit_btn = ttk.Button(form_frame, text="Borrow Book", command=borrow_book)
    submit_btn.pack(pady=20)

def show_return_view():
    clear_content()
    
    # Title
    title = ttk.Label(content_frame, text="Return Book", style='Title.TLabel')
    title.pack(pady=20)

    # Form
    form_frame = ttk.Frame(content_frame, style='Content.TFrame')
    form_frame.pack(pady=20, padx=20)

    # Book ID
    ttk.Label(form_frame, text="Book ID", style='Subtitle.TLabel').pack(pady=(0, 5))
    book_id_entry = ttk.Entry(form_frame, width=40, style='Custom.TEntry')
    book_id_entry.pack(pady=(0, 20))

    def return_book():
        try:
            book_id = int(book_id_entry.get())
            
            for book in books:
                if book['id'] == book_id and not book['available']:
                    book['available'] = True
                    global borrowed_books
                    borrowed_books = [b for b in borrowed_books if b['book_id'] != book_id]
                    save_data()
                    messagebox.showinfo("Success", f"Book '{book['title']}' has been returned successfully!")
                    book_id_entry.delete(0, 'end')
                    return

            messagebox.showerror("Error", "Book not found or already returned!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid book ID!")

    # Submit button
    submit_btn = ttk.Button(form_frame, text="Return Book", command=return_book)
    submit_btn.pack(pady=20)

def show_overdue_view():
    clear_content()
    
    # Title
    title = ttk.Label(content_frame, text="Overdue Books", style='Title.TLabel')
    title.pack(pady=20)

    # Create table
    columns = ('Book Title', 'Student', 'Due Date', 'Days Overdue')
    tree = ttk.Treeview(content_frame, columns=columns, show='headings', style='Custom.Treeview')

    # Define headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    # Add scrollbar
    scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Add data
    today = datetime.now()
    for borrowed in borrowed_books:
        due_date = datetime.strptime(borrowed['due_date'], '%Y-%m-%d')
        if today > due_date:
            days_overdue = (today - due_date).days
            tree.insert('', 'end', values=(borrowed['book_title'], borrowed['student_name'], 
                                         borrowed['due_date'], f"{days_overdue} days"))

    # Pack elements
    tree.pack(pady=20, padx=20, fill='both', expand=True, side='left')
    scrollbar.pack(pady=20, fill='y', side='right')

def show_borrowed_books_view():
    clear_content()
    
    # Title
    title = ttk.Label(content_frame, text="Currently Borrowed Books", style='Title.TLabel')
    title.pack(pady=20)

    # Create table frame
    table_frame = ttk.Frame(content_frame, style='Content.TFrame')
    table_frame.pack(fill='both', expand=True, padx=20, pady=20)

    # Create table
    columns = ('Book ID', 'Book Title', 'Student Name', 'Borrow Date', 'Due Date', 'Status')
    tree = ttk.Treeview(table_frame, columns=columns, show='headings', style='Custom.Treeview')

    # Define headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor='center')

    # Add data
    today = datetime.now()
    for borrowed in borrowed_books:
        due_date = datetime.strptime(borrowed['due_date'], '%Y-%m-%d')
        status = "Overdue" if today > due_date else "On Time"
        status_color = accent_color if status == "Overdue" else success_color
        
        tree.insert('', 'end', values=(
            borrowed['book_id'],
            borrowed['book_title'],
            borrowed['student_name'],
            borrowed['borrow_date'],
            borrowed['due_date'],
            status
        ))

    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)

    # Pack elements
    tree.pack(side='left', fill='both', expand=True)
    scrollbar.pack(side='right', fill='y')

    # Add export button
    def export_borrowed_books():
        try:
            with open('borrowed_books_report.txt', 'w') as f:
                f.write("LIBRARY BORROWED BOOKS REPORT\n")
                f.write("Generated on: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
                f.write("-" * 100 + "\n")
                
                for borrowed in borrowed_books:
                    due_date = datetime.strptime(borrowed['due_date'], '%Y-%m-%d')
                    status = "Overdue" if today > due_date else "On Time"
                    
                    f.write(f"Book ID: {borrowed['book_id']}\n")
                    f.write(f"Title: {borrowed['book_title']}\n")
                    f.write(f"Borrowed by: {borrowed['student_name']}\n")
                    f.write(f"Borrow Date: {borrowed['borrow_date']}\n")
                    f.write(f"Due Date: {borrowed['due_date']}\n")
                    f.write(f"Status: {status}\n")
                    f.write("-" * 100 + "\n")
            
            messagebox.showinfo("Success", "Report exported to 'borrowed_books_report.txt'")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")

    button_frame = ttk.Frame(content_frame, style='Content.TFrame')
    button_frame.pack(fill='x', padx=20, pady=10)
    
    export_btn = ttk.Button(button_frame, text="📄 Export Report", command=export_borrowed_books)
    export_btn.pack(side='right', padx=5)

def show_edit_book_dialog():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("No Selection", "Please select a book to edit.")
        return
    
    book_values = tree.item(selected_item)['values']
    book_id = book_values[0]
    book = next((book for book in books if book['id'] == book_id), None)
    
    if not book:
        messagebox.showerror("Error", "Book not found.")
        return
    
    # Create edit dialog
    edit_dialog = tk.Toplevel(app)
    edit_dialog.title("Edit Book")
    edit_dialog.geometry("400x300")
    edit_dialog.configure(bg=bg_color)
    
    # Center the dialog
    edit_dialog.transient(app)
    edit_dialog.grab_set()
    
    # Create and pack widgets
    ttk.Label(edit_dialog, text="Edit Book Details", style='Title.TLabel').pack(pady=10)
    
    # Title
    title_frame = ttk.Frame(edit_dialog)
    title_frame.pack(fill='x', padx=20, pady=5)
    ttk.Label(title_frame, text="Title:", style='Subtitle.TLabel').pack(side='left')
    title_entry = ttk.Entry(title_frame, style='Custom.TEntry')
    title_entry.pack(side='right', expand=True, fill='x', padx=(10, 0))
    title_entry.insert(0, book['title'])
    
    # Author
    author_frame = ttk.Frame(edit_dialog)
    author_frame.pack(fill='x', padx=20, pady=5)
    ttk.Label(author_frame, text="Author:", style='Subtitle.TLabel').pack(side='left')
    author_entry = ttk.Entry(author_frame, style='Custom.TEntry')
    author_entry.pack(side='right', expand=True, fill='x', padx=(10, 0))
    author_entry.insert(0, book['author'])
    
    # Year
    year_frame = ttk.Frame(edit_dialog)
    year_frame.pack(fill='x', padx=20, pady=5)
    ttk.Label(year_frame, text="Year:", style='Subtitle.TLabel').pack(side='left')
    year_entry = ttk.Entry(year_frame, style='Custom.TEntry', validate='key',
                         validatecommand=(validate_year_input, '%P'))
    year_entry.pack(side='right', expand=True, fill='x', padx=(10, 0))
    year_entry.insert(0, book['publication_year'])
    
    def save_changes():
        # Validate inputs
        if not all([title_entry.get(), author_entry.get(), year_entry.get()]):
            messagebox.showwarning("Invalid Input", "All fields are required.")
            return
        
        try:
            year = int(year_entry.get())
            if not (1000 <= year <= 9999):
                raise ValueError
        except ValueError:
            messagebox.showwarning("Invalid Year", "Please enter a valid year (1000-9999).")
            return
        
        # Update book
        book['title'] = title_entry.get()
        book['author'] = author_entry.get()
        book['publication_year'] = year
        
        # Save to file
        save_data()
        
        # Update display
        show_books_view()
        
        # Close dialog
        edit_dialog.destroy()
        messagebox.showinfo("Success", "Book updated successfully!")
    
    # Buttons frame
    buttons_frame = ttk.Frame(edit_dialog)
    buttons_frame.pack(pady=20)
    
    ttk.Button(buttons_frame, text="Save", command=save_changes, style='Sidebar.TButton').pack(side='left', padx=5)
    ttk.Button(buttons_frame, text="Cancel", command=edit_dialog.destroy, style='Delete.TButton').pack(side='left', padx=5)

def export_to_csv():
    """Export the current book list to a CSV file"""
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Title', 'Author', 'Year', 'Status'])
                for book in books:
                    writer.writerow([
                        book['id'],
                        book['title'],
                        book['author'],
                        book['publication_year'],
                        'Available' if book['available'] else 'Borrowed'
                    ])
            messagebox.showinfo("Success", "Data exported successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export data: {str(e)}")

if __name__ == "__main__":
    run()
