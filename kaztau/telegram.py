import os
from typing import Tuple
from telethon import TelegramClient
from kaztau.exceptions import KaztauError


def get_credential() -> Tuple[int, str, str]:
    telegram_api_id = os.environ.get('KAZTAU_TELEGRAM_API_ID')
    telegram_api_hash = os.environ.get('KAZTAU_TELEGRAM_API_HASH')
    telegram_bot_token = os.environ.get('KAZTAU_TELEGRAM_BOT_TOKEN')
    if not telegram_api_id:
        raise KaztauError("Please set KAZTAU_TELEGRAM_API_ID in your environment")
    if not telegram_api_hash:
        raise KaztauError("Please set KAZTAU_TELEGRAM_API_HASH in your environment")
    if not telegram_bot_token:
        raise KaztauError("Please set KAZTAU_TELEGRAM_BOT_TOKEN in your environment")
    return telegram_api_id, telegram_api_hash, telegram_bot_token


def bot_send_message(user_entity: str, message: str = "Hi, this message from kaztau") -> None:
    api_id, api_hash, bot_token = get_credential()
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
    with bot:
        bot.loop.run_until_complete(bot.send_message(user_entity, message))


def bot_send_file(user_entity: str, path_file: str) -> None:
    api_id, api_hash, bot_token = get_credential()
    bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
    with bot:
        bot.loop.run_until_complete(bot.send_file(user_entity, path_file))


def check_valid_contact(user_entity: str):
    api_id, api_hash, bot_token = get_credential()
    bot = TelegramClient('bot', api_id,
                         api_hash).start(bot_token=bot_token)
    with bot:
        try:
            bot.get_entity(user_entity)
            return True
        except ValueError:
            return False
