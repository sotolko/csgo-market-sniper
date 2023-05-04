import os
import logging
import sys
import time
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from locators import PageLocators

# This function checks the installed version of Google Chrome, automatically downloads the 
# corresponding version of ChromeDriver (if not already installed), and installs it in the 
# appropriate location. It simplifies the setup for Selenium WebDriver, which requires the 
# ChromeDriver executable to automate the Google Chrome browser. If a matching version of 
# ChromeDriver is already installed, it simply returns the path to the installed driver.
chromedriver_autoinstaller.install()

# Initialize the webdriver
chrome_options = Options()
chrome_options.add_extension('path_to_your_crx_file.crx') # Change this to the path of the CSGOFloat extension
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)

# Initialize buy count variable
buy_count = 0

def cls():
    """
    Clears the terminal.

    Returns:
    None
    """
    # The os.system command allows us to execute system-level commands. 'cls' clears the terminal on Windows ('nt') systems, 'clear' does it on Unix/Linux systems.
    os.system('cls' if os.name == 'nt' else 'clear')

def check_whole_page(count, config):
    """
    This function processes each page of the skin marketplace for potential purchases based on the user's specified criteria.
    It verifies if the items meet the necessary conditions and makes a purchase if they do.
    Information about each purchase is saved to a log file.

    Parameters:
    count (int): The current count of skins processed.
    config (list): A list containing configuration details about the skin URLs to process.

    Returns:
    None
    """

    skin_count = 0
    items = items_on_page(config[count][3])
    pages = int(page_count(config[count][3]))

    # Sort items by float
    try:
        find_and_click_sort_button()
    except:
        pass

    # Iterate through pages
    for page in range(1, pages + 1):
        # Load purchase buttons and item details
        try:
            buy_buttons, prices, names, floats, patterns = load_purchase_buttons()
            prices = extract_prices(prices)
        except Exception:
            break

        # Iterate through items on the current page
        for idx, _ in enumerate(prices):
            skin_count += 1
            progress_bar(skin_count, items, count + 1, buy_count, page)

            # Get user balance
            try:
                user_balance = check_user_balance()
            except Exception:
                sys.stderr.write("Can't get user balance. Are you logged in?")
                driver.quit()
                sys.exit()

            item_price = prices[idx]
            config_price = config[count][2]
            item_float = floats[idx]
            config_float = config[count][0]
            item_pattern = patterns[idx]
            config_pattern = config[count][1]

            # Check item conditions and user balance
            if not (check_item_price(item_price, config_price) and 
                    has_enough_balance(user_balance, item_price) and 
                    check_item_parameters(item_float, item_pattern, config_float, config_pattern)):
                continue

            # Attempt to buy the skin
            if not buy_skin(buy_buttons[idx]):
                continue

            # Log purchase details
            buy_log(names[idx].text, floats[idx], prices[idx])
        
        # Move to the next page if available
        if not find_next_page():
            continue

def page_count(max_page_count):
    """
    Get the minimum of the last page number and the maximum page count.
    
    Parameters:
    max_page_count (int): The maximum number of pages to process.
    
    Returns:
    int: The minimum of the last page number and the maximum page count, or 1 if the last page element cannot be located.
    """

    try:
        WebDriverWait(driver, 2).until(ec.presence_of_element_located(PageLocators.LAST_PAGE))
        last_page = driver.find_elements(*PageLocators.LAST_PAGE)
        return get_min(int(last_page[-1].text), int(max_page_count))
    except TimeoutException:
        return 1

def actual_page_number():
    """
    Get the current page number.
    
    Returns:
    int: The current page number, or 1 if the page number element cannot be located.
    """

    try:
        actual_page_num = WebDriverWait(driver, 2).until(ec.presence_of_element_located(PageLocators.PAGE_NUMBER)).text
        return int(actual_page_num)
    except TimeoutException:
        return 1

def items_on_page(max_page_count):
    """
    Get the total number of items on the page.
    
    Parameters:
    max_page_count (int): The maximum number of pages to process.
    
    Returns:
    int: The total number of items on the page.
    """
    
    return page_count(max_page_count) * 10

