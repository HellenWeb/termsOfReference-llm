from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.sqlite import insert as sqlite_insert
from sqlalchemy import select
from bot.infrastructure.db.models import User

class SqlAlchemyUserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_or_create(
        self,
        telegram_id: int,
        *,
        username: str,
        first_name: str
    ) -> tuple[User, bool]:
        stmt = (
            sqlite_insert(User)
            .values(telegram_id=telegram_id, username=username, first_name=first_name, credits_balance=0)
            .on_conflict_do_nothing(index_elements=["telegram_id"])
            .returning(User.id)
        )

        result = await self._session.execute(stmt)
        inserted_id = result.scalar_one_or_none()
        created = inserted_id is not None

        if created:
            await self._session.commit()
            user = await self._session.get(User, inserted_id)
        else:
            user = await self._session.scalar(
                select(User).where(User.telegram_id == telegram_id)
            )
            if user is not None:
                dirty = False
                if username is not None and user.username != username:
                    user.username = username
                    dirty = True
                if first_name is not None and user.first_name != first_name:
                    user.first_name = first_name
                    dirty = True
                if dirty:
                    await self._session.commit()

        if user is None:
            raise RuntimeError(f"User with telegram_id={telegram_id} not found after get_or_create")

        return user, created
        


    
