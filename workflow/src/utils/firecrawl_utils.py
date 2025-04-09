
from firecrawl import FirecrawlApp
from src.config import FIRECRAWL_API_KEY
from prefect import task, get_run_logger

@task(log_prints=True, retries=2, retry_delay_seconds=[5, 10])
def firecrawl_scrape(url: str) -> str:
    logger = get_run_logger()
    print(f"Calling firecrawl_scrape: {url}")
    try:
        app = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
        response = app.scrape_url(url=url, params={
            'formats': [ 'markdown' ],
        })
        print(f"firecrawl_scrape response: {response}")
        output = response['markdown']
    except Exception as e:
        logger.error(f"Error calling firecrawl_scrape {e}")
        return "", str(e)
    if len(output) > 1000000: # token limit
        print(f"firecrawl_scrape output length: {len(output)}")
        output = output[:100000]
    print(f"firecrawl_scrape output: {output}")
    return output, ""

if __name__ == "__main__":
    url = "https://dannyzheng.me/2025/01/12/building-effective-agents/"
    firecrawl_scrape(url)