def find_and_click_sort_button():
    """
    Find the sort button in the shadow DOM of the page and click it.

    This function navigates through the nested shadow DOM to reach the sort button, 
    waiting for the visibility of each necessary element before proceeding.
    After the sort button is found, the function pauses for 2 seconds to ensure the page has loaded, 
    then clicks the sort button.

    Returns:
    None
    """

    # Pause for 2 seconds to ensure the page has loaded
    time.sleep(2)

    # Navigate through the nested shadow DOM to reach the sort button
    csgofloat_utility_belt = WebDriverWait(driver, 10).until(ec.visibility_of_element_located(PageLocators.CSGOFLOAT_UTILITY_BELT))
    csgofloat_utility_belt_shadow_root = driver.execute_script("return arguments[0].shadowRoot", csgofloat_utility_belt)

    csgofloat_sort_floats = WebDriverWait(csgofloat_utility_belt_shadow_root, 10).until(ec.visibility_of_element_located(PageLocators.CSGOFLOAT_SORT_FLOATS))
    csgofloat_sort_floats_shadow_root = driver.execute_script("return arguments[0].shadowRoot", csgofloat_sort_floats)

    csgofloat_steam_button = WebDriverWait(csgofloat_sort_floats_shadow_root, 10).until(ec.visibility_of_element_located(PageLocators.CSGOFLOAT_STEAM_BUTTON))
    csgofloat_steam_button_shadow_root = driver.execute_script("return arguments[0].shadowRoot", csgofloat_steam_button)

    csgofloat_steam_button_a = WebDriverWait(csgofloat_steam_button_shadow_root, 10).until(ec.visibility_of_element_located(PageLocators.A))

    # Pause for 2 seconds to ensure the page has loaded, then click the sort button
    time.sleep(2)
    csgofloat_steam_button_a.click()

def load_purchase_buttons():
    """
    Load purchase buttons and associated information from the page.
    
    This function retrieves the purchase buttons, prices, item names, float values, and pattern values from the current page.
    The float and pattern values are extracted from the shadow DOM of each item row wrapper.
    The function waits until the necessary elements are visible or present before attempting to extract information.
    
    Returns:
    Tuple: A tuple containing lists of the buy buttons, prices, item names, float values, and pattern values.
    """

    try:
        # Wait for the visibility of purchase buttons
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located(PageLocators.BUY_BUTTON_END))

        # Find all purchase buttons, prices, and item names
        buy_buttons = driver.find_elements(*PageLocators.BUY_BUTTON_END)
        prices = driver.find_elements(*PageLocators.PRICES_BOX)
        names = driver.find_elements(*PageLocators.ITEM_NAME)

        # Initialize lists for float and pattern values
        floats = []
        patterns = []

        # Wait for the presence of all item row wrappers
        csgofloat_item_row_wrappers = WebDriverWait(driver, 10).until(ec.presence_of_all_elements_located(PageLocators.CSGOFLOAT_ITEM_ROW_WRAPPER))

        # Loop through each item row wrapper
        for csgofloat_item_row_wrapper in csgofloat_item_row_wrappers:
            # Access the shadow root of the item row wrapper
            csgofloat_item_row_wrapper_shadow_root = driver.execute_script("return arguments[0].shadowRoot", csgofloat_item_row_wrapper)
            
            # Wait for the presence of the item row content and extract the text
            csgofloat_item_row_content = WebDriverWait(csgofloat_item_row_wrapper_shadow_root, 10).until(ec.presence_of_element_located(PageLocators.DIV)).text
            
            # Extract the float and pattern values from the item row content and append them to the corresponding lists
            float_value = float(csgofloat_item_row_content.split("\n")[0].split(":")[1].strip())
            floats.append(float_value)

            pattern_value = int(csgofloat_item_row_content.split("\n")[1].split(":")[1].strip())
            patterns.append(pattern_value)

        # Return all lists
        return buy_buttons, prices, names, floats, patterns

    except TimeoutException:
        sys.stderr.write("Cant find buy buttons\n")
        return

