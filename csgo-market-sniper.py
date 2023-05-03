from functions import *
from config import load_config

# Clear the terminal
cls()

# Load the Steam login page
driver.get("https://steamcommunity.com/login/home/?goto=market%2Flistings%2F730")

# Load the configuration settings
config = load_config()

# If the config can't be loaded, quit the driver and exit the program
if config is None:
    driver.quit()
    sys.exit()

# Initialize count variable
count = 0

# Prompt the user to start the program after they've logged in
input("Press enter to start if you are logged in and ready!")

# Clear the terminal and print some new lines
cls()
print("\n\n")

# Main loop for searching skins to buy
while True:
    # If there are no items in the config, instruct the user to populate it and then exit the program
    if len(config) < 1:
        print("Populate config.yaml file and rerun. Exiting...")
        driver.quit()
        sys.exit()

    # If the count equals the length of the config, reset the count to 0
    if count == len(config):
        count = 0

    # Load the page for the current skin in the config
    driver.get(config[count][4])

    # Check the whole page for possible purchases
    check_whole_page(count, config)

    # Increment the count
    count += 1