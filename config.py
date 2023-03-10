import yaml

def load_config():
    print("Loading config file...")

    with open('settings/config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    url_info = [[None]*6 for _ in range(len(config['skins']))]

    # Access the products list and loop over each product
    for idx, skin in enumerate(config['skins']):
        # Access the URL and its parameters for each product
        url_info[idx][0] = skin['float']
        url_info[idx][1] = skin['pattern']
        url_info[idx][2] = skin['number_of_stickers']
        url_info[idx][3] = skin['price']
        url_info[idx][4] = skin['pages']
        url_info[idx][5] = skin['url']

        if url_info[idx][5] == None:
            print("There is skin that have URL empty in config.yaml.\nExiting...")
            return None
        
        if url_info[idx][1] is not None:
            if type(url_info[idx][1]) == str:
                url_info[idx][1] = url_info[idx][1].split(', ')

    print(f"Loaded {len(url_info)} skins!")
    return url_info
