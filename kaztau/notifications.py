from typing import List, Dict, Any
from kaztau.telegram import bot_send_message, bot_send_file


class Notification:

    def send(self, contact: str, message: str) -> None:
        bot_send_message(contact, message)

    def send_image(self, contact: str, path_file: str) -> None:
        bot_send_file(contact, path_file)

    def send_many_image(self, contact: str, path_imgs: [str]) -> None:
        pass

    def bulk_send(self, contacts: List[Dict[str, Any]], message: str) -> None:
        pass

    def bulk_send_img(self, contacts: List[Dict[str, Any]], path_img: str, message: str) -> None:
        pass
