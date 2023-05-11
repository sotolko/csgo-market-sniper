import logging
import os
import sys
import time
from typing import Dict, List, Optional, Tuple, Union

from colorama import Style
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from locators import PageLocators
from logger import prepare_buy_log

# Initialize buy count variable
buy_count = 0


def cls() -> None:
    """
    Clears the terminal.

    Returns:
    None
    """
    # The os.system command allows us to execute system-level commands. 'cls' clears the terminal on Windows ('nt') systems, 'clear' does it on Unix/Linux systems.
    os.system('cls' if os.name == 'nt' else 'clear')


def click_sort_button_if_needed(driver: WebDriver, sort_by_float: Optional[str]) -> None:
    """
    If needed, find the sort button in the page's shadow DOM and click it.

    Parameters:
    driver (WebDriver): The WebDriver instance used to interact with the page.
    sort_by_float (Optional[str]): The sorting order. It could be 'asc', 'desc' or None.

    Returns:
    None
    """

    if sort_by_float is None:
        return

    time.sleep(3)  # ensure the page has loaded

    # Navigate through nested shadow DOM to reach sort button
    shadow_root = driver
    for locator in [PageLocators.CSGOFLOAT_UTILITY_BELT, PageLocators.CSGOFLOAT_SORT_FLOATS, PageLocators.CSGOFLOAT_STEAM_BUTTON]:
        element = WebDriverWait(shadow_root, 10).until(
            ec.visibility_of_element_located(locator)
        )
        shadow_root = driver.execute_script(
            "return arguments[0].shadowRoot",
            element
        )

    button = WebDriverWait(shadow_root, 10).until(
        ec.visibility_of_element_located(PageLocators.A)
    )

    # Sort by specified order
    button.click()
    if sort_by_float == 'desc':
        button.click()


def get_min_of_two(num1: Union[int, None, str], num2: Union[int, None, str]) -> Union[int, None, str]:
    """
    Get the minimum of two numbers or return the other number if one is None, '', or 0.

    Parameters:
    num1, num2 (Union[int, None, str]): The numbers to compare.

    Returns:
    Union[int, None, str]: The minimum of the two numbers or the other number if one is None, '', or 0.
    """

    if num1 in {None, '', 0}:
        return num2
    if num2 in {None, '', 0}:
        return num1

    return min(num1, num2)


def get_page_count(driver: WebDriver, max_page_count: int) -> int:
    """
    Get the minimum of the last page number and the maximum page count.

    Parameters:
    driver (WebDriver): The WebDriver instance used to interact with the page.
    max_page_count (int): The maximum number of pages to process.

    Returns:
    int: The page count to process, which is the minimum of the last page number and the maximum page count.
    """

    try:
        WebDriverWait(driver, 10).until(
            ec.presence_of_all_elements_located(PageLocators.PAGE)
        )
        last_page_number = int(
            driver.find_elements(*PageLocators.PAGE)[-1].text)
        return get_min_of_two(last_page_number, max_page_count)
    except TimeoutException:
        return 1


def get_listings_per_page_count(driver: WebDriver) -> int:
    """
    Get the total number of items on the page.

    Parameters:
    driver (WebDriver): The WebDriver instance used to interact with the page.

    Returns:
    int: The total number of items on the page.
    """

    return int(WebDriverWait(driver, 10).until(ec.presence_of_element_located(PageLocators.SEARCH_RESULTS)).text)


def get_market_listings(driver: WebDriver) -> List[WebElement]:
    """
    Get the market listings from the page.

    Parameters:
    driver (WebDriver): The WebDriver instance.

    Returns:
    List[WebElement]: A list of market listings.
    """

    return driver.find_elements(*PageLocators.MARKET_LISTING_ROW)


