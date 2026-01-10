from app.database import Base
from app.db.session import engine

# importing this module registers all models in SQLAlchemy metadata
import app.db.base


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
