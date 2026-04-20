from datetime import datetime

from sqlalchemy import BIGINT, CHAR, DateTime, Index, JSON, Text, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class Users(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_user_email", "email"),
        Index("idx_user_id", "id"),
    )

    id: Mapped[str] = mapped_column(CHAR(7), primary_key=True, comment="用户ID")
    avatar: Mapped[str | None] = mapped_column(Text, nullable=True, comment="用户头像")
    nick_name: Mapped[str] = mapped_column(VARCHAR(20), nullable=False, comment="昵称")
    pwd: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="密码")
    email: Mapped[str] = mapped_column(VARCHAR(255), unique=True, nullable=False, comment="邮箱")
    last_online_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="最后在线时间",
    )
    voice_settings: Mapped[dict | None] = mapped_column(JSON, nullable=True, comment="语音设置")


class UserToken(Base):
    __tablename__ = "user_token"
    __table_args__ = (
        Index("idx_token", "token"),
        Index("idx_user_id", "user_id"),
    )

    id: Mapped[int] = mapped_column(BIGINT, autoincrement=True, primary_key=True, comment="令牌ID")
    user_id: Mapped[str] = mapped_column(CHAR(7), nullable=False, comment="用户ID")
    token: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, unique=True, comment="令牌值")
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="过期时间")

    def __repr__(self) -> str:
        return f"<UserToken(id={self.id}, user_id={self.user_id}, token={self.token!r})>"
