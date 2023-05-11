import time
from typing import Dict, List, Optional, Tuple

import yaml


def load_config() -> Optional[Tuple[List[Dict], str]]:
    """
    Loads configuration file (config.yaml), extracts and validates the necessary information.

    Returns:
    tuple: A tuple containing a nested list of skin dictionaries with their details (float, pattern, price, pages, url, sort_by_float),
           and a proxy configuration dictionary. Returns None if any skin's URL is not provided.
    """

    # Inform the user that the configuration file is being loaded
    print("Loading configuration file...")
    time.sleep(1)

    # Open and load the configuration file
    with open('settings/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Extract proxy and skins configuration
    proxy_url = config.get('proxy_url')
    skins_config = config.get('skins')

    # If no proxy is provided, inform the user
    if proxy_url is None:
        print("No proxy provided. Continuing without a proxy...")

    # If no skins are provided, inform the user and return None
    if skins_config is None or len(skins_config) < 1:
        print("No skins provided. Add skins to settings/config.yaml and rerun.\nExiting...")
        return None

    time.sleep(1)

    # Initialize a list to hold the information about each skin
    skins = []

    # For each skin in the configuration file...
    for skin in skins_config:
        # Extract the URL of the skin's Steam Community Market page
        url = skin.get('url')

        # If the URL is not provided, inform the user and skip to the next skin
        if url is None:
            print("The URL for skin number {} is not provided. Skipping...".format(
                skins_config.index(skin) + 1)
            )
            continue

        # If a pattern is provided as a string, split it into a list
        pattern = skin.get('pattern')
        if pattern is not None and isinstance(pattern, str):
            pattern = pattern.split(', ')

        # Add the skin's information to the list
        skin_info = {
            # The desired float value
            'float': skin.get('float'),
            # The desired pattern (can be a list of patterns)
            'pattern': pattern,
            # The maximum price for the skin
            'price': skin.get('price'),
            # The number of pages to search for the skin
            'pages': skin.get('pages'),
            # The URL of the skin's Steam Community Market page
            'url': url,
            # Whether to sort the search results by float value
            'sort_by_float': skin.get('sort_by_float')
        }
        skins.append(skin_info)

    # Inform the user of the number of skins loaded
    print(f"Loaded {len(skins)} skins!")
    time.sleep(1)

    # Return the list of skins and the proxy URL
    return skins, proxy_url
