import sqlite3

# WEEK 4: Database Management
class DatabaseManager:
    def __init__(self, db_name="snake_game.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                             (username TEXT PRIMARY KEY, 
                              password TEXT, 
                              first_name TEXT, 
                              last_name TEXT, 
                              email TEXT UNIQUE, 
                              phone TEXT UNIQUE,
                              high_score INTEGER DEFAULT 0)''')
        self.conn.commit()

    def register_user(self, username, password, fname, lname, email, phone):
        if phone.strip() == "":
            phone = None

        try:
            self.cursor.execute("""INSERT INTO users 
                                   (username, password, first_name, last_name, email, phone, high_score) 
                                   VALUES (?, ?, ?, ?, ?, ?, 0)""", 
                                (username, password, fname, lname, email, phone))
            self.conn.commit()
            return "Success"
        except sqlite3.IntegrityError:
            return "Registration failed (Duplicate Data)"

    def validate_login(self, identifier, password):
        query = """SELECT * FROM users 
                   WHERE (username = ? OR email = ? OR phone = ?) 
                   AND password = ?"""
        self.cursor.execute(query, (identifier, identifier, identifier, password))
        return self.cursor.fetchone()

    def update_score(self, username, new_score):
        self.cursor.execute("SELECT high_score FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result and new_score > result[0]:
            self.cursor.execute("UPDATE users SET high_score = ? WHERE username = ?", (new_score, username))
            self.conn.commit()

    def get_leaderboard(self):
        self.cursor.execute("SELECT username, high_score FROM users ORDER BY high_score DESC LIMIT 5")
        return self.cursor.fetchall()