from prefect import flow, task, get_run_logger
from datetime import datetime, timedelta, timezone
from src.config import SUPABASE_TABLE, SUPABASE_BUCKET_NAME
from src.utils.supabase_utils import supabase
from urllib.parse import urlparse
import os

@task(log_prints=True)
def get_target_day_records(days: int = 10):
    """
    Retrieve records from exactly 11 days ago from the database.
    """
    logger = get_run_logger()
    try:
        # Calculate start and end of the target day
        target_date = datetime.now(timezone.utc) - timedelta(days=days)
        start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        
        # Query records from the target day where speech_url or notebooklm_url is not null
        data = supabase.table(SUPABASE_TABLE)\
            .select('id', 'speech_url', 'notebooklm_url', 'created_at')\
            .gte('created_at', start_of_day.isoformat())\
            .lt('created_at', end_of_day.isoformat())\
            .or_('speech_url.neq.null,notebooklm_url.neq.null')\
            .execute()
            
        logger.info(f"Found {len(data.data)} records from target day to process")
        return data.data
    except Exception as error:
        logger.error(f"Error retrieving target day records: {error}")
        raise error

@task(log_prints=True, cache_key_fn=None)
def extract_filename_from_url(url: str) -> str:
    """
    Extract filename from Supabase storage URL.
    """
    if not url:
        return None
    return os.path.basename(urlparse(url).path)

@task(log_prints=True, cache_key_fn=None)
def delete_storage_file(filename: str):
    """
    Delete a file from Supabase storage.
    """
    logger = get_run_logger()
    if not filename:
        return
    try:
        supabase.storage.from_(SUPABASE_BUCKET_NAME).remove([filename])
        logger.info(f"Deleted file: {filename}")
    except Exception as error:
        logger.error(f"Error deleting file {filename}: {error}")

@task(log_prints=True, cache_key_fn=None)
def update_record_urls(record_id: int):
    """
    Set speech_url and notebooklm_url to null for a record.
    """
    logger = get_run_logger()
    try:
        updates = {
            'speech_url': None,
            'notebooklm_url': None
        }
        data = supabase.table(SUPABASE_TABLE)\
            .update(updates)\
            .eq('id', record_id)\
            .execute()
        logger.info(f"Updated record {record_id}: URLs set to null")
    except Exception as error:
        logger.error(f"Error updating record {record_id}: {error}")

@task(log_prints=True)
def delete_files_from_bucket(filenames: list[str]):
    """
    Manually delete specific files from Supabase storage bucket.
    
    Args:
        filenames: List of filenames to delete
    """
    logger = get_run_logger()
    failed_deletions = []
    for filename in filenames:
        try:
            supabase.storage.from_(SUPABASE_BUCKET_NAME).remove([filename])
            logger.info(f"Successfully deleted: {filename}")
        except Exception as error:
            logger.error(f"Failed to delete {filename}: {error}")
            failed_deletions.append(filename)
    
    if failed_deletions:
        logger.warning(f"Failed to delete {len(failed_deletions)} files: {failed_deletions}")
    
    return failed_deletions

@flow(name="cleanup_audio_files", log_prints=True)
def cleanup_audio_files(days: int = 10):
    """
    Main workflow to clean up files from exactly 11 days ago and update database records.
    """
    logger = get_run_logger()
    logger.info(f"Starting cleanup of files from {days} days ago")
    
    # Get records from day 11
    records = get_target_day_records(days)
    
    for record in records:
        # Extract filenames from URLs
        speech_filename = extract_filename_from_url(record.get('speech_url'))
        notebooklm_filename = extract_filename_from_url(record.get('notebooklm_url'))
        print(f"speech_filename: {speech_filename}, notebooklm_filename: {notebooklm_filename} created_at: {record['created_at']}")
        # Delete files from storage
        if speech_filename:
            delete_storage_file(speech_filename)
        if notebooklm_filename:
            delete_storage_file(notebooklm_filename)
        # Update database record
        update_record_urls(record['id'])
    
    logger.info(f"Cleanup completed. Processed {len(records)} records")
    return len(records)

