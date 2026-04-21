from pydantic import BaseModel, ConfigDict, NameEmail


class RegisterRequestUser(BaseModel):
    nick_name: str
    email: str
    verify_code: str
    pwd: str


class LoginRequestUser(BaseModel):
    email: str
    pwd: str


class UpdateUsersRequest(BaseModel):
    avatar: str | None = None
    nick_name: str | None = None
    pwd: str | None = None
    email: str | None = None
    voice_settings: dict | None = None


class ChangePasswordRequestUser(BaseModel):
    verify_code: str
    new_password: str


class ChangeEmailRequestUser(BaseModel):
    current_email: str
    current_verify_code: str
    new_email: str
    new_verify_code: str


class FindPasswordRequestUser(BaseModel):
    email: NameEmail
    verify_code: str
    new_password: str


class UserInfoResponse(BaseModel):
    id: str
    avatar: str | None
    nick_name: str
    email: str
    voice_settings: dict | None = None

    model_config = ConfigDict(from_attributes=True)


class UserSettingsRequest(BaseModel):
    settings: dict


class UserSettingsResponse(BaseModel):
    settings: dict


class UserAuthResponse(BaseModel):
    token: str
    user_info: UserInfoResponse

    model_config = ConfigDict(
        populate_by_name=True,
        from_attributes=True,
    )
