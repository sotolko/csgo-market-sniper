from pathlib import Path
from typing import Optional

import requests


def download_csgofloat_extension() -> Optional[str]:
    """
    Downloads the CSGOFloat Market Checker extension if it doesn't already exist in the resources directory.

    Returns:
    str: The full path of the extension if the download was successful, otherwise None.
    """

    # The URL to download the CSGOFloat Market Checker extension
    extension_url = "https://clients2.google.com/service/update2/crx?response=redirect&prodversion=49.0&acceptformat=crx3&x=id%3Djjicbefpemnphinccgikpdaagjebbnhg%26installsource%3Dondemand%26uc"
    
    # The path to save the extension locally
    extension_path = Path("resources/CSGOFloat.crx")

    # Create the resources directory if it doesn't exist
    extension_path.parent.mkdir(parents=True, exist_ok=True)

    # Check if the extension file already exists
    if not extension_path.exists():
        print("CSGOFloat Market Checker extension not found. Downloading...")

        # Download the extension
        response = requests.get(extension_url)
        
        # Check if the download was successful
        if response.status_code == 200:
            # Save the downloaded content as a .crx file
            with open(extension_path, "wb") as f:
                f.write(response.content)
            print("CSGOFloat Market Checker extension has been successfully downloaded.")
        else:
            # Print an error message and return None if the download failed
            print("Error occurred while downloading the CSGOFloat Market Checker extension.")
            return None

    # Return the full path of the extension
    return str(extension_path.resolve())