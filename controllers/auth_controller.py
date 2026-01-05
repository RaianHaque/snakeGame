from models.database_manager import DatabaseManager

class AuthController:
    def __init__(self):
        # DatabaseManager must be initialized here to persist across the session
        self.db = DatabaseManager()
        self.current_user = None

    def sign_up(self, username, password):
        # Basic validation: Prevents empty or tiny strings from entering the DB
        if len(username) < 5 or len(password) < 5:
            return "Too short!"
        success = self.db.register_user(username, password)
        return "Success!" if success else "Exists!"

    def login(self, username, password):
        # Returns True only if SQLite finds an exact match for user/pass
        user_data = self.db.validate_login(username, password)
        if user_data:
            self.current_user = username
            return True
        return False