def extract_prices(prices):
    """
    This function takes a list of price elements and extracts the numerical value of each price.
    It processes the text of each price element to remove non-numeric characters and converts the resulting string to a float.
    If there is any exception during the process, the function breaks out of the loop and returns the list of extracted prices so far.

    Parameters:
    prices (list): A list of price elements, where each element contains the price text.

    Returns:
    list: A list of float values representing the extracted prices.
    """

    price_text_num = []

    for price in prices:
        # Remove non-numeric characters from the price text, convert the result to an integer, and divide by 100 to get the actual price as a float
        price_value = int(''.join(c for c in price.text if c.isdigit())) / 100
        price_text_num.append(price_value)

    return price_text_num

def progress_bar(progress, total, urlcount, buycount, page):
    """
    Prints a progress bar to the console.

    Parameters:
    progress (int): The current progress.
    total (int): The total amount to complete.
    urlcount (int): The current count of URLs processed.
    buycount (int): The current count of items bought.
    page (int): The current page number.

    Returns:
    None
    """
    # Calculate the percentage of completion
    percent = 100 * (progress / float(total))
    # Create a progress bar using unicode characters
    bar = chr(9608) * int(percent) + chr(9617) * (100 - int(percent))
    # These two are ANSI escape sequences for moving the cursor up and clearing the line
    up = "\x1B[3A"
    clr = "\x1B[0K"

    # Generate the string of information
    info_str = f"Skin: {urlcount} | Page: {page} | Item: {progress} | Total items: {total} | Items bought: {buycount} | Balance: {str(check_user_balance())}"

    # Calculate the required padding to center the information string
    padding_left = (len(bar) - len(info_str)) // 2
    # Adjust the right padding if the length of the information string is an odd number
    padding_right = padding_left if len(info_str) % 2 == 0 else padding_left + 1

    # Print the progress bar, along with other information
    print(f"{up}|{' ' * padding_left}{info_str}{' ' * padding_right}|{clr}\n|{bar}| {percent:.2f}%{clr}\n")

def check_user_balance():
    """
    Checks the user's balance.

    Returns:
    float: The user's balance.
    """

    try:
        # Wait until the user balance element is present on the page
        user_balance = WebDriverWait(driver, 60).until(ec.presence_of_element_located(PageLocators.USER_BALANCE))
        # Extract only the digits from the user balance text
        user_balance_edit = ''.join(c for c in user_balance.text if c.isdigit())
        # Return the balance as a float
        return float(user_balance_edit) / 100
    except TimeoutException:
        # If there's a timeout exception (balance element not found within 60 seconds), write error message and quit the driver
        sys.stderr.write("Can't load user balance.")
        driver.quit()

def check_item_price(item_price, config_price):
    """
    This function checks if the price of the item is within the maximum price specified by the user.

    Parameters:
    item_price (float): The price of the current item.
    config_price (float): The maximum price specified by the user.

    Returns:
    bool: True if the price is less than or equal to the maximum price or if no maximum price is specified, False otherwise.
    """

    # Check if the maximum price is specified
    if config_price is not None:
        # If maximum price is specified, check if the item price is greater than the maximum price
        if float(item_price) > float(config_price):
            return False

    return True

def has_enough_balance(user_balance, item_price):
    """
    Checks if the user has enough balance for the item.

    Parameters:
    user_balance (float): The user's balance.
    item_price (float): The price of the item.

    Returns:
    bool: True if the user has enough balance, False otherwise.
    """
    return user_balance >= item_price

