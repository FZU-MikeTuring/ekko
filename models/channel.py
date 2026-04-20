import enum
from datetime import datetime

from sqlalchemy import (
    BIGINT,
    BOOLEAN,
    CHAR,
    DateTime,
    Enum,
    ForeignKeyConstraint,
    Index,
    Integer,
    PrimaryKeyConstraint,
    Text,
    VARCHAR,
)
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base
from models.domain import Domains
from models.users import Users


class ChannelType(enum.Enum):
    Voice = "voice"
    Text = "text"
    Both = "both"


class Channels(Base):
    __tablename__ = "channels"
    __table_args__ = (
        ForeignKeyConstraint(["domain_id"], [Domains.id], name="fk_channel_domain"),
        ForeignKeyConstraint(["create_id"], [Users.id], name="fk_channel_creator"),
        Index("idx_channel_domain", "domain_id"),
    )

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=True, comment="频道ID")
    domain_id: Mapped[str] = mapped_column(CHAR(8), nullable=False, comment="所属域ID")
    channel_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="频道名称")
    description: Mapped[str | None] = mapped_column(Text, nullable=True, comment="频道描述")
    create_id: Mapped[str] = mapped_column(CHAR(7), nullable=False, comment="创建者ID")
    max_capacity: Mapped[int] = mapped_column(Integer, default=10, comment="最大容量")
    current_voice_count: Mapped[int] = mapped_column(Integer, default=0, comment="当前语音人数")
    channel_type: Mapped[ChannelType] = mapped_column(
        Enum(ChannelType, values_callable=lambda items: [item.value for item in items]),
        default=ChannelType.Voice,
        comment="频道类型",
    )


class ChannelMembers(Base):
    __tablename__ = "channel_members"
    __table_args__ = (
        PrimaryKeyConstraint("channel_id", "member_id", name="pk_channel_member"),
        ForeignKeyConstraint(["channel_id"], [Channels.id], name="fk_channel_member_channel"),
        ForeignKeyConstraint(["member_id"], [Users.id], name="fk_channel_member_user"),
        Index("idx_channel_member_user", "member_id"),
    )

    channel_id: Mapped[int] = mapped_column(BIGINT, nullable=False, comment="频道ID")
    member_id: Mapped[str] = mapped_column(CHAR(7), nullable=False, comment="成员ID")
    join_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="加入时间")
    microphone_state: Mapped[bool] = mapped_column(BOOLEAN, default=False, comment="麦克风状态")
    speaker_state: Mapped[bool] = mapped_column(BOOLEAN, default=True, comment="扬声器状态")
    last_active_time: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="最后活跃时间",
    )
