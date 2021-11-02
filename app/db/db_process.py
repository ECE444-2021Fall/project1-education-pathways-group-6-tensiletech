from app import dbsql, login_manager
from .db_models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def add_(table_row):
    dbsql.session.add(table_row)
    dbsql.session.commit()

def querying_all(table):
    return table.query.all()

if __name__ == "__main__":
    user1 = User(username = "romil", email = "romil.sjain@gmail.com", password = "password")
    add_user(user1)
    users = querying_all(User)
    print(users)
