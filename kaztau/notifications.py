from typing import List, Dict, Any
from kaztau.telegram import bot_send_message, bot_send_file


class Notification:

    def send(self, contact: str, message: str) -> None:
        bot_send_message(contact, message)

    def send_image(self, contact: str, path_image: str) -> None:
        bot_send_file(contact, path_image)

    def send_multi_image(self, contact: str, path_images: [str]) -> None:
        for path in path_images:
            self.send_image(contact, path_image=path)

    def bulk_send(self, contacts: List[Dict[str, Any]], message: str) -> None:
        pass

    def bulk_send_img(self, contacts: List[Dict[str, Any]], path_img: str, message: str) -> None:
        pass
