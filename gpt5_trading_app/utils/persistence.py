from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from gpt5_trading_app.config.settings import settings
engine = create_engine(settings.DB_URL, future=True)
SessionLocal = sessionmaker(bind=engine, future=True)
def execute(sql: str, params: dict | None = None):
    with engine.begin() as conn:
        conn.execute(text(sql), params or {})
