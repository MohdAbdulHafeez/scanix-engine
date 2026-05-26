from fastapi import (
    UploadFile,
    HTTPException,
)


MAX_UPLOAD_MB = 10

ALLOWED_TYPES = {

    "image/jpeg",

    "image/png",

    "image/webp",

}


async def validate_upload(
    file: UploadFile,
):

    if not file:

        raise HTTPException(

            status_code=400,

            detail="File required",

        )

    content = await file.read()

    size = len(content)

    await file.seek(0)

    if size == 0:

        raise HTTPException(

            status_code=400,

            detail="Empty file",

        )

    if size > MAX_UPLOAD_MB * 1024 * 1024:

        raise HTTPException(

            status_code=413,

            detail="File too large",

        )

    if file.content_type not in ALLOWED_TYPES:

        raise HTTPException(

            status_code=415,

            detail="Unsupported file type",

        )

    return {

        "filename": file.filename,

        "size": size,

        "type": file.content_type,

    }