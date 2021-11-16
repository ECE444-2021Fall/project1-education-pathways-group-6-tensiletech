from app import create_app
import os

app = create_app()
app.run() #os.getenv('FLASK_CONFIG') or "default"

