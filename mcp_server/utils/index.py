import requests
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path="mcp_server\.env")

def post_image_to_host_server(image_bytes):
    image_hosting_url = os.getenv("IMAGE_HOST_SERVER_URL")
    client_id = os.getenv("CLIENT_ID")

    headers = {
        "Authorization": f"Client-ID {client_id}"
    }

    files = {
        "image": image_bytes
    }

    response = requests.post(image_hosting_url, headers = headers, files = files)
    status_code = response.status_code

    if status_code != 200:
        error_message = "fail to upload image to hosting server"
        raise requests.exceptions.HTTPError(error_message)
    
    link = response.json()["data"]["link"]
    return link