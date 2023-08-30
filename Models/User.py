class User:
    def __init__(self):
        self.loggedIn = False
        self.userID = None
        self.username = None

    def login(self, userID, email, firstName, lastName):
        self.userID = userID
        self.email = email
        self.firstName = firstName
        self.lastName = lastName
