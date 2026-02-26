from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import User, EnergyRecord


class EnergyService:

    @staticmethod
    async def get_or_create_user(
        session: AsyncSession,
        telegram_id: int,
        username: str | None,
    ) -> User:

        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalar_one_or_none()

        if user:
            return user

        user = User(
            telegram_id=telegram_id,
            username=username,
        )

        session.add(user)
        await session.flush()

        return user

    @staticmethod
    async def create_record(
        session: AsyncSession,
        telegram_id: int,
        username: str | None,
        energy: int,
        concentration: int,
        activity: str,
    ) -> None:

        user = await EnergyService.get_or_create_user(
            session=session,
            telegram_id=telegram_id,
            username=username,
        )

        record = EnergyRecord(
            user_id=user.id,
            energy=energy,
            concentration=concentration,
            activity=activity,
        )

        session.add(record)
        await session.commit()
