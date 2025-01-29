from config import settings
from enums.models import (
    LanguageEnum,
)
from sqlalchemy import (
    BigInteger,
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    select,
)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base, AsyncAttrs):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    is_whitelisted: Mapped[bool] = mapped_column(Boolean, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    settings: Mapped["UserSettings"] = relationship(
        "UserSettings", back_populates="user", uselist=False
    )

    def __repr__(self):
        return f"User(id={self.id}, tg_id={self.tg_id}, language_code={self.language_code})"  # noqa: E501


class UserSettings(Base, AsyncAttrs):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False, unique=True
    )
    language_code: Mapped[str] = mapped_column(Enum(LanguageEnum), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="settings")

    def __repr__(self):
        return (
            f"UserSettings(id={self.id}, user_id={self.user_id}, "
            f"language_code={self.language_code})"
        )


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)  # TODO: remove in production
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        existing_admin = await session.execute(
            select(User).where(User.tg_id == settings.TELEGRAM_ADMIN_ID)
        )
        admin = existing_admin.scalar()

        if not admin:
            admin = User(
                tg_id=settings.TELEGRAM_ADMIN_ID,
                is_whitelisted=True,
                is_admin=True,
            )
            session.add(admin)
            await session.flush()

            admin_settings = UserSettings(
                user_id=admin.id,
                language_code=LanguageEnum.EN,
            )
            session.add(admin_settings)

            await session.commit()
            print(
                f"✅ Administrator {settings.TELEGRAM_ADMIN_ID} was successfully added to the database."  # noqa: E501
            )
        else:
            print(f"ℹ️ Administrator {settings.TELEGRAM_ADMIN_ID} already exists.")
