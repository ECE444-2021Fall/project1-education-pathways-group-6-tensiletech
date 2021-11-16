from app import create_app
import os

app = create_app()
app.run(host='0.0.0.0') #os.getenv('FLASK_CONFIG') or "default"