def get_market_listing_details(driver: WebDriver, market_listing: WebElement) -> Tuple[WebElement, WebElement, WebElement, WebElement, WebElement]:
    """
    Load purchase buttons and associated information from the page.

    This function retrieves the purchase buttons, prices, item names, float values, and pattern values from the current page.
    The float and pattern values are extracted from the shadow DOM of each item row wrapper.
    The function waits until the necessary elements are visible or present before attempting to extract information.

    Returns:
    Tuple: A tuple containing lists of the buy buttons, prices, item names, float values, and pattern values.
    """

    # Find buy button, price, and name
    buy_button = market_listing.find_element(*PageLocators.BUY_BUTTON_END)
    price = get_price_number(
        market_listing.find_element(*PageLocators.LISTING_PRICE)
    )
    name = market_listing.find_element(*PageLocators.LISTING_NAME).text

    # Wait for the presence of item row wrapper
    csgofloat_item_row_wrapper = WebDriverWait(market_listing, 10).until(
        ec.presence_of_element_located(PageLocators.CSGOFLOAT_ITEM_ROW_WRAPPER)
    )

    # Access the shadow root of the item row wrapper
    csgofloat_item_row_wrapper_shadow_root = driver.execute_script(
        "return arguments[0].shadowRoot",
        csgofloat_item_row_wrapper
    )

    # Wait for the presence of the item row content and extract the text
    csgofloat_item_row_content = WebDriverWait(csgofloat_item_row_wrapper_shadow_root, 10).until(
        ec.presence_of_element_located(PageLocators.DIV)
    ).text

    # Extract the float and pattern values from the item row content
    float_value = float(
        csgofloat_item_row_content.split("\n")[0].split(":")[1].strip()
    )
    pattern = int(
        csgofloat_item_row_content.split("\n")[1].split(":")[1].strip()
    )

    # Return listing buy button, price, name, float value, and pattern
    return buy_button, price, name, float_value, pattern


def get_price_number(price_element: WebElement) -> float:
    """
    This function takes a list of price elements and extracts the numerical value of each price.
    It processes the text of each price element to remove non-numeric characters and converts the resulting string to a float.
    If there is any exception during the process, the function breaks out of the loop and returns the list of extracted prices so far.

    Parameters:
    prices (list): A list of price elements, where each element contains the price text.

    Returns:
    list: A list of float values representing the extracted prices.
    """

    return int(''.join(c for c in price_element.text if c.isdigit())) / 100


def get_user_balance(driver: WebDriver) -> float:
    """
    Retrieve the user's balance from the page.

    Parameters:
    driver (WebDriver): The WebDriver instance used to interact with the page.

    Returns:
    float: The user's balance.
    """

    # Wait for user balance element to appear and fetch its text
    balance_text = WebDriverWait(driver, 60).until(
        ec.presence_of_element_located(PageLocators.USER_BALANCE)
    ).text

    # Extract digits from balance text, convert to float and divide by 100 to get actual value
    return float(''.join(filter(str.isdigit, balance_text))) / 100


