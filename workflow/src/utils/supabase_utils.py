from supabase import create_client, Client
from pathlib import Path
from src.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET_NAME, SUPABASE_TABLE
from prefect import task, get_run_logger
# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def checkIfExists(story_id: int) -> bool:
    """Check if a story exists in the database."""
    result = searchRow(SUPABASE_TABLE, 'story_id', story_id)
    return len(result) > 0

def searchRow(tableName: str, searchColumn: str, searchValue: int):
    """Search for a row in the database."""
    try:
        data = supabase.table(tableName).select("*").eq(searchColumn, searchValue).execute()
        # print(f"searchRow result: {data.data}")
        return data.data
    except Exception as error:
        print(f"Error searching for a row: {error}")
        raise error

def insertRow(row):
    """Insert a row into the database."""
    try:
        data = supabase.table(SUPABASE_TABLE).insert(row).execute()
        print(f"insertRow result: {data.data}")
        return data.data
    except Exception as error:
        print(f"Error inserting a row: {error}")
        raise error

@task(log_prints=True)
def upload_audio_file(file_path: str, bucket_name: str = SUPABASE_BUCKET_NAME) -> str:
    """
    Upload an audio file to Supabase storage and return the public URL.
    
    Args:
        file_path: Path to the audio file
        bucket_name: Name of the storage bucket (default: SUPABASE_BUCKET_NAME)
    
    Returns:
        str: Public URL of the uploaded file
    """
    logger = get_run_logger()
    try:
        # Get the filename from the path
        file_name = Path(file_path).name
        
        # Read the file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        # Upload to Supabase storage
        response = supabase.storage.from_(bucket_name).upload(
            path=file_name,
            file=file_data,
            file_options={"content-type": "audio/mpeg"}
        )
        print(f"upload_audio_file response: {response}")
        # Get the public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        print(f"File uploaded successfully: {public_url}")
        return public_url
        
    except Exception as error:
        logger.error(f"Error uploading audio file: {error}")
    finally:
        # delete the file from local storage
        Path(file_path).unlink()