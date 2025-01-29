from enums.models import LanguageEnum
from sqlalchemy import select, update

from database.models import User, UserSettings, async_session


async def get_user_language(tg_id: int) -> LanguageEnum:
    async with async_session() as session:
        result = await session.execute(
            select(UserSettings.language_code).join(User).filter(User.tg_id == tg_id)
        )
        return result.scalars().first()


async def user_exists(tg_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(select(User).filter_by(tg_id=tg_id))
        return result.scalars().first() is not None


async def add_user(
    tg_id: int,
    language_code: LanguageEnum,
) -> None:
    async with async_session() as session:
        user = User(tg_id=tg_id)
        user_settings = UserSettings(language_code=language_code, user=user)
        session.add(user)
        session.add(user_settings)
        await session.commit()


async def update_user_language(tg_id: int, new_language_code: LanguageEnum) -> None:
    async with async_session() as session:
        subquery = select(User.id).where(User.tg_id == tg_id).scalar_subquery()
        await session.execute(
            update(UserSettings)
            .where(UserSettings.user_id == subquery)
            .values(language_code=new_language_code)
        )
        await session.commit()


async def user_is_whitelisted(tg_id: int) -> bool:
    async with async_session() as session:
        if await user_exists(tg_id):
            result = await session.execute(
                select(User.is_whitelisted).where(User.tg_id == tg_id)
            )
            return result.scalars().first()
        return False


async def user_is_admin(tg_id: int) -> bool:
    async with async_session() as session:
        if await user_exists(tg_id):
            result = await session.execute(
                select(User.is_admin).where(User.tg_id == tg_id)
            )
            return result.scalars().first()
        return False


async def set_user_is_whitelisted(tg_id: int, is_whitelisted: bool = True) -> None:
    async with async_session() as session:
        if not await user_exists(tg_id):
            return
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(is_whitelisted=is_whitelisted)
        )
        await session.commit()


async def set_user_is_admin(tg_id: int, is_admin: bool = True) -> None:
    async with async_session() as session:
        if not await user_exists(tg_id):
            return
        await session.execute(
            update(User).where(User.tg_id == tg_id).values(is_admin=is_admin)
        )
        await session.commit()
