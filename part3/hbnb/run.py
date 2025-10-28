"""Application entry point for the HBnB Flask application."""

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