def check_item_parameters(item_float, item_pattern, config_float, config_pattern):
    """
    This function checks the float and pattern of a CS:GO item against the maximum float and a list of acceptable patterns specified in the configuration.
    If the item's float is greater than the maximum value specified, or the item's pattern is not in the list of acceptable patterns, the item does not meet the purchase conditions and the function returns False.
    If the item's float and pattern meet the criteria, the item is eligible for purchase and the function returns True.

    Parameters:
    item_float (float): The float value of the item.
    item_pattern (int): The pattern id of the item.
    count (int): The index of the current item being checked.
    url_info (list): A list of tuples where each tuple contains the maximum float and a list of acceptable patterns for a specific item url.

    Returns:
    bool: True if the item meets the purchase conditions, False otherwise.
    """

    # If a maximum float is specified in the configuration, check if the item's float is less than or equal to the maximum float
    if config_float is not None:
        if item_float > float(config_float):
            return False
        
    # If a list of acceptable patterns is specified in the configuration, check if the item's pattern is in this list
    if config_pattern is not None:
        if str(item_pattern) not in config_pattern:
            return False

    # If the item's float and pattern meet the criteria, the item is eligible for purchase
    return True

def buy_skin(buy_button):
    """
    Purchases a skin.

    Parameters:
    buy_button (WebElement): The "Buy now" button element.

    Returns:
    bool: True if the purchase was successful, False otherwise.
    """

    # Click the "Buy now" button using JavaScript
    driver.execute_script("arguments[0].click();", buy_button)

    try:
        # Wait for the check box element to be present and click it using JavaScript
        check_box = WebDriverWait(driver, 5).until(ec.presence_of_element_located(PageLocators.CHECK_BOX))
        driver.execute_script("arguments[0].click();", check_box)

        # Wait for the buy button element to be present and click it using JavaScript
        buy_button = WebDriverWait(driver, 5).until(ec.presence_of_element_located(PageLocators.BUY_BUTTON))
        driver.execute_script("arguments[0].click();", buy_button)

        # Wait for the close button element to be present and click it using JavaScript
        close_button = WebDriverWait(driver, 5).until(ec.presence_of_element_located(PageLocators.CLOSE_BUTTON))
        driver.execute_script("arguments[0].click();", close_button)

        # Return True if the purchase was successful
        return True
    except TimeoutException:
        # If there's a timeout exception (buy button not found within 5 seconds), write an error message and return False
        sys.stderr.write("Can't find buy button.")
        return False

def buy_log(item_name, item_float, item_price):
    """
    Logs information about a purchase.

    Parameters:
    item_name (str): The name of the purchased item.
    item_float (float): The float value of the purchased item.
    item_price (float): The price of the purchased item.

    Returns:
    None
    """

    # Set up a logger with the name 'BUY' and set the logging level to INFO
    logger = logging.getLogger('BUY')
    logger.setLevel(logging.INFO)
    
    # Check if logger already has handlers
    if not logger.handlers:
        # Create a file handler to write log messages to a file
        file_handler = logging.FileHandler("buy.log", mode='a')
        file_handler.setLevel(logging.INFO)
        # Specify the format of the log messages
        formatter = logging.Formatter('[%(asctime)s] %(name)s > %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')
        # Add the formatter to the file handler
        file_handler.setFormatter(formatter)
        # Add the file handler to the logger
        logger.addHandler(file_handler)
    
    # Log the information about the purchase
    logger.info(f"Item: {item_name}, Float: {item_float}, Price: {item_price}")

    # Increment the global buy_count variable
    global buy_count
    buy_count += 1

    # Clear the terminal
    cls()

def find_next_page():
    """Function that will find next page and will go there"""
    try:
        next_page = WebDriverWait(driver, 5).until(
            ec.visibility_of_element_located(PageLocators.NEXT_PAGE))
        driver.execute_script("arguments[0].click();", next_page)
        time.sleep(2)
        return True
    except TimeoutException:
        sys.stderr.write(
            "Unable to find next page button. Going to next URL...")
        return False
    except NoSuchElementException:
        sys.stderr.write("No next page, going to next URL...")
        return False

def get_min(num1, num2):
    """
    Get the minimum of two numbers. If one number is None, '', or 0, return the other number.
    
    Parameters:
    num1, num2 (int): The numbers to compare.
    
    Returns:
    int: The minimum of the two numbers, or the other number if one number is None, '', or 0.
    """

    if num1 in {None, '', 0}:
        return num2
    elif num2 in {None, '', 0}:
        return num1
    else:
        return min(num1, num2)