from typing import Dict, Optional

import chromedriver_autoinstaller
from seleniumwire import webdriver

from extension import download_csgofloat_extension


def get_seleniumwire_options(proxy_url: Optional[str]) -> Dict[str, Dict[str, str]]:
    """
    Sets up the proxy server based on the provided configuration.

    Parameters:
    proxy_url (str): The proxy URL from the config.yaml file.

    Returns:
    dict: The proxy server configuration dictionary to be used when launching the browser, or None if no proxy is configured.
    """
    # Check if the proxy URL is not None
    if proxy_url is not None:
        # Return the proxy server configuration dictionary
        return {
            'proxy': {
                'http': f"http://{proxy_url}",
                'https': f"http://{proxy_url}",
                'no_proxy': 'localhost,127.0.0.1'
            }
        }
    else:
        # Return None if no proxy URL is provided
        return None


def init_driver(proxy_url: Optional[str]) -> Optional[webdriver.Chrome]:
    """
    Initializes a Chrome webdriver with the CSGOFloat Market Checker extension loaded, and with
    proxy capabilities if a proxy configuration is provided.
    """
    # This function checks the installed version of Google Chrome, automatically downloads the
    # corresponding version of ChromeDriver (if not already installed), and installs it in the
    # appropriate location. It simplifies the setup for Selenium WebDriver, which requires the
    # ChromeDriver executable to automate the Google Chrome browser.
    chromedriver_autoinstaller.install()

    # Initialize the Chrome options object
    chrome_options = webdriver.ChromeOptions()

    # Define Chrome's preferences to manage notifications and avoid automation detection
    chrome_options.add_experimental_option(
        'prefs', {'profile.default_content_setting_values.notifications': 1}
    )
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-automation', 'enable-logging']
    )
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument(
        '--disable-blink-features=AutomationControlled'
    )

    # Download the CSGOFloat Market Checker extension
    extension_path = download_csgofloat_extension()

    # Check if the extension was downloaded successfully
    if extension_path is None:
        print("Failed to download the CSGOFloat Market Checker extension.")
        return None

    # Add the extension to the Chrome options
    chrome_options.add_extension(extension_path)

    # Set up the proxy server if a proxy URL is provided
    seleniumwire_options = get_seleniumwire_options(proxy_url)

    # Initialize the Chrome driver with the defined options and return it
    driver = webdriver.Chrome(
        options=chrome_options,
        seleniumwire_options=seleniumwire_options
    )

    return driver
