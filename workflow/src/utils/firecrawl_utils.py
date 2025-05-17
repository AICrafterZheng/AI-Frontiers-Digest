from firecrawl import FirecrawlApp
from src.config import FIRECRAWL_API_KEY, FIRECRAWL_SELF_HOSTED_URL
from prefect import task, get_run_logger
import requests

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

@task(log_prints=True, retries=2, retry_delay_seconds=[5, 10])
def firecrawl_scrape_self_hosted(url: str) -> tuple[str, str]:
    logger = get_run_logger()
    print(f"Calling firecrawl_scrape_self_hosted: {url}")
    try:
        payload = {
            "url": url,
            "formats": ["markdown"],
        }
        headers = {
            "Authorization": "Bearer <token>",
            "Content-Type": "application/json"
        }
        response = requests.request("POST", FIRECRAWL_SELF_HOSTED_URL, json=payload, headers=headers)
        response_json = response.json()
        
        # Access the nested markdown content
        if response_json.get('success') and 'data' in response_json:
            output = response_json['data']['markdown']
        else:
            raise Exception(f"Unexpected response structure: {response_json}")
        
        if len(output) > 1000000:  # token limit
            print(f"firecrawl_scrape_self_hosted output length: {len(output)}")
            output = output[:100000]
            
        print(f"firecrawl_scrape_self_hosted output: {output}")
        return output, ""
        
    except Exception as e:
        logger.error(f"Error calling firecrawl_scrape_self_hosted {e}")
        return "", str(e)
    

if __name__ == "__main__":
    url = "https://dannyzheng.me/2025/01/12/building-effective-agents/"
    firecrawl_scrape(url)
