import boto3
from botocore.config import Config
from typing import Optional, BinaryIO
from pathlib import Path
from src.config import CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_ACCESS_KEY_ID, CLOUDFLARE_ACCESS_KEY_SECRET, CLOUDFLARE_BUCKET_NAME, CLOUDFLARE_AUDIO_URL
from prefect import task, get_run_logger

class R2Client:
    def __init__(
        self,
        account_id: Optional[str] = None,
        access_key_id: Optional[str] = None,
        access_key_secret: Optional[str] = None,
        bucket_name: Optional[str] = None
    ):
        """Initialize R2 client with credentials.
        
        Args:
            account_id: Cloudflare account ID
            access_key_id: R2 access key ID
            access_key_secret: R2 access key secret
            bucket_name: R2 bucket name
        """
        self.account_id = account_id or CLOUDFLARE_ACCOUNT_ID
        self.access_key_id = access_key_id or CLOUDFLARE_ACCESS_KEY_ID
        self.access_key_secret = access_key_secret or CLOUDFLARE_ACCESS_KEY_SECRET
        self.bucket_name = bucket_name or CLOUDFLARE_BUCKET_NAME

        if not all([self.account_id, self.access_key_id, self.access_key_secret, self.bucket_name]):
            raise ValueError("Missing required R2 credentials. Please provide them or set environment variables.")

        self.endpoint_url = f"https://{self.account_id}.r2.cloudflarestorage.com"
        
        self.s3_client = boto3.client(
            service_name='s3',
            endpoint_url=self.endpoint_url,
            aws_access_key_id=self.access_key_id,
            aws_secret_access_key=self.access_key_secret,
            config=Config(
                signature_version='s3v4',
                retries={'max_attempts': 3}
            )
        )

    def upload_file(
        self,
        file_path: str | Path,
        key: Optional[str] = None,
        content_type: Optional[str] = None
    ) -> str:
        """Upload a file to R2 bucket.
        
        Args:
            file_path: Path to the file to upload
            key: Optional key (path) in the bucket. If not provided, uses filename
            content_type: Optional content type. If not provided, tries to guess
            
        Returns:
            str: The key (path) of the uploaded file in the bucket
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Use filename as key if not provided
        if not key:
            key = file_path.name

        # Try to guess content type if not provided
        if not content_type:
            import mimetypes
            content_type, _ = mimetypes.guess_type(str(file_path))

        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type

        self.s3_client.upload_file(
            str(file_path),
            self.bucket_name,
            key,
            ExtraArgs=extra_args
        )

        return key

    @task(log_prints=True, cache_policy=None)
    def upload_file_to_r2(self, file: str) -> str:
        logger = get_run_logger()
        try:
            # Upload file
            logger.info(f"Uploading {file}")
            file_path = Path(file)
            key = file_path.name
            uploaded_key = self.upload_file(file_path, key=key)
            logger.info(f"File uploaded successfully: {uploaded_key}")
            public_url = f"{CLOUDFLARE_AUDIO_URL}/{uploaded_key}"
            logger.info(f"Public URL: {public_url}")
            return public_url
        except Exception as e:
            logger.error(f"Error uploading {file}: {e}")
            return ""

    def upload_fileobj(
        self,
        fileobj: BinaryIO,
        key: str,
        content_type: Optional[str] = None
    ) -> str:
        """Upload a file-like object to R2 bucket.
        
        Args:
            fileobj: File-like object to upload
            key: Key (path) in the bucket
            content_type: Optional content type
            
        Returns:
            str: The key (path) of the uploaded file in the bucket
        """
        extra_args = {}
        if content_type:
            extra_args['ContentType'] = content_type

        self.s3_client.upload_fileobj(
            fileobj,
            self.bucket_name,
            key,
            ExtraArgs=extra_args
        )

        return key

    def list_files(self, prefix: Optional[str] = None) -> list[dict]:
        """List files in the bucket.
        
        Args:
            prefix: Optional prefix to filter files
            
        Returns:
            list: List of file information dictionaries
        """
        params = {'Bucket': self.bucket_name}
        if prefix:
            params['Prefix'] = prefix

        response = self.s3_client.list_objects_v2(**params)
        
        files = []
        if 'Contents' in response:
            for obj in response['Contents']:
                files.append({
                    'key': obj['Key'],
                    'size': obj['Size'],
                    'last_modified': obj['LastModified']
                })
        
        return files

    def get_download_url(self, key: str, expires_in: int = 3600) -> str:
        """Generate a presigned download URL for a file.
        
        Args:
            key: Key (path) of the file in the bucket
            expires_in: URL expiration time in seconds (default: 1 hour)
            
        Returns:
            str: Presigned download URL
        """
        return self.s3_client.generate_presigned_url(
            'get_object',
            Params={
                'Bucket': self.bucket_name,
                'Key': key
            },
            ExpiresIn=expires_in
        )

    def delete_file(self, key: str) -> None:
        """Delete a file from the bucket.
        
        Args:
            key: Key (path) of the file to delete
        """
        self.s3_client.delete_object(
            Bucket=self.bucket_name,
            Key=key
        )
