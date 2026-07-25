from sqlalchemy.orm import Session

from app.db.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    # ============================================================
    # CREATE
    # ============================================================

    def create(self, user: User):
        self.db.add(user)
        return user

    # ============================================================
    # READ
    # ============================================================

    def get_by_id(self, user_id: int):
        return (
            self.db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    def get_by_email(self, email: str):
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )

    def get_by_organization_id(self, organization_id: int):
        return (
            self.db.query(User)
            .filter(User.organization_id == organization_id)
            .first()
        )