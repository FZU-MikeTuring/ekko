from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from models.channel import ChannelType


class ChannelCreateRequest(BaseModel):
    domain_id: str
    channel_name: str
    description: str | None = None
    max_capacity: int = Field(default=10, ge=1, le=100)
    channel_type: str = Field(default="voice")


class ChannelUpdateRequest(BaseModel):
    id: int
    channel_name: str | None = None
    description: str | None = None
    max_capacity: int | None = Field(default=None, ge=1, le=100)
    channel_type: str | None = None


class ChannelJoinRequest(BaseModel):
    channel_id: int


class ChannelLeaveRequest(BaseModel):
    channel_id: int


class ChannelMemberStateUpdateRequest(BaseModel):
    channel_id: int
    microphone_state: bool | None = None
    speaker_state: bool | None = None


class ChannelInfo(BaseModel):
    id: int
    domain_id: str
    channel_name: str
    description: str | None
    create_id: str
    max_capacity: int
    current_voice_count: int
    channel_type: ChannelType

    model_config = ConfigDict(from_attributes=True)


class ChannelInfosPage(BaseModel):
    total: int
    channel_infos: list[ChannelInfo]


class ChannelMemberInfo(BaseModel):
    channel_id: int
    member_id: str
    join_time: datetime
    microphone_state: bool
    speaker_state: bool
    last_active_time: datetime

    model_config = ConfigDict(from_attributes=True)


class ChannelMembersPage(BaseModel):
    total: int
    channel_members: list[ChannelMemberInfo]


class LiveKitJoinResponse(BaseModel):
    room_name: str
    participant_identity: str
    participant_name: str
    livekit_url: str
    token: str