def display_progress_bar(
    current_skin: int,
    current_page: int,
    current_listing: int,
    total_listings_count: int,
    buy_count: int,
    user_balance: float
) -> None:
    """
    Displays a progress bar on the console with relevant information.

    Parameters:
    current_skin (int): The current skin index.
    current_page (int): The current page number.
    current_listing (int): The current listing index.
    total_listings_count (int): The total number of listings to process.
    buy_count (int): The number of skins bought.
    user_balance (float): The user's current balance.
    """

    # Calculate the percentage of listings processed
    percent = (current_listing / total_listings_count) * 100

    # Create the filled part of the progress bar
    filled_bar = chr(9608) * int(percent)

    # Create the unfilled part of the progress bar
    empty_bar = chr(9617) * (100 - int(percent))

    # ANSI escape sequences for moving the cursor up and clearing the line
    cursor_up = "\x1B[3A"
    clear_line = "\x1B[0K"

    # Create the information string, including the current skin, page, listing, number of skins bought, and the user balance
    info_str = (
        f"{Style.NORMAL}Skin:{Style.BRIGHT} {current_skin} {Style.DIM}| "
        f"{Style.NORMAL}Page:{Style.BRIGHT} {current_page} {Style.DIM}| "
        f"{Style.NORMAL}Listing:{Style.BRIGHT} {current_listing} {Style.DIM}| "
        f"{Style.NORMAL}Skins bought:{Style.BRIGHT} {buy_count} {Style.DIM}| "
        f"{Style.NORMAL}Balance:{Style.BRIGHT} {user_balance}{Style.RESET_ALL}"
    )

    # Create a version of the information string that will be used for calculating padding
    visible_info_str = (
        f"Skin: {current_skin} | Page: {current_page} | "
        f"Listing: {current_listing} | Skins bought: {buy_count} | Balance: {user_balance}"
    )

    # Calculate the padding needed to center the information string
    padding_left = (100 - len(visible_info_str)) // 2
    padding_right = padding_left if len(
        visible_info_str
    ) % 2 == 0 else padding_left + 1

    # Print the progress bar, along with the other information
    print(
        f"{cursor_up}{Style.NORMAL}|{Style.RESET_ALL}{' ' * padding_left}{info_str}{' ' * padding_right}"
        f"{Style.NORMAL}|{Style.RESET_ALL}{clear_line}\n"
        f"{Style.NORMAL}|{Style.RESET_ALL}{filled_bar}{empty_bar}{Style.NORMAL}|"
        f"{Style.RESET_ALL} {Style.BRIGHT}{percent:.2f}%{Style.RESET_ALL}{clear_line}\n"
    )


def is_listing_matching_purchase_criteria(
    user_balance: float,
    listing_price: float,
    listing_float: Optional[float],
    listing_pattern: Optional[int],
    config_price: Optional[float] = None,
    config_float: Optional[float] = None,
    config_pattern: Optional[List[int]] = None
) -> bool:
    """
    This function checks all the criteria for purchasing a listing including:
    - User has enough balance for the listing
    - Listing price is within the user's specified maximum price (if specified)
    - Listing's float is less than or equal to the maximum float (if specified)
    - Listing's pattern is in the list of acceptable patterns (if specified)

    Parameters:
    user_balance (float): The user's balance.
    listing_price (float): The price of the current listing.
    listing_float (float): The float value of the listing.
    listing_pattern (int): The pattern ID of the listing.
    config_price (float): The maximum price specified by the user.
    config_float (float): The maximum acceptable float value from the configuration.
    config_pattern (list): The list of acceptable pattern IDs from the configuration.

    Returns:
    bool: True if the listing meets all the purchase conditions, False otherwise.
    """

    # Check if the user has enough balance for the listing
    if user_balance < listing_price:
        return False    

    # Check if the maximum price is specified and if the listing price is greater than the maximum price
    if config_price is not None and listing_price > config_price:
        return False

    # Check if the listing's float is less than or equal to the maximum float, if specified in the configuration
    if config_float is not None and listing_float > config_float:
        return False

    # Check if the listing's pattern is in the list of acceptable patterns, if specified in the configuration
    if config_pattern is not None and listing_pattern not in config_pattern:
        return False

    return True


def attempt_skin_purchase(driver: WebDriver, buy_button: WebElement) -> bool:
    """
    Attempts to purchase a skin.

    Parameters:
    driver (webdriver): The Selenium webdriver instance.
    buy_button (WebElement): The "Buy now" button element.

    Returns:
    bool: True if the purchase was successful, False otherwise.
    """

    # Attempt to purchase the skin
    driver.execute_script("arguments[0].click();", buy_button)
    try:
        # Accept the terms and conditions
        check_box = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located(PageLocators.CHECK_BOX)
        )
        driver.execute_script("arguments[0].click();", check_box)

        # Confirm the purchase
        confirm_button = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located(PageLocators.BUY_BUTTON)
        )
        driver.execute_script("arguments[0].click();", confirm_button)

        # Close the confirmation dialog
        close_button = WebDriverWait(driver, 5).until(
            ec.presence_of_element_located(PageLocators.CLOSE_BUTTON)
        )
        driver.execute_script("arguments[0].click();", close_button)

        # The purchase was successful
        return True
    except:
        # An error occurred during the purchase attempt
        return False


