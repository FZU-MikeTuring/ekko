from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, UploadFile

from models.users import Users
from utils.auth import get_current_user
from utils.file_storage import save_image_upload
from utils.response import success_response


ekko = APIRouter(prefix="/api/uploads", tags=["uploads"])


@ekko.post("/avatar")
async def upload_avatar(
    scope: Annotated[str, Form(...)],
    file: Annotated[UploadFile, File(...)],
    user: Users = Depends(get_current_user),
):
    _ = user
    path = await save_image_upload(file, scope=scope)
    return success_response(
        message="Upload success",
        data={"path": path},
    )
