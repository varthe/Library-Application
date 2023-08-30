CREATE TABLE IF NOT EXISTS users (
        userID INTEGER PRIMARY KEY,
        email VARCHAR(20),
        firstName VARCHAR(20),
        lastName VARCHAR(20),
        password VARCHAR(80))
CREATE TABLE IF NOT EXISTS books (
        bookID INTEGER PRIMARY KEY,
        imagePath VARCHAR(50) DEFAULT NULL,
        title VARCHAR(50),
        description VARCHAR(300),
        available INTEGER DEFAULT 1,
        dueDate VARCHAR(20) DEFAULT NULL,
        userID INTEGER DEFAULT NULL,
        FOREIGN KEY (userID) REFERENCES users(userID))
INSERT INTO books (imagePath, title, description) VALUES ('Images/Books/1.jpg', 'Frankenstein', 'Frankenstein; or, The Modern Prometheus is an 1818 novel written by English author Mary Shelley. Frankenstein tells the story of Victor Frankenstein, a young scientist who creates a sapient creature in an unorthodox scientific experiment.')
INSERT INTO books (imagePath, title, description) VALUES ('Images/Books/2.jpg', 'The Lord of the Rings', 'The Lord of the Rings is an epic high-fantasy novel by the English author and scholar J. R. R. Tolkien. Set in Middle-earth, the story began as a sequel to Tolkiens 1937 childrens book The Hobbit, but eventually developed into a much larger work.')
INSERT INTO books (imagePath, title, description) VALUES ('Images/Books/3.jpg', '1984', 'Nineteen Eighty-Four is a dystopian social science fiction novel and cautionary tale by English writer George Orwell. It was published on 8 June 1949 by Secker & Warburg as Orwells ninth and final book completed in his lifetime.')
