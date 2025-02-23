from prefect import task, get_run_logger
import requests

# Different divider options:
divider_options = {
    "none": "",
    "simple": "─" * 30,
    "double": "═" * 30,
    "bold": "━" * 30,
    "dotted": "┄" * 30,
    "dashed": "┅" * 30,
    "fancy": "✧･ﾟ: *✧･ﾟ:* *:･ﾟ✧*:･ﾟ✧",
    "stars": "★━━━━━━━━━━━━━━━━━━━★",
    "clean": "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬",
}
discord_limit = 1800
# Discord has 2000 character limit, so split the message
# needs to have async to be able to send in parallel
@task(log_prints=True, cache_policy=None)
def split_messages_to_send_discord(discord_webhook, message, divider_style: str = "none"):
    while len(message) > 0 or message != "":
        print(f"split_messages_to_send message length: {len(message)}")
        if len(message) < discord_limit:
            send_discord(discord_webhook, message, divider_style)
            message = ''
        else:
            split_index = message[:discord_limit].rfind("\n")
            print(f"split_messages_to_send split_index: {split_index}")
            if split_index == -1 or split_index == 0:
                split_index = discord_limit
            send_discord(discord_webhook, message[:split_index], divider_style)
            message = message[split_index:]

@task(log_prints=True, cache_policy=None)
def send_discord(discord_webhook, message, divider_style: str = "simple"):
    logger = get_run_logger()
    divider = divider_options.get(divider_style, divider_options["simple"])

    if discord_webhook == "" or message == "":
        logger.error(f"send_discord discord webhook or message is empty: discord_webhook: {discord_webhook},\n message: {message}")
        return

    if len(message) > discord_limit:
        logger.error(f"send_discord message is too long: {len(message)}, sending first {discord_limit} characters")
        message = message[:discord_limit]
    message = f"{message}\n{divider}"
    logger.info(f"send_discord message: \n {message}")
    try:
        data = {
            'content': message
        }
        response = requests.post(discord_webhook, json=data)
        # Check for success
        if response.status_code == 204:
            print(f"send_discord message sent successfully. \n {response}")
        else:
            logger.error(f"send_discord failed to send message, status code: {response.status_code} \n message: {response}")
    except Exception as error:
        logger.error(f"send_discord error sending discord message: {error}")
