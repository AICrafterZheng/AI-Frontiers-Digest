import os
from supabase import create_client, Client
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
SUPABASE_TABLE = os.getenv("SUPABASE_TABLE", "")

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

if __name__ == "__main__":
   row = searchRow(SUPABASE_TABLE, 'story_id', 1)
   print(f"searchRow result: {row}")