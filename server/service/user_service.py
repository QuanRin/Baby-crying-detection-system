from flask_sqlalchemy import SQLAlchemy
from entity.user import User


class UserService:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def create(self, username: str, age: int, email: str, phone_number: str):
        user = User(username=username, age=age,
                    email=email, phone_number=phone_number)
        self.db.session.add(user)
        self.db.session.commit()
        return user

    def update(self, id: int, detail: dict):
        User.query.filter_by(id=id).update(detail)
        self.db.session.commit()
