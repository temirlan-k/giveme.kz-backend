from fastapi import HTTPException, status
import filetype


async def validate_file_size_type(file):
    FILE_SIZE = 2 * 1024 * 1024  # 2MB

    accepted_file_types = [
        "image/png",
        "image/jpeg",
        "image/jpg",
        "image/heic",
        "image/heif",
        "image/heics",
        "png",
        "jpeg",
        "jpg",
        "heic",
        "heif",
        "heics",
    ]
    file_info = filetype.guess(file.file)
    if file_info is None:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unable to determine file type. File must be an image",
        )

    detected_content_type = file_info.extension.lower()

    if (
        file.content_type not in accepted_file_types
        or detected_content_type not in accepted_file_types
    ):
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail="Unsupported file type",
        )

    real_file_size = 0
    for chunk in file.file:
        real_file_size += len(chunk)
        if real_file_size > FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="Too large, max size - 2mb",
            )
