import sys

import urllib3
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait

from config import load_config
from driver import init_driver
from functions import cls, process_skin_marketplace
from locators import PageLocators


def main():
    """
    The main function to control the flow of the program.
    It loads the configuration settings, initializes the webdriver, and enters the main loop for searching skins to buy.
    """
    # Load the configuration settings from the config file
    skins, proxy_url = load_config()

    # Check if the configuration was loaded successfully
    if skins is None:
        print("No valid skins configuration found. Please check your settings.\nExiting...")
        return

    # Initialize the webdriver for browsing the Steam Community Market
    driver = init_driver(proxy_url)

    # Check if the driver was initialized successfully
    if driver is None:
        print("Failed to initialize the webdriver. Please check your settings and internet connection.\nExiting...")
        return

    try:
        # Load the Steam login page
        driver.get(
            "https://steamcommunity.com/login/home/?goto=market%2Flistings%2F730"
        )

        print("Steam login page loaded. Please log in to your account...")

        # Wait until the logout button appears (indicating that the user has successfully logged in)
        WebDriverWait(driver, float("inf")).until(
            ec.presence_of_element_located(PageLocators.LOGOUT_BUTTON)
        )
        print("Login successful! Starting the bot...")

        # Load the first skin's page
        driver.get(skins[0].get('url'))

        # Clear the console
        cls()

        # Main loop for searching skins to buy
        while True:
            # Initialize the current skin being searched
            skin_index = 0

            # Loop over all the skins in the configuration
            for skin in skins:
                # Process the current skin's marketplace
                process_skin_marketplace(driver, skin, skin_index)
                skin_index += 1

    # Catch exceptions to provide informative messages and clean up before exiting
    except NoSuchWindowException:
        print("The browser window was closed by the user.\nExiting...")
        sys.exit(0)
    except KeyboardInterrupt or urllib3.exceptions.ProtocolError or urllib3.exceptions.MaxRetryError or urllib3.exceptions.ProtocolError:
        print("Bot interrupted.\nExiting...")
        sys.exit(0)
    finally:
        # Close the browser window
        driver.quit()
        print("Browser closed.\nGoodbye!")


# Run the program
if __name__ == "__main__":
    main()
