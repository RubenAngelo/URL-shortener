from sqlalchemy.orm import Session

from app.core.logging_config import setup_logging
from app.models.user_db_model import User
from app.schema.user_schema import UserCreate
from app.utils.utils import get_password_hash

logger = setup_logging("user_crud")


def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Busca um usuário pelo nome de usuário.
    """

    logger.info("Autenticando usuário...")

    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Busca um usuário pelo ID.
    """
    return db.query(User).get(user_id)


def create_user(db: Session, user: UserCreate) -> User:
    """
    Cria um novo usuário no banco de dados.
    A senha é hasheada antes de ser armazenada.
    """

    logger.info("Criando usuário...")

    password = get_password_hash(user.password)

    db_user = User(email=user.email, password=password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
