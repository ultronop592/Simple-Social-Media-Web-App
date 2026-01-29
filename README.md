# Simple Social Media Web App

A full-stack social media web application built with FastAPI (backend) and Streamlit (frontend). Users can register, log in, upload images/videos with captions, and view a feed of posts.

## Features

- User registration and authentication (JWT)
- Upload images and videos with captions
- View a feed of all posts
- Delete your own posts
- Modern Streamlit frontend
- SQLite database (default, easy to switch to PostgreSQL/MySQL)
- ImageKit integration for media storage

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── app.py           # FastAPI main app (routes, endpoints)
│   ├── db.py            # Database models and connection
│   ├── image.py         # ImageKit integration
│   ├── schemas.py       # Pydantic schemas
│   ├── user.py          # User management/auth
├── frontend.py          # Streamlit frontend
├── main.py              # Uvicorn entrypoint
├── pyproject.toml       # Python dependencies
├── .env                 # Environment variables (ImageKit keys, etc.)
├── README.md            # Project documentation
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/ultronop592/Simple-Social-Media-Web-App.git
cd Simple-Social-Media-Web-App
```

### 2. Set up the environment

Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Activate the venv:
# On Windows:
.venv\Scripts\activate
# On Mac/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

Or, if using `uv`:

```bash
python -m uv pip install -r pyproject.toml
```

### 3. Configure environment variables

Create a `.env` file in the root directory:

```
IMAGEKIT_PRIVATE_KEY=your_private_key
IMAGEKIT_PUBLIC_KEY=your_public_key
IMAGEKIT_URL_ENDPOINT=your_url_endpoint
```

### 4. Run the backend

```bash
python main.py
```
The FastAPI backend will run on [http://localhost:8001](http://localhost:8001).

### 5. Run the frontend

```bash
streamlit run frontend.py
```
The Streamlit app will run on [http://localhost:8501](http://localhost:8501).

## Usage

- Register a new user or log in.
- Upload images or videos with captions.
- View and interact with the feed.
- Delete your own posts.

## Tech Stack

- **Backend:** FastAPI, SQLAlchemy, SQLite, FastAPI Users, ImageKit
- **Frontend:** Streamlit
- **Auth:** JWT

## License

MIT License

---

Feel free to customize this README for your needs!
