import tkinter as tk
import tkinter.messagebox
from PIL import ImageTk, Image
from Models import Book
import datetime
from Databases import db
from Utils import data
from Models import User
class LibraryApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.geometry(self, "1024x640+50+50")

        """
        Frames will be "stacked" on top of each other in the container
        Active frame will be raised above others
        """
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for page in (LoginPage, SignupPage, LibraryPage):
            pageName = page.__name__
            frame = page(parent=container, controller=self)
            self.frames[pageName] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame("LoginPage")

    """
    Raises specified frame to the top of the container (makes it visible)
    """
    def showFrame(self, pageName):
        self.winfo_toplevel().title(pageName)
        frame = self.frames[pageName]
        frame.tkraise()
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        """
        GUI declarations
        """
        book = Image.open("Images/book.png")
        bookImage = ImageTk.PhotoImage(book.resize((196, 196)))
        bookLabel = tk.Label(self, image=bookImage)
        bookLabel.image = bookImage
        bookLabel.pack()
        titleLabel = tk.Label(self, text="Login page")
        titleLabel.pack(pady=10)

        emailLabel = tk.Label(self, text="Email")
        emailLabel.pack()
        inputEmail = tk.Entry(self, width=25, font="Montserrat 10")
        inputEmail.pack()

        passwordLabel = tk.Label(self, text="Password")
        passwordLabel.pack()
        inputPassword = tk.Entry(self, show="*", width=25, font="Montserrat 10")
        inputPassword.pack()

        errorLabel = tk.Label(self, fg="red")
        errorLabel.pack()

        loginButton = tk.Button(self, text="Log in", command=lambda: loginUser())
        loginButton.pack()
        orLabel = tk.Label(self, text="or")
        orLabel.pack(pady=10)
        signupButton = tk.Button(self, text="Create an account", command=lambda: controller.showFrame("SignupPage"))
        signupButton.pack()

        def loginUser():
            """
            Attempts to log in the user
            Returns an error message upon failure
            Redirects user to LibraryPage upon success
            :return: Error message
            """
            email = inputEmail.get()
            password = inputPassword.get()
            errorText = ""
            if not data.validateEmail(email):
                errorText += "Email should not be empty!\n"
            if not data.validatePassword(password):
                errorText += "Password should be between 8 and 20 characters long and contain at least one special character!\n"
            if(len(errorText)) > 0:
                errorLabel.config(text=errorText)
                return
            else:
                userInfo = db.loginUser(email, password)
                if userInfo:
                    user.login(userInfo["userID"], userInfo["email"], userInfo["firstName"], userInfo["lastName"])
                    tkinter.messagebox.showinfo("Library Application", "Logged in as " + user.firstName + "! Redirecting...")
                    controller.showFrame("LibraryPage")
                else:
                    errorLabel.config(text="Password doesn't match the specified email!")
class SignupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        """
        GUI declarations
        """
        book = Image.open("Images/book.png")
        bookImage = ImageTk.PhotoImage(book.resize((196, 196)))
        bookLabel = tk.Label(self, image=bookImage)
        bookLabel.image = bookImage
        bookLabel.pack()

        titleLabel = tk.Label(self, text="Signup Page")
        titleLabel.pack()

        emailLabel = tk.Label(self, text="Email")
        emailLabel.pack()
        inputEmail = tk.Entry(self, width=25, font="Montserrat 10")
        inputEmail.pack()

        firstNameLabel = tk.Label(self, text="First name")
        firstNameLabel.pack()
        inputFirstName = tk.Entry(self, width=25, font="Montserrat 10")
        inputFirstName.pack()
        lastNameLabel = tk.Label(self, text="Last name")
        lastNameLabel.pack()
        inputLastName = tk.Entry(self, width=25, font="Montserrat 10")
        inputLastName.pack()

        passwordLabel = tk.Label(self, text="Password")
        passwordLabel.pack()
        inputPassword = tk.Entry(self, show="*", width=25, font="Montserrat 10")
        inputPassword.pack()

        errorLabel = tk.Label(self, fg="red")
        errorLabel.pack()

        registerButton = tk.Button(self, text="Register", command=lambda: signupUser())
        registerButton.pack()

        def signupUser():
            """
            Attempts to create a new account
            Returns an error message upon failure
            Redirects user to login upon success
            :return: Error message
            """
            email = inputEmail.get()
            password = inputPassword.get()
            firstName = inputFirstName.get()
            lastName = inputLastName.get()
            errorText = ""

            if not data.validateEmail(email):
                errorText += "Email should not be empty!\n"
            if not data.validateName(firstName) or not data.validateName(lastName):
                errorText += "Names should only contain letters!\n"
            if not data.validatePassword(password):
                errorText += "Password should be between 8 and 20 characters long and contain at least one special character!\n"

            if(len(errorText)) > 0:
                errorLabel.config(text=errorText)
                return
            else:
                hashedPassword = data.hashPassword(password)
                if db.createUser(email, hashedPassword, firstName, lastName):
                    tkinter.messagebox.showinfo("Library Application", "User created! Redirecting...")
                    controller.showFrame("LoginPage")
                else:
                    errorText += "User already exists!"
                    errorLabel.config(text=errorText)

class LibraryPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        logoutButton = tk.Button(self, text="Logout", command=lambda: logoutUser())
        logoutButton.pack(pady=20)

        def populateFrames(bookList):
            """
            Rebuilds destroyed frames with updated information from the database
            :param bookList: List of books to be displayed
            """

            """
            Filter GUI declarations
            """
            filterBarFrame = tk.Frame(self)
            filterBarFrame.pack()
            filterBarLabel = tk.Label(filterBarFrame, text="Filter by: ")
            filterBarLabel.pack(side="top")

            availableButton = tk.Button(filterBarFrame, text="Available", command=lambda: filterByAvailable([filterBarFrame, booksFrame]))
            availableButton.pack()
            dueTodayButton = tk.Button(filterBarFrame, text="Due today", command=lambda: filterByDueToday([filterBarFrame, booksFrame]))
            dueTodayButton.pack()
            unavailableButton = tk.Button(filterBarFrame, text="Unavailable", command=lambda: filterByUnavailable([filterBarFrame, booksFrame]))
            unavailableButton.pack()
            showAllButton = tk.Button(filterBarFrame, text="Show All", command=lambda: showAll([filterBarFrame, booksFrame]))
            showAllButton.pack()

            """
            Create parent frame for the book list
            """
            booksFrame = tk.Frame(self)
            booksFrame.pack()
            books = []
            for result in bookList:  # create a new instance of Book and add it to the books array
                book = Book.Book(result[0], result[1], result[2], result[3], result[4], result[5], result[6])
                books.append(book)

            row = 0
            for book in books:  # create new frame for each book
                frame = tk.Frame(booksFrame, borderwidth=2, relief="solid")
                frame.grid(row=row, column=0, padx=10, pady=10)

                if book.imagePath:  # if the image path is in the database, display the image
                    cover = Image.open(book.imagePath)
                    image = ImageTk.PhotoImage(cover.resize((50, 70)))
                    imageLabel = tk.Label(frame, image=image)
                    imageLabel.image = image
                    imageLabel.grid(row=row, column=1)

                title = tk.Label(frame, text=book.title)
                title.grid(row=row, column=2, padx=20)

                available = tk.Label(frame, text="Available", fg="green")
                available.grid(row=row, column=3, padx=20)
                bookInfoButton = tk.Button(frame, text="Book Info",
                                       command=lambda desc=book.description: tkinter.messagebox.showinfo(
                                           "Book Information", desc))
                bookInfoButton.grid(row=row, column=5, padx=10)

                if (book.available == 0):  # if the book is Unavailable, display the due date and borrower information
                    available.config(text="Unavailable", fg="red")
                    dueDate = tk.Label(frame, text="Due date: " + book.dueDate)
                    dueDate.grid(row=row, column=4, padx=20)
                    borrower = db.getBorrowerInfo(book)
                    borrowerInfoButton = tk.Button(frame, text="Borrower Info", command=lambda currentBorrower=borrower:
                    tkinter.messagebox.showinfo("Borrower Info",
                                                "Name: " + borrower["firstName"] + " " + borrower["lastName"] +
                                                "\n" + "Email: " + borrower["email"]))
                    borrowerInfoButton.grid(row=row, column=6, padx=10)
                else:
                    borrowButton = tk.Button(frame, text="Borrow",
                                             command=lambda currentBook=book: borrowBook(currentBook, user, [filterBarFrame, booksFrame]))
                    borrowButton.grid(row=row, column=6, padx=10)
                row += 1

        def clearFrames(frames):
            """
            Destroys frames
            :param frames: List of frames to be destroyed
            """
            for frame in frames:
                tk.Frame.destroy(frame)

        def borrowBook(book, user, frames):
            """
            Allows the user to "borrow" a book
            Updates database with the borrower information and due date
            Repopulates frames with updated information
            :param book: Book to be borrowed
            :param user: Instance of the User class
            :param frames: List of frames to be repopulated
            """
            dateToday = datetime.datetime.now()
            dueDate = dateToday + datetime.timedelta(days=10)
            dueDate = dueDate.strftime("%x")
            db.borrowBook(book, user, dueDate)
            tkinter.messagebox.showinfo("Library Application", str(user.firstName) + " has borrowed " + str(book.title) +
                                        "\nDue date is: " + str(dueDate))
            clearFrames(frames)
            bookList = db.listAllBooks()
            populateFrames(bookList)
        def filterByAvailable(frames):
            """
            Only lists books marked as "Available"
            :param frames: Frames to be repopulated
            """
            bookList = db.listAvailableBooks()
            clearFrames(frames)
            populateFrames(bookList)
        def filterByDueToday(frames):
            """
            Only lists books which are due in today
            :param frames: Frames to be repopulated
            :return:
            """
            bookList = db.listBooksDueToday()
            clearFrames(frames)
            populateFrames(bookList)
        def filterByUnavailable(frames):
            """
            Only lists books which are marked as "Unavailable"
            :param frames: Frames to be repopualted
            :return:
            """
            bookList = db.listUnavailableBooks()
            clearFrames(frames)
            populateFrames(bookList)
        def showAll(frames):
            """
            Lists all books in the database
            :param frames: Frames to be repopulated
            :return:
            """
            bookList = db.listAllBooks()
            clearFrames(frames)
            populateFrames(bookList)
        def logoutUser():
            global user
            controller.showFrame("LoginPage")
            tkinter.messagebox.showinfo("Logged out", user.firstName + " has logged out")
            user = User.User()

        bookList = db.listAllBooks()
        populateFrames(bookList)

if __name__ == "__main__":
    user = User.User()
    app = LibraryApplication()

    app.mainloop()
