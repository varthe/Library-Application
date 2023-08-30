from PIL import ImageTk


class Book():
    def __init__(self, bookID, imagePath, title, description, available, dueDate, userID):
        self.bookID = bookID
        self.imagePath = imagePath
        self.title = title
        self.description = description
        self.available = available
        self.dueDate = dueDate
        self.userID = userID