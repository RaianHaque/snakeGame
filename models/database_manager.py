import sqlite3

class DatabaseManager:
    def __init__(self, db_name="snake_game.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                             (username TEXT PRIMARY KEY, password TEXT, high_score INTEGER DEFAULT 0)''')
        self.conn.commit()

    def register_user(self, username, password):
        try:
            self.cursor.execute("INSERT INTO users (username, password, high_score) VALUES (?, ?, 0)", (username, password))
            self.conn.commit()
            return True
        except: return False

    def validate_login(self, username, password):
        self.cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return self.cursor.fetchone()

    def update_score(self, username, new_score):
        # Update personal best
        self.cursor.execute("SELECT high_score FROM users WHERE username = ?", (username,))
        result = self.cursor.fetchone()
        if result and new_score > result[0]:
            self.cursor.execute("UPDATE users SET high_score = ? WHERE username = ?", (new_score, username))
            self.conn.commit()

    def get_leaderboard(self):
        # Fetch Top 5 scores
        self.cursor.execute("SELECT username, high_score FROM users ORDER BY high_score DESC LIMIT 5")
        return self.cursor.fetchall()