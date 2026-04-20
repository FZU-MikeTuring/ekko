from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.domain import DomainMemberRole


class DomainRequest(BaseModel):
    avatar: str | None = None
    domain_name: str = Field(...)
    description: str = Field(...)
    is_public: bool = Field(default=True)


class DomainUpdateRequest(BaseModel):
    id: str = Field(...)
    avatar: str | None = None
    domain_name: str | None = None
    description: str | None = None
    is_public: bool | None = None


class DomainResearchRequest(BaseModel):
    id: str | None = None
    domain_name: str | None = None
    description: str | None = None


class DomainInfo(BaseModel):
    id: str
    create_id: str
    avatar: str | None
    domain_name: str
    description: str | None
    is_public: bool

    model_config = ConfigDict(from_attributes=True)


class DomainInfosPage(BaseModel):
    total: int
    domain_infos: list[DomainInfo]

    model_config = ConfigDict(from_attributes=True)


class DomainMemberInfo(BaseModel):
    domain_id: str
    member_id: str
    alias: str | None
    join_time: datetime
    role: DomainMemberRole

    model_config = ConfigDict(from_attributes=True)


class DomainMemberSearchInfosRequest(BaseModel):
    domain_id: str
    role: str | None = None


class DomainMembersInfoPage(BaseModel):
    total: int
    domain_infos: list[DomainMemberInfo]

    model_config = ConfigDict(from_attributes=True)


class ChangeDomainMemberRoleRequest(BaseModel):
    domain_id: str
    member_id: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class DomainMemberAliasUpdateRequest(BaseModel):
    domain_id: str
    alias: str | None = Field(default=None, max_length=50)


class KickDomainMemberRequest(BaseModel):
    domain_id: str
    member_id: str
