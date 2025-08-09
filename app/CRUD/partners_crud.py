from sqlalchemy.orm import Session
from app.models.api_key_model import ApiKey
from app.core.env_config import settings
from app.core.logging_config import setup_logging

logger = setup_logging("partners_crud")


def create_initial_api_key(db: Session):
    """
    Cria uma chave de API inicial para o administrador se ela não existir.
    """

    logger.info("Criando chave de API para 'admin'...")

    existing_key = db.query(ApiKey).filter(ApiKey.client_name == "admin").first()

    if not existing_key:
        admin_key = ApiKey(key=settings.ADM_KEY, client_name="admin", is_active=True)

        db.add(admin_key)
        db.commit()
        db.refresh(admin_key)

        logger.info("Chave de API para 'admin' criada com sucesso!")

    else:
        logger.info("Chave de API para 'admin' já existente.")
