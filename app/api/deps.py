from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session


async def get_session() -> AsyncSession:
    async for session in get_db_session():
        return session
    raise RuntimeError("Failed to acquire DB session.")
