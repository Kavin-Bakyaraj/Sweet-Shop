import boto3
from botocore.exceptions import NoCredentialsError
from PIL import Image
import io
from fastapi import UploadFile, HTTPException
from app.core.config import settings
import uuid

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    def compress_image(self, file: UploadFile) -> io.BytesIO:
        try:
            image = Image.open(file.file)
            
            # Convert to RGB if necessary (e.g. for PNGs with transparency)
            if image.mode in ('RGBA', 'P'):
                image = image.convert('RGB')
                
            # Resize if too large (max 1920x1080)
            max_size = (1920, 1080)
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
            
            # Compress
            output = io.BytesIO()
            image.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            return output
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Image compression failed: {str(e)}")

    async def upload_file(self, file: UploadFile) -> str:
        try:
            compressed_image = self.compress_image(file)
            file_extension = ".jpg" # We convert everything to JPEG
            filename = f"{uuid.uuid4()}{file_extension}"
            
            self.s3_client.upload_fileobj(
                compressed_image,
                self.bucket_name,
                filename,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
            
            # Construct URL
            url = f"https://{self.bucket_name}.s3.{settings.AWS_REGION}.amazonaws.com/{filename}"
            return url
        except NoCredentialsError:
            raise HTTPException(status_code=500, detail="AWS credentials not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"S3 upload failed: {str(e)}")

s3_service = S3Service()
