import yaml

def load_config():
    """
    Loads configuration file (config.yaml), extracts and validates the necessary information.
    
    Returns:
    list: A nested list where each sublist represents a skin and contains its details (float, pattern, price, pages, url).
          Returns None if any skin's URL is not provided.
    """

    print("Loading config file...")

    # Open and load the configuration file
    with open('settings/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Initialize a list to hold the information about each skin
    skin_info_list = [[None]*6 for _ in range(len(config['skins']))]

    # Loop over each skin in the config file
    for idx, skin in enumerate(config['skins']):
        # Extract the details for each skin
        skin_info_list[idx][0] = skin.get('float')
        skin_info_list[idx][1] = skin.get('pattern')
        skin_info_list[idx][2] = skin.get('price')
        skin_info_list[idx][3] = skin.get('pages')
        skin_info_list[idx][4] = skin.get('url')

        # Check if the URL for the skin is provided
        if skin_info_list[idx][4] is None:
            print("There is a skin without a provided URL in config.yaml.\nExiting...")
            return None
        
        # If the pattern is provided as a string, split it into a list
        if skin_info_list[idx][1] is not None and isinstance(skin_info_list[idx][1], str):
            skin_info_list[idx][1] = skin_info_list[idx][1].split(', ')

    print(f"Loaded {len(skin_info_list)} skins!")
    return skin_info_list