import asyncio
from pathlib import Path
from tempfile import NamedTemporaryFile
from playwright.async_api import async_playwright
from src.utils.twitter import TwitterClient
from prefect import task, flow, get_run_logger

@task
async def take_screenshot(url: str) -> str:
    """
    Take a screenshot of a webpage using Playwright.
    
    Args:
        url: The URL to take a screenshot of
        
    Returns:
        Path to the screenshot file
    """
    logger = get_run_logger()
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        try:
            await page.goto(url, wait_until="networkidle")
            # Wait a bit for any lazy-loaded content
            await page.wait_for_timeout(2000)
            
            # Create a temporary file for the screenshot
            with NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                await page.screenshot(path=tmp.name, full_page=True)
                logger.info(f"Screenshot saved to {tmp.name}")
                return tmp.name
                
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            raise
        finally:
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

@flow
async def send_screenshot_tweet(url: str, text: str = None):
    """
    Take a screenshot of a URL and post it to Twitter.
    
    Args:
        url: The URL to take a screenshot of
        text: Optional text to include with the tweet. If not provided, 
              will use the URL as the tweet text.
    """
    logger = get_run_logger()
    logger.info(f"Taking screenshot of {url}")
    
    screenshot_path = await take_screenshot(url)
    tweet_text = text if text else url
    
    logger.info(f"Posting tweet with text: {tweet_text}")
    return post_to_twitter(tweet_text, screenshot_path)