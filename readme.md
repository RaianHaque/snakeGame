# Snake Game

A Python-based desktop Snake game built with `pygame`. The project includes multiple play modes, theme support, audio, user authentication with persistent high-scores (SQLite), and optional OpenCV-powered menu video backgrounds. It is designed as a modular MVC-like project for learning and distribution.

## Features

- Play modes: **Classic** (wraparound), **Box** (walls kill), **Obstacles** (pre-generated obstacles).
- Themes: Classic, Desert, Jungle, Ocean.
- Audio: Background music and SFX (eat, death, click) with mute control.
- Authentication: Sign up / Login and per-user high-score persistence via SQLite.
- Leaderboard: Top scores displayed in the menu.
- Dev tools: Dev Mode to set score manually for testing.
- Responsive window resizing and adaptive UI layout.
- Packaging support: PyInstaller `.spec` included for building a distributable executable.

## Requirements

- Python 3.8+ (3.x)
- Dependencies:
  - `pygame`
  - `opencv-python` (optional — for video backgrounds)
  - `sqlite3` (built-in with Python)

Install dependencies:

```powershell
pip install pygame
pip install opencv-python   # optional
```

## Project Structure

- `snakeGameMain.py` — application bootstrap, main loop, and state handling (LOGIN, SIGNUP, MODE_SELECT, GAME, PAUSED, GAME_OVER).
- `controllers/` — controllers (e.g., `controllers/auth_controller.py`).
- `models/` — domain models and persistence (`snake.py`, `food.py`, `database_manager.py`).
- `views/` — UI and rendering (`game_view.py`, `menu_view.py`).
- `assets/` — images and optional video background files.
- `sounds/` — audio files (music and SFX).
- `snakeGameMain.spec` — PyInstaller spec for building an executable.
- `project_report.txt` — generated project report summary.

## Quick Start

1. Install Python 3.x and dependencies.
2. From the project root, run:

```powershell
python snakeGameMain.py
```

Notes: If `opencv-python` is not installed or `assets/menu_bg.mp4` is missing, the menu will fall back to static images.

## Authentication & Database

- User accounts and high-scores are stored in a local SQLite database `snake_game.db` managed by `models/database_manager.py`.
- Current schema fields: `username` (PRIMARY KEY), `password` (stored plaintext in this version — must be hashed for production), `first_name`, `last_name`, `email`, `phone`, `high_score`.
- Key functions:
  - `register_user(username, password, fname, lname, email, phone)` — create user record.
  - `validate_login(identifier, password)` — authenticate by username/email/phone.
  - `update_score(username, new_score)` — updates high score if higher.
  - `get_leaderboard()` — returns top 5 scores.

## Dev Mode (Testing)

- Enable Dev Mode from the login/menu screen via the dev trigger in the top-right corner.
- Enter the developer PIN (default `1234`) to enable Dev Mode.
- When Dev Mode is active, you can click the score during gameplay to edit it for testing purposes.

## Packaging (PyInstaller)

Use PyInstaller to create a bundled executable. Example:

```powershell
pyinstaller --onefile snakeGameMain.spec
```

If packaging, ensure the `assets/` and `sounds/` folders are included using PyInstaller `--add-data` or within the `.spec` file.

## Known Limitations & Suggested Improvements

- Passwords are stored as plaintext — replace with secure hashing (e.g., `bcrypt`) before any real deployments.
- No cloud sync or remote leaderboard — consider adding a server-backed leaderboard.
- Input validation and security are minimal — sanitize/validate inputs and add rate-limiting or reCAPTCHA for web endpoints if added later.
- Consider unit tests and CI integration for reliability.

## Contributing

- Fork the repository, create a feature branch, implement changes, and open a pull request.
- Suggested improvements:
  - Add password hashing and secure authentication flows.
  - Add cloud-backed leaderboard and user sync.
  - Improve UI polish and an options/settings menu.

## Screenshots

- Add screenshots under `screenshots/` (e.g., `screenshots/login.png`, `screenshots/gameplay.png`, `screenshots/leaderboard.png`) and update this README to reference them.

## License

Specify a license for the project (e.g., MIT, GPL) and add a `LICENSE` file.

## Contact

Author / Maintainer: [Your Name / ID]
Repository: RaianHaque/snakeGame (branch: raian)
snake game
Dev Mode:
Enabling Dev Mode:

On the Login Screen, look at the Top Right Corner. There is a switch.

Click it. It will ask for a PIN.

Enter 1234 and press Enter.

It will say "DEV MODE ON".

Modifying Score (In-Game):

Start a game.

Look at the Score Text in the top left.

Because Dev Mode is ON, you will see green text saying [CLICK SCORE TO EDIT].

Click the score number.

Type a new number (e.g., 500) and press Enter.

Result: Your score jumps to 500, and the snake speed increases immediately to match that score level. This is great for testing high-speed collisions without playing for hours.