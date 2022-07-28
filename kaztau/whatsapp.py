import requests
import os
from kaztau.exceptions import KaztauError


def get_wa_device_id() -> str:
    device_id = os.environ.get('WA_DEVICE_ID')

    if not device_id:
        raise KaztauError("Please set WA_DEVICE_ID in your environment")
    return device_id


def wa_send_message(identifier: str, message: str = "Hi, this message from kaztau", to_group: bool = False) -> dict:
    device_id = get_wa_device_id()
    payload = {
        'device_id': device_id,
        'message': message
    }

    if to_group:
        payload['group'] = identifier
        url = "https://app.whacenter.com/api/sendGroup"
    else:
        payload['number'] = identifier
        url = "https://app.whacenter.com/api/send"

    response = requests.request("POST", url, data=payload)
    return response.json()


def upload_file_io(path_file: str) -> str:
    files = {'file': open(path_file, 'rb')}
    response = requests.request("POST", "https://file.io/", files=files)
    if not response:
        raise KaztauError("Something wrong when upload file to file.io")

    resp_json = response.json()
    if resp_json and not resp_json['success']:
        raise KaztauError("Something wrong when upload file to file.io")

    return f"https://file.io/{resp_json['key']}"


def wa_send_file(identifier: str, path_file: str, message: str = "Hi, this message from kaztau",
                 to_group: bool = False) -> dict:
    # while it only supports images
    device_id = get_wa_device_id()
    file_url = upload_file_io(path_file)
    payload = {
        'device_id': device_id,
        'message': message,
        'file': file_url
    }

    if to_group:
        payload['group'] = identifier
        url = "https://app.whacenter.com/api/sendGroup"
    else:
        payload['number'] = identifier
        url = "https://app.whacenter.com/api/send"

    response = requests.request("POST", url, data=payload)
    return response.json()
