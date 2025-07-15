# imdbclone

A Django-based IMDb clone web application.

## Features

- User authentication (sign up, login, logout)
- Movie listing with search and filter
- Movie detail pages with ratings and reviews
- Add, edit, and delete movies (admin only)
- User profile pages
- RESTful API endpoints for movies and reviews

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite (default, can be changed)

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/imdbclone.git
   cd imdbclone
   ```

2. **Create a virtual environment and activate it:**
   ```sh
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```

7. **Access the app:**
   - Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Project Structure

- `imdbclone/` - Django project settings
- `movies/` - Main app for movie models, views, and templates
- `users/` - User authentication and profiles

## API Usage

- API endpoints are available under `/home/` & `/user/`
- Example: `/home/list/`, `/user/login/`