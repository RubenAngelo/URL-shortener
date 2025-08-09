from sqlalchemy import Column, String, Text

from app.core.database_config import base


class UrlLookup(base):
    __tablename__ = "url_lookup"

    url_hash = Column(String(10), primary_key=True, index=True)
    url = Column(Text, nullable=False, unique=True, index=True)
    user_id = Column(Text, nullable=False)
