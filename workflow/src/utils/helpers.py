import re
from prefect import task, get_run_logger
from src.utils.supabase_utils import insertRow, updateRow

def extract_llm_response(text: str, tag: str):
    # Try to match <mermaid> tags first
    if text is None or text == "":
        print(f"text is None or empty")
        return ""
    match = re.search(fr'<{re.escape(tag)}>(.*?)</{re.escape(tag)}>', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # If <mermaid> tags are not found, try to match ```mermaid code blocks
    match = re.search(fr'```{re.escape(tag)}\s*(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # If no matches are found, return the original text
    return text.strip()

# filter keywords
def has_mentioned_keywords(story, keywords):
    # If any keywords are mentioned in the story title
    if story and story.url:
        title = story.title.lower()
        # Check if the title does not start with "ask hn"
        if "ask hn" not in title:
            # Use a regular expression to find whole word matches for each keyword
            for keyword in keywords:
                # Prepare the pattern to match the keyword with word boundaries
                pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
                if re.search(pattern, title):
                    # print(f"Found keyword: {keyword} in title: {title}")
                    return True
    return False

@task(log_prints=True, cache_key_fn=None)
def save_to_supabase(stories):
    logger = get_run_logger()
    for story in stories:
        try:
            print(f"Saving story: {story.title}")
            # Safely handle summary splitting
            summary = story.summary.split("\n", 1)[1] if story.summary and "\n" in story.summary else story.summary
            insertRow({
                "story_id": int(story.id), 
                "title": story.title, 
                "url": story.url, 
                "score": story.score, 
                "hn_url": story.hn_url, 
                "summary": summary, 
                "comments_summary": story.comments_summary, 
                "source": story.source,
                "speech_url": story.speech_url,
                "notebooklm_url": story.notebooklm_url
            })
        except Exception as e:
            logger.error(f"Error saving story {story.title}: {e}")

@task(log_prints=True, cache_key_fn=None)
def update_supabase_row(stories, key_column: str, columns: list[str]):
    logger = get_run_logger()
    if len(columns) == 0:
        logger.error("No columns to update")
        return
    logger.info(f"Updating {len(stories)} stories")
    for story in stories:
        try:
            # Use getattr to access object attributes
            # fields = {
            #     column: getattr(story, column) for column in columns
            # }
            fields = {}
            for column in columns:
                if column == "story_id":
                    value = story.id
                else:
                    value = getattr(story, column)
                fields[column] = value
            print(f"Updating story {story.url} with fields: {fields}")
            if key_column == "story_id":
                value = story.id
            elif key_column == "url":
                value = story.url
            updateRow(fields, key_column, value)
        except AttributeError as e:
            logger.error(f"Story missing attribute: {e}")
        except Exception as e:
            logger.error(f"Error updating story {story.url}: {e}")
