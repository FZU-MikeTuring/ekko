import enum
from datetime import datetime

from sqlalchemy import CHAR, DateTime, Enum, ForeignKeyConstraint, Index, PrimaryKeyConstraint, TEXT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import BOOLEANTYPE

from models.base import Base
from models.users import Users


class Domains(Base):
    __tablename__ = "domain"

    id: Mapped[str] = mapped_column(CHAR(8), primary_key=True, comment="域ID")
    create_id: Mapped[str] = mapped_column(CHAR(7), nullable=False, comment="创建者ID")
    avatar: Mapped[str | None] = mapped_column(TEXT, nullable=True, comment="域头像URL或Base64")
    domain_name: Mapped[str] = mapped_column(VARCHAR(255), nullable=False, comment="域名称")
    description: Mapped[str | None] = mapped_column(TEXT, nullable=True, comment="域描述")
    is_public: Mapped[bool] = mapped_column(BOOLEANTYPE, default=True, comment="是否公开")


class DomainMemberRole(enum.Enum):
    Owner = "owner"
    Admin = "admin"
    Member = "member"


class DomainMembers(Base):
    __tablename__ = "domain_members"
    __table_args__ = (
        PrimaryKeyConstraint("domain_id", "member_id", name="pk_domain_member"),
        ForeignKeyConstraint(["domain_id"], [Domains.id], name="fk_domain_members_domain"),
        ForeignKeyConstraint(["member_id"], [Users.id], name="fk_domain_members_user"),
        Index("idx_domain_member", "member_id"),
    )

    domain_id: Mapped[str] = mapped_column(CHAR(8), nullable=False, comment="域ID")
    member_id: Mapped[str] = mapped_column(CHAR(7), nullable=False, comment="成员ID")
    alias: Mapped[str | None] = mapped_column(VARCHAR(50), nullable=True, comment="域内别名")
    join_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, comment="加入时间")
    role: Mapped[DomainMemberRole] = mapped_column(
        Enum(DomainMemberRole, values_callable=lambda items: [item.value for item in items]),
        default=DomainMemberRole.Member,
        comment="成员角色",
    )
