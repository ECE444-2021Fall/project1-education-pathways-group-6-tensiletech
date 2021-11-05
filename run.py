from app import create_app
import os

if __name__ == "__main__":
    app = create_app()
    app.run(os.getenv('FLASK_CONFIG') or "default")

