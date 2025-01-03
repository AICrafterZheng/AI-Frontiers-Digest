import asyncio
from pathlib import Path
from tempfile import NamedTemporaryFile
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from src.utils.twitter import TwitterClient
from prefect import task, flow, get_run_logger
from src.utils.supabase_utils import supabase
from src.config import SUPABASE_TABLE
from datetime import datetime, timedelta
from dateutil import tz

@task
async def take_screenshot(url: str):
    logger = get_run_logger()
    async with async_playwright() as p:
        try:
            # Launch browser with high DPI settings
            browser = await p.chromium.launch(headless=True)
            
            # Create context with high DPI settings
            context = await browser.new_context(
                viewport={'width': 1920, 'height': 1080},  # 4K resolution
                device_scale_factor=3  # Higher scale factor for better quality
            )
            
            # Create page and navigate
            page = await context.new_page()
            await page.goto(url, wait_until="networkidle")
            
            # Wait for the card to be visible and ensure it's rendered
            card = page.locator('.newsletter-card').first
            await card.wait_for(state='visible', timeout=5000)
            await page.wait_for_timeout(1000)  # Extra time for fonts to load
            
            # Get the bounding box of the card
            box = await card.bounding_box()
            logger.info(f"Found card with dimensions: {box}")
            # Add some padding to height and width
            padding = 40
            box['height'] = box['height'] + (padding * 2)
            box['width'] = box['width'] + (padding * 2)
            
            # Create a temporary file for the screenshot
            with NamedTemporaryFile(suffix=".jpeg", delete=False) as tmp:
                # Take high-quality screenshot of the card area
                await page.screenshot(
                path=tmp.name,
                clip={
                    'x': max(0, box['x'] - padding),
                    'y': max(0, box['y'] - padding),
                    'width': box['width'],
                    'height': box['height']
                },
                full_page=True,
                type="jpeg",
                quality=100
                )
                logger.info(f"Screenshot saved to {tmp.name}")
            return tmp.name
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            raise
        finally:
            await context.close()
            await browser.close()

@task
def post_to_twitter(text: str, image_path: str):
    """
    Post a tweet with text and image.
    
    Args:
        text: The text content of the tweet
        image_path: Path to the image file
    """
    logger = get_run_logger()
    client = TwitterClient()
    try:
        response = client.send_tweet(text=text, image_path=image_path)
        logger.info(f"Tweet posted successfully: {response}")
        return response
    except Exception as e:
        logger.error(f"Error posting tweet: {e}")
        raise
    finally:
        # Clean up the temporary screenshot file
        try:
            Path(image_path).unlink()
        except Exception as e:
            logger.error(f"Error deleting temporary file: {e}")

@task
def fetch_hackernews_records(limit: int = 10):
    """
    Fetch records from Supabase where source is 'hackernews' and created in the specified time range.
    
    Args:
        limit: Maximum number of records to fetch
        
    Returns:
        List of records from the database
    """
    logger = get_run_logger()
    try:
        # Get yesterday's date in UTC
        now = datetime.now(tz.tzutc())
        yesterday_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
        yesterday_start_str = yesterday_start.strftime('%Y-%m-%dT%H:%M:%S.000000+00:00')
        
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_start_str = today_start.strftime('%Y-%m-%dT%H:%M:%S.000000+00:00')
        
        logger.info(f"Fetching records between {yesterday_start_str} and {today_start_str}")
        
        # Now try with source filter
        data = supabase.table(SUPABASE_TABLE) \
            .select("*") \
            .eq("source", "HackerNews") \
            .gte("created_at", yesterday_start_str) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        
        logger.info(f"Fetched {len(data.data)} HackerNews records between {yesterday_start_str} and {today_start_str}")
        return data.data
    except Exception as error:
        logger.error(f"Error fetching HackerNews records: {error}")

@flow
async def run_send_twitter_flow():
    logger = get_run_logger()
    stories = fetch_hackernews_records()
    for story in stories:
        # await send_screenshot_tweet(story["url"], story["title"])
        url = f"https://aicrafter.info/news/{story['id']}"
        # url = f"http://localhost:5173/news/{story['id']}"
        logger.info(f"Taking screenshot of {url}")
        screenshot_path = await take_screenshot(url)
        text = f"{story['title']}\n Interested in listening to the podcast? Visit: {url}"
        logger.info(f"Posting tweet with text: {text}")
        post_to_twitter(text, screenshot_path)
        await asyncio.sleep(60)
