# WEEK 4: Authentication Logic
from models.database_manager import DatabaseManager

class AuthController:
    def __init__(self):
        self.db = DatabaseManager()
        self.current_user = None

    def sign_up(self, username, password):
        if len(username) < 5 or len(password) < 5:
            return "Too short!"
        success = self.db.register_user(username, password)
        return "Success!" if success else "Exists!"

    def login(self, username, password):
        user_data = self.db.validate_login(username, password)
        if user_data:
            self.current_user = username
            return True
        return False