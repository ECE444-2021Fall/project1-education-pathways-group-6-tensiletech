from app import dbsql, login_manager
from .db_models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def add_user(user):
    dbsql.session.add(user)
    dbsql.session.commit()
