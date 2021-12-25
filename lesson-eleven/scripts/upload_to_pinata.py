import os
import requests
from pathlib import Path


def main():

    PINATA_BASE_URL = "https://api.pinata.cloud/"
    END_POINT = "pinning/pinFileToIPFS"
    filepath = "./img/pug.png"
    filename = filepath.split("/")[-1:][0]

    headers = {
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_API_SECRET"),
    }

    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload to IPFS
        response = requests.post(
            PINATA_BASE_URL + END_POINT,
            files={"file": (filename, image_binary)},
            headers=headers,
        )
        print(response.json())
