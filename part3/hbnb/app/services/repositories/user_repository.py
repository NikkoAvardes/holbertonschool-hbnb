from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self, model):
        super().__init__(model)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()
