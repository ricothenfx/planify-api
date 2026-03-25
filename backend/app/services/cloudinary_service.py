import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException, status
from app.core.config import settings

cloudinary.config(
    cloud_name=settings.CLOUDINARY_CLOUD_NAME,
    api_key=settings.CLOUDINARY_API_KEY,
    api_secret=settings.CLOUDINARY_API_SECRET,
)

ALLOWED_TYPES = {
    "image/jpeg", "image/png", "image/gif", "image/webp",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain",
}

# Max file size 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024


class CloudinaryService:
    async def upload(self, file: UploadFile, folder: str = "planify") -> dict:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {file.content_type} is not allowed",
            )

        contents = await file.read()

        if len(contents) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File size exceeds 10MB limit",
            )

        result = cloudinary.uploader.upload(
            contents,
            folder=folder,
            resource_type="auto",
        )

        return {
            "file_url": result["secure_url"],
            "public_id": result["public_id"],
            "file_size": len(contents),
        }

    async def delete(self, public_id: str) -> None:
        cloudinary.uploader.destroy(public_id)