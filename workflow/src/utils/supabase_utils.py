from supabase import create_client, Client
from pathlib import Path
from src.config import SUPABASE_URL, SUPABASE_KEY, SUPABASE_BUCKET_NAME, SUPABASE_TABLE
from prefect import task, get_run_logger
# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def checkIfExists(column: str, value: any) -> bool:
    """Check if a story exists in the database."""
    result = searchRow(SUPABASE_TABLE, column, value)
    return len(result) > 0

def searchRow(tableName: str, searchColumn: str, searchValue: any, filter_column: str = None, filter_value: any = None):
    """Search for a row in the database."""
    try:
        query = supabase.table(tableName).select("*").eq(searchColumn, searchValue).order("created_at", desc=True)
        
        # If filtering for NULL values
        if filter_column and filter_value is None:
            query = query.is_(filter_column, 'null')
        # For non-NULL filter values
        elif filter_column and filter_value is not None:
            query = query.eq(filter_column, filter_value)
        data = query.execute()
        return data.data
    except Exception as error:
        print(f"Error searching for a row: {error}")
        raise error

@task(log_prints=True, cache_key_fn=None)
def insertRow(row):
    """Insert a row into the database."""
    try:
        data = supabase.table(SUPABASE_TABLE).insert(row).execute()
        print(f"insertRow result: {data.data}")
        return data.data
    except Exception as error:
        print(f"Error inserting a row: {error}")
        raise error


# update row
def updateRow(updates: dict, searchColumn: str, searchValue: int):
    """
    Update multiple columns in a row in the database.
    Args:
        updates: Dictionary of column names and their new values
        searchColumn: Column to search by
        searchValue: Value to search for
    """
    try:
        data = supabase.table(SUPABASE_TABLE).update(updates).eq(searchColumn, searchValue).execute()
        print(f"updateRow result: {data.data}")
        return data.data
    except Exception as error:
        print(f"Error updating a row: {error}")
        raise error

@task(log_prints=True, cache_key_fn=None)
def upload_audio_file(file_path: str, bucket_name: str = SUPABASE_BUCKET_NAME) -> str:
    """
    Upload an audio file to Supabase storage and return the public URL.
    """
    logger = get_run_logger()
    try:
        # Get the filename from the path
        file_name = Path(file_path).name
        print(f"upload_audio_file file_name: {file_path}")
        # Read the file
        with open(file_path, 'rb') as f:
            file_data = f.read()
        # Upload to Supabase storage
        supabase.storage.from_(bucket_name).upload(
            path=file_name,
            file=file_data,
            file_options={"content-type": "audio/mpeg"}
        )
        
        # Get the public URL
        public_url = supabase.storage.from_(bucket_name).get_public_url(file_name)
        print(f"File uploaded successfully: {public_url}")
        return public_url
        
    except Exception as error:
        logger.error(f"Error uploading audio file: {error}")
    finally:
        # delete the file from local storage
        if Path(file_path).exists():
            Path(file_path).unlink()