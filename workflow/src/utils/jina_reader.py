from prefect import task, get_run_logger
import requests

@task(log_prints=True, retries=2, retry_delay_seconds=[5, 10])
def call_jina_reader(url) -> str:
    logger = get_run_logger()
    url = f"https://r.jina.ai/{url}"
    print(f"Calling Jina reader: {url}")
    try:
        headers = {
            'X-Return-Format': 'text'
        }
        response = requests.get(url, headers=headers)
        output = response.text
    except Exception as e:
        logger.error(f"Error calling Jina reader {e}")
        return "", str(e)
    if len(output) > 1000000: # token limit
        print(f"call_jina_reader output length: {len(output)}")
        output = output[:100000]
    print(f"call_jina_reader output: {output}")
    if "Page Not Found" in output:
        return "", output
    # if not output.startswith("Title"): # trigger retries
    #     logger.error(f"Error calling Jina reader {output}")
    #     return "", output
    return output, ""

if __name__ == "__main__":
    url = "https://github.com/PrefectHQ/ControlFlow"
    output = call_jina_reader(url)
    print(f"Summary: {output}")
