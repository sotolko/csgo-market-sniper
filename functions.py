import os
import logging
import sys
import time

import requests
import chromedriver_autoinstaller
import math

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from locators import PageLocators

chromedriver_autoinstaller.install()
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=chrome_options)
buy_count = 0


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def progress_bar(progress, total, urlcount, buycount, page):
    percent = 100 * (progress / float(total))
    bar = chr(9608) * int(percent) + chr(9617) * (100 - int(percent))
    up = "\x1B[3A"
    clr = "\x1B[0K"

    print(f"{up}URL No: {urlcount} | Page: {page} | Orders executed: {buycount} | Balance: {check_user_balance()}{clr}\n|{bar}| {percent:.2f}%{clr}\n")


def check_user_balance():
    """Function that is checking user balance"""
    try:
        user_balance = WebDriverWait(driver, 60).until(ec.presence_of_element_located(PageLocators.USER_BALANCE))
        user_balance_edit = (''.join(c for c in user_balance.text if c.isdigit()))
        return user_balance_edit
    except TimeoutException:
        sys.stderr.write("Can't load user balance.")
        driver.quit()


def buy_log(item_name, item_float, item_pattern, item_price, count):
    """Function that will save information about purchase to logfile"""
    logger = logging.getLogger('BUYLOGGER')
    logger.setLevel(logging.INFO)
    file_handler = logging.FileHandler("purchaseHistory.log", mode='a')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s%(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p %Z')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.info(
        f"Item name: {item_name} , Float: {item_float} , Pattern: {item_pattern} , Price: {item_price}"
    )
    count += 1
    cls()


def check_stickers(json, quantity):
    """Function that will check if skin have stickers"""
    if len(json["iteminfo"]['stickers']) != int(quantity):
        return False
    elif 'stickers' not in json["iteminfo"] or len(json["iteminfo"]['stickers']) == 0:
        return False
    else:
        return True


def buy_skin(buy_button):
    """Function that will buy skin"""
    # Buy now button
    driver.execute_script("arguments[0].click();", buy_button)

    # Execute order
    try:
        check_box = WebDriverWait(driver, 5).until(ec.presence_of_element_located(PageLocators.CHECK_BOX))
        driver.execute_script("arguments[0].click();", check_box)

        buy_button = WebDriverWait(driver, 5).until(ec.presence_of_element_located(PageLocators.BUY_BUTTON))
        driver.execute_script("arguments[0].click();", buy_button)

        close_button = WebDriverWait(driver, 5).until(ec.presence_of_element_located(PageLocators.CLOSE_BUTTON))
        driver.execute_script("arguments[0].click();", close_button)
        return True
    except TimeoutException:
        sys.stderr.write("Can't find buy button.")
        return False


def find_next_page():
    """Function that will find next page and will go there"""
    try:
        next_page = WebDriverWait(driver, 5).until(ec.visibility_of_element_located(PageLocators.NEXT_PAGE))
        driver.execute_script("arguments[0].click();", next_page)
        time.sleep(2)
        return True
    except TimeoutException:
        sys.stderr.write("Unable to find next page button. Going to next URL...")
        return False
    except NoSuchElementException:
        sys.stderr.write("No next page, going to next URL...")
        return False


def load_purchase_buttons():
    """Function that will load purchase buttons from page"""
    try:
        WebDriverWait(driver, 10).until(ec.visibility_of_element_located(PageLocators.BUY_BUTTON_END))

        inspect_button = driver.find_elements(*PageLocators.INSPECT_BUTTON)
        buy_buttons = driver.find_elements(*PageLocators.BUY_BUTTON_END)
        prices_box = driver.find_elements(*PageLocators.PRICES_BOX)
        return inspect_button, buy_buttons, prices_box
    except TimeoutException:
        sys.stderr.write("Cant find buy buttons\n")
        return


def check_whole_page(count, url_info):
    max_price_reached = False
    skin_count = 0
    items = items_on_page()
    pages = int(page_count())
    page = 0

    while not max_price_reached:
        page += 1
        try:
            buttons, buy_now, prices = load_purchase_buttons()
        except NoSuchElementException:
            continue

        try:
            price_text_num = []
            for price in prices:
                price_text_num.append(int(''.join(c for c in price.text if c.isdigit())) / 100)
        except (StaleElementReferenceException, ValueError):
            break

        for idx, btn in enumerate(buttons):
            skin_count += 1

            progress_bar(skin_count, items, count+1, buy_count, page)

            # Check if max price is reached
            if not check_max_price(idx, price_text_num, count, url_info):
                max_price_reached = True
                break

            # Save JSON information
            try:
                item_name, item_float, item_pattern, whole_json = save_json_response(btn)
            except (NoSuchElementException, StaleElementReferenceException):
                continue

            # Check user balance
            try:
                user_bal_num = float(check_user_balance()) / 100
            except ValueError:
                sys.stderr.write("Can't get user balance. Are you logged in?")
                driver.quit()
                sys.exit()

            # Check if user have enough money for skin
            if user_bal_num < price_text_num[idx]:
                continue

            # Check if float and pattern match with user input
            if check_item_parameters(item_float, item_pattern, whole_json, count, url_info) is False:
                continue

            # Buy skin
            buy_skin(buy_now[idx])

            # Save information to file
            buy_log(item_name, item_float, item_pattern, price_text_num[idx], buy_count)

        if url_info[count][4] is not None:
            if page >= url_info[count][4] or int(page_count()) == url_info[count][4]:
                break
        elif page >= int(page_count()):
            break
        else:
            find_next_page()


def save_json_response(button):
    """Function that will save JSON into variables"""
    driver.execute_script("arguments[0].click();", button)

    try:
        popup = WebDriverWait(driver, 5).until(ec.presence_of_element_located(PageLocators.POPUP))
        href = popup.get_attribute('href')
        response = requests.get('https://api.csgofloat.com/?url=' + href)
        response.raise_for_status()
        json_response = response.json()
        json_response_name = str(json_response["iteminfo"]["full_item_name"])
        json_response_float = float(json_response["iteminfo"]["floatvalue"])
        json_response_pattern = int(json_response["iteminfo"]["paintseed"])

        return json_response_name, json_response_float, json_response_pattern, json_response
    except TimeoutException:
        sys.stderr.write("Waiting too long to open item link.")
        return None
    except NoSuchElementException:
        sys.stderr.write("Can't open item link")
        return None


def check_item_parameters(item_float, item_pattern, whole, count, url_info):
    """Function that will compare user set parameters with skin"""
    match = False

    if url_info[count][0] is not None:
        if item_float > float(url_info[count][0]):
            return False

    if url_info[count][1] is not None:
        if type(url_info[count][1]) is not int:
            for pattern in url_info[count][1]:
                if int(pattern) == item_pattern:
                    match = True
                    break
            if not match:
                return False

    if url_info[count][2] is not None:
        if not check_stickers(whole, url_info[count][2]):
            return False

    return True


def check_max_price(order, price, count, url_info):
    if url_info[count][3] is not None:
        if float(url_info[count][3]) <= float(price[order]):
            return False

    return True


def page_count():
    try:
        WebDriverWait(driver, 2).until(ec.presence_of_element_located(PageLocators.LAST_PAGE))
        last_page = driver.find_elements(*PageLocators.LAST_PAGE)
        return last_page[-1].text
    except TimeoutException:
        return 1


def actual_page_number():
    try:
        actual = WebDriverWait(driver, 2).until(ec.presence_of_element_located(PageLocators.PAGE_NUMBER)).text
        return int(actual)
    except TimeoutException:
        return 1


def items_on_page():
    return int(page_count())*10
