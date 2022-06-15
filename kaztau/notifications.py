from typing import List, Dict, Any


class Notification:

    def send(self, contact: str, message: str) -> None:
        pass

    def send_image(self, contact: str, path_img: str, message: str) -> None:
        pass

    def send_many_image(self, contact: str, path_img: [str], message: str) -> None:
        pass

    def bulk_send(self, contacts: List[Dict[str, Any]], message: str) -> None:
        pass

    def bulk_send_img(self, contacts: List[Dict[str, Any]], path_img: str, message: str) -> None:
        pass
