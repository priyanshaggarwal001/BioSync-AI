from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService(BaseService[User]):

    def __init__(self):
        super().__init__(User)

    def get_by_email(
        self,
        db: Session,
        email: str,
    ) -> User | None:

        statement = select(User).where(User.email == email)
        return db.scalar(statement)

    def create_user(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> User:

        user = User(
    email=user_data.email,
    password_hash=user_data.password,
)

        return self.create(db, user)

    def update_user(
        self,
        db: Session,
        user: User,
        user_data: UserUpdate,
    ) -> User:

        updates = user_data.model_dump(exclude_unset=True)

        return self.update(
            db,
            user,
            updates,
        )


user_service = UserService()