def record_purchase(logger: logging.Logger, listing_name: str, listing_float: float, listing_price: float) -> None:
    """
    Records information about a purchase using a provided logger.

    Parameters:
    logger (logging.Logger): The logger to use for recording the purchase.
    listing_name (str): The name of the purchased listing.
    listing_float (float): The float value of the purchased listing.
    listing_price (float): The price of the purchased listing.

    Returns:
    None
    """

    # Log the purchase details
    logger.info(
        f"Listing: {listing_name}, Float: {listing_float}, Price: {listing_price}"
    )

    # Increment the global buy_count variable
    global buy_count
    buy_count += 1


def navigate_to_next_page(driver: WebDriver) -> bool:
    """
    Navigates to the next page of the skin marketplace if it exists.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.

    Returns:
    bool: True if the next page is found and navigated to, False otherwise.
    """

    try:
        # Navigate to the next page
        driver.find_element(*PageLocators.NEXT_PAGE).click()

        # Allow the page to load
        time.sleep(3)

        return True
    except:
        # The next page is not available or an error occurred
        return False


def process_skin_marketplace(driver: WebDriver, skin: Dict, current_skin: int) -> None:
    """
    Navigates the marketplace of a specific skin, checks each listing against user-defined criteria,
    and attempts to purchase listings that meet these criteria. Details of each successful purchase are logged.

    Parameters:
    driver (WebDriver): The Selenium WebDriver instance.
    skin (Dict): A dictionary containing user-defined criteria for potential purchases.
    current_skin (int): The index of the current skin in the list of skins to process.

    Returns:
    None
    """

    # Navigate to the skin's marketplace page if not already there
    if skin.get('url') != driver.current_url:
        driver.get(skin.get('url'))

    # If the user wants to sort listings by their float values, attempt to do so
    try:
        click_sort_button_if_needed(driver, skin.get('sort_by_float'))
    except:
        pass

    # Determine the total number of listings to process
    maximum_pages = skin.get('pages')
    page_count = get_page_count(driver, maximum_pages)
    listings_per_page_count = get_listings_per_page_count(driver)
    total_listings_count = listings_per_page_count * page_count

    # For each page in the range to process...
    for current_page in range(1, page_count + 1):
        # Fetch the listings on the current page
        market_listings = get_market_listings(driver)

        # For each listing on the current page...
        for index, market_listing in enumerate(market_listings, start=1):
            # Attempt to get the user's current balance
            try:
                user_balance = get_user_balance(driver)
            except Exception:
                sys.stderr.write(
                    "Can't get user balance. Make sure that you're logged in.\nExiting..."
                )
                driver.quit()
                sys.exit(0)

            # Update the progress bar
            current_listing = (current_page - 1) * \
                listings_per_page_count + index
            display_progress_bar(
                current_skin,
                current_page,
                current_listing,
                total_listings_count,
                buy_count,
                user_balance
            )

            # Attempt to get the details of the current listing
            try:
                buy_button, price, name, float_value, pattern = get_market_listing_details(
                    driver,
                    market_listing
                )
            except Exception:
                # If an error occurs, skip to the next listing
                continue

            # Get the user-defined criteria for potential purchases
            config_price = skin.get('price')
            config_float = skin.get('float')
            config_pattern = skin.get('pattern')

            # Check if the user has enough balance and the listing meets the purchase criteria
            if not is_listing_matching_purchase_criteria(user_balance, price, float_value, pattern, config_price, config_float, config_pattern):
                continue

            # If the listing meets the criteria, attempt to purchase it
            if not attempt_skin_purchase(driver, buy_button):
                continue

            # If the purchase is successful, log the details of the purchase
            logger = prepare_buy_log()
            record_purchase(logger, name, float_value, price)

        # If there are more pages to process, navigate to the next page
        if not navigate_to_next_page(driver):
            continue
