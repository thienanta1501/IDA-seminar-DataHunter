import requests

def upload_image_to_imgur(client_id, url, image_bytes):
    headers = {
        "Authorization": f"Client-ID {client_id}"
    }
    files = {
        "image": image_bytes
    }
    response = requests.post(url, headers=headers, files=files)
    link = response.json()["data"]["link"]
    return link


def removeUnnecessaryFieldFromDict(data: dict, no_need_fields: list[str]) -> dict:
    """Remove unnecessary fields from a dictionary."""
    for field in no_need_fields:
        if field in data:
            del data[field]
    return data