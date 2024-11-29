import mysql.connector
from tkinter import *
from tkinter import messagebox, simpledialog
from tkinter import ttk
from datetime import datetime
from PIL import Image, ImageTk

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="R2k4s6j8@",  # Replace with your MySQL password
    database="library_management"
)

cursor = conn.cursor()

# Create required tables if they don't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    Username VARCHAR(255) UNIQUE,
    Password VARCHAR(255)
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Students (
    ERP INT PRIMARY KEY,
    Name VARCHAR(255),
    Course VARCHAR(255),
    Year INT,
    Contact VARCHAR(255),
    Email VARCHAR(255),
    NoBook INT DEFAULT 0
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Books (
    BookID INT PRIMARY KEY,
    Title VARCHAR(255),
    Author VARCHAR(255),
    Edition VARCHAR(255),
    Quantity INT DEFAULT 1,
    Status VARCHAR(50) DEFAULT 'Available'
)""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS IssuedBooks (
    ERP INT,
    BookID INT,
    IssueDate DATE,
    ReturnDate DATE,
    FOREIGN KEY (ERP) REFERENCES Students(ERP),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
)""")

# Create triggers
cursor.execute("""
CREATE TRIGGER IF NOT EXISTS update_book_quantity
AFTER INSERT ON IssuedBooks
FOR EACH ROW
BEGIN
    UPDATE Books SET Quantity = Quantity - 1 WHERE BookID = NEW.BookID;
    UPDATE Students SET NoBook = NoBook + 1 WHERE ERP = NEW.ERP;
END
""")

cursor.execute("""
CREATE TRIGGER IF NOT EXISTS restore_book_quantity
AFTER DELETE ON IssuedBooks
FOR EACH ROW
BEGIN
    UPDATE Books SET Quantity = Quantity + 1 WHERE BookID = OLD.BookID;
    UPDATE Students SET NoBook = NoBook - 1 WHERE ERP = OLD.ERP;
END
""")

conn.commit()

class LibraryManagement:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        self.root.geometry("1000x600")
        self.root.configure(bg="#e8f0f2")
        
        # Load background image
        self.bg_image = Image.open("D:/SEM 5/library_258219-35.webp")
        self.bg_image = self.bg_image.resize((2000, 1200), Image.Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        # Add background image
        bg_label = Label(root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Title
        title = Label(root, text="Library Management System", font=("Arial", 20, "bold"), bg="#00203f", fg="#adefd1")
        title.pack(side=TOP, fill=X)

        # Buttons
        Button(root, text="Add Student", command=self.add_student, width=20, font=("Arial", 12), bg="#adefd1").place(x=50, y=100)
        Button(root, text="Delete Student", command=self.delete_student, width=20, font=("Arial", 12), bg="#adefd1").place(x=50, y=160)
        Button(root, text="Add Book", command=self.add_book, width=20, font=("Arial", 12), bg="#adefd1").place(x=50, y=220)
        Button(root, text="Delete Book", command=self.delete_book, width=20, font=("Arial", 12), bg="#adefd1").place(x=50, y=280)
        Button(root, text="View Students", command=self.view_students, width=20, font=("Arial", 12), bg="#adefd1").place(x=300, y=100)
        Button(root, text="View Books", command=self.view_books, width=20, font=("Arial", 12), bg="#adefd1").place(x=300, y=160)
        Button(root, text="View Issued Books", command=self.view_issued_books, width=20, font=("Arial", 12), bg="#adefd1").place(x=300, y=220)
        Button(root, text="Issue Book", command=self.issue_book, width=20, font=("Arial", 12), bg="#adefd1").place(x=550, y=100)
        Button(root, text="Return Book", command=self.return_book, width=20, font=("Arial", 12), bg="#adefd1").place(x=550, y=160)

    def add_student(self):
        def save_student():
            erp = student_erp_entry.get()
            name = student_name_entry.get()
            course = student_course_entry.get()
            year = student_year_entry.get()
            contact = student_contact_entry.get()
            email = student_email_entry.get()

            if not all([erp, name, course, year, contact, email]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                cursor.execute("INSERT INTO Students (ERP, Name, Course, Year, Contact, Email) VALUES (%s, %s, %s, %s, %s, %s)",
                               (erp, name, course, year, contact, email))
                conn.commit()
                messagebox.showinfo("Success", "Student added successfully!")
                add_student_window.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Student with this ERP already exists!")

        add_student_window = Toplevel(self.root)
        add_student_window.title("Add Student")
        add_student_window.geometry("400x400")

        Label(add_student_window, text="ERP", font=("Arial", 14)).place(x=50, y=30)
        student_erp_entry = Entry(add_student_window, font=("Arial", 14))
        student_erp_entry.place(x=150, y=30)

        Label(add_student_window, text="Name", font=("Arial", 14)).place(x=50, y=70)
        student_name_entry = Entry(add_student_window, font=("Arial", 14))
        student_name_entry.place(x=150, y=70)

        Label(add_student_window, text="Course", font=("Arial", 14)).place(x=50, y=110)
        student_course_entry = Entry(add_student_window, font=("Arial", 14))
        student_course_entry.place(x=150, y=110)

        Label(add_student_window, text="Year", font=("Arial", 14)).place(x=50, y=150)
        student_year_entry = Entry(add_student_window, font=("Arial", 14))
        student_year_entry.place(x=150, y=150)

        Label(add_student_window, text="Contact", font=("Arial", 14)).place(x=50, y=190)
        student_contact_entry = Entry(add_student_window, font=("Arial", 14))
        student_contact_entry.place(x=150, y=190)

        Label(add_student_window, text="Email", font=("Arial", 14)).place(x=50, y=230)
        student_email_entry = Entry(add_student_window, font=("Arial", 14))
        student_email_entry.place(x=150, y=230)

        Button(add_student_window, text="Save", command=save_student, width=10, font=("Arial", 12), bg="#adefd1").place(x=150, y=300)

    def delete_student(self):
        erp = simpledialog.askinteger("Delete Student", "Enter ERP of the student to delete:")
        if erp:
            try:
                cursor.execute("DELETE FROM Students WHERE ERP = %s", (erp,))
                conn.commit()
                messagebox.showinfo("Success", "Student deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Could not delete student: {err}")

    def add_book(self):
        def save_book():
            book_id = book_id_entry.get()
            title = book_title_entry.get()
            author = book_author_entry.get()
            edition = book_edition_entry.get()
            quantity = book_quantity_entry.get()

            if not all([book_id, title, author, edition, quantity]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                cursor.execute("INSERT INTO Books (BookID, Title, Author, Edition, Quantity) VALUES (%s, %s, %s, %s, %s)",
                               (book_id, title, author, edition, quantity))
                conn.commit()
                messagebox.showinfo("Success", "Book added successfully!")
                add_book_window.destroy()
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Book with this ID already exists!")

        add_book_window = Toplevel(self.root)
        add_book_window.title("Add Book")
        add_book_window.geometry("400x400")

        Label(add_book_window, text="Book ID", font=("Arial", 14)).place(x=50, y=30)
        book_id_entry = Entry(add_book_window, font=("Arial", 14))
        book_id_entry.place(x=150, y=30)

        Label(add_book_window, text="Title", font=("Arial", 14)).place(x=50, y=70)
        book_title_entry = Entry(add_book_window, font=("Arial", 14))
        book_title_entry.place(x=150, y=70)

        Label(add_book_window, text="Author", font=("Arial", 14)).place(x=50, y=110)
        book_author_entry = Entry(add_book_window, font=("Arial", 14))
        book_author_entry.place(x=150, y=110)

        Label(add_book_window, text="Edition", font=("Arial", 14)).place(x=50, y=150)
        book_edition_entry = Entry(add_book_window, font=("Arial", 14))
        book_edition_entry.place(x=150, y=150)

        Label(add_book_window, text="Quantity", font=("Arial", 14)).place(x=50, y=190)
        book_quantity_entry = Entry(add_book_window, font=("Arial", 14))
        book_quantity_entry.place(x=150, y=190)

        Button(add_book_window, text="Save", command=save_book, width=10, font=("Arial", 12), bg="#adefd1").place(x=150, y=250)

    def delete_book(self):
        book_id = simpledialog.askinteger("Delete Book", "Enter ID of the book to delete:")
        if book_id:
            try:
                cursor.execute("DELETE FROM Books WHERE BookID = %s", (book_id,))
                conn.commit()
                messagebox.showinfo("Success", "Book deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Could not delete book: {err}")

    def view_students(self):
        view_window = Toplevel(self.root)
        view_window.title("View Students")
        view_window.geometry("800x400")

        tree = ttk.Treeview(view_window, columns=("ERP", "Name", "Course", "Year", "Contact", "Email", "NoBook"), show='headings')
        tree.heading("ERP", text="ERP")
        tree.heading("Name", text="Name")
        tree.heading("Course", text="Course")
        tree.heading("Year", text="Year")
        tree.heading("Contact", text="Contact")
        tree.heading("Email", text="Email")
        tree.heading("NoBook", text="No. of Books")
        tree.pack(fill=BOTH, expand=True)

        cursor.execute("SELECT * FROM Students")
        for row in cursor.fetchall():
            tree.insert('', END, values=row)
    def issue_book(self):
        """Issue a book to a student."""
        def save_issue():
            erp = student_erp_entry.get()
            book_id = book_id_entry.get()
            issue_date = issue_date_entry.get()

            if not all([erp, book_id, issue_date]):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                cursor.execute("SELECT Quantity FROM Books WHERE BookID = %s", (book_id,))
                book = cursor.fetchone()

                if not book:
                    messagebox.showerror("Error", "Book ID does not exist!")
                    return
                
                if book[0] < 1:
                    messagebox.showerror("Error", "Book is currently unavailable!")
                    return

                cursor.execute("SELECT NoBook FROM Students WHERE ERP = %s", (erp,))
                student = cursor.fetchone()

                if not student:
                    messagebox.showerror("Error", "Student ERP does not exist!")
                    return

                if student[0] >= 3:  # Assuming a maximum of 3 books per student
                    messagebox.showerror("Error", "Student has already reached the limit of issued books!")
                    return
                
                # Issue the book
                cursor.execute(
                    "INSERT INTO IssuedBooks (ERP, BookID, IssueDate) VALUES (%s, %s, %s)",
                    (erp, book_id, issue_date)
                )
                conn.commit()
                messagebox.showinfo("Success", "Book issued successfully!")
                issue_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to issue book: {err}")

        issue_window = Toplevel(self.root)
        issue_window.title("Issue Book")
        issue_window.geometry("400x300")

        Label(issue_window, text="Student ERP", font=("Arial", 14)).place(x=50, y=30)
        student_erp_entry = Entry(issue_window, font=("Arial", 14))
        student_erp_entry.place(x=150, y=30)

        Label(issue_window, text="Book ID", font=("Arial", 14)).place(x=50, y=70)
        book_id_entry = Entry(issue_window, font=("Arial", 14))
        book_id_entry.place(x=150, y=70)

        Label(issue_window, text="Issue Date (YYYY-MM-DD)", font=("Arial", 14)).place(x=50, y=110)
        issue_date_entry = Entry(issue_window, font=("Arial", 14))
        issue_date_entry.place(x=150, y=110)

        Button(issue_window, text="Issue", command=save_issue, width=10, font=("Arial", 12), bg="#adefd1").place(x=150, y=200)

    def return_book(self):
        """Return an issued book."""
        def save_return():
            erp = student_erp_entry.get()
            book_id = book_id_entry.get()
            return_date = return_date_entry.get()

            if not all([erp, book_id, return_date]):
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                cursor.execute(
                    "SELECT * FROM IssuedBooks WHERE ERP = %s AND BookID = %s", (erp, book_id)
                )
                issued_book = cursor.fetchone()

                if not issued_book:
                    messagebox.showerror("Error", "No record of this book being issued to the student!")
                    return

                # Return the book
                cursor.execute(
                    "DELETE FROM IssuedBooks WHERE ERP = %s AND BookID = %s", (erp, book_id)
                )
                conn.commit()
                messagebox.showinfo("Success", "Book returned successfully!")
                return_window.destroy()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Failed to return book: {err}")

        return_window = Toplevel(self.root)
        return_window.title("Return Book")
        return_window.geometry("400x300")

        Label(return_window, text="Student ERP", font=("Arial", 14)).place(x=50, y=30)
        student_erp_entry = Entry(return_window, font=("Arial", 14))
        student_erp_entry.place(x=150, y=30)

        Label(return_window, text="Book ID", font=("Arial", 14)).place(x=50, y=70)
        book_id_entry = Entry(return_window, font=("Arial", 14))
        book_id_entry.place(x=150, y=70)

        Label(return_window, text="Return Date (YYYY-MM-DD)", font=("Arial", 14)).place(x=50, y=110)
        return_date_entry = Entry(return_window, font=("Arial", 14))
        return_date_entry.place(x=150, y=110)

        Button(return_window, text="Return", command=save_return, width=10, font=("Arial", 12), bg="#adefd1").place(x=150, y=200)


    def view_books(self):
        view_window = Toplevel(self.root)
        view_window.title("View Books")
        view_window.geometry("800x400")

        tree = ttk.Treeview(view_window, columns=("BookID", "Title", "Author", "Edition", "Quantity", "Status"), show='headings')
        tree.heading("BookID", text="Book ID")
        tree.heading("Title", text="Title")
        tree.heading("Author", text="Author")
        tree.heading("Edition", text="Edition")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Status", text="Status")
        tree.pack(fill=BOTH, expand=True)

        cursor.execute("SELECT * FROM Books")
        for row in cursor.fetchall():
            tree.insert('', END, values=row)

    def view_issued_books(self):
        view_window = Toplevel(self.root)
        view_window.title("View Issued Books")
        view_window.geometry("800x400")

        tree = ttk.Treeview(view_window, columns=("ERP", "Name", "BookID", "Title", "IssueDate", "ReturnDate"), show='headings')
        tree.heading("ERP", text="Student ERP")
        tree.heading("Name", text="Name")
        tree.heading("BookID", text="Book ID")
        tree.heading("Title", text="Book Title")
        tree.heading("IssueDate", text="Issue Date")
        tree.heading("ReturnDate", text="Return Date")
        tree.pack(fill=BOTH, expand=True)

        cursor.execute("""
        SELECT IssuedBooks.ERP, Students.Name, IssuedBooks.BookID, Books.Title, IssuedBooks.IssueDate, IssuedBooks.ReturnDate
        FROM IssuedBooks
        JOIN Students ON IssuedBooks.ERP = Students.ERP
        JOIN Books ON IssuedBooks.BookID = Books.BookID
        """)
        for row in cursor.fetchall():
            tree.insert('', END, values=row)


if __name__ == "__main__":
    root = Tk()
    app = LibraryManagement(root)
    root.mainloop()
