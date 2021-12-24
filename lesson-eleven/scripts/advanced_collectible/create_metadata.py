from pathlib import Path
from brownie import AdvancedCollectible, config, network

from scripts.utils import get_account, get_breed, get_contract
from metadata.sample_metadata import metadata_template

import requests

def main():
    """
    We have both on chain and off chain components for the NFT.
    Here we upload the off chain components (metadata and image) to IPFS.
    """
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_colletibles = advanced_collectible.tokenCounter()

    print(f"Number of advanced collectibles: {number_of_advanced_colletibles}")

    for token in range(number_of_advanced_colletibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token))
        metadata_file_name = f"./metadata/{network.show_active()}/{token}-{breed}.json"
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists. Delete to override.")
        else:
            print(f"Creating metadata file {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"An adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["imageURI"] = image_uri


def upload_to_ipfs(filepath):
    """
    Uploads the metadata and image to IPFS.
    """
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
        # upload to IPFS
        ipfs_url = "http://127.0.0.1:5001"
        # call post /add
        endpoint = "/api/v0/add"
        response = requests.post(ipfs_url + endpoint, files={"file":image_binary})
        # response will be the hash of the file
        ipfs_hash = response.json()["Hash"]
        # "./img/0-PUG.png" -> "0-PUG.png" 
        filename = filepath.split("/")[-1:][0]
        # https://ipfs.io/ipfs/Qmd9MCGtdVz2miNumBHDbvj8bigSgTwnr4SbyH6DNnpWdt?filename=0-PUG.png
        image_uri = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(image_uri)
        return image_uri
